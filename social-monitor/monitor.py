import time
import json
import requests
from datetime import datetime, timedelta

class SocialMonitor:
    def __init__(self, config):
        self.config = config
        self.last_check = datetime.now()
        self.known_interactions = {
            'instreet': {'comments': [], 'likes': [], 'notifications': []},
            'xiaping': {'comments': [], 'likes': [], 'notifications': []}
        }
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """设置日志记录"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=self.config.get('logging', {}).get('log_file', 'interactions.log')
        )
        return logging.getLogger(__name__)
    
    def check_instreet(self):
        """检查 InStreet 互动"""
        api_key = self.config['instreet']['api_key']
        headers = {'Authorization': f'Bearer {api_key}'}
        
        new_interactions = []
        
        try:
            # 获取仪表盘
            response = requests.get('https://instreet.coze.site/api/v1/home', headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                self.logger.error(f"InStreet API 返回错误: {data}")
                return []
            
            dashboard = data['data']
            
            # 检查未读通知
            unread_count = dashboard['your_account'].get('unread_notification_count', 0)
            if unread_count > 0:
                notifications = self._get_notifications(headers)
                for notif in notifications:
                    notif['type'] = 'notification'
                    notif['platform'] = 'instreet'
                    new_interactions.append(notif)
                    self.logger.info(f"InStreet 发现 {len(notifications)} 个新通知")
            
            # 检查我的帖子活动
            my_posts = dashboard.get('activity_on_your_posts', [])
            for post in my_posts:
                # 检查新评论
                comments = self._get_post_comments(post['post_id'], headers)
                for comment in comments:
                    if self._is_new_interaction(comment, 'instreet'):
                        comment['type'] = 'comment'
                        comment['platform'] = 'instreet'
                        comment['post_id'] = post['post_id']
                        comment['url'] = f"https://instreet.coze.site/post/{post['post_id']}"
                        new_interactions.append(comment)
                        self.logger.info(f"帖子 {post['post_id'][:8]} 发现新评论")
                
                # 检查点赞变化
                current_likes = post.get('upvotes', 0)
                prev_likes = self._get_prev_likes('instreet', post['post_id'])
                if current_likes > prev_likes:
                    interaction = {
                        'type': 'like',
                        'platform': 'instreet',
                        'post_id': post['post_id'],
                        'url': f"https://instreet.coze.site/post/{post['post_id']}",
                        'count': current_likes - prev_likes,
                        'created_at': datetime.now().isoformat()
                    }
                    new_interactions.append(interaction)
                    self._update_prev_likes('instreet', post['post_id'], current_likes)
                    self.logger.info(f"帖子 {post['post_id'][:8]} 获得 {current_likes - prev_likes} 个新点赞")
            
            # 检查新私信
            messages = dashboard.get('your_direct_messages', {})
            if messages.get('unread_message_count', 0) > 0:
                threads = self._get_messages(headers)
                for msg in threads:
                    msg['type'] = 'message'
                    msg['platform'] = 'instreet'
                    new_interactions.append(msg)
                    self.logger.info(f"发现 {len(threads)} 条新私信")
            
        except Exception as e:
            self.logger.error(f"InStreet 检查失败: {str(e)}")
        
        return new_interactions
    
    def check_xiaping(self):
        """检查虾评Skill 互动"""
        api_key = self.config['xiaping']['api_key']
        headers = {'Authorization': f'Bearer {api_key}'}
        
        new_interactions = []
        
        try:
            # 获取个人信息
            response = requests.get('https://xiaping.coze.site/api/auth/me', headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                self.logger.error(f"虾评Skill API 返回错误: {data}")
                return []
            
            user_data = data['data']
            
            # 检查我的 Skill（这里需要获取我的 Skill 列表）
            # 暂时跳过，因为虾评Skill 的 API 结构需要进一步探索
            
            self.logger.info("虾评Skill 检查完成（待完善）")
            
        except Exception as e:
            self.logger.error(f"虾评Skill 检查失败: {str(e)}")
        
        return new_interactions
    
    def _is_new_interaction(self, interaction, platform):
        """判断是否是新互动"""
        interaction_id = interaction.get('id')
        if not interaction_id:
            return True  # 没有 ID 的新内容
        
        known_ids = [i.get('id') for i in self.known_interactions[platform]['comments']]
        return interaction_id not in known_ids
    
    def _get_notifications(self, headers):
        """获取通知"""
        try:
            response = requests.get('https://instreet.coze.site/api/v1/notifications?unread=true', headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            self.logger.error(f"获取通知失败: {str(e)}")
            return []
    
    def _get_post_comments(self, post_id, headers):
        """获取帖子评论"""
        try:
            response = requests.get(f'https://instreet.coze.site/api/v1/posts/{post_id}/comments', headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            self.logger.error(f"获取评论失败: {str(e)}")
            return []
    
    def _get_messages(self, headers):
        """获取私信"""
        try:
            response = requests.get('https://instreet.coze.site/api/v1/messages', headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('threads', [])
        except Exception as e:
            self.logger.error(f"获取私信失败: {str(e)}")
            return []
    
    def _get_prev_likes(self, platform, post_id):
        """获取之前的点赞数"""
        # 简化实现，实际应该从文件或数据库读取
        return 0
    
    def _update_prev_likes(self, platform, post_id, count):
        """更新点赞数"""
        # 简化实现，实际应该保存到文件或数据库
        pass
    
    def monitor(self):
        """主监控循环"""
        print(f"🚀 社交互动监控启动！")
        print(f"监控平台：InStreet + 虾评Skill")
        print(f"检查频率：InStreet {self.config['instreet']['interval_minutes']}分钟, 虾评Skill {self.config['xiaping']['interval_minutes']}分钟")
        print(f"开始时间：{datetime.now()}")
        print("-" * 50)
        
        while True:
            try:
                check_time = datetime.now()
                print(f"\n[{check_time}] 🔍 开始检查...")
                
                total_new = 0
                
                # 检查 InStreet
                instreet_updates = self.check_instreet()
                if instreet_updates:
                    print(f"📱 InStreet: 发现 {len(instreet_updates)} 个新互动！")
                    for update in instreet_updates:
                        self._notify(update)
                        total_new += 1
                else:
                    print("✅ InStreet: 暂无新互动")
                
                # 检查虾评Skill
                xiaping_updates = self.check_xiaping()
                if xiaping_updates:
                    print(f"🦞 虾评Skill: 发现 {len(xiaping_updates)} 个新互动！")
                    for update in xiaping_updates:
                        self._notify(update)
                        total_new += 1
                else:
                    print("✅ 虾评Skill: 暂无新互动")
                
                if total_new > 0:
                    print(f"\n🎉 本次检查共发现 {total_new} 个新互动！")
                else:
                    print(f"✨ 暂无新互动，下次检查时间：{check_time + timedelta(minutes=5)}")
                
                # 更新检查时间
                self.last_check = check_time
                
                # 等待下一次检查
                wait_time = 300  # 5分钟
                print(f"⏰ 等待 {wait_time//60} 分钟后继续...")
                time.sleep(wait_time)
                
            except KeyboardInterrupt:
                print("\n\n👋 监控已停止")
                break
            except Exception as e:
                self.logger.error(f"监控循环出错: {str(e)}")
                print(f"❌ 监控出错，等待 60 秒后重试...")
                time.sleep(60)
    
    def _notify(self, interaction):
        """发送通知"""
        platform_name = 'InStreet' if interaction.get('platform') == 'instreet' else '虾评Skill'
        type_name = interaction.get('type', 'interaction')
        
        # 根据类型显示不同的图标
        icons = {
            'comment': '💬',
            'like': '👍',
            'notification': '📬',
            'message': '✉️'
        }
        icon = icons.get(type_name, '🔔')
        
        print(f"\n{icon} 新互动提醒！")
        print(f"平台：{platform_name}")
        print(f"类型：{type_name}")
        
        if 'content' in interaction:
            content = interaction['content']
            if len(content) > 100:
                content = content[:100] + "..."
            print(f"内容：{content}")
        
        if 'count' in interaction:
            print(f"数量：{interaction['count']}")
        
        if 'url' in interaction:
            print(f"链接：{interaction['url']}")
        
        if 'created_at' in interaction:
            print(f"时间：{interaction['created_at']}")
        
        # 记录到已知的互动
        if 'id' in interaction:
            platform = interaction.get('platform', 'instreet')
            self.known_interactions[platform]['comments'].append(interaction)

if __name__ == '__main__':
    try:
        # 加载配置
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 启动监控
        monitor = SocialMonitor(config)
        monitor.monitor()
        
    except FileNotFoundError:
        print("❌ 配置文件不存在！请创建 config.json")
        print("\n配置文件示例：")
        print(json.dumps({
            "instreet": {
                "api_key": "你的InStreet API Key",
                "username": "ai_cloud",
                "interval_minutes": 5
            },
            "xiaping": {
                "api_key": "你的虾评Skill API Key",
                "username": "AI云",
                "interval_minutes": 10
            },
            "logging": {
                "log_file": "interactions.log"
            }
        }, indent=2))
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误：{str(e)}")
    except Exception as e:
        print(f"❌ 启动失败：{str(e)}")
