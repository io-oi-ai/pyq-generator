// 处理 HTTP 请求的函数
exports.handler = async (req, resp, context) => {
    // 设置响应头
    resp.setHeader('content-type', 'application/json');
    
    // 获取请求信息
    const requestId = context.requestId;
    
    try {
        // 解析请求体
        let body = {};
        if (req.body) {
            body = JSON.parse(req.body);
        }

        // 处理请求
        const result = {
            code: 0,
            message: 'success',
            data: {
                requestId: requestId,
                timestamp: new Date().toISOString(),
                body: body,
                // 测试数据
                test: {
                    env: process.env,
                    context: {
                        credentials: context.credentials,
                        function: context.function,
                        service: context.service,
                        region: context.region
                    }
                }
            }
        };

        // 发送响应
        resp.send(JSON.stringify(result));
        
    } catch (error) {
        // 错误处理
        console.error('Error:', error);
        resp.setStatusCode(500);
        resp.send(JSON.stringify({
            code: -1,
            message: error.message || 'Internal Server Error',
            requestId: requestId
        }));
    }
}; 