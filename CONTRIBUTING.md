# 🤝 贡献指南

感谢您考虑为 CodeMao SDK 做出贡献！我们欢迎各种形式的贡献，包括错误报告、功能建议、文档改进和代码贡献。

## 🚀 快速开始

1. **Fork 项目** - 点击右上角的 "Fork" 按钮
2. **克隆项目** - 将您的 fork 克隆到本地
3. **创建分支** - 为您的功能或修复创建新分支
4. **进行更改** - 进行您的改进
5. **运行测试** - 确保所有测试通过
6. **提交 PR** - 提交 Pull Request

## 📋 贡献类型

### 🐛 报告错误

如果您发现了错误，请通过 [GitHub Issues](https://github.com/nichengfuben/codemao-sdk-for-python/issues) 报告。

**错误报告模板**：
```markdown
**描述**
清晰简洁地描述错误。

**重现步骤**
1. 转到 '...'
2. 点击 '...'
3. 向下滚动到 '...'
4. 看到错误

**预期行为**
清晰简洁地描述您期望发生的事情。

**截图**
如果适用，请添加截图以帮助解释您的问题。

**环境 (请完成以下信息):**
- OS: [例如 iOS]
- Python版本: [例如 3.9]
- SDK版本: [例如 1.0.0]

**附加上下文**
在此处添加有关问题的任何其他上下文。
```

### 💡 功能建议

如果您有功能建议，请通过 [GitHub Issues](https://github.com/nichengfuben/codemao-sdk-for-python/issues) 提交。

**功能建议模板**：
```markdown
**您的功能请求是否与问题相关？请描述。**
清晰简洁地描述问题是什么。例如，当[...]时我总是感到沮丧

**描述您想要的解决方案**
清晰简洁地描述您想要发生的事情。

**描述您考虑过的替代方案**
清晰简洁地描述您考虑过的任何替代解决方案或功能。

**附加上下文**
在此处添加有关功能请求的任何其他上下文或截图。
```

### 📝 文档改进

文档改进总是受欢迎的！您可以：
- 修复拼写错误
- 改进文档清晰度
- 添加更多示例
- 改进API文档

### 💻 代码贡献

#### 开发环境设置

1. **克隆项目**：
```bash
git clone https://github.com/YOUR_USERNAME/codemao-sdk-for-python.git
cd codemao-sdk-for-python
```

2. **创建虚拟环境**：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. **安装开发依赖**：
```bash
pip install -e .[dev]
```

4. **安装预提交钩子**：
```bash
pre-commit install
```

#### 代码风格

我们使用以下工具确保代码质量：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **mypy**: 类型检查

**运行代码质量检查**：
```bash
# 格式化代码
black src/ tests/
isort src/ tests/

# 运行代码检查
flake8 src/ tests/
mypy src/

# 运行所有检查
pre-commit run --all-files
```

#### 测试

**运行测试**：
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_client.py

# 运行带有覆盖率的测试
pytest --cov=src --cov-report=html

# 运行慢速测试
pytest -m "not slow"
```

**测试覆盖率要求**：
- 单元测试覆盖率：90%+
- 集成测试覆盖率：80%+

#### 提交消息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**类型说明**：
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行的更改）
- `refactor`: 代码重构（既不修复错误也不添加功能）
- `perf`: 性能改进
- `test`: 添加缺失的测试或更正现有测试
- `build`: 影响构建系统或外部依赖的更改
- `ci`: CI配置文件和脚本的更改
- `chore`: 其他不修改src或测试文件的更改
- `revert`: 恢复先前的提交

**示例**：
```
feat: add async support for client

Implement async/await pattern for all API methods to improve performance
and user experience.

Closes #123
```

## 🔄 工作流程

### 1. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-description
```

### 2. 进行更改

- 编写代码
- 添加测试
- 更新文档
- 运行测试确保通过

### 3. 提交更改

```bash
git add .
git commit -m "feat: add new feature"
```

### 4. 推送到您的fork

```bash
git push origin feature/your-feature-name
```

### 5. 创建Pull Request

1. 转到 GitHub 上的您的 fork
2. 点击 "Compare & pull request"
3. 填写 PR 模板
4. 提交 PR

## 📝 Pull Request 模板

**请使用以下模板创建 PR**：

```markdown
## 📋 描述

简要描述此 PR 中的更改。

## 🔗 相关问题

链接到相关问题（如果有）：
Fixes #(issue)

## 🚀 更改类型

- [ ] 🐛 错误修复（非破坏性更改，修复了一个问题）
- [ ] ✨ 新功能（非破坏性更改，添加了功能）
- [ ] 💥 破坏性更改（会导致现有功能无法按预期工作的修复或功能）
- [ ] 📚 文档更新
- [ ] 🧪 测试添加或更新
- [ ] 🔧 代码重构
- [ ] ⚡ 性能改进
- [ ] 🏗️ 构建系统更改
- [ ] 🔄 CI/CD 更改

## ✅ 检查清单

- [ ] 我的代码遵循本项目的代码风格
- [ ] 我已经进行了自我审查
- [ ] 我已经添加了测试，证明我的修复有效或新功能按预期工作
- [ ] 我已经相应地更新了文档
- [ ] 我的更改没有产生新的警告
- [ ] 任何相关更改都已记录到 CHANGELOG.md

## 🧪 测试

描述您如何测试这些更改。

## 📸 截图（如果适用）

添加截图以帮助解释您的更改。

## 📝 附加注释

添加任何其他注释或信息。
```

## 🎯 优先级

我们优先处理以下类型的贡献：

1. **🐛 错误修复** - 修复现有功能中的错误
2. **📚 文档改进** - 改进现有文档
3. **✨ 新功能** - 添加新功能（请先讨论）
4. **🧪 测试** - 添加缺失的测试
5. **⚡ 性能** - 性能改进

## 🏷️ 标签

我们使用以下标签来分类问题和 PR：

- `bug`: 需要修复的问题
- `enhancement`: 新功能或改进
- `documentation`: 文档改进
- `good first issue`: 适合新贡献者的问题
- `help wanted`: 需要帮助的问题
- `question`: 需要回答的问题

## 💬 沟通

- **GitHub Issues**: 错误报告和功能建议
- **GitHub Discussions**: 一般讨论和问题
- **Pull Requests**: 代码贡献

## 🙏 感谢

感谢您对 CodeMao SDK 的贡献！您的贡献有助于让这个项目变得更好。

## 📞 联系

如果您有任何问题，请随时联系我们：

- **邮件**: [contact@codemao-sdk.com](mailto:contact@codemao-sdk.com)
- **GitHub Discussions**: [项目讨论区](https://github.com/nichengfuben/codemao-sdk-for-python/discussions)

---

**再次感谢您的贡献！** 🎉