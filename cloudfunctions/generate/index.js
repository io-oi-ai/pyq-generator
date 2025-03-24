// 云函数入口文件
const cloud = require('wx-server-sdk')
const axios = require('axios')

// 初始化云开发
cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

// API配置
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY
const DEEPSEEK_BASE_URL = process.env.DEEPSEEK_BASE_URL || 'https://ark.cn-beijing.volces.com/api/v3'
const DEEPSEEK_MODEL = process.env.DEEPSEEK_MODEL || 'deepseek-r1-250120'

// 添加API调用日志
function logApiCall(details) {
  console.log('=== DeepSeek API Call Details ===')
  console.log('Timestamp:', new Date().toISOString())
  console.log('API URL:', DEEPSEEK_BASE_URL)
  console.log('Model:', DEEPSEEK_MODEL)
  // 不记录API密钥
  const safeDetails = { ...details }
  if (safeDetails.requestData) {
    safeDetails.requestData = { ...safeDetails.requestData }
    delete safeDetails.requestData.headers?.Authorization
  }
  console.log('Request Details:', JSON.stringify(safeDetails, null, 2))
  console.log('===============================')
}

// 获取平台特定的写作指南
function getPlatformGuide(platform) {
  const guides = {
    '微信朋友圈': `
- 文风要亲和自然，像朋友间的对话
- 可以使用emoji，但不要过度
- 适合分享生活感悟、日常心情
- 建议使用第一人称，增加亲近感
- 可以适当加入互动元素，如提问
    `,
    '微博': `
- 文风可以更加活泼、网络化
- 可以大量使用emoji和网络用语
- 适合热点话题和即时感受
- 可以使用话题标签和@功能
- 鼓励互动和转发
    `,
    '小红书': `
- 文风要真实、生活化、体验感强
- 多用emoji，标题吸引眼球
- 分点描述，结构要清晰
- 适合种草、测评、分享
- 多用"安利"、"测评"等小红书平台常用语
    `,
    '抖音': `
- 文案要简短有力，朗朗上口
- 可以用押韵或节奏感强的语言
- 适合潮流、趣味性内容
- 多用"前方高能"、"爆款"等抖音平台常用语
- 标题要有吸引力
    `
  }
  return guides[platform] || ''
}

// 构建prompt
function buildPrompt(params) {
  const { inputText, platform, style, trend, length } = params
  
  // 获取平台特定的写作指南
  const platformGuide = getPlatformGuide(platform)
  
  // 构建更详细的系统提示
  const systemPrompt = `你是一位擅长理解用户意图并进行文案创作的资深文案写手。
你的任务是：
1. 首先理解用户输入文案中表达的核心情感和意图
2. 然后基于这个核心意图，用${style}的语气进行延展和创作
3. 保持原文案的情感基调，但使表达更加丰富生动
4. 根据平台特点调整表达方式：
${platformGuide}
5. 控制文案长度在${length}字以内，但要确保表达完整
6. 如果原文案很短（少于10字），注重延展和丰富内容
7. 如果原文案较长，注重提炼和优化表达`

  // 构建用户提示
  const userPrompt = `请帮我创作一条基于以下文案的${platform}内容：
"${inputText}"

要求：
1. 保持原文案的核心情感和意图
2. 用${style}的语气表达
3. 根据平台特点和文案长度${length}字以内的要求，适当延展和优化内容
4. 加入适合${platform}平台的表达方式和emoji
5. 确保文案生动有趣，能引起共鸣`

  return {
    systemPrompt,
    userPrompt
  }
}

// 调用DeepSeek API生成内容
async function generateWithDeepSeek(prompt) {
  try {
    console.log('Starting DeepSeek API call...')
    
    // 添加重试逻辑
    let retryCount = 0;
    const maxRetries = 3;
    
    while (retryCount < maxRetries) {
      try {
        console.log(`Attempt ${retryCount + 1} of ${maxRetries}`)
        
        const requestData = {
          model: DEEPSEEK_MODEL,
          messages: [
            {
              role: 'system',
              content: prompt.systemPrompt
            },
            {
              role: 'user',
              content: prompt.userPrompt
            }
          ],
          temperature: 0.8,
          max_tokens: 250,
          stream: false
        }

        // 记录API调用详情
        logApiCall({
          method: 'POST',
          endpoint: '/chat/completions',
          requestData: requestData
        })

        const response = await axios({
          method: 'post',
          url: `${DEEPSEEK_BASE_URL}/chat/completions`,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
          },
          data: requestData,
          timeout: 30000
        });

        // 记录API响应
        console.log('=== DeepSeek API Response ===')
        console.log('Status:', response.status)
        console.log('Response Data:', JSON.stringify(response.data, null, 2))
        console.log('===============================')

        if (!response.data?.choices?.[0]?.message?.content) {
          console.error('Invalid API response format:', response.data);
          throw new Error('API返回结果格式错误');
        }

        return response.data.choices[0].message.content.trim();
      } catch (error) {
        retryCount++;
        console.error(`Attempt ${retryCount} failed:`, {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          headers: error.response?.headers
        });
        
        if (retryCount === maxRetries) {
          throw error;
        }
        
        // 等待一段时间后重试
        await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
      }
    }
  } catch (error) {
    console.error('DeepSeek API Error:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    });
    throw error;
  }
}

// 云函数入口函数
exports.main = async (event, context) => {
  console.log('Generate function started with params:', event)
  
  const wxContext = cloud.getWXContext()
  const db = cloud.database()
  
  try {
    const { inputText, platform, style, trend, length } = event

    if (!inputText) {
      throw new Error('请输入初始文案')
    }

    const prompt = buildPrompt({ inputText, platform, style, trend, length })
    console.log('Generated prompt:', prompt)

    // 设置超时
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('请求超时')), 35000);
    })

    // 使用Promise.race来处理超时
    const generatedText = await Promise.race([
      generateWithDeepSeek(prompt),
      timeoutPromise
    ])

    console.log('Generated text:', generatedText)

    // 异步保存历史记录
    db.collection('content_history').add({
      data: {
        inputText,
        platform,
        style,
        trend,
        length,
        generatedText,
        createTime: db.serverDate(),
        creator: wxContext.OPENID
      }
    }).catch(err => {
      console.error('Failed to save history:', err)
    })

    return {
      code: 0,
      message: 'Generated successfully',
      data: {
        result: generatedText
      }
    }

  } catch (error) {
    console.error('Error in generate function:', error)
    
    let errorMessage = error.message
    if (error.code === 'DATABASE_QUERY_FAILED') {
      errorMessage = '数据库操作失败，请重试'
    } else if (error.response?.data?.error) {
      errorMessage = `DeepSeek API错误: ${error.response.data.error.message}`
    } else if (error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT' || errorMessage === '请求超时') {
      errorMessage = '网络连接超时，请重试'
    }
    
    return {
      code: -1,
      message: errorMessage,
      error: error.message
    }
  }
} 