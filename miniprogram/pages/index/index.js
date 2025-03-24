Page({
  data: {
    inputText: '',
    platforms: ['微信朋友圈', '微博', '小红书', 'B站'],
    platformIndex: 0,
    styles: ['轻松', '正式', '幽默', '文艺'],
    styleIndex: 0,
    trends: ['无', '当前热梗1', '当前热梗2', '当前热梗3'],
    trendIndex: 0,
    textLength: 100,
    isGenerating: false,
    generatedText: '',
  },

  onLoad() {
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力')
      return
    }
    wx.cloud.init({
      env: 'a1-0g8ooiutd21020c6',
      traceUser: true
    })
  },

  onInputChange(e) {
    this.setData({
      inputText: e.detail.value
    })
  },

  onPlatformChange(e) {
    this.setData({
      platformIndex: e.detail.value
    })
  },

  onStyleChange(e) {
    this.setData({
      styleIndex: e.detail.value
    })
  },

  onTrendChange(e) {
    this.setData({
      trendIndex: e.detail.value
    })
  },

  onLengthChange(e) {
    this.setData({
      textLength: e.detail.value
    })
  },

  async onGenerate() {
    if (!this.data.inputText) {
      wx.showToast({
        title: '请输入初始文案',
        icon: 'none'
      })
      return
    }

    this.setData({ 
      isGenerating: true,
      generatedText: ''
    })

    wx.showLoading({
      title: '正在生成...',
      mask: true
    })

    try {
      const result = await wx.cloud.callFunction({
        name: 'generate',
        data: {
          inputText: this.data.inputText,
          platform: this.data.platforms[this.data.platformIndex],
          style: this.data.styles[this.data.styleIndex],
          trend: this.data.trends[this.data.trendIndex],
          length: this.data.textLength
        }
      })

      console.log('Generation result:', result)

      if (result.result.code !== 0) {
        throw new Error(result.result.message || '生成失败')
      }

      if (!result.result.data || !result.result.data.result) {
        throw new Error('生成结果为空')
      }

      this.setData({
        generatedText: result.result.data.result,
        isGenerating: false
      })

      wx.hideLoading()

    } catch (error) {
      console.error('Generate failed:', error)
      wx.hideLoading()
      
      wx.showToast({
        title: error.message || '生成失败，请重试',
        icon: 'none',
        duration: 2000
      })
      
      this.setData({ 
        isGenerating: false
      })
    }
  },

  onCopy() {
    if (!this.data.generatedText) {
      wx.showToast({
        title: '没有可复制的内容',
        icon: 'none'
      })
      return
    }

    wx.setClipboardData({
      data: this.data.generatedText,
      success: () => {
        wx.showToast({
          title: '已复制到剪贴板',
          icon: 'success'
        })
      }
    })
  }
}) 