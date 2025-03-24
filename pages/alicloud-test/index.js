const { ossService } = require('../../services/alicloud');

Page({
  data: {
    imageList: [],
    uploadStatus: '未开始'
  },

  onLoad() {
    this.loadImageList();
  },

  // 加载图片列表
  async loadImageList() {
    try {
      const result = await ossService.listFiles('images/');
      const imageList = result.map(item => ({
        key: item.name,
        url: ossService.getFileUrl(item.name)
      }));
      this.setData({ imageList });
    } catch (error) {
      console.error('加载图片列表失败:', error);
      wx.showToast({
        title: '加载图片失败',
        icon: 'none'
      });
    }
  },

  // 选择并上传图片
  chooseAndUploadImage() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePath = res.tempFilePaths[0];
        this.setData({ uploadStatus: '上传中...' });

        // 生成文件名
        const fileName = `images/${Date.now()}_${Math.random().toString(36).slice(2)}.jpg`;

        // 上传到OSS
        ossService.uploadFile(tempFilePath, fileName)
          .then(() => {
            this.setData({ uploadStatus: '上传成功' });
            this.loadImageList();
          })
          .catch(error => {
            console.error('上传图片失败:', error);
            this.setData({ uploadStatus: '上传失败' });
            wx.showToast({
              title: '上传失败',
              icon: 'none'
            });
          });
      }
    });
  },

  // 预览图片
  previewImage(e) {
    const { url } = e.currentTarget.dataset;
    wx.previewImage({
      urls: [url]
    });
  },

  // 删除图片
  deleteImage(e) {
    const { key } = e.currentTarget.dataset;
    ossService.deleteFile(key)
      .then(() => {
        this.loadImageList();
        wx.showToast({
          title: '删除成功',
          icon: 'success'
        });
      })
      .catch(error => {
        console.error('删除图片失败:', error);
        wx.showToast({
          title: '删除失败',
          icon: 'none'
        });
      });
  }
}); 