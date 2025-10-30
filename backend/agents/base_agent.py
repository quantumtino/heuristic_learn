#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基础Agent类
所有Agent的基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from backend.config.settings import settings


class BaseAgent(ABC):
    """基础Agent类"""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        初始化Agent
        
        Args:
            model_name (str, optional): 使用的模型名称
        """
        self.model_name = model_name
        self.api_key = settings.dashscope_api_key
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        处理输入数据的抽象方法
        
        Args:
            input_data: 输入数据
            
        Returns:
            处理结果
        """
        pass
    
    def _call_model(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        调用大模型API
        
        Args:
            prompt (str): 用户提示词
            system_prompt (str, optional): 系统提示词
            
        Returns:
            模型响应
        """
        # 这里将实现实际的模型调用逻辑
        # 暂时返回模拟响应
        return f"Model response for prompt: {prompt}"
