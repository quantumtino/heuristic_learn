# 中学生启发式知识辅助学习系统

## 📖 项目简介

这是一个基于大语言模型的**智能教学工作流系统**，专为中学生设计，通过**三阶段智能处理流程**和**严格的知识审查机制**，确保生成高质量、事实准确的启发式学习内容。系统采用多Agent协作架构，将提示词优化、内容生成和知识审查有机结合，为学生提供安全、可靠、易于理解的学习辅助。

---

## 🌟 工作流特点与创新点

### 1. **三阶段智能工作流**（核心创新）

系统采用创新的三阶段处理流程，每个阶段由专门的AI Agent负责：

```
用户输入 → 提示词优化 → 内容生成 → 知识审查 → 最终输出
```

#### 阶段一：提示词优化（Prompt Optimizer Agent）
- **模型**: qwen-flash（快速响应）
- **功能**: 将用户的简单问题转化为结构化、明确的教学提示词
- **创新点**: 
  - 自动识别学科领域和知识点
  - 针对中学生认知水平优化表达方式
  - 补充必要的背景信息和学习目标

#### 阶段二：启发式内容生成（Content Generator Agent）
- **模型**: qwen-plus-character/qwen3-max（高质量生成）
- **功能**: 生成启发式对话内容，引导学生主动思考
- **创新点**:
  - 采用苏格拉底式问答法，而非直接给出答案
  - 使用生活化类比和实例，降低理解难度
  - 分步骤引导，培养学生的逻辑思维能力
  - 适应中学生的语言习惯和理解水平

#### 阶段三：知识审查（Knowledge Reviewer Agent）⭐（关键创新）
- **模型**: qwen-flash（高效审查）
- **功能**: 对生成内容进行严格的事实性审查
- **创新点**:
  - **多维度审查标准**：事实准确性、时效性、科学性
  - **二元判定机制**：明确的PASS/FAIL结果
  - **详细反馈机制**：指出具体错误并提供改进建议
  - **安全阀机制**：只有通过审查的内容才会呈现给学生

### 2. **知识审查机制的重要性** ⭐⭐⭐（突出重点）

**为什么审查环节至关重要？**

#### 🛡️ 保障内容准确性
大语言模型虽然强大，但可能产生"幻觉"（hallucination），即生成看似合理但实际错误的内容。知识审查Agent作为**最后一道防线**，确保：
- ✅ 所有事实信息经过验证
- ✅ 避免传播错误知识
- ✅ 保护学生免受误导

#### 📚 适配教育场景
教育内容的准确性要求远高于一般应用：
- 错误的知识可能影响学生的学习基础
- 中学阶段是建立知识体系的关键时期
- 不准确的信息可能导致考试失分

#### 🔍 审查机制的工作原理

```python
# 审查标准（来自 knowledge_reviewer_agent.py）
1. 内容中的事实信息必须准确无误
2. 不得包含过时或已被证实错误的信息
3. 数据、日期、人物、事件等必须核实准确
```

**审查流程**：
1. 接收生成的教学内容
2. 使用专业的审查提示词调用模型
3. 从事实准确性、时效性等多个维度评估
4. 返回明确的 PASS/FAIL 判定
5. 提供详细的反馈信息

**示例**：
```
❌ 未通过审查：
"光速约为 30万公里/秒" → FAIL
反馈：光速的准确值是 299,792,458 米/秒，约为 3×10⁸ 米/秒

✅ 通过审查：
"光在真空中的传播速度约为 3×10⁸ 米/秒" → PASS
反馈：内容事实准确，可以发布
```

### 3. **反馈重试机制**（增强创新）
- 当内容未通过审查时，系统会将审查反馈作为上下文提供给内容生成器
- 最多允许3次重试，提高内容质量
- 确保最终输出内容既符合教育要求又准确无误

### 4. **多模型协同架构**
系统采用**分工明确的多模型策略**：
- **qwen-flash**: 用于快速任务（优化、审查）
- **qwen-plus-character/qwen3-max**: 用于高质量内容生成
- 各模型发挥所长，平衡质量与效率

### 5. **可扩展的架构设计**
- **知识库接口**: 预留RAG（检索增强生成）接口，支持上传PDF/DOCX文档
- **MCP服务器**: 预留科学计算和外部工具调用接口
- **思维导图生成**: 将知识点可视化，帮助学生建立知识网络
- **模块化设计**: 易于添加新的Agent或功能模块

---

## 💡 使用方法

### 环境要求
- Python 3.8+
- 阿里云DashScope API密钥

### 方法一：使用Conda（推荐）

```bash
# 1. 克隆项目
git clone <repository-url>
cd heuristic_learn

# 2. 创建并激活Conda环境
conda env create -f environment.yml
conda activate heuristic-learn

# 3. 配置API密钥
# 复制 .env.example 为 .env，并填写您的 DASHSCOPE_API_KEY
cp .env.example .env
# 编辑 .env 文件

# 4. 运行系统
# 方式A：控制台应用（命令行交互）
cd backend
python console_app.py

# 方式B：Web服务
cd backend
python main.py
# 然后在浏览器中打开 frontend/index.html
# 访问地址：http://localhost:8000
```

### 方法二：使用pip

```bash
# 1. 克隆项目
git clone <repository-url>
cd heuristic_learn

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安装依赖
# 方式A：直接安装
pip install -r requirements.txt

# 方式B：使用安装脚本（自动处理依赖问题）
python install_dependencies.py

# 5. 测试安装
python test_installation.py

# 6. 配置API密钥（同上）

# 7. 运行系统（同上）
```

### 配置说明

在 `.env` 文件中配置以下参数：

```bash
# 必需配置
DASHSCOPE_API_KEY=your_api_key_here

# 可选配置（使用默认值即可）
OPTIMIZER_MODEL=qwen-flash        # 提示词优化模型
GENERATOR_MODEL=qwen-plus-character  # 内容生成模型
REVIEWER_MODEL=qwen-flash         # 知识审查模型
```

**获取API密钥**：
1. 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 创建API密钥
4. 复制密钥到 `.env` 文件

### 运行模式

#### 控制台模式

```bash
cd backend
python console_app.py
```

**交互示例**：
```
请输入您的问题（输入 'quit' 退出）: 为什么天空是蓝色的？

正在优化提示词...
正在进行第 1 次生成和审查...
正在生成对话内容...
正在审查内容...
内容审查通过（第 1 次尝试），处理完成

=== 处理结果 ===
原始输入: 为什么天空是蓝色的？

优化后的提示词:
请为中学生解释"天空为什么是蓝色"这一物理现象，要求：
1. 使用启发式教学方法，通过提问引导学生思考
2. 涉及光的散射原理（瑞利散射）
3. 使用生活化的类比帮助理解
4. 适合初中物理水平

生成的对话内容:
[启发式对话内容...]

审查结果: ✅ 通过
审查反馈: 内容事实准确，可以发布。
重试次数: 0次
```

#### Web服务模式

```bash
cd backend
python main.py
```

然后在浏览器中打开 `frontend/index.html`，通过图形界面与系统交互。

#### 批量对比测试

```bash
# 运行批量对比测试（需要API密钥）
python run_full_test.py

# 选择选项2运行批量对比测试
# 或直接运行
python batch_tests/batch_test_comparison.py
```

---

## 🔬 工作流详解

### WorkflowManager 核心逻辑

```python
def process_request(self, user_input: str) -> Dict[str, Any]:
    """完整的三阶段处理流程（支持审查失败后反馈重试）"""
    
    # 阶段1: 提示词优化（只需要一次）
    optimized_prompt = self.prompt_optimizer.process(user_input)
    
    # 阶段2 & 3: 内容生成与知识审查，最多循环3次
    max_retries = 3
    current_attempt = 0
    review_passed = False
    
    while current_attempt <= max_retries and not review_passed:
        current_attempt += 1
        
        if current_attempt == 1:
            # 第一次尝试，直接使用优化后的提示词
            dialog_content = self.content_generator.process(optimized_prompt)
        else:
            # 重试时，将审查反馈作为上下文提供给内容生成器
            feedback_enhanced_prompt = f"""原始要求：{optimized_prompt}

之前的生成内容：
{dialog_content}

审查反馈：
{review_feedback}

请根据审查反馈改进内容，确保事实准确、符合要求。"""
            dialog_content = self.content_generator.process(feedback_enhanced_prompt)
        
        # 阶段3: 知识审查
        review_passed, review_feedback = self.knowledge_reviewer.process(dialog_content)
        
        if review_passed:
            # 通过审查，返回内容
            return dialog_content
        else:
            # 未通过审查，准备重试（除非已达到最大重试次数）
            if current_attempt < max_retries:
                print(f"审查未通过，将反馈提供给内容生成器，准备第 {current_attempt + 1} 次尝试...")
            else:
                print("已达到最大重试次数，无法提供内容")
    
    # 所有尝试都失败
    return None
```

### 审查机制的保障作用

```
┌─────────────────┐
│   用户输入      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 提示词优化Agent │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 内容生成Agent   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 知识审查Agent ⭐│  ← 最后一道防线
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   PASS    FAIL &
    │    Feedback
    ▼         │
 输出内容  ←────┘
         最多3次重试
```

---

## 📊 效果评估与对比测试

### 批量对比测试结果

我们使用qwen-flash模拟中学生视角，对**三阶段工作流**与**直接使用qwen-max**进行了对比测试。测试从易理解性、启发性、趣味性、完整性、实用性五个维度评分（每项0-10分）。**重要的是，总分由程序直接计算各分项分数之和（满分50分），避免了模型在数学计算方面可能存在的问题。**

#### 测试方法
1. 使用qwen-flash生成5个典型中学生问题
2. 分别用两种方法生成回答
3. 从中学生视角对回答质量进行多维度评分
4. 统计分析两种方法的差异

#### 测试结果摘要

| 方法 | 平均分 | 最高分 | 最低分 | 成功率 |
|------|--------|--------|--------|--------|
| **三阶段工作流** | **47.4/50** | 50 | 44 | 100% |
| 直接qwen-max | 41.4/50 | 43 | 39 | 100% |
| **优势** | **+6.0分** | **+7分** | **+5分** | - |

#### 各维度对比

| 评分维度 | 三阶段工作流 | 直接qwen-max | 差异 | 提升比例 |
|----------|--------------|--------------|------|----------|
| **启发性** ⭐ | **10/10** | 7.6/10 | **+2.4** | **+31.6%** |
| 易理解性 | 9.6/10 | 8.6/10 | +1.0 | +11.6% |
| 趣味性 | 9.2/10 | 6.8/10 | +2.4 | +35.3% |
| 完整性 | 9.2/10 | 9.2/10 | 0 | 0% |
| 实用性 | 9.2/10 | 8.8/10 | +0.4 | +4.5% |

#### 关键发现

1. **启发性显著提升** ⭐：三阶段工作流在启发性维度得分10/10，比直接使用qwen-max高出2.4分（+31.6%），这正是启发式教学的核心价值所在。

2. **整体质量更优**：三阶段工作流平均分47.4/50，比直接使用qwen-max高出6.0分（+14.5%），证明了三阶段处理流程的有效性。

3. **审查机制保障**：所有通过三阶段工作流生成的内容都经过了知识审查Agent的验证，确保了事实准确性。

4. **适合中学生**：在易理解性、趣味性和启发性方面均有显著提升，更符合中学生的认知特点和学习需求。

#### 测试问题示例
- 为什么天空是蓝色的？
- 光合作用是怎么进行的？
- 勾股定理是什么？
- 电流是怎么产生的？
- 细胞是怎么分裂的？

#### 运行批量测试

```bash
# 运行批量对比测试（需要API密钥）
python batch_tests/batch_test_comparison.py

# 测试将生成详细的JSON报告文件
# 文件名格式：test_report_YYYYMMDD_HHMMSS.json
```

**注意**：批量测试会调用多次API，请确保有足够的API配额。测试完成后会在当前目录生成详细的JSON格式测试报告。

---

## 📁 项目结构

```
heuristic_learn/
├── backend/                    # 后端核心代码
│   ├── __init__.py
│   ├── main.py                # FastAPI Web服务入口
│   ├── console_app.py         # 控制台应用入口
│   ├── workflow.py            # 工作流管理器 ⭐
│   │
│   ├── agents/                # AI Agent模块
│   │   ├── __init__.py
│   │   ├── base_agent.py              # Agent基类
│   │   ├── prompt_optimizer_agent.py  # 提示词优化Agent
│   │   ├── content_generator_agent.py # 内容生成Agent
│   │   └── knowledge_reviewer_agent.py # 知识审查Agent ⭐
│   │
│   ├── config/                # 配置模块
│   │   ├── __init__.py
│   │   └── settings.py        # 系统配置
│   │
│   ├── knowledge_base/        # 知识库模块（预留RAG接口）
│   │   ├── __init__.py
│   │   └── document_processor.py
│   │
│   └── utils/                 # 工具模块
│       ├── __init__.py
│       └── mind_map_generator.py  # 思维导图生成器
│
├── frontend/                  # 前端界面
│   └── index.html            # Web界面
│
├── batch_tests/              # 批量测试代码与结果
│   ├── batch_test_comparison.py      # 批量对比测试脚本
│   ├── visualize_results.py          # 结果可视化脚本
│   └── test_results_YYYYMMDD/        # 测试结果目录（不上传git）
│       ├── *.png                     # 可视化图表
│       └── *.json                    # 测试报告数据
│
├── debug_tests/              # 调试测试代码（不上传git）
│   └── *.py
│
├── mcp_servers/              # MCP服务器（预留扩展接口）
│   ├── __init__.py
│   └── README.md
│
├── .env.example              # 环境变量模板
├── .env                      # 环境变量配置（需自行创建）
├── .gitignore
├── environment.yml           # Conda环境配置
├── requirements.txt          # pip依赖列表
├── install_dependencies.py   # 依赖安装脚本
├── run_full_test.py         # 完整测试套件
└── README.md                # 本文件
```

---

## 🎯 应用场景

1. **日常学习辅导**: 学生遇到不理解的知识点时，获得启发式引导
2. **作业答疑**: 不直接给出答案，而是引导学生思考解题思路
3. **知识预习**: 在学习新知识前，通过对话建立初步认知
4. **概念理解**: 对抽象概念进行具象化解释和类比
5. **知识复习**: 通过问答形式巩固已学知识

---

## 🛠️ 开发与测试

### 运行测试

```bash
# 测试核心功能
python test_core_functions.py

# 测试工作流
python backend/test_workflow.py

# 测试控制台应用
python test_console_app.py

# 运行完整测试
python run_full_test.py

# 批量对比测试
python batch_tests/batch_test_comparison.py
```

### 可视化测试结果

```bash
# 生成测试结果的可视化图表
python batch_tests/visualize_results.py

# 该脚本会生成以下图表文件：
# - overall_comparison.png: 整体性能对比图
# - detailed_comparison.png: 详细维度对比图
# - total_scores_comparison.png: 总分对比图
# - dimension_averages_comparison.png: 各维度平均分对比图
```

### 开发计划

- [x] 实现基础框架
- [x] 开发提示词优化Agent
- [x] 开发内容生成Agent
- [x] 开发知识审查Agent ⭐
- [x] 实现三阶段工作流
- [x] 构建控制台应用
- [x] 构建Web界面
- [x] 实现思维导图生成功能
- [x] 实现审查失败后反馈重试机制（最多3次）
- [x] 添加测试结果可视化功能
- [ ] 集成RAG知识库检索
- [ ] 添加MCP科学计算工具
- [ ] 实现多轮对话记忆
- [ ] 添加学习进度跟踪

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 贡献方向
- 改进审查机制的准确性
- 优化提示词模板
- 添加新的学科领域支持
- 改进前端交互体验
- 完善文档和示例

---

## 📄 许可证

MIT License

---

## 📮 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- Pull Request
- Email:quantum-liu@outlook.com

---

## 🙏 致谢

- 阿里云提供的大语言模型api服务
- 北京大学《物理与人工智能》2025秋授课老师与助教的悉心教导

---

**注意**: 本系统的核心价值在于通过**严格的知识审查机制**确保内容质量，这是区别于普通AI对话系统的关键创新点。审查环节不仅保障了内容的准确性，更体现了对教育质量的负责态度。
