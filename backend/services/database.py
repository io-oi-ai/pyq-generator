import sqlite3
from datetime import datetime
import json
import threading

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance.init_database()
            return cls._instance
    
    def init_database(self):
        """初始化数据库和表"""
        self.conn = sqlite3.connect('app.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # 创建用户表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                first_visit TIMESTAMP,
                last_visit TIMESTAMP,
                visit_count INTEGER DEFAULT 0,
                platform TEXT,
                device_info TEXT
            )
        ''')
        
        # 创建生成记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                timestamp TIMESTAMP,
                input_text TEXT,
                platform TEXT,
                style TEXT,
                trend TEXT,
                length INTEGER,
                success BOOLEAN,
                error_message TEXT,
                response_time FLOAT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # 创建API调用记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                endpoint TEXT,
                method TEXT,
                timestamp TIMESTAMP,
                response_code INTEGER,
                response_time FLOAT,
                error_message TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        self.conn.commit()
    
    def track_user_visit(self, user_id, platform=None, device_info=None):
        """记录用户访问"""
        with self._lock:
            now = datetime.now()
            
            # 检查用户是否存在
            self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = self.cursor.fetchone()
            
            if user is None:
                # 新用户
                self.cursor.execute('''
                    INSERT INTO users (user_id, first_visit, last_visit, visit_count, platform, device_info)
                    VALUES (?, ?, ?, 1, ?, ?)
                ''', (user_id, now, now, platform, json.dumps(device_info)))
            else:
                # 更新现有用户
                self.cursor.execute('''
                    UPDATE users 
                    SET last_visit = ?, visit_count = visit_count + 1
                    WHERE user_id = ?
                ''', (now, user_id))
            
            self.conn.commit()
    
    def track_generation(self, user_id, input_text, platform, style, trend, length, 
                        success=True, error_message=None, response_time=None):
        """记录内容生成"""
        with self._lock:
            self.cursor.execute('''
                INSERT INTO generations (
                    user_id, timestamp, input_text, platform, style, trend, length,
                    success, error_message, response_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, datetime.now(), input_text, platform, style, trend, length,
                success, error_message, response_time
            ))
            self.conn.commit()
    
    def track_api_call(self, user_id, endpoint, method, response_code, 
                      response_time=None, error_message=None):
        """记录API调用"""
        with self._lock:
            self.cursor.execute('''
                INSERT INTO api_calls (
                    user_id, endpoint, method, timestamp, response_code,
                    response_time, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, endpoint, method, datetime.now(), response_code,
                response_time, error_message
            ))
            self.conn.commit()
    
    def get_user_stats(self, user_id):
        """获取用户统计信息"""
        with self._lock:
            # 基本信息
            self.cursor.execute('''
                SELECT visit_count, first_visit, last_visit
                FROM users WHERE user_id = ?
            ''', (user_id,))
            user_info = self.cursor.fetchone()
            
            # 生成统计
            self.cursor.execute('''
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
                FROM generations WHERE user_id = ?
            ''', (user_id,))
            gen_stats = self.cursor.fetchone()
            
            return {
                'visit_count': user_info[0] if user_info else 0,
                'first_visit': user_info[1] if user_info else None,
                'last_visit': user_info[2] if user_info else None,
                'total_generations': gen_stats[0] if gen_stats else 0,
                'successful_generations': gen_stats[1] if gen_stats else 0
            }
    
    def __del__(self):
        """清理数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close() 