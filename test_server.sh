#!/bin/bash

# 测试服务器连接
echo "测试服务器连接..."
curl -I http://47.236.0.225/test

# 如果测试失败，检查服务状态
if [ $? -ne 0 ]; then
    echo "连接失败，检查服务状态..."
    # 尝试重启服务
    echo "尝试重启服务..."
    sudo systemctl restart pyq
    sudo systemctl restart nginx
    
    # 等待服务启动
    sleep 5
    
    # 再次测试
    echo "再次测试连接..."
    curl -I http://47.236.0.225/test
fi 