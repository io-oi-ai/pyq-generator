import requests
import base64
import os

# GitHub API配置
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # 从环境变量获取token
REPO_OWNER = 'io-oi-ai'
REPO_NAME = 'pyq-generator'
BRANCH = 'main'

# README内容
README_CONTENT = '''# PYQ Generator (朋友圈生成器)

一个智能的朋友圈文案生成器，基于微信小程序开发，能够根据用户提供的场景和风格自动生成个性化的朋友圈文案。

## 功能特点

- 🎯 智能场景识别：自动识别用户上传的图片场景
- 🎨 多样化风格：支持多种文案风格（文艺、搞笑、励志等）
- 🤖 AI驱动：使用OpenAI API生成高质量文案
- 📱 微信小程序：便捷的用户界面和操作体验
- 🔄 历史记录：保存生成历史，方便查看和复用

## 技术架构

- 前端：微信小程序
- 后端：Python Flask
- 云服务：腾讯云
- AI服务：OpenAI API
- 数据库：MongoDB

## 项目结构

```
PYQ/
├── miniprogram/          # 微信小程序前端代码
├── backend/             # Python后端服务
├── cloudfunctions/      # 云函数
├── services/           # 核心服务模块
└── utils/             # 工具函数
```

## 环境要求

- Python 3.8+
- Node.js 14+
- 微信开发者工具
- OpenAI API密钥

## 快速开始

1. 克隆项目
```bash
git clone https://github.com/io-oi-ai/pyq-generator.git
```

2. 安装依赖
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd ../miniprogram
npm install
```

3. 配置环境变量
- 复制 `.env.example` 为 `.env`
- 填写必要的配置信息（OpenAI API密钥等）

4. 启动服务
```bash
# 启动后端服务
cd backend
python app.py

# 使用微信开发者工具打开miniprogram目录
```

## 使用说明

1. 打开微信小程序
2. 上传图片或选择场景
3. 选择文案风格
4. 点击生成按钮
5. 查看生成结果并分享

## 开发计划

- [ ] 支持更多场景识别
- [ ] 添加自定义风格模板
- [ ] 优化生成速度
- [ ] 增加批量生成功能
- [ ] 添加用户反馈机制

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件至：[your-email@example.com]

## 致谢

感谢所有为这个项目做出贡献的开发者！
'''

def upload_readme():
    if not GITHUB_TOKEN:
        print("错误：请设置GITHUB_TOKEN环境变量")
        return

    # 准备请求头
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # 检查文件是否存在
    check_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/README.md'
    response = requests.get(check_url, headers=headers)
    
    if response.status_code == 200:
        # 文件存在，获取SHA
        sha = response.json()['sha']
        # 更新文件
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/README.md'
        data = {
            'message': 'Update README.md',
            'content': base64.b64encode(README_CONTENT.encode()).decode(),
            'sha': sha
        }
    else:
        # 文件不存在，创建新文件
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/README.md'
        data = {
            'message': 'Create README.md',
            'content': base64.b64encode(README_CONTENT.encode()).decode()
        }

    # 发送请求
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print("README.md 上传成功！")
    else:
        print(f"上传失败：{response.status_code}")
        print(response.json())

if __name__ == '__main__':
    upload_readme() 