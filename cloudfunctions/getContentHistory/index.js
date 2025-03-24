const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

// 云函数入口函数
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const db = cloud.database()
  
  try {
    const { page = 1, pageSize = 10 } = event
    
    // 获取总数
    const countResult = await db.collection('content_history')
      .where({
        _openid: wxContext.OPENID
      })
      .count()
    
    // 获取列表
    const listResult = await db.collection('content_history')
      .where({
        _openid: wxContext.OPENID
      })
      .orderBy('createTime', 'desc')
      .skip((page - 1) * pageSize)
      .limit(pageSize)
      .get()

    return {
      code: 0,
      message: 'success',
      data: {
        total: countResult.total,
        list: listResult.data,
        page,
        pageSize
      }
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