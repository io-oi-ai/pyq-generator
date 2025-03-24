#!/bin/bash

# 配置变量
APP_NAME="pyq"
DEPLOY_PATH="/var/www/pyq"
LOG_PATH="/var/log/pyq"

# 创建必要的目录
sudo mkdir -p $DEPLOY_PATH
sudo mkdir -p $LOG_PATH
sudo mkdir -p $DEPLOY_PATH/backend

# 设置权限
sudo chown -R admin:admin $DEPLOY_PATH
sudo chown -R admin:admin $LOG_PATH

# 复制应用文件
cp app.py $DEPLOY_PATH/backend/
cp -r services $DEPLOY_PATH/backend/
cp requirements.txt $DEPLOY_PATH/

# 设置Python虚拟环境
cd $DEPLOY_PATH
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 创建systemd服务文件
sudo tee /etc/systemd/system/$APP_NAME.service << EOL
[Unit]
Description=PYQ Backend Service
After=network.target

[Service]
User=admin
Group=admin
WorkingDirectory=$DEPLOY_PATH/backend
Environment="PATH=$DEPLOY_PATH/venv/bin"
Environment="PYTHONPATH=$DEPLOY_PATH"
ExecStart=$DEPLOY_PATH/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# 创建日志目录
sudo mkdir -p /var/log/$APP_NAME
sudo chown -R admin:admin /var/log/$APP_NAME

# 重新加载systemd并启动服务
sudo systemctl daemon-reload
sudo systemctl restart $APP_NAME
sudo systemctl enable $APP_NAME

# 配置Nginx
sudo tee /etc/nginx/conf.d/$APP_NAME.conf << EOL
server {
    listen 80;
    server_name 47.236.0.225;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOL

# 测试Nginx配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx

# 显示服务状态
echo "显示服务状态..."
sudo systemctl status $APP_NAME
sudo systemctl status nginx 