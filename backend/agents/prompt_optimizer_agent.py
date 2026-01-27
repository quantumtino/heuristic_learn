#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
提示词优化Agent
负责优化用户输入的提示词，使其更适合生成启发性内容
"""

from typing import Any, Dict
from backend.agents.base_agent import BaseAgent
from backend.config.settings import settings
from backend.prompts import (
    PROMPT_OPTIMIZER_SYSTEM,
    PROMPT_OPTIMIZER_USER_TEMPLATE,
)


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
        system_prompt = PROMPT_OPTIMIZER_SYSTEM
        user_prompt = PROMPT_OPTIMIZER_USER_TEMPLATE.format(input_data=input_data)
        
        # 调用模型进行优化
        optimized_prompt = self._call_model(
            prompt=user_prompt,
            system_prompt=system_prompt
        )
        
        return optimized_prompt
