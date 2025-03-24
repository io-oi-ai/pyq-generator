// 阿里云服务配置文件

const AlibabaCloud = require('alibabacloud-oss-client');

const client = new AlibabaCloud({
    accessKeyId: process.env.ALICLOUD_ACCESS_KEY_ID,
    accessKeySecret: process.env.ALICLOUD_ACCESS_KEY_SECRET,
    region: process.env.ALICLOUD_REGION || 'cn-hangzhou'
});

// OSS配置
const config = {
  accessKeyId: process.env.ALICLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALICLOUD_ACCESS_KEY_SECRET,
  bucket: process.env.ALICLOUD_BUCKET || 'wx-miniprogram-pyq',
  region: process.env.ALICLOUD_REGION || 'oss-cn-shenzhen'
};

// OSS操作方法
const ossService = {
  // 上传文件
  uploadFile(filePath, fileName) {
    return new Promise((resolve, reject) => {
      const policy = this.getPolicy();
      const signature = this.getSignature(policy);

      wx.uploadFile({
        url: `https://${config.bucket}.${config.region}.aliyuncs.com`, // OSS上传地址
        filePath: filePath,
        name: 'file',
        formData: {
          'key': fileName,
          'policy': policy,
          'OSSAccessKeyId': config.accessKeyId,
          'success_action_status': '200',
          'signature': signature
        },
        success(res) {
          if (res.statusCode === 200) {
            resolve({
              url: `https://${config.bucket}.${config.region}.aliyuncs.com/${fileName}`
            });
          } else {
            reject(new Error(`Upload failed with status ${res.statusCode}`));
          }
        },
        fail(err) {
          reject(err);
        }
      });
    });
  },

  // 获取文件列表（需要后端支持）
  listFiles(prefix = '') {
    return new Promise((resolve, reject) => {
      // 这里需要调用后端API来获取文件列表
      // 为了演示，返回空数组
      resolve([]);
    });
  },

  // 删除文件（需要后端支持）
  deleteFile(fileName) {
    return new Promise((resolve, reject) => {
      // 这里需要调用后端API来删除文件
      // 为了演示，直接返回成功
      resolve();
    });
  },

  // 获取文件URL
  getFileUrl(fileName) {
    return `https://${config.bucket}.${config.region}.aliyuncs.com/${fileName}`;
  },

  // 获取Policy
  getPolicy() {
    const date = new Date();
    date.setHours(date.getHours() + 1);
    const policyText = {
      expiration: date.toISOString(),
      conditions: [
        ['content-length-range', 0, 10485760], // 限制文件大小在10MB以内
        ['starts-with', '$key', 'images/'] // 限制上传文件路径必须以 images/ 开头
      ]
    };
    return wx.arrayBufferToBase64(new TextEncoder().encode(JSON.stringify(policyText)));
  },

  // 计算签名
  getSignature(policy) {
    // 将policy进行base64解码
    const policyBase64 = wx.base64ToArrayBuffer(policy);
    const policyStr = new TextDecoder().decode(policyBase64);
    
    // 使用HMAC-SHA1算法计算签名
    const hmacSha1 = (data) => {
      const key = config.accessKeySecret;
      let keyData = new TextEncoder().encode(key);
      let dataData = new TextEncoder().encode(data);
      
      let length = 64;
      if (keyData.length > length) {
        keyData = new Uint8Array(sha1(keyData));
      }
      
      const ipad = new Uint8Array(length);
      const opad = new Uint8Array(length);
      
      for (let i = 0; i < length; i++) {
        ipad[i] = 0x36;
        opad[i] = 0x5c;
      }
      
      for (let i = 0; i < keyData.length; i++) {
        ipad[i] ^= keyData[i];
        opad[i] ^= keyData[i];
      }
      
      const innerHash = sha1(concat(ipad, dataData));
      const finalHash = sha1(concat(opad, innerHash));
      
      return wx.arrayBufferToBase64(finalHash);
    };
    
    return hmacSha1(policyStr);
  }
};

// 辅助函数：SHA1
function sha1(data) {
  if (typeof data === 'string') {
    data = new TextEncoder().encode(data);
  }
  
  const h0 = 0x67452301;
  const h1 = 0xEFCDAB89;
  const h2 = 0x98BADCFE;
  const h3 = 0x10325476;
  const h4 = 0xC3D2E1F0;
  
  const padded = new Uint8Array(Math.ceil((data.length + 9) / 64) * 64);
  padded.set(data);
  padded[data.length] = 0x80;
  
  const view = new DataView(padded.buffer);
  view.setUint32(padded.length - 4, data.length * 8);
  
  for (let offset = 0; offset < padded.length; offset += 64) {
    const w = new Uint32Array(80);
    for (let i = 0; i < 16; i++) {
      w[i] = view.getUint32(offset + i * 4);
    }
    
    for (let i = 16; i < 80; i++) {
      w[i] = rotl(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1);
    }
    
    let a = h0;
    let b = h1;
    let c = h2;
    let d = h3;
    let e = h4;
    
    for (let i = 0; i < 80; i++) {
      const f = i < 20 ? (b & c) | (~b & d) :
                i < 40 ? b ^ c ^ d :
                i < 60 ? (b & c) | (b & d) | (c & d) :
                b ^ c ^ d;
      
      const k = i < 20 ? 0x5A827999 :
                i < 40 ? 0x6ED9EBA1 :
                i < 60 ? 0x8F1BBCDC :
                0xCA62C1D6;
      
      const temp = (rotl(a, 5) + f + e + k + w[i]) >>> 0;
      e = d;
      d = c;
      c = rotl(b, 30);
      b = a;
      a = temp;
    }
    
    h0 = (h0 + a) >>> 0;
    h1 = (h1 + b) >>> 0;
    h2 = (h2 + c) >>> 0;
    h3 = (h3 + d) >>> 0;
    h4 = (h4 + e) >>> 0;
  }
  
  const result = new Uint8Array(20);
  const resultView = new DataView(result.buffer);
  resultView.setUint32(0, h0);
  resultView.setUint32(4, h1);
  resultView.setUint32(8, h2);
  resultView.setUint32(12, h3);
  resultView.setUint32(16, h4);
  
  return result;
}

// 辅助函数：左旋转
function rotl(x, n) {
  return ((x << n) | (x >>> (32 - n))) >>> 0;
}

// 辅助函数：连接两个 Uint8Array
function concat(a, b) {
  const c = new Uint8Array(a.length + b.length);
  c.set(a);
  c.set(b, a.length);
  return c;
}

module.exports = {
  ossService
}; 