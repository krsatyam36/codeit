from setuptools import setup, find_packages

setup(
    name="codeit",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn>=0.28.0",
        "click>=8.1.7",
        "pymupdf>=1.23.26",
        "httpx>=0.27.0",
        "nbformat>=5.10.2",
        "jinja2>=3.1.3",
        "python-multipart>=0.0.9",
    ],
    entry_points={
        "console_scripts": [
            "codeit=codeit.cli:main",
        ],
    },
)
