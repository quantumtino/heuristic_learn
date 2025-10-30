#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
核心功能测试脚本
验证系统的核心功能是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_components():
    """测试所有核心组件"""
    tests = [
        ("配置管理", "backend.config.settings", "settings"),
        ("基础Agent", "backend.agents.base_agent", "BaseAgent"),
        ("提示词优化Agent", "backend.agents.prompt_optimizer_agent", "PromptOptimizerAgent"),
        ("内容生成Agent", "backend.agents.content_generator_agent", "ContentGeneratorAgent"),
        ("知识审查Agent", "backend.agents.knowledge_reviewer_agent", "KnowledgeReviewerAgent"),
        ("工作流管理器", "backend.workflow", "WorkflowManager"),
        ("控制台应用", "backend.console_app", "main")
    ]
    
    failed_tests = []
    
    print("=== 核心功能测试 ===\n")
    
    for test_name, module_name, component_name in tests:
        try:
            # 导入模块
            module = __import__(module_name, fromlist=[component_name])
            
            # 检查组件是否存在
            if hasattr(module, component_name):
                print(f"✓ {test_name} - {component_name}")
            else:
                print(f"✗ {test_name} - {component_name} (组件不存在)")
                failed_tests.append(f"{test_name} - {component_name}")
                
        except ImportError as e:
            print(f"✗ {test_name} - {component_name} (导入失败: {e})")
            failed_tests.append(f"{test_name} - {component_name}")
        except Exception as e:
            print(f"✗ {test_name} - {component_name} (错误: {e})")
            failed_tests.append(f"{test_name} - {component_name}")
    
    # 测试结果
    print(f"\n=== 测试结果 ===")
    if failed_tests:
        print(f"以下测试失败:")
        for test in failed_tests:
            print(f"  - {test}")
        print("\n请检查系统配置或依赖安装。")
        return False
    else:
        print("🎉 所有核心功能测试通过！")
        return True

def main():
    """主函数"""
    print("=== 中学生知识辅助学习系统核心功能测试 ===\n")
    
    success = test_all_components()
    
    if success:
        print("\n系统核心功能正常，可以开始使用。")
        print("\n运行以下命令启动控制台应用:")
        print("  cd backend && python console_app.py")
    else:
        print("\n系统存在错误，请检查并修复后再使用。")

if __name__ == "__main__":
    main()
