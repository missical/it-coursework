# Second-Hand Marketplace

A Django-based web application for buying and selling second-hand items. This platform allows users to list their used items for sale, browse products, communicate with sellers, and complete transactions online.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **User Dashboard**: Manage personal profile, view favorited items and listed products
- **Product Management**: Create, edit, and delete product listings with images, descriptions, prices, and categories
- **Product Search and Filtering**: Search by category, price range, keywords, and location
- **Order Management**: Place orders, track order status, and view order history
- **Payment Simulation**: Simulate online payments for purchases
- **Messaging System**: Built-in chat functionality between buyers and sellers
- **Ratings and Reviews**: Rate and review sellers after completed transactions
- **Reporting System**: Report fraudulent or inappropriate listings

## Technology Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Image Processing**: Pillow
- **Forms**: django-crispy-forms with crispy-bootstrap5

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd secondhand-marketplace
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Initial Setup

After installation, you should:

1. Log in to the admin panel at http://127.0.0.1:8000/admin/
2. Create some product categories
3. Create some initial products (or register as a regular user and create them through the UI)

## Project Structure

- `marketplace/`: Main project settings
- `users/`: User authentication and profile management
- `products/`: Product listing, search, and management
- `orders/`: Order processing and payment
- `messages/`: Messaging system between users
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `media/`: User-uploaded files

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# 单元测试文档生成器

这是一个用于生成单元测试报告的Python工具，可以将单元测试结果转换为格式化的Word文档。

## 功能特点

- 支持从Python的unittest测试套件中收集测试结果
- 生成包含测试摘要、详细测试结果和结论的Word文档
- 使用颜色和格式化表格提高可读性
- 自动计算测试通过率和统计数据
- 可以手动添加测试结果或从unittest测试套件中自动收集

## 安装依赖

在使用此工具前，请确保安装了所需的依赖：

```bash
pip install python-docx
```

## 文件说明

- `unit_test_report.py`: 核心文档生成器类
- `example_tests.py`: 示例单元测试类
- `generate_test_report.py`: 运行测试并生成报告的示例脚本

## 使用方法

### 1. 运行示例

直接运行示例脚本生成测试报告：

```bash
python generate_test_report.py
```

这将运行示例测试并生成名为"单元测试报告.docx"的Word文档。

### 2. 集成到您自己的项目

#### 步骤1: 导入文档生成器

```python
from unit_test_report import UnitTestDocumentGenerator
```

#### 步骤2: 创建文档生成器实例

```python
generator = UnitTestDocumentGenerator(
    project_name="您的项目名称",
    version="1.0.0",
    author="您的团队名称"
)
```

#### 步骤3: 添加测试结果

方法A - 从unittest测试套件添加：

```python
import unittest
# 创建测试套件
test_suite = unittest.TestSuite()
# 添加测试用例
test_suite.addTest(unittest.makeSuite(YourTestClass))
# 将测试结果添加到生成器
generator.add_test_results_from_unittest(test_suite)
```

方法B - 手动添加测试结果：

```python
from unit_test_report import TestResult
# 添加单个测试结果
generator.add_test_result(TestResult(
    name="test_function_name",
    status="通过",  # "通过", "失败", "错误", "跳过"
    execution_time=0.123,  # 秒
    details="可选的详细信息"
))
```

#### 步骤4: 生成文档

```python
output_path = "测试报告.docx"
success = generator.generate(output_path)
if success:
    print(f"测试报告已生成: {output_path}")
else:
    print("生成测试报告失败")
```

## 自定义

您可以通过修改`unit_test_report.py`中的方法来自定义报告的外观和内容：

- `_add_title()`: 修改标题格式
- `_add_summary()`: 修改摘要表格
- `_add_test_details()`: 修改测试详情表格
- `_add_conclusion()`: 修改结论部分

## 注意事项

- 确保您的环境中安装了python-docx库
- 生成的文档可以使用Microsoft Word或其他兼容的文档编辑器打开
- 对于大型测试套件，生成文档可能需要一些时间 