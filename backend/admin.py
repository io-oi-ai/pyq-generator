from flask_admin import Admin # type: ignore
from flask_admin.contrib.sqla import ModelView # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask import Flask
from models import db, User, GenerationRecord, ApiCall  # type: ignore # 假设这些是你的模型

def setup_admin(app: Flask):
    admin = Admin(app, name='AI文案生成器管理后台', template_mode='bootstrap3')
    
    # 添加模型视图
    class UserView(ModelView):
        column_list = ['id', 'visit_count', 'last_visit', 'created_at']
        column_searchable_list = ['id']
        column_filters = ['created_at', 'last_visit']
    
    class GenerationView(ModelView):
        column_list = ['user_id', 'input_text', 'generated_text', 'success', 'created_at']
        column_searchable_list = ['user_id', 'input_text']
        column_filters = ['success', 'created_at']
    
    class ApiCallView(ModelView):
        column_list = ['endpoint', 'method', 'status_code', 'response_time', 'created_at']
        column_filters = ['endpoint', 'status_code', 'created_at']
    
    # 注册视图
    admin.add_view(UserView(User, db.session))
    admin.add_view(GenerationView(GenerationRecord, db.session))
    admin.add_view(ApiCallView(ApiCall, db.session))
    
    return admin 