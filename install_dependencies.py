#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
依赖安装脚本
帮助用户安装项目所需的依赖包，特别处理dashscope包的安装问题
"""

import subprocess
import sys
import os

def install_package(package):
    """安装指定的包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败: {e}")
        return False

def install_from_requirements():
    """从requirements.txt安装依赖"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 所有依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 从requirements.txt安装依赖失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 中学生知识辅助学习系统依赖安装脚本 ===\n")
    
    # 检查是否在项目根目录
    if not os.path.exists("requirements.txt"):
        print("错误: 请在项目根目录运行此脚本")
        return
    
    print("1. 尝试直接从requirements.txt安装所有依赖...")
    if install_from_requirements():
        print("\n所有依赖安装完成！")
        return
    
    print("\n2. 分步安装依赖...")
    
    # 从requirements.txt读取依赖列表
    with open("requirements.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 过滤掉注释和空行
    packages = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    
    # 分步安装每个包
    failed_packages = []
    for package in packages:
        print(f"\n正在安装 {package}...")
        if not install_package(package):
            failed_packages.append(package)
    
    # 特别处理dashscope
    if "dashscope>=1.14.0" in failed_packages or any("dashscope" in pkg for pkg in failed_packages):
        print("\n3. 特别处理dashscope包...")
        print("尝试安装最新版本的dashscope...")
        if install_package("dashscope"):
            # 从失败列表中移除dashscope相关项
            failed_packages = [pkg for pkg in failed_packages if "dashscope" not in pkg]
    
    # 最终结果
    if failed_packages:
        print(f"\n以下包安装失败:")
        for pkg in failed_packages:
            print(f"  - {pkg}")
        print("\n请手动安装这些包，或检查网络连接和Python环境。")
    else:
        print("\n所有依赖安装完成！")

if __name__ == "__main__":
    main()
