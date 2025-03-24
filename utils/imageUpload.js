// 图片上传工具类
class ImageUploader {
    constructor() {
        // 配置信息
        this.config = {
            maxSize: 2 * 1024 * 1024, // 2MB
            allowedTypes: ['jpg', 'jpeg', 'png', 'gif'],
            uploadUrl: '/api/upload'
        };
    }

    // 检查文件类型
    checkFileType(filePath) {
        const ext = filePath.split('.').pop().toLowerCase();
        return this.config.allowedTypes.includes(ext);
    }

    // 上传图片
    async upload(filePath) {
        return new Promise((resolve, reject) => {
            wx.uploadFile({
                url: this.config.uploadUrl,
                filePath: filePath,
                name: 'image',
                success: (res) => {
                    const data = JSON.parse(res.data);
                    resolve(data);
                },
                fail: (error) => {
                    reject(error);
                }
            });
        });
    }

    // 选择图片
    async chooseImage() {
        return new Promise((resolve, reject) => {
            wx.chooseImage({
                count: 1,
                sizeType: ['compressed'],
                sourceType: ['album', 'camera'],
                success: (res) => {
                    const tempFilePath = res.tempFilePaths[0];
                    
                    // 检查文件大小
                    wx.getFileInfo({
                        filePath: tempFilePath,
                        success: (fileInfo) => {
                            if (fileInfo.size > this.config.maxSize) {
                                reject(new Error('图片大小不能超过2MB'));
                                return;
                            }
                            
                            if (!this.checkFileType(tempFilePath)) {
                                reject(new Error('不支持的文件类型'));
                                return;
                            }
                            
                            resolve(tempFilePath);
                        },
                        fail: reject
                    });
                },
                fail: reject
            });
        });
    }
}

export default new ImageUploader(); 