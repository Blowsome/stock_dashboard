from setuptools import setup, find_packages

setup(
    name="stock_dashboard",
    version="0.1.0",
    description="A Python package for creating stock dashboards",
    author="Daoming Qin",
    author_email="daomingqin80@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "yfinance",
        "streamlit",
        "numpy",
        "seaborn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)