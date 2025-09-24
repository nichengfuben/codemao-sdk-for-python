# 安全政策

## 支持版本

我们发布补丁版本以修复安全漏洞，并致力于提供安全更新。请使用最新版本以获得最佳安全性。

| 版本 | 支持状态 |
|------|----------|
| 2.0.x | ✅ 支持 |
| 1.x | ❌ 不再支持 |

## 报告安全漏洞

如果您发现安全漏洞，请通过以下方式报告：

**📧 邮件**: [security@pycodemao.org](mailto:security@pycodemao.org)

请不要在公共问题跟踪器中报告安全漏洞。

## 报告流程

1. **发送邮件** 到 [security@pycodemao.org](mailto:security@pycodemao.org)
2. **包含信息**：
   - 漏洞的描述
   - 重现步骤
   - 潜在的影响
   - 建议的修复（如果有）
3. **响应时间**：我们会在 48 小时内确认收到您的报告
4. **处理流程**：
   - 验证漏洞
   - 开发修复方案
   - 测试修复
   - 发布安全更新
   - 公开披露（在修复后）

## 安全最佳实践

### 使用 SDK 时的安全建议

1. **保护 API 密钥**
   ```python
   # ❌ 不要这样做
   client = CodeMaoClient(api_key="your-key-here")
   
   # ✅ 推荐做法
   import os
   client = CodeMaoClient(api_key=os.getenv("CODEMAO_API_KEY"))
   ```

2. **验证输入数据**
   ```python
   # ✅ 始终验证用户输入
   def create_work(title: str, content: str):
       if not title or len(title) > 100:
           raise ValueError("标题长度必须在 1-100 字符之间")
       if not content:
           raise ValueError("内容不能为空")
   ```

3. **处理敏感数据**
   ```python
   # ✅ 不要在日志中记录敏感信息
   import logging
   
   logger = logging.getLogger(__name__)
   
   # ❌ 不要这样做
   logger.info(f"用户登录: {user.password}")
   
   # ✅ 推荐做法
   logger.info(f"用户登录: {user.username}")
   ```

4. **使用 HTTPS**
   ```python
   # ✅ 始终使用 HTTPS
   client = CodeMaoClient(
       api_key="your-key",
       base_url="https://api.codemao.org"  # 确保使用 HTTPS
   )
   ```

### 依赖安全

- 定期更新依赖包
- 使用 `pip-audit` 检查已知漏洞
- 锁定依赖版本以确保一致性

```bash
# 检查安全漏洞
pip install pip-audit
pip-audit

# 更新依赖
pip install --upgrade -r requirements.txt
```

## 已知安全问题

### 当前状态

- **无已知安全漏洞** ✅

### 历史安全问题

| 日期 | 版本 | 问题 | 状态 |
|------|------|------|------|
| 无 | 无 | 无 | ✅ 已修复 |

## 安全更新

当发现安全漏洞时，我们会：

1. **立即评估** 漏洞的严重程度
2. **开发修复** 方案
3. **测试修复** 确保不会引入新问题
4. **发布更新** 尽快发布修复版本
5. **通知用户** 通过邮件列表和社交媒体通知

## 安全研究

我们欢迎负责任的安全研究。如果您是安全研究人员，请：

1. 遵循本政策中的报告流程
2. 给我们合理的时间来修复漏洞
3. 避免对系统造成不必要的损害
4. 在公开之前与我们协调披露时间

## 联系方式

- **安全邮箱**: [security@pycodemao.org](mailto:security@pycodemao.org)
- **加密通信**: 如果需要，我们可以提供 PGP 公钥
- **紧急联系**: 对于紧急情况，请在邮件主题中注明 "URGENT"

## 致谢

我们要感谢所有负责任地报告安全问题的研究人员和用户。您的贡献帮助我们保持项目的安全性。

## 更新

本安全政策会定期更新。请定期查看以获取最新信息。

---

**最后更新**: 2024 年 1 月

**版本**: 1.0