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
        处理用户请求的完整流程（支持审查失败后反馈重试）
        
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
            "final_content": "",
            "retry_count": 0  # 添加重试次数记录
        }
        
        try:
            # 1. 优化提示词（只需要一次）
            print("正在优化提示词...")
            optimized_prompt = self.prompt_optimizer.process(user_input)
            result["optimized_prompt"] = optimized_prompt
            
            # 2. 生成对话内容并进行审查，最多重试3次
            max_retries = 3
            current_attempt = 0
            dialog_content = ""
            review_passed = False
            review_feedback = ""
            
            while current_attempt <= max_retries:
                current_attempt += 1
                print(f"正在进行第 {current_attempt} 次生成和审查...")
                
                if current_attempt == 1:
                    # 第一次尝试，直接使用优化后的提示词
                    print("正在生成对话内容...")
                    dialog_content = self.content_generator.process(optimized_prompt)
                else:
                    # 重试时，将审查反馈作为上下文提供给内容生成器
                    print(f"第 {current_attempt} 次生成（基于审查反馈）...")
                    # 构造新的提示词，包含审查反馈
                    feedback_enhanced_prompt = f"""原始要求：{optimized_prompt}

之前的生成内容：
{dialog_content}

审查反馈：
{review_feedback}

请根据审查反馈改进内容，确保事实准确、符合要求。"""
                    dialog_content = self.content_generator.process(feedback_enhanced_prompt)
                
                # 3. 知识审查
                print("正在审查内容...")
                review_passed, review_feedback = self.knowledge_reviewer.process(dialog_content)
                
                # 记录审查结果
                result["review_feedback"] = review_feedback
                result["retry_count"] = current_attempt - 1  # 实际重试次数（第一次不算重试）
                
                if review_passed:
                    print(f"内容审查通过（第 {current_attempt} 次尝试），处理完成")
                    result["review_passed"] = True
                    result["dialog_content"] = dialog_content
                    result["final_content"] = dialog_content
                    break
                else:
                    print(f"第 {current_attempt} 次审查未通过，{review_feedback}")
                    if current_attempt < max_retries:
                        print("将审查反馈提供给内容生成器，准备重新生成...")
                    else:
                        print("已达到最大重试次数，停止生成")
            
            # 如果所有尝试都失败了
            if not review_passed:
                result["review_passed"] = False
                result["final_content"] = ""
                print("所有尝试均未通过审查，无法提供内容")
                
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
