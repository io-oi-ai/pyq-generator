from flask import render_template, Blueprint
from services.database import DatabaseService

monitor_bp = Blueprint('monitor', __name__, template_folder='templates')
db = DatabaseService()

@monitor_bp.route('/monitor')
def monitor_dashboard():
    stats = {
        'total_users': db.get_user_count(),
        'total_generations': db.get_generation_count(),
        'success_rate': db.get_success_rate(),
        'recent_errors': db.get_recent_errors(limit=5),
        'api_stats': db.get_api_stats()
    }
    return render_template('monitor.html', stats=stats) 