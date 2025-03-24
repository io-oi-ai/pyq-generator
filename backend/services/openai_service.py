import os
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 初始化OpenAI客户端
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("未找到 OPENAI_API_KEY 环境变量")
            
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # 使用gpt-4o-mini模型

    def generate_content(self, input_text, platform, style, length):
        """
        使用GPT-4o-mini生成内容
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(input_text, platform, style, length)
            
            # 调用API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的社交媒体文案撰写专家，擅长根据用户的输入生成吸引人的文案。请直接返回生成的文案，不要添加任何解释或说明。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=length * 2,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            # 获取生成的内容
            generated_text = completion.choices[0].message.content.strip()
            
            return generated_text

        except Exception as e:
            error_msg = str(e)
            print(f"OpenAI API error: {error_msg}")  # 记录详细错误信息
            
            if "API key" in error_msg:
                return "系统配置有误，请联系管理员"
            elif "model" in error_msg:
                return "AI模型暂时不可用，请稍后重试"
            else:
                return "内容生成遇到问题，请重试"

    def _build_prompt(self, input_text, platform, style, length):
        """
        构建提示词
        """
        platform_prompts = {
            '微信朋友圈': "这是一条微信朋友圈，需要简洁有趣，富有个人特色",
            '小红书': "这是一条小红书笔记，需要真实感人，富有情感共鸣",
            '微博': "这是一条微博，需要简短有力，易于传播",
            'B站': "这是一条B站动态，需要有趣生动，贴近年轻人文化"
        }

        style_prompts = {
            '轻松': "使用轻松愉快的语气",
            '正式': "使用正式专业的语气",
            '幽默': "使用幽默诙谐的语气",
            '文艺': "使用优美文艺的语气"
        }

        prompt = f"""
请根据以下要求生成一段社交媒体文案：

1. 原始文本：{input_text}
2. 平台特点：{platform_prompts.get(platform, '通用社交平台')}
3. 文案风格：{style_prompts.get(style, '自然风格')}
4. 长度要求：控制在{length}字以内
5. 其他要求：
   - 保持语言自然流畅
   - 突出情感共鸣
   - 避免过度修饰
   - 不要使用标签和emoji
   - 确保内容积极向上
   - 保持文案的原创性和真实性

请直接返回生成的文案，不需要任何额外的解释或说明。
"""
        return prompt 