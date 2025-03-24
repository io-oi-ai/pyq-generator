App({
  onLaunch: function () {
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力');
    } else {
      wx.cloud.init({
        env: 'a1-0g8ooiutd21020c6',
        traceUser: true
      });
    }

    // 获取启动参数
    const launchOptions = wx.getLaunchOptionsSync()
    console.log('启动参数:', launchOptions)
  },
  globalData: {
    userInfo: null
  }
}); 