from setuptools import setup, find_packages

setup(
    name="reddit-research-tool",
    version="1.0.0",
    description="Lightweight Reddit API client for research - stdlib only, no pip dependencies",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
