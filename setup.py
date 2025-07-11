#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="ai-commit",
    version="1.0.0",
    description="AI-powered commit message generator using Ollama",
    author="m3",
    author_email="m3@example.com",
    url="https://github.com/m3/ai-commit",
    py_modules=["ai_commit"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-commit=ai_commit:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="git commit ai ollama automation",
    project_urls={
        "Bug Reports": "https://github.com/m3/ai-commit/issues",
        "Source": "https://github.com/m3/ai-commit",
    },
)