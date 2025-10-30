#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
提示词优化Agent
负责优化用户输入的提示词，使其更适合生成启发性内容
"""

from typing import Any, Dict
from backend.agents.base_agent import BaseAgent
from backend.config.settings import settings


class PromptOptimizerAgent(BaseAgent):
    """提示词优化Agent"""
    
    def __init__(self):
        """初始化提示词优化Agent"""
        super().__init__(model_name=settings.optimizer_model)
    
    def process(self, input_data: str) -> str:
        """
        优化提示词
        
        Args:
            input_data (str): 原始提示词
            
        Returns:
            str: 优化后的提示词
        """
        # 构建系统提示词
        system_prompt = """你是一个专业的提示词优化专家。你的任务是将用户输入的提示词优化得更加清晰、具体，
        适合用于生成面向中学生的启发性教学内容。请确保优化后的提示词能够引导模型产生：
        1. 易于理解的表达方式
        2. 对话式的交互形式
        3. 启发性的思考角度
        4. 准确的知识点覆盖
        
        请直接返回优化后的提示词，不要添加任何解释或其他内容。
        """
        
        # 构建用户提示词
        user_prompt = f"请优化以下提示词：{input_data}"
        
        # 调用模型进行优化
        optimized_prompt = self._call_model(
            prompt=user_prompt,
            system_prompt=system_prompt
        )
        
        return optimized_prompt
