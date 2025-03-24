#!/bin/bash

# 配置信息
SERVER_USER="root"
SERVER_HOST="47.112.185.79"

# 获取本地公钥
PUBLIC_KEY=$(cat ~/.ssh/id_rsa.pub)

# 在服务器上设置SSH密钥
ssh $SERVER_USER@$SERVER_HOST "
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    echo '$PUBLIC_KEY' >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
"

echo "SSH密钥已添加到服务器" 