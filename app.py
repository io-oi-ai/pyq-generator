from flask import Flask, request, jsonify # type: ignore
from services.content_generator import ContentGenerator
from services.version_manager import VersionManager
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

content_generator = ContentGenerator()
version_manager = VersionManager()

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'success': True,
        'message': 'Server is running'
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        result = content_generator.generate_content(data)
        return result
    except Exception as e:
        return "", 500

@app.route('/api/versions', methods=['POST'])
def save_version():
    try:
        data = request.json
        content = data.get('content')
        version_name = data.get('version_name')
        description = data.get('description')
        
        if not content:
            return jsonify({
                'success': False,
                'error': '内容不能为空'
            }), 400
            
        version_info = version_manager.save_version(
            content=content,
            version_name=version_name,
            description=description
        )
        return jsonify({
            'success': True,
            'version': version_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/versions', methods=['GET'])
def list_versions():
    try:
        versions = version_manager.list_versions()
        return jsonify({
            'success': True,
            'versions': versions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/versions/<version_id>', methods=['GET'])
def get_version(version_id):
    try:
        version = version_manager.get_version(version_id=int(version_id))
        if not version:
            return jsonify({
                'success': False,
                'error': '版本不存在'
            }), 404
            
        return jsonify({
            'success': True,
            'version': version
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 