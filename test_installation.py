#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
依赖安装测试脚本
验证项目所需的依赖包是否正确安装
"""

def test_imports():
    """测试导入依赖包"""
    packages = {
        "fastapi": "FastAPI Web框架",
        "uvicorn": "ASGI服务器",
        "dotenv": "环境变量加载",
        "langchain": "LangChain框架",
        "dashscope": "阿里云DashScope API",
        "pypdf": "PDF处理",
        "docx": "DOCX处理",
        "faiss": "向量数据库",
        "pydantic": "数据验证",
        "requests": "HTTP请求"
    }
    
    failed_imports = []
    
    print("=== 依赖包导入测试 ===\n")
    
    # 测试每个包的导入
    for package, description in packages.items():
        try:
            if package == "dotenv":
                from dotenv import load_dotenv
            elif package == "docx":
                from docx import Document
            elif package == "faiss":
                import faiss
            else:
                __import__(package)
            print(f"✓ {package} - {description}")
        except ImportError as e:
            print(f"✗ {package} - {description} (导入失败: {e})")
            failed_imports.append(package)
    
    # 测试结果
    print(f"\n=== 测试结果 ===")
    if failed_imports:
        print(f"以下包导入失败:")
        for pkg in failed_imports:
            print(f"  - {pkg}")
        print("\n请检查依赖安装或Python环境配置。")
        return False
    else:
        print("所有依赖包导入成功！")
        return True

def test_basic_functionality():
    """测试基本功能"""
    print("\n=== 基本功能测试 ===")
    
    try:
        # 测试FastAPI
        from fastapi import FastAPI
        app = FastAPI()
        print("✓ FastAPI 初始化成功")
        
        # 测试Pydantic
        from pydantic import BaseModel
        class TestModel(BaseModel):
            name: str
            value: int
        
        test_model = TestModel(name="test", value=42)
        assert test_model.name == "test"
        assert test_model.value == 42
        print("✓ Pydantic 数据模型工作正常")
        
        # 测试环境变量加载
        from dotenv import load_dotenv
        load_dotenv()
        print("✓ 环境变量加载功能正常")
        
        print("基本功能测试通过！")
        return True
        
    except Exception as e:
        print(f"基本功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 中学生知识辅助学习系统依赖测试 ===\n")
    
    # 测试导入
    import_success = test_imports()
    
    # 测试基本功能
    if import_success:
        functionality_success = test_basic_functionality()
        
        if functionality_success:
            print("\n🎉 所有测试通过！您的环境已正确配置。")
        else:
            print("\n⚠ 导入成功但功能测试失败，请检查配置。")
    else:
        print("\n❌ 依赖包导入失败，请重新安装依赖。")

if __name__ == "__main__":
    main()
