#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
内容生成Agent
负责根据优化后的提示词生成启发性对话内容
"""

from typing import Any, Dict, Tuple
from backend.agents.base_agent import BaseAgent
from backend.config.settings import settings
from backend.prompts import (
    CONTENT_GENERATOR_SYSTEM,
    CONTENT_GENERATOR_USER_TEMPLATE,
)


class ContentGeneratorAgent(BaseAgent):
    """内容生成Agent"""
    
    def __init__(self):
        """初始化内容生成Agent"""
        super().__init__(model_name=settings.generator_model)
    
    def process(self, input_data: str) -> str:
        """
        生成启发性对话内容
        
        Args:
            input_data (str): 优化后的提示词
            
        Returns:
            str: 生成的对话内容
        """
        system_prompt = CONTENT_GENERATOR_SYSTEM
        user_prompt = CONTENT_GENERATOR_USER_TEMPLATE.format(input_data=input_data)
        
        # 调用模型生成内容
        response = self._call_model(
            prompt=user_prompt,
            system_prompt=system_prompt
        )
        
        return response.strip()
