#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量测试脚本 - 对比三阶段工作流与直接使用qwen-max的效果
使用qwen-flash模拟中学生提问并评分
"""

import sys
import os
import json
import time
from typing import Dict, List, Any
from datetime import datetime

# 添加项目根目录到Python路径，以便正确导入backend模块
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from dashscope import Generation
from backend.workflow import WorkflowManager
from backend.config.settings import settings


class BatchTestComparison:
    """批量测试对比类"""
    
    def __init__(self, num_questions=6):
        """初始化测试"""
        self.workflow_manager = WorkflowManager()
        self.api_key = settings.dashscope_api_key
        self.test_results = []
        self.num_questions = num_questions
        
    def generate_student_questions(self, num_questions: int = None) -> List[str]:
        """
        使用qwen-flash生成中学生风格的问题
        
        Args:
            num_questions: 生成问题数量
            
        Returns:
            问题列表
        """
        if num_questions is None:
            num_questions = self.num_questions
            
        print(f"\n{'='*60}")
        print("步骤1: 生成中学生问题")
        print(f"{'='*60}")
        
        system_prompt = f"""你是一位初中生，对各学科知识充满好奇.
请生成{num_questions}个典型的中学生会问的问题，要求：
1. 涵盖物理、化学、数学、生物等不同学科
2. 问题要简单直白，符合中学生的提问方式
3. 既有基础概念问题，也有现象解释问题
4. 每个问题一行，不要编号

示例：
为什么天空是蓝色的
光合作用是怎么进行的
勾股定理是什么
"""
        
        try:
            response = Generation.call(
                model='qwen-flash',
                prompt=system_prompt,
                api_key=self.api_key
            )
            
            if response.status_code == 200:
                # 兼容不同的响应结构
                if hasattr(response.output, 'text'):
                    questions_text = response.output.text.strip()
                elif hasattr(response.output, 'choices') and response.output.choices:
                    questions_text = response.output.choices[0].message.content.strip()
                else:
                    questions_text = str(response.output).strip()
                
                questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
                # 取前num_questions个问题
                questions = questions[:num_questions]
                
                print(f"\n[SUCCESS] 成功生成 {len(questions)} 个问题:")
                for i, q in enumerate(questions, 1):
                    print(f"  {i}. {q}")
                
                return questions
            else:
                print(f"[ERROR] 问题生成失败: {response.message}")
                return []
                
        except Exception as e:
            print(f"[ERROR] 生成问题时出错: {e}")
            return []
    
    def get_workflow_response(self, question: str) -> Dict[str, Any]:
        """
        使用三阶段工作流获取回答
        
        Args:
            question: 问题
            
        Returns:
            包含回答和元数据的字典
        """
        print(f"\n  → 使用三阶段工作流处理...")
        start_time = time.time()
        
        try:
            result = self.workflow_manager.process_request(question)
            elapsed_time = time.time() - start_time
            
            return {
                "method": "三阶段工作流",
                "response": result.get("final_content", ""),
                "review_passed": result.get("review_passed", False),
                "review_feedback": result.get("review_feedback", ""),
                "time_cost": elapsed_time,
                "success": bool(result.get("final_content"))
            }
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "method": "三阶段工作流",
                "response": "",
                "error": str(e),
                "time_cost": elapsed_time,
                "success": False
            }
    
    def get_direct_max_response(self, question: str) -> Dict[str, Any]:
        """
        直接使用qwen-max获取回答
        
        Args:
            question: 问题
            
        Returns:
            包含回答和元数据的字典
        """
        print(f"  → 使用qwen-max直接回答...")
        start_time = time.time()
        
        system_prompt = """你是一位中学教师，请用简洁易懂的语言回答学生的问题。"""
        
        try:
            response = Generation.call(
                model='qwen-max',
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                api_key=self.api_key
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                # 兼容不同的响应结构
                if hasattr(response.output, 'choices') and response.output.choices:
                    content = response.output.choices[0].message.content
                elif hasattr(response.output, 'text'):
                    content = response.output.text
                else:
                    content = str(response.output)
                
                return {
                    "method": "直接使用qwen-max",
                    "response": content,
                    "time_cost": elapsed_time,
                    "success": True
                }
            else:
                return {
                    "method": "直接使用qwen-max",
                    "response": "",
                    "error": response.message,
                    "time_cost": elapsed_time,
                    "success": False
                }
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "method": "直接使用qwen-max",
                "response": "",
                "error": str(e),
                "time_cost": elapsed_time,
                "success": False
            }
    
    def evaluate_response(self, question: str, response: str, method: str) -> Dict[str, Any]:
        """
        使用qwen-flash从中学生视角评估回答质量
        
        Args:
            question: 原始问题
            response: 回答内容
            method: 回答方法
            
        Returns:
            评分结果
        """
        print(f"  → 评估 {method} 的回答...")
        
        evaluation_prompt = f"""你是一位初中生，刚刚问了老师一个问题并得到了回答。
请从中学生的视角评估这个回答的质量。

问题：{question}

回答：
{response}

请从以下几个维度评分（每项0-10分）：
1. 易理解性：语言是否简单易懂，没有过多专业术语
2. 启发性：是否引导我思考，而不是直接灌输答案
3. 趣味性：内容是否生动有趣，有吸引力
4. 完整性：是否完整回答了我的问题
5. 实用性：是否对我的学习有实际帮助

请严格按照以下JSON格式返回（不要添加任何其他内容）：
{{
    "易理解性": 分数,
    "启发性": 分数,
    "趣味性": 分数,
    "完整性": 分数,
    "实用性": 分数,
    "总分": 总分,
    "评语": "简短评语"
}}
"""
        
        try:
            response_obj = Generation.call(
                model='qwen-flash',
                prompt=evaluation_prompt,
                api_key=self.api_key
            )
            
            if response_obj.status_code == 200:
                result_text = response_obj.output.text.strip()
                
                # 尝试提取JSON
                try:
                    # 如果响应包含markdown代码块，提取其中的JSON
                    if "```json" in result_text:
                        start = result_text.find("```json") + 7
                        end = result_text.find("```", start)
                        result_text = result_text[start:end].strip()
                    elif "```" in result_text:
                        start = result_text.find("```") + 3
                        end = result_text.find("```", start)
                        result_text = result_text[start:end].strip()
                    
                    scores = json.loads(result_text)
                    
                    # 程序自己计算总分，而不是依赖模型计算
                    if all(key in scores for key in ["易理解性", "启发性", "趣味性", "完整性", "实用性"]):
                        calculated_total = scores["易理解性"] + scores["启发性"] + scores["趣味性"] + scores["完整性"] + scores["实用性"]
                        scores["总分"] = calculated_total
                    else:
                        # 如果缺少某些分数，则计算可用分数的总和
                        total = 0
                        for key in ["易理解性", "启发性", "趣味性", "完整性", "实用性"]:
                            if key in scores:
                                total += scores[key]
                        scores["总分"] = total
                    
                    return scores
                except json.JSONDecodeError:
                    print(f"  [ERROR] JSON解析失败，原始响应: {result_text[:100]}...")
                    return {
                        "易理解性": 0,
                        "启发性": 0,
                        "趣味性": 0,
                        "完整性": 0,
                        "实用性": 0,
                        "总分": 0,
                        "评语": "评分失败"
                    }
            else:
                print(f"  [ERROR] 评估失败: {response_obj.message}")
                return {
                    "易理解性": 0,
                    "启发性": 0,
                    "趣味性": 0,
                    "完整性": 0,
                    "实用性": 0,
                    "总分": 0,
                    "评语": "评估失败"
                }
                
        except Exception as e:
            print(f"  [ERROR] 评估时出错: {e}")
            return {
                "易理解性": 0,
                "启发性": 0,
                "趣味性": 0,
                "完整性": 0,
                "实用性": 0,
                "总分": 0,
                "评语": f"评估出错: {str(e)}"
            }
    
    def run_comparison_test(self):
        """运行对比测试"""
        print("\n" + "="*60)
        print("中学生知识辅助学习系统 - 批量对比测试")
        print("="*60)
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 生成问题
        questions = self.generate_student_questions(self.num_questions)
        
        if not questions:
            print("\n[ERROR] 未能生成测试问题，测试终止")
            return
        
        # 2. 对每个问题进行测试
        print(f"\n{'='*60}")
        print("步骤2: 对比测试")
        print(f"{'='*60}")
        
        for i, question in enumerate(questions, 1):
            print(f"\n【问题 {i}/{len(questions)}】: {question}")
            print("-" * 60)
            
            test_case = {
                "question": question,
                "workflow_result": {},
                "direct_max_result": {},
                "workflow_score": {},
                "direct_max_score": {}
            }
            
            # 2.1 使用三阶段工作流
            workflow_result = self.get_workflow_response(question)
            test_case["workflow_result"] = workflow_result
            
            if workflow_result["success"]:
                workflow_score = self.evaluate_response(
                    question, 
                    workflow_result["response"], 
                    "三阶段工作流"
                )
                test_case["workflow_score"] = workflow_score
                print(f"  [SUCCESS] 三阶段工作流得分: {workflow_score.get('总分', 0)}/50")
            else:
                print(f"  [ERROR] 三阶段工作流失败")
            
            # 2.2 直接使用qwen-max
            direct_result = self.get_direct_max_response(question)
            test_case["direct_max_result"] = direct_result
            
            if direct_result["success"]:
                direct_score = self.evaluate_response(
                    question,
                    direct_result["response"],
                    "直接使用qwen-max"
                )
                test_case["direct_max_score"] = direct_score
                print(f"  [SUCCESS] 直接qwen-max得分: {direct_score.get('总分', 0)}/50")
            else:
                print(f"  [ERROR] 直接qwen-max失败")
            
            self.test_results.append(test_case)
            
            # 避免API调用过快
            time.sleep(1)
        
        # 3. 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print(f"\n{'='*60}")
        print("步骤3: 生成测试报告")
        print(f"{'='*60}")
        
        # 计算统计数据
        workflow_scores = []
        direct_scores = []
        
        for result in self.test_results:
            if result["workflow_score"].get("总分"):
                workflow_scores.append(result["workflow_score"]["总分"])
            if result["direct_max_score"].get("总分"):
                direct_scores.append(result["direct_max_score"]["总分"])
        
        # 生成报告内容
        report = {
            "测试时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "测试问题数": len(self.test_results),
            "三阶段工作流": {
                "平均分": sum(workflow_scores) / len(workflow_scores) if workflow_scores else 0,
                "最高分": max(workflow_scores) if workflow_scores else 0,
                "最低分": min(workflow_scores) if workflow_scores else 0,
                "成功率": f"{len(workflow_scores) / len(self.test_results) * 100:.1f}%"
            },
            "直接qwen-max": {
                "平均分": sum(direct_scores) / len(direct_scores) if direct_scores else 0,
                "最高分": max(direct_scores) if direct_scores else 0,
                "最低分": min(direct_scores) if direct_scores else 0,
                "成功率": f"{len(direct_scores) / len(self.test_results) * 100:.1f}%"
            },
            "详细结果": self.test_results
        }
        
        # 创建按精确时间组织的目录结构（精确到秒）
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_dir = f"batch_tests/test_results_{time_str}"
        os.makedirs(results_dir, exist_ok=True)
        
        # 保存到JSON文件
        report_file = f"{results_dir}/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n[SUCCESS] 详细报告已保存至: {report_file}")
        
        # 打印摘要
        print(f"\n{'='*60}")
        print("测试结果摘要")
        print(f"{'='*60}")
        print(f"\n测试问题数: {len(self.test_results)}")
        
        print(f"\n[三阶段工作流]")
        print(f"  平均分: {report['三阶段工作流']['平均分']:.2f}/50")
        print(f"  最高分: {report['三阶段工作流']['最高分']:.2f}")
        print(f"  最低分: {report['三阶段工作流']['最低分']:.2f}")
        print(f"  成功率: {report['三阶段工作流']['成功率']}")
        
        print(f"\n[直接使用qwen-max]")
        print(f"  平均分: {report['直接qwen-max']['平均分']:.2f}/50")
        print(f"  最高分: {report['直接qwen-max']['最高分']:.2f}")
        print(f"  最低分: {report['直接qwen-max']['最低分']:.2f}")
        print(f"  成功率: {report['直接qwen-max']['成功率']}")
        
        # 对比分析
        if workflow_scores and direct_scores:
            diff = report['三阶段工作流']['平均分'] - report['直接qwen-max']['平均分']
            print(f"\n[对比分析]")
            if diff > 0:
                print(f"  [SUCCESS] 三阶段工作流平均分高出 {diff:.2f} 分 ({diff/50*100:.1f}%)")
                print(f"  [INFO] 三阶段工作流在中学生视角下表现更优")
            elif diff < 0:
                print(f"  [ERROR] 三阶段工作流平均分低 {abs(diff):.2f} 分 ({abs(diff)/50*100:.1f}%)")
                print(f"  [INFO] 直接使用qwen-max表现更优")
            else:
                print(f"  [=] 两种方法得分相当")
        print(f"\n{'='*60}")
        
        return report

    def generate_visualization(self, report_file_path: str):
        """生成可视化图表"""
        try:
            # 导入可视化模块
            from batch_tests.visualize_results import generate_visualizations
            # 生成带时间戳的图表
            generate_visualizations(report_file_path)
            print(f"✓ 可视化图表已生成")
        except ImportError:
            print("[INFO] 无法导入可视化模块，跳过图表生成")
        except Exception as e:
            print(f"[ERROR] 生成可视化图表时出错: {e}")


def main():
    """主函数"""
    import sys
    # 从命令行参数获取测试次数，默认为6
    num_questions = 6
    if len(sys.argv) > 1:
        try:
            num_questions = int(sys.argv[1])
        except ValueError:
            print(f"[INFO] 无效的参数，使用默认值: {num_questions}")
    
    tester = BatchTestComparison(num_questions=num_questions)
    report = tester.run_comparison_test()
    
    # 在测试完成后自动生成可视化图表
    if hasattr(tester, 'test_results') and tester.test_results:
        # 获取最新生成的报告文件路径
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_dir = f"batch_tests/test_results_{time_str}"
        import glob
        report_files = glob.glob(f"{results_dir}/test_report_*.json")
        if report_files:
            latest_report = max(report_files, key=os.path.getctime)
            tester.generate_visualization(latest_report)


if __name__ == "__main__":
    main()
