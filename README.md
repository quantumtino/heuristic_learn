# 中学生知识辅助学习系统

这是一个基于大模型的工作流系统，旨在帮助中学生更好地理解和掌握知识。系统通过优化提示词、生成启发性对话内容，并结合知识审查机制来确保内容的准确性和适龄性。

## 功能特点

- **个性化知识库**: 支持PDF和DOCX格式文件上传
- **智能提示词优化**: 使用qwen-flash模型优化输入提示词
- **启发性内容生成**: 利用qwen-plus-character/qwen3-max模型生成易于理解的对话式内容
- **知识审查机制**: 通过qwen-flash模型对生成内容进行事实性审查
- **思维导图生成**: 将知识点以可视化方式呈现
- **MCP接口预留**: 为未来科学计算功能扩展预留接口

## 技术架构

### 后端
- Python 3.8+
- FastAPI (Web框架)
- DashScope (阿里云模型服务)
- LangChain (提示词管理)
- FAISS (向量数据库 - 预留RAG接口)

### 前端
- React.js (可选)
- 或者简单的HTML/CSS/JavaScript

## 快速开始

### 使用Conda环境（推荐）
1. 克隆项目
2. 创建Conda环境: `conda env create -f environment.yml`
3. 激活环境: `conda activate heuristic-learn`
4. 配置环境变量: 编辑`.env`文件并填写您的DashScope API密钥
5. 运行控制台应用: `cd backend && python console_app.py`
   - 或者运行Web服务: `cd backend && python main.py`，然后在浏览器中打开`frontend/index.html`，访问地址为 `http://localhost:8000`

### 使用pip安装依赖
1. 克隆项目
2. 创建虚拟环境: `python -m venv venv`
3. 激活虚拟环境: 
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. 安装依赖:
   - 方法一：`pip install -r requirements.txt`
   - 方法二：运行安装脚本：`python install_dependencies.py`
   - 注意：如果遇到dashscope安装问题，请单独安装：`pip install dashscope`
5. 测试依赖安装: `python test_installation.py`
6. 配置环境变量: 编辑`.env`文件并填写您的DashScope API密钥
7. 运行控制台应用: `cd backend && python console_app.py`
   - 或者运行Web服务: `cd backend && python main.py`，然后在浏览器中打开`frontend/index.html`，访问地址为 `http://localhost:8000`

## 配置说明

在 `.env` 文件中配置以下参数:

- `DASHSCOPE_API_KEY`: 您的阿里云DashScope API密钥
- `OPTIMIZER_MODEL`: 提示词优化使用的模型 (默认: qwen-flash)
- `GENERATOR_MODEL`: 内容生成使用的模型 (默认: qwen-plus-character)
- `REVIEWER_MODEL`: 内容审查使用的模型 (默认: qwen-flash)

## 目录结构

```
project/
├── backend/             # 后端代码
│   ├── __init__.py      # 包初始化文件
│   ├── main.py          # 应用入口
│   ├── workflow.py      # 工作流管理器
│   ├── config/          # 配置文件
│   │   ├── __init__.py
│   │   └── settings.py  # 系统配置设置
│   ├── agents/          # 各种AI代理实现
│   │   ├── __init__.py
│   │   ├── base_agent.py           # 基础Agent类
│   │   ├── prompt_optimizer_agent.py  # 提示词优化Agent
│   │   ├── content_generator_agent.py # 内容生成Agent
│   │   └── knowledge_reviewer_agent.py # 知识审查Agent
│   ├── knowledge_base/  # 知识库处理模块
│   │   ├── __init__.py
│   │   └── document_processor.py   # 文档处理器
│   └── utils/           # 工具函数
│       ├── __init__.py
│       └── mind_map_generator.py   # 思维导图生成器
├── frontend/            # 前端代码
│   └── index.html       # 前端页面
├── mcp_servers/         # MCP服务器实现
│   ├── __init__.py
│   └── README.md        # MCP服务器说明
├── .env                 # 环境变量配置
├── .gitignore           # Git忽略文件
├── requirements.txt     # Python依赖
└── README.md            # 项目说明
```

## 开发计划

- [x] 实现基础框架
- [x] 开发提示词优化Agent
- [x] 开发内容生成Agent
- [x] 开发知识审查Agent
- [x] 实现思维导图生成功能
- [x] 构建前端界面
- [ ] 集成测试

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License
