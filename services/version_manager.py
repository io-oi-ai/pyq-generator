import json
from datetime import datetime
from pathlib import Path

class VersionManager:
    def __init__(self, versions_file="versions.json"):
        self.versions_file = versions_file
        self.versions = self._load_versions()

    def _load_versions(self):
        """加载版本信息"""
        if Path(self.versions_file).exists():
            with open(self.versions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"versions": []}

    def _save_versions(self):
        """保存版本信息"""
        with open(self.versions_file, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, ensure_ascii=False, indent=2)

    def save_version(self, content, version_name=None, description=None):
        """
        保存新版本
        :param content: 内容
        :param version_name: 版本名称（可选）
        :param description: 版本描述（可选）
        :return: 版本信息
        """
        timestamp = datetime.now().isoformat()
        version_info = {
            "id": len(self.versions["versions"]) + 1,
            "name": version_name or f"v{len(self.versions['versions']) + 1}",
            "content": content,
            "description": description,
            "created_at": timestamp
        }
        self.versions["versions"].append(version_info)
        self._save_versions()
        return version_info

    def get_version(self, version_id=None, version_name=None):
        """
        获取指定版本
        :param version_id: 版本ID
        :param version_name: 版本名称
        :return: 版本信息
        """
        for version in self.versions["versions"]:
            if (version_id and version["id"] == version_id) or \
               (version_name and version["name"] == version_name):
                return version
        return None

    def list_versions(self):
        """获取所有版本列表"""
        return self.versions["versions"] 