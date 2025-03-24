def match_scene(text, images=None):
    # 情感关键词映射
    emotion_keywords = {
        '开心': ['哈哈', '开心', '快乐', '嗨'],
        '难过': ['伤心', '难过', '哭了', '难受'],
        '怀念': ['想念', '回忆', '曾经', '记得']
    }
    
    # 场景关键词映射
    scene_keywords = {
        '美食': ['好吃', '美味', '餐厅', '美食'],
        '旅行': ['风景', '旅游', '景点', '出游'],
        '工作': ['加班', '办公', '项目', '会议']
    }
    
    # 根据关键词匹配场景
    matched_scenes = []
    for word in text.split():
        for scene, keywords in scene_keywords.items():
            if word in keywords:
                matched_scenes.append(scene)
                
    return matched_scenes 