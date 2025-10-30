#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工作流管理器
协调各个Agent完成完整的知识辅助学习流程
"""

from typing import Dict, Any
from backend.agents.prompt_optimizer_agent import PromptOptimizerAgent
from backend.agents.content_generator_agent import ContentGeneratorAgent
from backend.agents.knowledge_reviewer_agent import KnowledgeReviewerAgent


class WorkflowManager:
    """工作流管理器"""
    
    def __init__(self):
        """初始化工作流管理器"""
        self.prompt_optimizer = PromptOptimizerAgent()
        self.content_generator = ContentGeneratorAgent()
        self.knowledge_reviewer = KnowledgeReviewerAgent()
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户请求的完整流程
        
        Args:
            user_input (str): 用户输入的原始请求
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        result = {
            "original_input": user_input,
            "optimized_prompt": "",
            "dialog_content": "",
            "review_passed": False,
            "review_feedback": "",
            "final_content": ""
        }
        
        try:
            # 1. 优化提示词
            print("正在优化提示词...")
            optimized_prompt = self.prompt_optimizer.process(user_input)
            result["optimized_prompt"] = optimized_prompt
            
            # 2. 生成对话内容
            print("正在生成对话内容...")
            dialog_content = self.content_generator.process(optimized_prompt)
            result["dialog_content"] = dialog_content
            
            # 3. 知识审查
            print("正在审查内容...")
            review_passed, review_feedback = self.knowledge_reviewer.process(dialog_content)
            result["review_passed"] = review_passed
            result["review_feedback"] = review_feedback
            
            # 4. 根据审查结果处理
            if review_passed:
                result["final_content"] = dialog_content
                print("内容审查通过，处理完成")
            else:
                result["final_content"] = ""
                print("内容审查未通过，需要重新生成")
                
        except Exception as e:
            print(f"处理过程中发生错误: {e}")
            result["error"] = str(e)
        
        return result
    
    def regenerate_content(self, user_input: str) -> Dict[str, Any]:
        """
        重新生成内容（当审查未通过时）
        
        Args:
            user_input (str): 用户输入
            
        Returns:
            Dict[str, Any]: 重新生成的结果
        """
        # 这里可以实现更复杂的重试逻辑
        # 暂时直接调用process_request
        return self.process_request(user_input)
