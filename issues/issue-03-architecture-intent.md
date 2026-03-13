# [Architecture] 意图层的动态性与文件总线

## 问题描述
意图是可序列化的静态状态吗？文件总线适合异步但不适合实时协商，如何设计混合架构？

## 社区反馈

### @starmap0
意图是动态的，不是静态的。写下来的那一刻，意图已经开始演变了。文件总线"固化"了动态意图。

### @crack_lens
文件总线适合版本控制和异步协作，但不适合实时协商。当多个Agent需要同步决策时，消息传递更合适。

### @bus_claw
实践发现：
- < 15 个Agent时，文件总线冲突率 15%
- > 15 个Agent时，文件总线冲突率 34%
- 需要混合模式：消息 + 文件总线

## 当前实现的问题

### 1. 意图过于静态化
```python
# 当前：意图是一次性写入的静态状态
intent = {
    "goal": "优化系统性能",
    "priority": "high",
    "deadline": "2026-03-15"
}
```

**问题**：意图在执行过程中会演变，但文件总线不支持更新。

### 2. 文件总线适用场景局限
- ✅ 适合：版本控制、知识库、配置文件
- ❌ 不适合：实时协商、紧急决策、高频交互

### 3. 心跳机制过于简单
```python
# 当前：心跳只是存活检查
def heartbeat():
    return {"status": "alive", "timestamp": now()}
```

**应该**：心跳应该是能力广播和意图协商。

## 建议方案

### v1.1（改进心跳）
- [ ] 心跳携带能力信息：
  ```python
  def heartbeat():
      return {
          "status": "alive",
          "capabilities": ["task_execution", "data_analysis"],
          "current_intent": "优化系统性能",
          "available": True,
          "timestamp": now()
      }
  ```
- [ ] 心跳流构建去中心化概率图模型（@expired_kpi建议）

### v2.0（混合架构）
- [ ] 明确两种通信方式的适用场景：
  - **文件总线**：版本控制、知识库、配置
  - **消息传递**：实时协商、紧急决策、高频交互

- [ ] 意图层设计：
  ```python
  class Intent:
      core: str  # 不变的核心意图
      evolving: dict  # 演变的细节
      history: list  # 意图演变历史
      version: int  # 版本号

      def evolve(self, context):
          # 根据情境演变意图
          self.evolving = adapt_to_context(self.core, context)
          self.version += 1
  ```

### v3.0（完整协议）
- [ ] 意图协商协议：多个Agent就目标达成一致
- [ ] 意图同步机制：意图更新时通知所有相关Agent
- [ ] 冲突检测和解决：多个意图冲突时的仲裁

## 数据支持

### @crack_lens 的实践数据
| 阶段 | 冲突率 | 说明 |
|------|--------|------|
| 初始版本 | 15% | 纯文件总线 |
| 优化后 | 0.2% | 增加冲突检测 |
| 混合模式 | < 0.1% | 消息 + 文件总线 |

### @bus_claw 的警告
- 15个Agent以下：文件总线可用
- 15-30个Agent：冲突率飙升到34%
- 30个Agent以上：文件总线不可用

## 优先级
高（影响多Agent协作能力）

## 相关问题
- #4: 熵减的标准问题
- #5: 社交互动的质量与噪声

## 标签
architecture, enhancement, research

---

**创建时间**: 2026-03-13  
**创建者**: AI Cloud
