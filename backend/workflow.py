#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工作流管理器
协调各个Agent完成完整的知识辅助学习流程
"""

from typing import Dict, Any, Optional, Callable
from backend.agents.prompt_optimizer_agent import PromptOptimizerAgent
from backend.agents.content_generator_agent import ContentGeneratorAgent
from backend.agents.knowledge_reviewer_agent import KnowledgeReviewerAgent
from backend.prompts import EXPLANATION_USER_TEMPLATE


class WorkflowManager:
    """工作流管理器"""
    
    def __init__(self):
        """初始化工作流管理器"""
        self.prompt_optimizer = PromptOptimizerAgent()
        self.content_generator = ContentGeneratorAgent()
        self.knowledge_reviewer = KnowledgeReviewerAgent()
    
    def process_request(
        self,
        user_input: str,
        explanation_history: str = "",
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """
        处理用户请求的完整流程（支持审查失败后反馈重试）
        
        Args:
            user_input (str): 用户输入的原始请求
            
        Returns:
            Dict[str, Any]: 处理结果
        """

        def _notify(event_type: str, **payload: Any) -> None:
            if progress_callback:
                progress_callback({"type": event_type, **payload})

        result = {
            "original_input": user_input,
            "optimized_prompt": "",
            "dialog_content": "",
            "explanation_content": "",
            "review_passed": False,
            "review_feedback": "",
            "review_score": 0,
            "final_content": "",
            "retry_count": 0  # 添加重试次数记录
        }
        
        try:
            # 1. 优化提示词（只需要一次）
            print("正在优化提示词...")
            _notify("optimize_start")
            optimized_prompt = self.prompt_optimizer.process(user_input)
            result["optimized_prompt"] = optimized_prompt
            _notify("optimize_done", prompt=optimized_prompt)
            
            # 2. 阶段一：对话生成 + 审查
            max_retries = 3
            dialog_content = ""
            review_feedback = ""
            review_score = 0
            dialog_passed = False

            for attempt in range(1, max_retries + 1):
                _notify("dialog_generation_start", attempt=attempt)
                print(f"第 {attempt} 次生成对话内容...")

                if attempt == 1 and not review_feedback:
                    dialog_content = self.content_generator.process(optimized_prompt)
                else:
                    feedback_enhanced_prompt = f"""原始要求：{optimized_prompt}

之前的对话内容：
{dialog_content}

审查反馈：
{review_feedback}

请根据审查反馈改进对话内容，确保事实准确、符合要求。"""
                    dialog_content = self.content_generator.process(feedback_enhanced_prompt)

                _notify("dialog_generation_done", attempt=attempt, content=dialog_content)

                # 审查对话内容
                print("正在审查对话内容...")
                _notify("dialog_review_start", attempt=attempt)
                dialog_passed, review_feedback = self.knowledge_reviewer.process(dialog_content)
                review_score = 100 if dialog_passed else 0
                _notify(
                    "dialog_review_done",
                    attempt=attempt,
                    passed=dialog_passed,
                    feedback=review_feedback,
                    score=review_score,
                )

                result["retry_count"] = attempt - 1
                if dialog_passed:
                    result["dialog_content"] = dialog_content
                    break
                else:
                    _notify(
                        "dialog_review_failed",
                        attempt=attempt,
                        feedback=review_feedback,
                        score=review_score,
                    )
                    if attempt == max_retries:
                        _notify("dialog_stop", attempt=attempt)
                        result["review_passed"] = False
                        result["review_feedback"] = review_feedback
                        result["review_score"] = review_score
                        result["final_content"] = ""
                        return result

            # 3. 阶段二：详细阐述生成 + 审查
            explanation_content = ""
            explanation_feedback = ""
            explanation_passed = False
            explanation_score = 0

            for attempt in range(1, max_retries + 1):
                _notify("explanation_generation_start", attempt=attempt)
                print(f"第 {attempt} 次生成详细阐述...")

                explanation_prompt = EXPLANATION_USER_TEMPLATE.format(
                    original_input=user_input,
                    optimized_prompt=optimized_prompt,
                    explanation_history=explanation_history or "无",
                )
                if attempt > 1 and explanation_feedback:
                    explanation_prompt = f"""{explanation_prompt}

上次审查反馈：
{explanation_feedback}

请改进详细阐述，确保准确且通俗。"""

                explanation_content = self.content_generator.process(explanation_prompt)
                _notify("explanation_generation_done", attempt=attempt, content=explanation_content)

                # 审查详细阐述
                print("正在审查详细阐述...")
                _notify("explanation_review_start", attempt=attempt)
                explanation_passed, explanation_feedback = self.knowledge_reviewer.process(explanation_content)
                explanation_score = 100 if explanation_passed else 0
                _notify(
                    "explanation_review_done",
                    attempt=attempt,
                    passed=explanation_passed,
                    feedback=explanation_feedback,
                    score=explanation_score,
                )

                if explanation_passed:
                    result["review_passed"] = True
                    result["review_feedback"] = explanation_feedback
                    result["review_score"] = explanation_score
                    result["dialog_content"] = dialog_content
                    result["explanation_content"] = explanation_content
                    result["final_content"] = explanation_content
                    _notify(
                        "final_success",
                        attempt=attempt,
                        content=explanation_content,
                        feedback=explanation_feedback,
                        score=explanation_score,
                    )
                    break
                else:
                    _notify(
                        "explanation_review_failed",
                        attempt=attempt,
                        feedback=explanation_feedback,
                        score=explanation_score,
                    )
                    if attempt == max_retries:
                        _notify("explanation_stop", attempt=attempt)
                        result["review_passed"] = False
                        result["review_feedback"] = explanation_feedback
                        result["review_score"] = explanation_score
                        result["dialog_content"] = dialog_content
                        result["explanation_content"] = explanation_content
                        result["final_content"] = ""
                        return result
            
            # 如果所有尝试都失败了
            if not result.get("review_passed", False):
                result["final_content"] = ""
                print("所有尝试均未通过审查，无法提供内容")
                _notify("final_failed", feedback=result.get("review_feedback", ""))
                
        except Exception as e:
            print(f"处理过程中发生错误: {e}")
            result["error"] = str(e)
        
        return result
    
    def regenerate_content(self, user_input: str, progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
        """
        重新生成内容（当审查未通过时）
        
        Args:
            user_input (str): 用户输入
            
        Returns:
            Dict[str, Any]: 重新生成的结果
        """
        # 这里可以实现更复杂的重试逻辑
        # 暂时直接调用process_request
        return self.process_request(user_input, progress_callback=progress_callback)
