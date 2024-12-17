from setuptools import setup, find_packages

setup(
    name='pbot',  # 包的名称
    version='0.1.0',  # 版本号
    description='A brief description of the package.',  # 简短描述
    long_description=open('README.md').read(),  # 详细描述
    long_description_content_type='text/markdown',  # 详细描述的格式
    url='https://github.com/yourusername/pbot',  # 项目主页
    author='Your Name',  # 作者名字
    author_email='your.email@example.com',  # 作者邮箱
    license='MIT',  # 许可证
    classifiers=[  # 分类器
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(where='src'),  # 找到所有包
    package_dir={'': 'src'},  # 指定包的根目录
    install_requires=[  # 依赖包
        # 'dependency1',
        # 'dependency2',
    ],
    python_requires='>=3.6',  # 支持的Python版本
)
