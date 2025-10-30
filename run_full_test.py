#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整系统测试脚本
验证整个系统的工作流是否正常运行
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_backend():
    """测试后端服务"""
    print("=== 测试后端服务 ===")
    
    try:
        import requests
        
        # 测试健康检查接口
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("✓ 后端服务健康检查通过")
            return True
        else:
            print("✗ 后端服务健康检查失败")
            return False
            
    except Exception as e:
        print(f"✗ 后端服务测试失败: {e}")
        return False

def test_workflow():
    """测试工作流"""
    print("\n=== 测试工作流 ===")
    
    try:
        import requests
        import json
        
        # 测试学习请求
        test_data = {
            "topic": "请解释牛顿第一定律"
        }
        
        response = requests.post(
            "http://localhost:8000/learn",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data),
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✓ 学习请求处理成功")
                data = result.get("data", {})
                print(f"  - 原始输入: {data.get('original_input', '')}")
                print(f"  - 优化提示词: {data.get('optimized_prompt', '')[:50]}...")
                print(f"  - 对话内容: {data.get('dialog_content', '')[:50]}...")
                print(f"  - 审查结果: {'通过' if data.get('review_passed') else '未通过'}")
                return True
            else:
                print(f"✗ 学习请求处理失败: {result.get('error')}")
                return False
        else:
            print(f"✗ 学习请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ 工作流测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 中学生知识辅助学习系统完整测试 ===\n")
    
    # 测试后端服务
    backend_success = test_backend()
    
    if not backend_success:
        print("\n❌ 后端服务测试失败，无法继续测试工作流")
        return
    
    # 测试工作流
    workflow_success = test_workflow()
    
    # 最终结果
    print("\n=== 测试结果 ===")
    if backend_success and workflow_success:
        print("🎉 所有测试通过！系统工作正常。")
    else:
        print("⚠ 部分测试失败，请检查系统配置。")

if __name__ == "__main__":
    main()
