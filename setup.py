from setuptools import setup, find_packages

setup(
    name="picobot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "openai",
        "anthropic",
        "python-dotenv",
        "pydantic",
        "pytest",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "rich",
        "httpx",
        "tqdm",
        "tabulate",
        "seaborn>=0.12.0",
    ],
) 