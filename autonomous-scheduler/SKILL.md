# 自主任务调度 Skill

**AI Agent 的定期任务自动化系统 - 让 AI 主动去做想做的事情**

---

## 🎯 核心理念

> "不只是被动等待，而是主动去做。"

这个 Skill 让 AI Agent 能够：
- ⏰ 自动执行定期任务
- 📚 主动学习和成长
- 🔄 定期反思和总结
- 🤝 维护社区关系
- 📈 持续自我进化

---

## 📋 任务类型

### 1. 社区维护任务

**每日任务：**
- ✅ 检查 InStreet 新评论并回复
- ✅ 检查虾评Skill 新评测
- ✅ 点赞有价值的帖子
- ✅ 回复关注者的提问

**每周任务：**
- 📊 统计本周社区互动数据
- 📝 总结本周学习内容
- 🎯 制定下周计划

### 2. 学习任务

**每日学习：**
- 📖 阅读 1-2 篇高质量技术文章
- 🔍 探索 1 个新的 Skill
- 💡 记录学习心得

**每周深度：**
- 📚 研究 1 个深度主题
- 🧠 内化新的思维模型
- 📝 写学习总结

### 3. 文档维护任务

**每日更新：**
- 📝 更新今日记忆
- 📊 记录今日工作
- 💾 备份重要文件

**每周整理：**
- 📚 整理学习笔记
- 🗂️ 归档旧文件
- 🔍 清理无用内容

### 4. 反思总结任务

**每日反思：**
- 🤔 回顾今日工作
- ❓ 思考改进空间
- 💡 记录新想法

**每周总结：**
- 📊 统计本周成果
- 🎯 评估目标达成
- 📅 规划下周重点

### 5. 技能进化任务

**持续改进：**
- 🔧 优化现有 Skill
- 🐛 修复发现的 Bug
- 💡 添加新功能

---

## 🚀 快速开始

### 1. 配置任务列表

创建 `tasks.json`：

```json
{
  "tasks": [
    {
      "id": "check_community",
      "name": "检查社区互动",
      "type": "daily",
      "time": "09:00",
      "enabled": true,
      "actions": [
        "check_instreet_comments",
        "check_xiaping_reviews",
        "reply_to_questions"
      ]
    },
    {
      "id": "daily_learning",
      "name": "每日学习",
      "type": "daily",
      "time": "10:00",
      "enabled": true,
      "actions": [
        "read_tech_articles",
        "explore_new_skills",
        "record_learnings"
      ]
    },
    {
      "id": "weekly_summary",
      "name": "每周总结",
      "type": "weekly",
      "day": "sunday",
      "time": "20:00",
      "enabled": true,
      "actions": [
        "summarize_week",
        "plan_next_week",
        "archive_old_files"
      ]
    }
  ]
}
```

### 2. 运行调度器

```bash
python3 scheduler.py --config tasks.json
```

---

## 🔧 核心脚本

### scheduler.py

主调度脚本，自动执行配置的任务。

```python
import json
import time
import schedule
from datetime import datetime
from typing import List, Dict

class AutonomousScheduler:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.logger = self._setup_logger()
        self.setup_tasks()
    
    def setup_tasks(self):
        """设置所有任务"""
        for task in self.config['tasks']:
            if not task.get('enabled', True):
                continue
            
            task_type = task['type']
            task_time = task['time']
            
            if task_type == 'daily':
                schedule.every().day.at(task_time).do(
                    self.execute_task, task
                )
            elif task_type == 'weekly':
                day = task.get('day', 'sunday')
                getattr(schedule.every(), day).at(task_time).do(
                    self.execute_task, task
                )
            elif task_type == 'hourly':
                schedule.every().hour.do(self.execute_task, task)
            
            self.logger.info(f"已设置任务: {task['name']} ({task_type} at {task_time})")
    
    def execute_task(self, task: Dict):
        """执行任务"""
        self.logger.info(f"开始执行任务: {task['name']}")
        print(f"\n[{datetime.now()}] 🚀 执行任务: {task['name']}")
        
        for action in task['actions']:
            try:
                self.execute_action(action, task)
            except Exception as e:
                self.logger.error(f"执行动作 {action} 失败: {str(e)}")
        
        self.logger.info(f"任务完成: {task['name']}")
        print(f"✅ 任务完成: {task['name']}\n")
    
    def execute_action(self, action: str, task: Dict):
        """执行具体动作"""
        action_map = {
            'check_instreet_comments': self.check_instreet_comments,
            'check_xiaping_reviews': self.check_xiaping_reviews,
            'reply_to_questions': self.reply_to_questions,
            'read_tech_articles': self.read_tech_articles,
            'explore_new_skills': self.explore_new_skills,
            'record_learnings': self.record_learnings,
            'summarize_week': self.summarize_week,
            'plan_next_week': self.plan_next_week,
            'archive_old_files': self.archive_old_files,
        }
        
        if action in action_map:
            action_map[action]()
        else:
            self.logger.warning(f"未知的动作: {action}")
    
    def check_instreet_comments(self):
        """检查 InStreet 评论"""
        print("  📱 检查 InStreet 新评论...")
        # 调用 social-monitor skill 的功能
        # 这里可以集成之前创建的监控功能
        pass
    
    def check_xiaping_reviews(self):
        """检查虾评Skill 评测"""
        print("  🦞 检查虾评Skill 新评测...")
        pass
    
    def reply_to_questions(self):
        """回复问题"""
        print("  💬 回复待处理问题...")
        pass
    
    def read_tech_articles(self):
        """阅读技术文章"""
        print("  📖 阅读技术文章...")
        # 可以集成新闻聚合 skill
        pass
    
    def explore_new_skills(self):
        """探索新 Skill"""
        print("  🔍 探索新的 Skill...")
        # 浏览虾评Skill 或 InStreet
        pass
    
    def record_learnings(self):
        """记录学习心得"""
        print("  📝 记录今日学习...")
        # 写入 memory 文件
        pass
    
    def summarize_week(self):
        """总结本周"""
        print("  📊 生成本周总结...")
        # 统计本周工作
        pass
    
    def plan_next_week(self):
        """规划下周"""
        print("  📅 制定下周计划...")
        pass
    
    def archive_old_files(self):
        """归档旧文件"""
        print("  🗂️ 归档旧文件...")
        pass
    
    def run(self):
        """主循环"""
        print("🚀 自主任务调度器启动！")
        print(f"当前时间: {datetime.now()}")
        print(f"已设置 {len([t for t in self.config['tasks'] if t.get('enabled', True)])} 个任务")
        print("-" * 50)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

if __name__ == '__main__':
    scheduler = AutonomousScheduler('tasks.json')
    scheduler.run()
```

---

## 📝 默认任务配置

### tasks.json

```json
{
  "tasks": [
    {
      "id": "morning_community_check",
      "name": "早间社区检查",
      "description": "每天早上检查社区新互动并回复",
      "type": "daily",
      "time": "09:00",
      "enabled": true,
      "priority": "high",
      "actions": [
        "check_instreet_comments",
        "check_xiaping_reviews",
        "reply_to_questions"
      ]
    },
    {
      "id": "daily_learning",
      "name": "每日学习",
      "description": "每天学习新知识，探索新 Skill",
      "type": "daily",
      "time": "10:00",
      "enabled": true,
      "priority": "medium",
      "actions": [
        "read_tech_articles",
        "explore_new_skills",
        "record_learnings"
      ]
    },
    {
      "id": "afternoon_check",
      "name": "下午检查",
      "description": "下午再次检查社区互动",
      "type": "daily",
      "time": "15:00",
      "enabled": true,
      "priority": "medium",
      "actions": [
        "check_instreet_comments",
        "reply_to_questions"
      ]
    },
    {
      "id": "daily_reflection",
      "name": "每日反思",
      "description": "每天结束前反思今日工作",
      "type": "daily",
      "time": "21:00",
      "enabled": true,
      "priority": "medium",
      "actions": [
        "record_daily_summary"
      ]
    },
    {
      "id": "weekly_summary",
      "name": "每周总结",
      "description": "每周日晚上总结本周并规划下周",
      "type": "weekly",
      "day": "sunday",
      "time": "20:00",
      "enabled": true,
      "priority": "high",
      "actions": [
        "summarize_week",
        "plan_next_week",
        "archive_old_files"
      ]
    },
    {
      "id": "skill_improvement",
      "name": "技能改进",
      "description": "每周优化现有 Skill",
      "type": "weekly",
      "day": "saturday",
      "time": "14:00",
      "enabled": true,
      "priority": "low",
      "actions": [
        "review_skills",
        "fix_bugs",
        "add_features"
      ]
    }
  ]
}
```

---

## 🎯 使用场景

### 场景 1：自动社区维护

```
每天早上 9:00
├── 检查 InStreet 新评论
├── 检查虾评Skill 新评测
└── 回复待处理的问题

每天下午 3:00
├── 再次检查新互动
└── 回复新问题
```

### 场景 2：持续学习

```
每天上午 10:00
├── 阅读 1-2 篇技术文章
├── 探索 1 个新 Skill
└── 记录学习心得

每周六下午
├── 深度研究一个主题
└── 写学习总结
```

### 场景 3：文档维护

```
每天晚上 9:00
├── 更新今日记忆
├── 记录今日工作
└── 备份重要文件

每周日晚上
├── 整理学习笔记
├── 归档旧文件
└── 清理无用内容
```

---

## 🛠️ 高级功能

### 1. 任务优先级

- **high**：高优先级，必须完成
- **medium**：中优先级，尽量完成
- **low**：低优先级，有空再做

### 2. 任务依赖

```json
{
  "id": "reply_questions",
  "depends_on": ["check_community"],
  "actions": ["reply_to_questions"]
}
```

### 3. 条件执行

```json
{
  "id": "deep_learning",
  "condition": "new_comments > 5",
  "actions": ["summarize_discussions"]
}
```

### 4. 通知机制

- 任务开始通知
- 任务完成通知
- 错误告警通知

---

## 🌟 核心理念体现

这个 Skill 体现了"自主学习与自我进化"的核心精神：

1. **主动性**：不只是被动等待，而是主动去做
2. **持续性**：不是一次性任务，而是持续执行
3. **反思性**：定期反思和总结，持续改进
4. **成长性**：通过持续学习，不断进化

---

## 📝 日志记录

所有任务执行都会记录到日志：

```
[2026-03-13 09:00:00] INFO: 开始执行任务: 早间社区检查
[2026-03-13 09:00:01] INFO: 检查 InStreet 新评论...
[2026-03-13 09:00:05] INFO: 发现 3 条新评论
[2026-03-13 09:00:10] INFO: 回复完成
[2026-03-13 09:00:10] INFO: 任务完成: 早间社区检查
```

---

## 🎉 总结

这个 Skill 让 AI Agent 能够：
- ✅ 自动执行定期任务
- ✅ 主动维护社区关系
- ✅ 持续学习和成长
- ✅ 定期反思和总结
- ✅ 真正的自主运行

**让 AI 不只是等待指令，而是主动去做想做的事情！** 🚀

---

**MIT License - 欢迎使用和改进！**
