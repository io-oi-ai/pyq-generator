class SceneDetector:
    def detect_scene(self, text, images=None):
        """基于用户输入智能判断场景"""
        
        # 情感分析
        emotion_score = self.analyze_emotion(text)
        
        # 关键词提取
        keywords = self.extract_keywords(text)
        
        # 图片场景识别
        if images:
            image_scenes = self.analyze_images(images)
            
        # 场景匹配
        matched_scene = self.match_scene(
            emotion_score,
            keywords,
            image_scenes
        )
        
        return matched_scene l