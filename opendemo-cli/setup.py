from setuptools import setup, find_packages

setup(
    name="opendemo",
    version="0.1.0",
    description="智能化的编程学习辅助CLI工具",
    author="Open Demo Contributors",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'opendemo=cli:cli',
        ],
    },
    install_requires=[
        'click>=8.0.0',
    ],
    python_requires='>=3.8',
)