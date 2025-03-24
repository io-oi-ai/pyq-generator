#!/bin/bash

# 配置信息
SERVER_USER="root"
SERVER_HOST="47.236.0.225"
DEPLOY_PATH="/var/www/pyq"
APP_NAME="pyq"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}开始部署 $APP_NAME 到阿里云...${NC}"

# 1. 打包项目文件
echo "打包项目文件..."
tar --exclude='.git' --exclude='venv' --exclude='.venv' --exclude='__pycache__' \
    --exclude='*.pyc' --exclude='.DS_Store' -czf /tmp/$APP_NAME.tar.gz .

# 2. 上传到服务器
echo "上传文件到阿里云服务器..."
scp /tmp/$APP_NAME.tar.gz $SERVER_USER@$SERVER_HOST:/tmp/

# 3. 在服务器上执行部署
echo "在阿里云服务器上执行部署..."
ssh $SERVER_USER@$SERVER_HOST << 'ENDSSH'
    # 设置环境变量
    export APP_NAME="pyq"
    export DEPLOY_PATH="/var/www/pyq"
    
    # 安装必要的系统包
    dnf upgrade-minimal --security -y
    yum install -y python39 python39-devel gcc nginx
    
    # 创建必要的目录
    mkdir -p $DEPLOY_PATH
    mkdir -p /var/log/$APP_NAME
    mkdir -p /var/run/$APP_NAME
    
    # 设置目录权限
    chown -R $USER:$USER $DEPLOY_PATH
    chown -R $USER:$USER /var/log/$APP_NAME
    chown -R $USER:$USER /var/run/$APP_NAME
    
    # 解压文件
    cd $DEPLOY_PATH
    tar -xzf /tmp/$APP_NAME.tar.gz
    
    # 设置 Python 虚拟环境
    python3.9 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # 配置 Nginx
    cat > /etc/nginx/conf.d/$APP_NAME.conf << 'EOL'
server {
    listen 80;
    server_name your_domain_or_ip;  # 替换为你的域名或IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOL

    # 创建或更新 systemd 服务
    cat > /etc/systemd/system/$APP_NAME.service << 'EOL'
[Unit]
Description=PYQ Backend Service
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$DEPLOY_PATH/backend
Environment="PATH=$DEPLOY_PATH/venv/bin"
Environment="PYTHONPATH=$DEPLOY_PATH"
ExecStart=$DEPLOY_PATH/venv/bin/gunicorn -c gunicorn_config.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOL
    
    # 启动服务
    systemctl daemon-reload
    systemctl restart nginx
    systemctl restart $APP_NAME
    systemctl enable nginx
    systemctl enable $APP_NAME
    
    # 配置防火墙
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --reload
    
    # 清理临时文件
    rm /tmp/$APP_NAME.tar.gz
    
    # 显示服务状态
    echo "Nginx 状态:"
    systemctl status nginx
    echo "应用服务状态:"
    systemctl status $APP_NAME
ENDSSH

# 4. 检查部署结果
echo "检查服务状态..."
ssh $SERVER_USER@$SERVER_HOST "systemctl status $APP_NAME"

echo -e "${GREEN}部署完成！${NC}"

# 5. 显示访问信息
echo -e "${GREEN}应用已部署完成！${NC}"
echo -e "你可以通过以下地址访问应用："
echo -e "http://$SERVER_HOST" 