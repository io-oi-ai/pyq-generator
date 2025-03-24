from flask import Blueprint, jsonify
from services.database import DatabaseService

debug_bp = Blueprint('debug', __name__)
db = DatabaseService()

@debug_bp.route('/debug/stats', methods=['GET'])
def get_stats():
    """获取系统统计信息"""
    return jsonify({
        'user_count': db.get_user_count(),
        'generation_count': db.get_generation_count(),
        'success_rate': db.get_success_rate(),
        'average_response_time': db.get_average_response_time()
    })

@debug_bp.route('/debug/recent-generations', methods=['GET'])
def get_recent_generations():
    """获取最近的生成记录"""
    return jsonify({
        'generations': db.get_recent_generations(limit=10)
    })

@debug_bp.route('/debug/error-logs', methods=['GET'])
def get_error_logs():
    """获取错误日志"""
    return jsonify({
        'errors': db.get_recent_errors(limit=10)
    }) 