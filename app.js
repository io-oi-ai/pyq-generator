App({
  onLaunch: async function() {
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力')
      return
    }
    
    wx.cloud.init({
      env: 'a1-0g8ooiutd21020c6',
      traceUser: true
    })

    try {
      // 检查数据库集合是否存在
      const db = wx.cloud.database()
      const collections = await db.collections()
      const hasApiTasksCollection = collections.some(col => col.name === 'api_tasks')
      
      if (!hasApiTasksCollection) {
        console.error('api_tasks集合不存在，请在云开发控制台创建')
        // 尝试创建集合
        try {
          await wx.cloud.callFunction({
            name: 'createCollection',
            data: {
              collectionName: 'api_tasks'
            }
          })
          console.log('api_tasks集合创建成功')
        } catch (err) {
          console.error('创建集合失败:', err)
        }
      }
    } catch (error) {
      console.error('数据库初始化检查失败:', error)
    }
  },
  
  globalData: {
    userInfo: null
  }
}) 