from setuptools import setup, find_packages

setup(
    name="datehelper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    description="A simple Date helper API Python library",
    author="Annie",
    python_requires='>=3.7',
)
