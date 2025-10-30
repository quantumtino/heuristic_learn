#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文档处理器
负责处理用户上传的PDF和DOCX文件
"""

import os
from typing import List, Dict
from pypdf import PdfReader
from docx import Document
from backend.config.settings import settings


class DocumentProcessor:
    """文档处理器"""
    
    def __init__(self):
        """初始化文档处理器"""
        self.allowed_extensions = settings.allowed_extensions.split(",")
        self.max_file_size = settings.max_file_size
    
    def validate_file(self, file_path: str) -> bool:
        """
        验证文件是否符合要求
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            bool: 验证结果
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return False
        
        # 检查文件大小
        if os.path.getsize(file_path) > self.max_file_size:
            return False
        
        # 检查文件扩展名
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.allowed_extensions:
            return False
        
        return True
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        从PDF文件中提取文本
        
        Args:
            pdf_path (str): PDF文件路径
            
        Returns:
            str: 提取的文本内容
        """
        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"提取PDF文本时出错: {e}")
        
        return text
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """
        从DOCX文件中提取文本
        
        Args:
            docx_path (str): DOCX文件路径
            
        Returns:
            str: 提取的文本内容
        """
        text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"提取DOCX文本时出错: {e}")
        
        return text
    
    def process_document(self, file_path: str) -> str:
        """
        处理文档文件
        
        Args:
            file_path (str): 文档文件路径
            
        Returns:
            str: 处理后的文本内容
        """
        if not self.validate_file(file_path):
            raise ValueError("文件验证失败")
        
        _, ext = os.path.splitext(file_path)
        
        if ext.lower() == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext.lower() == ".docx":
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
