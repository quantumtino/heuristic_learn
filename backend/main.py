#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主应用入口文件
"""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow import WorkflowManager
from knowledge_base.document_processor import DocumentProcessor

# 加载环境变量
load_dotenv()

# 初始化FastAPI应用
app = FastAPI(title="中学生知识辅助学习系统", version="1.0.0")

# 添加CORS中间件，允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
workflow_manager = WorkflowManager()
document_processor = DocumentProcessor()

# 数据模型
class LearningRequest(BaseModel):
    topic: str

# API路由
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回简单的欢迎页面"""
    return """
    <html>
        <head>
            <title>中学生知识辅助学习系统</title>
        </head>
        <body>
            <h1>中学生知识辅助学习系统</h1>
            <p>系统正在运行中...</p>
            <p>请通过前端界面或API接口访问系统功能。</p>
        </body>
    </html>
    """

@app.post("/learn")
async def learn_topic(request: LearningRequest):
    """处理学习请求"""
    try:
        result = workflow_manager.process_request(request.topic)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    """上传知识库文件"""
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 处理文档
        processed_content = document_processor.process_document(file_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "content": processed_content[:500] + "..." if len(processed_content) > 500 else processed_content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

def main():
    """主函数"""
    print("中学生知识辅助学习系统")
    print("正在启动...")
    
    # 启动Web服务
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
