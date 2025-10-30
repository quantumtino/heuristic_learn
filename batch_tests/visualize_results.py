#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
根据测试报告生成可视化图表
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


def load_test_report(report_path):
    """
    加载测试报告
    
    Args:
        report_path (str): 测试报告文件路径
        
    Returns:
        dict: 测试报告数据
    """
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def plot_overall_comparison(report_data, results_dir):
    """
    绘制整体对比图

    Args:
        report_data (dict): 测试报告数据
        results_dir (str): 结果保存目录
    """
    # 准备数据
    methods = ['三阶段工作流', '直接qwen-max']
    avg_scores = [
        report_data['三阶段工作流']['平均分'],
        report_data['直接qwen-max']['平均分']
    ]
    max_scores = [
        report_data['三阶段工作流']['最高分'],
        report_data['直接qwen-max']['最高分']
    ]
    min_scores = [
        report_data['三阶段工作流']['最低分'],
        report_data['直接qwen-max']['最低分']
    ]
    
    # 创建子图
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 设置柱状图位置
    x = np.arange(len(methods))
    width = 0.25
    
    # 绘制柱状图
    bars1 = ax.bar(x - width, avg_scores, width, label='平均分', color='skyblue', alpha=0.8)
    bars2 = ax.bar(x, max_scores, width, label='最高分', color='lightgreen', alpha=0.8)
    bars3 = ax.bar(x + width, min_scores, width, label='最低分', color='lightcoral', alpha=0.8)
    
    # 添加数值标签
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=10)
    
    # 设置图表标题和标签
    ax.set_xlabel('方法', fontsize=12)
    ax.set_ylabel('分数', fontsize=12)
    ax.set_title(f'三阶段工作流 vs 直接qwen-max - 整体性能对比\n(测试时间: {report_data["测试时间"]})', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend()
    
    # 添加网格
    ax.grid(axis='y', alpha=0.3)
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'overall_comparison_{timestamp}.png'
    filepath = os.path.join(results_dir, filename)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"已生成整体对比图: {filepath}")
    
    return fig


def plot_detailed_comparison(report_data, results_dir):
    """
    绘制详细对比图（各维度评分）

    Args:
        report_data (dict): 测试报告数据
        results_dir (str): 结果保存目录
    """
    # 准备数据
    questions = [item['question'] for item in report_data['详细结果']]
    dimensions = ['易理解性', '启发性', '趣味性', '完整性', '实用性']
    
    # 为每个问题和方法创建评分矩阵
    workflow_scores = []
    direct_scores = []
    
    for item in report_data['详细结果']:
        workflow_scores.append([item['workflow_score'][dim] for dim in dimensions])
        direct_scores.append([item['direct_max_score'][dim] for dim in dimensions])
    
    # 创建子图
    fig, axes = plt.subplots(2, 3, figsize=(18, 14))  # 增加高度以容纳问题说明
    axes = axes.flatten()
    
    # 为每个维度绘制对比图
    for i, dim in enumerate(dimensions):
        if i < len(axes):
            ax = axes[i]
            
            # 准备数据
            x = np.arange(len(questions))
            width = 0.35
            
            # 提取当前维度的评分
            workflow_dim_scores = [scores[i] for scores in workflow_scores]
            direct_dim_scores = [scores[i] for scores in direct_scores]
            
            # 绘制柱状图
            bars1 = ax.bar(x - width/2, workflow_dim_scores, width, label='三阶段工作流', 
                          color='skyblue', alpha=0.8)
            bars2 = ax.bar(x + width/2, direct_dim_scores, width, label='直接qwen-max', 
                          color='lightcoral', alpha=0.8)
            
            # 添加数值标签
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:  # 只为非零值添加标签
                        ax.annotate(f'{int(height)}',
                                   xy=(bar.get_x() + bar.get_width() / 2, height),
                                   xytext=(0, 3),
                                   textcoords="offset points",
                                   ha='center', va='bottom', fontsize=8)
            
            # 设置标题和标签
            ax.set_title(f'{dim}评分对比', fontsize=12)
            ax.set_xticks(x)
            # 使用问题1, 问题2...作为标签
            question_labels = [f'问题{i+1}' for i in range(len(questions))]
            ax.set_xticklabels(question_labels, rotation=0, ha='center', fontsize=9)
            ax.set_ylabel('分数', fontsize=10)
            ax.legend(fontsize=9)
            ax.grid(axis='y', alpha=0.3)
    
    # 隐藏多余的子图
    for i in range(len(dimensions), len(axes)):
        axes[i].set_visible(False)
    
    # 在图下方添加问题说明
    fig.text(0.5, 0.02, '问题列表：\n' + '\n'.join([f'问题{i+1}: {q}' for i, q in enumerate(questions)]), 
             ha='center', va='bottom', fontsize=10, wrap=True)
    
    # 调整布局，为底部文本留出空间
    plt.subplots_adjust(bottom=0.15)
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'detailed_comparison_{timestamp}.png'
    filepath = os.path.join(results_dir, filename)
    
    # 保存图片
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"已生成详细对比图: {filepath}")
    
    return fig


def plot_total_scores_comparison(report_data, results_dir):
    """
    绘制总分对比图

    Args:
        report_data (dict): 测试报告数据
        results_dir (str): 结果保存目录
    """
    # 准备数据
    questions = [item['question'] for item in report_data['详细结果']]
    workflow_total_scores = [item['workflow_score']['总分'] for item in report_data['详细结果']]
    direct_total_scores = [item['direct_max_score']['总分'] for item in report_data['详细结果']]
    
    # 创建子图
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 设置位置
    x = np.arange(len(questions))
    width = 0.35
    
    # 绘制柱状图
    bars1 = ax.bar(x - width/2, workflow_total_scores, width, label='三阶段工作流', 
                  color='skyblue', alpha=0.8)
    bars2 = ax.bar(x + width/2, direct_total_scores, width, label='直接qwen-max', 
                  color='lightcoral', alpha=0.8)
    
    # 添加数值标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=10)
    
    # 设置标题和标签
    ax.set_xlabel('问题', fontsize=12)
    ax.set_ylabel('总分', fontsize=12)
    ax.set_title('各问题总分对比 - 三阶段启发式工作流 vs 直接使用qwen-max', fontsize=14)
    ax.set_xticks(x)
    # 水平显示标签，并在过长时换行
    formatted_labels = []
    for q in questions:
        if len(q) > 15:
            # 将长标签按空格分割成多行
            words = q.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + word) <= 15:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
            formatted_labels.append('\n'.join(lines))
        else:
            formatted_labels.append(q)
    ax.set_xticklabels(formatted_labels, rotation=0, ha='center', fontsize=10)
    ax.legend()
    
    # 添加网格
    ax.grid(axis='y', alpha=0.3)
    
    # 调整布局
    plt.tight_layout()
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'total_scores_comparison_{timestamp}.png'
    filepath = os.path.join(results_dir, filename)
    
    # 保存图片
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"已生成总分对比图: {filepath}")
    
    return fig


def plot_dimension_averages(report_data, results_dir):
    """
    绘制各维度平均分对比图

    Args:
        report_data (dict): 测试报告数据
        results_dir (str): 结果保存目录
    """
    # 准备数据
    dimensions = ['易理解性', '启发性', '趣味性', '完整性', '实用性']
    
    # 计算各维度的平均分
    workflow_avg_scores = []
    direct_avg_scores = []
    
    for dim in dimensions:
        workflow_scores = [item['workflow_score'][dim] for item in report_data['详细结果']]
        direct_scores = [item['direct_max_score'][dim] for item in report_data['详细结果']]
        
        workflow_avg_scores.append(sum(workflow_scores) / len(workflow_scores))
        direct_avg_scores.append(sum(direct_scores) / len(direct_scores))
    
    # 创建子图
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 设置位置
    x = np.arange(len(dimensions))
    width = 0.35
    
    # 绘制柱状图
    bars1 = ax.bar(x - width/2, workflow_avg_scores, width, label='三阶段工作流', 
                  color='skyblue', alpha=0.8)
    bars2 = ax.bar(x + width/2, direct_avg_scores, width, label='直接qwen-max', 
                  color='lightcoral', alpha=0.8)
    
    # 添加数值标签
    for bars in [bars1, bars2]:
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=10)
    
    # 设置标题和标签
    ax.set_xlabel('评分维度', fontsize=12)
    ax.set_ylabel('平均分', fontsize=12)
    ax.set_title('各维度平均分对比 - 三阶段启发式工作流 vs 直接使用qwen-max', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(dimensions)
    ax.legend()
    
    # 添加网格
    ax.grid(axis='y', alpha=0.3)
    
    # 调整布局
    plt.tight_layout()
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'dimension_averages_comparison_{timestamp}.png'
    filepath = os.path.join(results_dir, filename)
    
    # 保存图片
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"已生成维度平均分对比图: {filepath}")
    
    return fig


def generate_visualizations(report_path='test_report_20251030_210320.json'):
    """
    生成所有可视化图表

    Args:
        report_path (str): 测试报告文件路径
    """
    print(f"正在加载测试报告: {report_path}")
    report_data = load_test_report(report_path)
    
    # 从报告路径中提取日期目录
    import os
    from datetime import datetime
    report_dir = os.path.dirname(report_path)
    if not report_dir:
        # 如果报告路径中没有目录，则创建默认日期目录
        date_str = datetime.now().strftime('%Y%m%d')
        report_dir = f"test_results_{date_str}"
        os.makedirs(report_dir, exist_ok=True)
    
    print("正在生成可视化图表...")
    
    # 生成各种对比图
    plot_overall_comparison(report_data, report_dir)
    plot_detailed_comparison(report_data, report_dir)
    plot_total_scores_comparison(report_data, report_dir)
    plot_dimension_averages(report_data, report_dir)
    
    print("\n可视化图表生成完成！")
    print(f"生成的文件保存在: {report_dir}")


if __name__ == "__main__":
    # 查找最新的测试报告
    report_files = [f for f in os.listdir('.') if f.startswith('test_report_') and f.endswith('.json') and not f.startswith('test_report_sample')]
    if report_files:
        latest_report = max(report_files, key=lambda x: x)
        print(f"找到最新的测试报告: {latest_report}")
        generate_visualizations(latest_report)
    else:
        print("未找到测试报告文件，使用默认文件: test_report_20251030_210320.json")
        generate_visualizations()
