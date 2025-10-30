#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试审查逻辑
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.workflow import WorkflowManager

def test_review_logic():
    """测试审查逻辑"""
    print("正在测试审查逻辑...")
    
    wm = WorkflowManager()
    result = wm.process_request('为什么天空是蓝色的')
    
    print('审查结果:', result.get('review_passed'))
    print('审查反馈:', result.get('review_feedback'))
    print('重试次数:', result.get('retry_count', 0))
    
    if result.get('final_content'):
        print('\n最终内容预览:')
        print(result['final_content'][:200] + '...' if len(result['final_content']) > 200 else result['final_content'])

if __name__ == "__main__":
    test_review_logic()
