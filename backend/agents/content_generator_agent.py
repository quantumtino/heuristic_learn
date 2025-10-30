#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
内容生成Agent
负责根据优化后的提示词生成启发性对话内容
"""

from typing import Any, Dict, Tuple
from backend.agents.base_agent import BaseAgent
from backend.config.settings import settings


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
        # 构建系统提示词
        system_prompt = """你是一位经验丰富的中学教师，擅长以对话的形式向学生传授知识。
        你的任务是根据给定的主题生成一段启发性的对话内容，要求：
        1. 采用师生对话的形式，生动有趣
        2. 语言简洁明了，适合中学生理解
        3. 引导学生主动思考，而非直接给出答案
        4. 内容准确，符合教育标准
        """
        
        # 构建用户提示词
        user_prompt = f"请根据以下主题生成启发性对话内容：{input_data}"
        
        # 调用模型生成内容
        response = self._call_model(
            prompt=user_prompt,
            system_prompt=system_prompt
        )
        
        return response.strip()
