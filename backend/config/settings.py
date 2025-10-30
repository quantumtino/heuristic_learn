#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统配置设置
从环境变量加载配置
"""

import os
from typing import Optional

# 处理Pydantic版本兼容性问题
try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        # 如果两个都失败，抛出一个更清晰的错误信息
        raise ImportError(
            "Cannot import BaseSettings. Please install pydantic-settings package: "
            "pip install pydantic-settings"
        )

from pydantic import Field


class Settings(BaseSettings):
    # DashScope API配置
    dashscope_api_key: str = Field(..., env="DASHSCOPE_API_KEY")
    
    # 模型配置
    optimizer_model: str = Field("qwen-flash", env="OPTIMIZER_MODEL")
    generator_model: str = Field("qwen-plus-character", env="GENERATOR_MODEL")
    reviewer_model: str = Field("qwen-flash", env="REVIEWER_MODEL")
    
    # 文件上传配置
    allowed_extensions: str = Field(".pdf,.docx", env="ALLOWED_EXTENSIONS")
    max_file_size: int = Field(10485760, env="MAX_FILE_SIZE")  # 10MB
    
    # 应用设置
    debug: bool = Field(True, env="DEBUG")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings()
