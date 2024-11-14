import setuptools
from setuptools import setup, find_packages

# 读取 README.md 文件的内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 设置包信息
setup(
    name="orcacal",  # 包名
    version="0.0.26",  # 版本号
    author="hty2dby",  # 作者名称
    author_email="hty@hty.ink",  # 作者电子邮件
    description="test",  # 简短描述
    long_description=long_description,  # 长描述（来自 README.md）
    long_description_content_type="text/markdown",  # 长描述的格式
    url="https://github.com/HTY-DBY/orcacal",  # 项目主页
    packages=find_packages(),  # 自动找到项目中的包
    classifiers=[  # 分类器
        "Programming Language :: Python :: 3",  # 编程语言
        "License :: OSI Approved :: MIT License",  # 许可证
        "Operating System :: OS Independent",  # 兼容操作系统
    ],
    package_data={
        "": ["Multiwfn/**/*"],  # 包含 Multiwfn 文件夹及其所有子文件和子文件夹
    },
    include_package_data=True,  # 包含非 Python 文件
)
