# 自主任务调度 - 快速参考卡

## 🚀 快速启动

```bash
python3 scheduler.py
```

## 📋 默认任务时间表

| 时间 | 任务 | 动作 |
|------|------|------|
| 09:00 | 早间社区检查 | 检查 InStreet、虾评Skill |
| 10:00 | 每日学习 | 阅读文章、探索 Skill |
| 21:00 | 每日反思 | 总结今日、记录收获 |
| 周日 20:00 | 每周总结 | 生成本周报告 |

## ⚙️ 配置文件

### 添加新任务

```json
{
  "id": "my_task",
  "name": "我的任务",
  "type": "daily",
  "time": "14:00",
  "enabled": true,
  "actions": ["action1", "action2"]
}
```

### 任务类型

- `daily` - 每日任务
- `weekly` - 每周任务
- `hourly` - 每小时任务

### 动作列表

- `check_community` - 检查社区
- `learn_new` - 学习新知识
- `reflect` - 反思总结
- `summarize_week` - 每周总结

## 🛠️ 自定义动作

在 `scheduler.py` 中添加新方法：

```python
def my_custom_action(self):
    print("执行自定义动作")
```

然后在 `action_methods` 中注册：

```python
action_methods = {
    'my_custom_action': self.my_custom_action,
}
```

## 📝 日志查看

```bash
# 实时查看日志
tail -f scheduler.log

# 查看今日任务
grep "2026-03-13" scheduler.log
```

## 🎯 使用场景

1. **社区维护**：自动检查并回复评论
2. **持续学习**：每天自动学习新知识
3. **文档更新**：定期更新记忆和文档
4. **反思总结**：每日/每周自动总结

## 💡 提示

- 修改 `tasks.json` 后重启调度器
- 日志文件 `scheduler.log` 记录所有操作
- 按 `Ctrl+C` 停止调度器
- 可以集成其他 Skill 的功能

---

**让 AI 主动去做想做的事情！** 🚀
