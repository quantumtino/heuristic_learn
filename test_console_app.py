#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
控制台应用测试脚本
验证简化后的系统功能是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入依赖包"""
    packages = {
        "backend.workflow": "工作流管理器",
        "backend.agents.prompt_optimizer_agent": "提示词优化Agent",
        "backend.agents.content_generator_agent": "内容生成Agent",
        "backend.agents.knowledge_reviewer_agent": "知识审查Agent"
    }
    
    failed_imports = []
    
    print("=== 依赖包导入测试 ===\n")
    
    # 测试每个包的导入
    for package, description in packages.items():
        try:
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

def test_workflow():
    """测试工作流"""
    print("\n=== 测试工作流 ===")
    
    try:
        from backend.workflow import WorkflowManager
        
        # 创建工作流管理器
        workflow_manager = WorkflowManager()
        print("✓ 工作流管理器初始化成功")
        
        # 测试处理请求
        test_input = "请解释牛顿第一定律"
        result = workflow_manager.process_request(test_input)
        
        print("✓ 请求处理成功")
        print(f"  - 原始输入: {result.get('original_input', '')}")
        print(f"  - 优化提示词: {result.get('optimized_prompt', '')[:50]}...")
        print(f"  - 对话内容: {result.get('dialog_content', '')[:50]}...")
        print(f"  - 审查结果: {'通过' if result.get('review_passed') else '未通过'}")
        
        return True
        
    except Exception as e:
        print(f"✗ 工作流测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 中学生知识辅助学习系统控制台版测试 ===\n")
    
    # 测试导入
    import_success = test_imports()
    
    # 测试工作流
    if import_success:
        workflow_success = test_workflow()
        
        # 最终结果
        print("\n=== 测试结果 ===")
        if import_success and workflow_success:
            print("🎉 所有测试通过！系统工作正常。")
            print("\n您可以运行以下命令来启动控制台应用:")
            print("  cd backend && python console_app.py")
        else:
            print("⚠ 部分测试失败，请检查系统配置。")
    else:
        print("\n❌ 依赖包导入失败，请重新安装依赖。")

if __name__ == "__main__":
    main()
