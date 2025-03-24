const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

// 云函数入口函数
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const db = cloud.database()
  
  try {
    const { historyId } = event
    
    // 检查记录是否存在且属于当前用户
    const record = await db.collection('content_history')
      .doc(historyId)
      .get()
    
    if (!record.data || record.data._openid !== wxContext.OPENID) {
      throw new Error('无权删除此记录')
    }
    
    // 删除记录
    await db.collection('content_history')
      .doc(historyId)
      .remove()

    return {
      code: 0,
      message: 'success'
    }

  } catch (error) {
    console.error('Error:', error)
    return {
      code: -1,
      message: error.message,
      error: error
    }
  }
} 