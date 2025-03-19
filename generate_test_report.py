#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单元测试报告生成器
运行单元测试并生成Word格式的测试报告
"""

import os
import sys
import unittest
from unit_test_report import UnitTestDocumentGenerator
from example_tests import get_test_suite


def generate_test_report(project_name, version, author, output_path):
    """运行单元测试并生成测试报告
    
    Args:
        project_name: 项目名称
        version: 版本号
        author: 作者
        output_path: 输出文件路径
    
    Returns:
        bool: 是否成功生成报告
    """
    # 创建文档生成器
    generator = UnitTestDocumentGenerator(
        project_name=project_name,
        version=version,
        author=author
    )
    
    # 获取测试套件
    test_suite = get_test_suite()
    
    # 从测试套件添加测试结果
    generator.add_test_results_from_unittest(test_suite)
    
    # 生成文档
    success = generator.generate(output_path)
    
    return success


def main():
    """主函数"""
    # 设置项目信息
    project_name = "示例项目"
    version = "1.0.0"
    author = "测试团队"
    
    # 设置输出文件路径
    output_path = "单元测试报告.docx"
    
    # 生成测试报告
    success = generate_test_report(
        project_name=project_name,
        version=version,
        author=author,
        output_path=output_path
    )
    
    # 输出结果
    if success:
        print(f"单元测试报告已生成: {os.path.abspath(output_path)}")
        return 0
    else:
        print("生成单元测试报告失败")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 