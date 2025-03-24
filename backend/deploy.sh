#!/bin/bash

echo "开始部署后端服务..."

# 安装基础软件
echo "正在安装基础软件..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-venv nginx git

# 创建应用目录
echo "创建应用目录..."
sudo mkdir -p /var/www/pyq
sudo chown -R $USER:$USER /var/www/pyq

# 创建日志目录
echo "创建日志目录..."
sudo mkdir -p /var/log/pyq
sudo mkdir -p /var/run/pyq
sudo chown -R $USER:$USER /var/log/pyq
sudo chown -R $USER:$USER /var/run/pyq

# 创建虚拟环境
echo "创建Python虚拟环境..."
cd /var/www/pyq
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
echo "安装Python依赖..."
pip install wheel
pip install gunicorn gevent
pip install -r requirements.txt

# 配置Nginx
echo "配置Nginx..."
sudo tee /etc/nginx/sites-available/pyq << EOL
server {
    listen 80;
    server_name localhost;  # 后续替换为实际域名

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # 启用gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # 安全相关配置
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
}
EOL

# 启用Nginx配置
echo "启用Nginx配置..."
sudo ln -sf /etc/nginx/sites-available/pyq /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 创建systemd服务
echo "创建系统服务..."
sudo tee /etc/systemd/system/pyq.service << EOL
[Unit]
Description=PYQ Backend Service
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/var/www/pyq
Environment="PATH=/var/www/pyq/venv/bin"
ExecStart=/var/www/pyq/venv/bin/gunicorn -c gunicorn_config.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# 启动服务
echo "启动服务..."
sudo systemctl daemon-reload
sudo systemctl start pyq
sudo systemctl enable pyq

# 检查服务状态
echo "检查服务状态..."
sudo systemctl status pyq

echo "部署完成！"
echo "请检查服务是否正常运行，并确保防火墙已开放80端口"