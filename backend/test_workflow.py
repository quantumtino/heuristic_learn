#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工作流测试脚本
用于测试整个工作流是否正常运行
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow import WorkflowManager


def test_workflow():
    """测试工作流"""
    print("=== 中学生知识辅助学习系统测试 ===\n")
    
    # 创建工作流管理器
    workflow_manager = WorkflowManager()
    
    # 测试用例
    test_cases = [
        "请解释牛顿第一定律",
        "什么是光合作用？",
        "请介绍中国古代四大发明"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_input}")
        print("-" * 50)
        
        # 处理请求
        result = workflow_manager.process_request(test_input)
        
        # 输出结果
        print(f"原始输入: {result['original_input']}")
        print(f"优化后的提示词: {result['optimized_prompt']}")
        print(f"对话内容: {result['dialog_content'][:100]}..." if len(result['dialog_content']) > 100 else f"对话内容: {result['dialog_content']}")
        print(f"思维导图: {result['mind_map'][:100]}..." if len(result['mind_map']) > 100 else f"思维导图: {result['mind_map']}")
        print(f"审查结果: {'通过' if result['review_passed'] else '未通过'}")
        if result['review_feedback']:
            print(f"审查反馈: {result['review_feedback']}")
        
        print("\n" + "="*50 + "\n")
    
    print("测试完成！")


if __name__ == "__main__":
    test_workflow()
