const app = getApp()

Page({
  data: {
    title: 'AI帮助你更好展现自己',
    inputText: '',
    platforms: ['微信朋友圈', '微博', '小红书', 'B站'],
    platformIndex: 0,
    styles: ['轻松', '正式', '幽默', '文艺'],
    styleIndex: 0,
    trends: ['无', '当前热梗1', '当前热梗2', '当前热梗3'],
    trendIndex: 0,
    textLength: 100,
    isGenerating: false,
    generatedText: ''
  },

  onLoad() {
    // 初始化云开发
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力')
      return
    }
    wx.cloud.init({
      env: 'your-env-id', // 替换为你的云开发环境ID
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

  onGenerate() {
    if (!this.data.inputText) {
      wx.showToast({
        title: '请输入初始文案',
        icon: 'none'
      })
      return
    }

    this.setData({ isGenerating: true })

    // 调用云函数
    wx.cloud.callFunction({
      name: 'generateContent',
      data: {
        inputText: this.data.inputText,
        platform: this.data.platforms[this.data.platformIndex],
        style: this.data.styles[this.data.styleIndex],
        trend: this.data.trends[this.data.trendIndex],
        length: this.data.textLength
      }
    }).then(res => {
      console.log('Generated result:', res)
      if (res.result.code === 0) {
        this.setData({
          generatedText: res.result.data.generated_text,
          isGenerating: false
        })
      } else {
        throw new Error(res.result.message)
      }
    }).catch(error => {
      console.error('Generate failed:', error)
      wx.showToast({
        title: '生成失败，请重试',
        icon: 'none'
      })
      this.setData({ isGenerating: false })
    })
  },

  onCopy() {
    wx.setClipboardData({
      data: this.data.generatedText,
      success: () => {
        wx.showToast({
          title: '已复制到剪贴板',
          icon: 'success'
        })
      }
    })
  },
  // 添加错误处理中间件
  handleError: async function(fn) {
    try {
      return await fn()
    } catch (error) {
      console.error('操作失败:', error)
      wx.showToast({
        title: error.message || '操作失败',
        icon: 'none'
      })
      throw error
    }
  },
  // 使用中间件包装创建任务函数
  createTask: async function(taskData) {
    return this.handleError(async () => {
      const result = await wx.cloud.callFunction({
        name: 'createTask',
        data: taskData
      })
      
      console.log('Create task result:', result)
      
      if (!result.result.success) {
        throw new Error(result.result.message)
      }
      
      wx.showToast({
        title: '创建成功',
        icon: 'success'
      })
      
      return result.result.taskId
    })
  }
}) 