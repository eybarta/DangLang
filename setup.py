from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="danglang",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A LangChain-based pipeline for orchestrating multiple AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/DangLang",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "langchain-core>=0.1.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "pylint>=3.0.0",
        "pytest>=7.4.0",
        "aiohttp>=3.9.0",
        "pydantic>=2.5.0",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "mypy",
            "pytest-cov",
            "pytest-asyncio",
        ]
    }
)