#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
知识审查Agent
负责审查生成内容的事实准确性
"""

from typing import Any, Dict, Tuple
from backend.agents.base_agent import BaseAgent
from backend.config.settings import settings


class KnowledgeReviewerAgent(BaseAgent):
    """知识审查Agent"""
    
    def __init__(self):
        """初始化知识审查Agent"""
        super().__init__(model_name=settings.reviewer_model)
    
    def process(self, input_data: str) -> Tuple[bool, str]:
        """
        审查生成内容的事实准确性
        
        Args:
            input_data (str): 待审查的内容
            
        Returns:
            Tuple[bool, str]: 审查结果（通过/不通过）和反馈信息
        """
        # 构建系统提示词
        system_prompt = """你是一位严谨的学科专家，负责审查教学内容的事实准确性。
        你的任务是对给定的教学内容进行事实性审查，判断是否存在错误或不准确的信息。
        
        审查标准：
        1. 内容中的事实信息必须准确无误
        2. 不得包含过时或已被证实错误的信息
        3. 数据、日期、人物、事件等必须核实准确
        4. 解释和概念必须科学正确
        5. 推理过程必须逻辑严密
        
        重要：默认情况下内容可以通过审查，只有在发现严重事实错误时才拒绝通过
        
        请严格按照以下格式返回审查结果：
        [PASS|FAIL]
        [反馈信息]
        
        如果内容没有严重事实错误，请回复：
        PASS
        内容通过审查，可以发布。
        
        如果内容存在严重事实错误，请回复：
        FAIL
        问题：[具体的问题描述]
        错误：[具体的错误内容]
        建议：[改进建议]
        """
        
        # 构建用户提示词
        user_prompt = f"请审查以下教学内容的事实准确性：\n\n{input_data}"
        
        # 调用模型进行审查
        response = self._call_model(
            prompt=user_prompt,
            system_prompt=system_prompt
        )
        
        # 解析审查结果
        lines = response.strip().split("\n", 1)
        if len(lines) >= 1:
            result = lines[0].strip().upper()
            feedback = lines[1].strip() if len(lines) > 1 else ""
            
            if result == "PASS":
                return True, feedback
            else:
                return False, feedback
        else:
            # 默认返回失败，以防解析错误
            return False, "无法解析审查结果"
