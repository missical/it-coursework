#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例单元测试
用于演示如何将实际测试结果集成到单元测试文档中
"""

import unittest
import time
import random


class Calculator:
    """简单计算器类，用于测试"""
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def subtract(a, b):
        return a - b
    
    @staticmethod
    def multiply(a, b):
        return a * b
    
    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


class UserManager:
    """用户管理类，用于测试"""
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = {"password": password, "active": True}
        return True
    
    def authenticate(self, username, password):
        if username not in self.users:
            return False
        if self.users[username]["password"] != password:
            return False
        return self.users[username]["active"]
    
    def deactivate_user(self, username):
        if username not in self.users:
            return False
        self.users[username]["active"] = False
        return True


class CalculatorTest(unittest.TestCase):
    """计算器测试类"""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        """测试加法功能"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-1, -1), -2)
    
    def test_subtract(self):
        """测试减法功能"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 1), 0)
        self.assertEqual(self.calc.subtract(-1, -1), 0)
    
    def test_multiply(self):
        """测试乘法功能"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertEqual(self.calc.multiply(3, 5), 15)
        self.assertEqual(self.calc.multiply(-1, 1), -1)
        self.assertEqual(self.calc.multiply(-1, -1), 1)
    
    def test_divide(self):
        """测试除法功能"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertEqual(self.calc.divide(6, 3), 2)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        self.assertEqual(self.calc.divide(-1, 1), -1)
        
        # 测试除以零的情况
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)


class UserManagerTest(unittest.TestCase):
    """用户管理测试类"""
    
    def setUp(self):
        self.user_manager = UserManager()
        # 预先添加一个测试用户
        self.user_manager.add_user("testuser", "password123")
    
    def test_add_user_success(self):
        """测试成功添加用户"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertTrue(self.user_manager.add_user("newuser", "newpass"))
        self.assertIn("newuser", self.user_manager.users)
    
    def test_add_user_duplicate(self):
        """测试添加重复用户"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertFalse(self.user_manager.add_user("testuser", "anotherpass"))
    
    def test_authenticate_success(self):
        """测试成功认证用户"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertTrue(self.user_manager.authenticate("testuser", "password123"))
    
    def test_authenticate_wrong_password(self):
        """测试错误密码认证"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertFalse(self.user_manager.authenticate("testuser", "wrongpass"))
    
    def test_authenticate_nonexistent_user(self):
        """测试不存在的用户认证"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertFalse(self.user_manager.authenticate("nonexistent", "anypass"))
    
    def test_deactivate_user(self):
        """测试停用用户"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟执行时间
        self.assertTrue(self.user_manager.deactivate_user("testuser"))
        self.assertFalse(self.user_manager.users["testuser"]["active"])
        self.assertFalse(self.user_manager.authenticate("testuser", "password123"))
    
    @unittest.skip("此功能尚未实现")
    def test_reset_password(self):
        """测试重置密码功能（尚未实现）"""
        pass


def get_test_suite():
    """获取完整的测试套件"""
    suite = unittest.TestSuite()
    
    # 添加计算器测试
    suite.addTest(unittest.makeSuite(CalculatorTest))
    
    # 添加用户管理测试
    suite.addTest(unittest.makeSuite(UserManagerTest))
    
    return suite


if __name__ == "__main__":
    # 运行所有测试
    unittest.main() 