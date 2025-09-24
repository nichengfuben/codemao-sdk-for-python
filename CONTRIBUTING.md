# 贡献指南

感谢您对 PyCodeMao 项目的关注！我们欢迎所有形式的贡献，包括代码、文档、测试、问题报告等。

## 开始之前

在贡献之前，请先阅读以下内容：

1. 阅读我们的 [行为准则](CODE_OF_CONDUCT.md)
2. 查看现有的 [问题](https://github.com/pycodemao/pycodemao/issues) 和 [拉取请求](https://github.com/pycodemao/pycodemao/pulls)
3. 加入我们的 [Discord 社区](https://discord.gg/pycodemao) 进行讨论

## 贡献方式

### 报告问题

如果您发现了 bug 或者有功能建议，请通过以下方式报告：

1. **搜索现有问题**：在创建新问题之前，请先搜索是否已经有类似的问题
2. **创建新问题**：使用我们的问题模板创建详细的问题报告
3. **提供详细信息**：包括复现步骤、期望行为、实际行为、环境信息等

### 代码贡献

#### 开发环境设置

1. **Fork 项目**：点击 GitHub 上的 Fork 按钮
2. **克隆项目**：
   ```bash
   git clone https://github.com/您的用户名/pycodemao.git
   cd pycodemao
   ```

3. **创建虚拟环境**：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或者
   .\venv\Scripts\activate  # Windows
   ```

4. **安装开发依赖**：
   ```bash
   pip install -e ".[dev]"
   ```

5. **安装预提交钩子**：
   ```bash
   pre-commit install
   ```

#### 开发流程

1. **创建分支**：
   ```bash
   git checkout -b feature/您的功能名称
   # 或者
   git checkout -b fix/问题修复
   ```

2. **编写代码**：
   - 遵循项目的编码规范
   - 添加适当的类型注解
   - 编写单元测试
   - 更新文档

3. **运行测试**：
   ```bash
   pytest
   pytest --cov=src --cov-report=html  # 带覆盖率
   ```

4. **代码质量检查**：
   ```bash
   black src/ tests/
   isort src/ tests/
   mypy src/
   pylint src/
   ```

5. **提交代码**：
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   ```

#### 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：
```bash
git commit -m "feat: 添加用户搜索功能"
git commit -m "fix: 修复认证超时问题"
git commit -m "docs: 更新 API 文档"
```

### 文档贡献

我们欢迎文档改进，包括：

- 修复拼写错误或语法错误
- 改进现有文档的清晰度
- 添加新的使用示例
- 翻译文档到其他语言

文档文件位于 `docs/` 目录下，使用 Markdown 格式编写。

### 测试贡献

- 添加新的测试用例
- 改进现有测试的覆盖率
- 报告测试中发现的问题

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 编码规范
- 使用 [Black](https://black.readthedocs.io/) 进行代码格式化
- 使用 [isort](https://pycqa.github.io/isort/) 管理导入语句
- 所有函数和方法必须包含类型注解
- 遵循 [PEP 257](https://www.python.org/dev/peps/pep-0257/) 文档字符串规范

### 项目结构

```
src/pycodemao/
├── __init__.py          # 包初始化
├── client.py           # 主要客户端类
├── models.py           # 数据模型
├── exceptions.py       # 异常定义
├── utils.py            # 工具函数
└── types.py            # 类型定义

tests/
├── unit/               # 单元测试
├── integration/        # 集成测试
└── conftest.py        # 测试配置
```

### 测试要求

- 所有新功能必须包含相应的测试
- 测试覆盖率应保持在 90% 以上
- 使用 pytest 作为测试框架
- 测试文件应以 `test_` 开头

示例测试：
```python
import pytest
from pycodemao import CodeMaoClient, UserNotFoundError

@pytest.mark.asyncio
async def test_get_user_success():
    async with CodeMaoClient(api_key="test_key") as client:
        user = await client.get_user("test_user")
        assert user.username == "test_user"

@pytest.mark.asyncio
async def test_get_user_not_found():
    async with CodeMaoClient(api_key="test_key") as client:
        with pytest.raises(UserNotFoundError):
            await client.get_user("non_existent_user")
```

### 文档要求

- 所有公共函数和类必须有文档字符串
- 文档字符串应遵循 Google 风格或 NumPy 风格
- 复杂的算法或业务逻辑需要详细注释
- 更新 API 文档以反映代码变更

## 拉取请求流程

1. **创建拉取请求**：在 GitHub 上创建新的拉取请求
2. **填写模板**：完整填写拉取请求模板
3. **关联问题**：如果修复了某个问题，请关联该问题
4. **等待审查**：等待项目维护者进行代码审查
5. **处理反馈**：根据审查意见进行修改
6. **合并**：审查通过后，代码将被合并到主分支

### 拉取请求模板

```markdown
## 描述
简要描述这个变更的目的

## 类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 代码重构
- [ ] 文档更新

## 检查清单
- [ ] 我的代码遵循项目的编码规范
- [ ] 我添加了相应的测试
- [ ] 我更新了相关文档
- [ ] 我通过了所有测试
- [ ] 我通过了代码质量检查

## 相关问题
修复 #123
```

## 发布流程

新版本的发布遵循以下流程：

1. **更新版本号**：在 `src/pycodemao/_version.py` 中更新版本号
2. **更新变更日志**：在 `CHANGELOG.md` 中添加新版本记录
3. **创建发布标签**：创建新的 Git 标签
4. **构建发布包**：构建并上传到 PyPI
5. **创建 GitHub 发布**：在 GitHub 上创建新的发布

## 社区参与

### Discord 社区

加入我们的 Discord 社区：
- 获取帮助和支持
- 参与功能讨论
- 了解最新动态
- 结识其他贡献者

### 邮件列表

订阅我们的邮件列表以获取更新通知。

## 奖励和认可

### 贡献者列表

所有贡献者都会被添加到项目的贡献者列表中。

### 特别贡献

对于特别重要的贡献，我们可能会：
- 在发布说明中特别提及
- 邀请加入核心团队
- 提供项目相关的奖励

## 联系信息

如果您有任何问题或建议，请通过以下方式联系我们：

- **GitHub Issues**: [创建新问题](https://github.com/pycodemao/pycodemao/issues/new)
- **Discord**: [加入社区](https://discord.gg/pycodemao)
- **邮件**: contact@pycodemao.org

## 许可证

通过贡献代码，您同意您的贡献将在项目的 MIT 许可证下发布。

## 致谢

感谢所有为 PyCodeMao 项目做出贡献的开发者和用户！

---

**Happy coding! 🚀**