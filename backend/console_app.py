#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
控制台应用入口
用于在终端中直接运行和测试系统功能
"""

import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.workflow import WorkflowManager

def main():
    """主函数"""
    print("=== 中学生知识辅助学习系统 (控制台版) ===\n")
    
    # 初始化工作流管理器
    workflow_manager = WorkflowManager()
    
    # 获取用户输入
    print("请输入您想学习的知识点:")
    user_input = input("> ")
    
    if not user_input.strip():
        print("输入不能为空!")
        return
    
    print(f"\n正在处理您的请求: {user_input}")
    print("=" * 50)
    
    # 处理请求
    start_time = time.time()
    result = workflow_manager.process_request(user_input)
    end_time = time.time()
    
    # 输出结果
    print("\n" + "=" * 50)
    print("处理结果:")
    print("=" * 50)
    
    print(f"\n原始输入: {result.get('original_input', '')}")
    
    print(f"\n优化后的提示词:")
    print("-" * 30)
    print(result.get('optimized_prompt', ''))
    
    print(f"\n生成的对话内容:")
    print("-" * 30)
    print(result.get('dialog_content', ''))
    
    print(f"\n知识审查结果:")
    print("-" * 30)
    review_passed = result.get('review_passed', False)
    print(f"审查状态: {'通过' if review_passed else '未通过'}")
    print(f"审查反馈: {result.get('review_feedback', '')}")
    
    if review_passed:
        print(f"\n最终内容:")
        print("-" * 30)
        print(result.get('final_content', ''))
    else:
        print("\n内容未通过审查，建议重新生成或修改输入。")
    
    print(f"\n处理耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()
