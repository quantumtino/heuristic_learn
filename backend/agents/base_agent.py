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
        try:
            from dashscope import Generation
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = Generation.call(
                model=self.model_name,
                messages=messages,
                api_key=self.api_key
            )
            
            if response.status_code == 200:
                # 检查响应结构
                if hasattr(response.output, 'choices') and response.output.choices:
                    return response.output.choices[0].message.content
                elif hasattr(response.output, 'text'):
                    return response.output.text
                else:
                    raise Exception(f"无法解析API响应结构: {response.output}")
            else:
                raise Exception(f"API调用失败 (状态码: {response.status_code}): {response.message}")
                
        except Exception as e:
            raise Exception(f"模型调用出错: {str(e)}")
