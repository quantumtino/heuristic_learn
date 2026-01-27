#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
知识审查Agent
负责审查生成内容的事实准确性
"""

from typing import Any, Dict, Tuple
from backend.agents.base_agent import BaseAgent
from backend.config.settings import settings
from backend.prompts import (
    REVIEWER_SYSTEM,
    REVIEWER_USER_TEMPLATE,
)


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
        system_prompt = REVIEWER_SYSTEM
        user_prompt = REVIEWER_USER_TEMPLATE.format(input_data=input_data)
        
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
