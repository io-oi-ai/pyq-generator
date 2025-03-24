from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from services.content_generator import ContentGenerator
from services.database import Database
import time
import traceback

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# 初始化数据库服务
db = Database()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/test')
def test():
    return jsonify({
        "code": 0,
        "message": "Server is running",
        "timestamp": time.time()
    })

@app.route('/')
def index():
    user_id = request.headers.get('X-User-ID')
    if user_id:
        db.track_user_visit(
            user_id=user_id,
            platform=request.headers.get('X-Platform'),
            device_info={
                'user_agent': request.headers.get('User-Agent'),
                'ip': request.remote_addr
            }
        )
    
    return jsonify({
        "code": 0,
        "message": "API server is running",
        "client_ip": request.remote_addr
    })

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    start_time = time.time()
    user_id = request.headers.get('X-User-ID')
    
    try:
        data = request.get_json(force=True)
        
        # 获取生成参数
        input_text = data.get('input_text', '')
        platform = data.get('platform', '微信朋友圈')
        style = data.get('style', '轻松')
        trend = data.get('trend', '无')
        length = data.get('length', 100)
        
        # 调用内容生成器
        generator = ContentGenerator()
        content = generator.generate_content(
            input_text=input_text,
            platform=platform,
            style=style,
            trend=trend,
            length=length
        )
        
        # 记录成功的生成
        if user_id:
            response_time = time.time() - start_time
            db.track_generation(
                user_id=user_id,
                input_text=input_text,
                platform=platform,
                style=style,
                trend=trend,
                length=length,
                success=True,
                response_time=response_time
            )
            
            # 记录API调用
            db.track_api_call(
                user_id=user_id,
                endpoint='/generate',
                method='POST',
                response_code=200,
                response_time=response_time
            )
        
        return jsonify({
            "code": 0,
            "generated_text": content,
            "message": "success"
        })

    except Exception as e:
        error_message = str(e)
        response_time = time.time() - start_time
        
        # 记录失败的生成
        if user_id:
            db.track_generation(
                user_id=user_id,
                input_text=data.get('input_text', '') if 'data' in locals() else '',
                platform=data.get('platform', '') if 'data' in locals() else '',
                style=data.get('style', '') if 'data' in locals() else '',
                trend=data.get('trend', '') if 'data' in locals() else '',
                length=data.get('length', 0) if 'data' in locals() else 0,
                success=False,
                error_message=error_message,
                response_time=response_time
            )
            
            # 记录失败的API调用
            db.track_api_call(
                user_id=user_id,
                endpoint='/generate',
                method='POST',
                response_code=500,
                response_time=response_time,
                error_message=error_message
            )
        
        return jsonify({
            "code": -1,
            "message": f"生成失败: {error_message}",
            "error_type": type(e).__name__,
            "error_details": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)