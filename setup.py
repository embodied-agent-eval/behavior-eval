# coding:utf-8

from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='behavior-eval',  
    version='1.0',   
    author='stanford',  
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/embodied-agent-eval/behavior-eval",    
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'igibson',
        'bddl',
    ],

)