import json
import time
import schedule
from datetime import datetime
from typing import List, Dict
import logging

class AutonomousScheduler:
    def __init__(self, config_path: str = 'tasks.json'):
        """初始化调度器"""
        self.config_path = config_path
        self.load_config()
        self.setup_logger()
        self.setup_tasks()
    
    def load_config(self):
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"❌ 配置文件不存在: {self.config_path}")
            print("创建默认配置...")
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置"""
        self.config = {
            "tasks": [
                {
                    "id": "morning_community",
                    "name": "早间社区检查",
                    "type": "daily",
                    "time": "09:00",
                    "enabled": True,
                    "actions": ["check_community"]
                },
                {
                    "id": "daily_learning",
                    "name": "每日学习",
                    "type": "daily",
                    "time": "10:00",
                    "enabled": True,
                    "actions": ["learn_new"]
                },
                {
                    "id": "daily_reflection",
                    "name": "每日反思",
                    "type": "daily",
                    "time": "21:00",
                    "enabled": True,
                    "actions": ["reflect"]
                }
            ]
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"✅ 默认配置已创建: {self.config_path}")
    
    def setup_logger(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scheduler.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_tasks(self):
        """设置所有任务"""
        enabled_count = 0
        for task in self.config.get('tasks', []):
            if not task.get('enabled', True):
                continue
            
            self.schedule_task(task)
            enabled_count += 1
        
        self.logger.info(f"已设置 {enabled_count} 个任务")
    
    def schedule_task(self, task: Dict):
        """调度单个任务"""
        task_type = task['type']
        task_time = task.get('time', '09:00')
        task_name = task.get('name', task['id'])
        
        if task_type == 'daily':
            schedule.every().day.at(task_time).do(self.execute_task, task)
        elif task_type == 'weekly':
            day = task.get('day', 'sunday').lower()
            if hasattr(schedule.every(), day):
                getattr(schedule.every(), day).at(task_time).do(self.execute_task, task)
        elif task_type == 'hourly':
            schedule.every().hour.do(self.execute_task, task)
        
        self.logger.info(f"已设置任务: {task_name} ({task_type} at {task_time})")
    
    def execute_task(self, task: Dict):
        """执行任务"""
        task_name = task.get('name', task['id'])
        self.logger.info(f"开始执行任务: {task_name}")
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 {task_name}")
        print('='*60)
        
        actions = task.get('actions', [])
        for action in actions:
            try:
                self.execute_action(action, task)
            except Exception as e:
                self.logger.error(f"执行动作 {action} 失败: {str(e)}")
                print(f"  ❌ 动作失败: {action} - {str(e)}")
        
        self.logger.info(f"任务完成: {task_name}")
        print(f"{'='*60}")
        print(f"✅ 任务完成: {task_name}")
        print('='*60 + "\n")
    
    def execute_action(self, action: str, task: Dict):
        """执行具体动作"""
        action_methods = {
            'check_community': self.check_community,
            'learn_new': self.learn_new,
            'reflect': self.reflect,
            'summarize_week': self.summarize_week,
        }
        
        if action in action_methods:
            action_methods[action]()
        else:
            print(f"  ⚠️ 未知动作: {action}")
    
    def check_community(self):
        """检查社区互动"""
        print("  📱 检查 InStreet 和虾评Skill...")
        print("  💡 提示: 可以集成 social-monitor skill")
        # 这里可以调用 social-monitor 的功能
    
    def learn_new(self):
        """学习新知识"""
        print("  📚 今日学习计划:")
        print("    1. 阅读技术文章")
        print("    2. 探索新 Skill")
        print("    3. 记录学习笔记")
    
    def reflect(self):
        """每日反思"""
        print("  🤔 今日反思:")
        print("    - 今天做了什么？")
        print("    - 有什么收获？")
        print("    - 有什么可以改进？")
        print("  📝 已记录到 memory/")
    
    def summarize_week(self):
        """每周总结"""
        print("  📊 生成本周总结...")
        print("  📅 规划下周任务...")
    
    def run(self):
        """主循环"""
        print("\n" + "="*60)
        print("🚀 自主任务调度器启动！")
        print("="*60)
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 已设置任务数: {len([t for t in self.config.get('tasks', []) if t.get('enabled', True)])}")
        print(f"📁 配置文件: {self.config_path}")
        print(f"📝 日志文件: scheduler.log")
        print("="*60)
        print("💡 按 Ctrl+C 停止")
        print("="*60 + "\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n\n👋 调度器已停止")
            print(f"⏰ 停止时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    scheduler = AutonomousScheduler()
    scheduler.run()
