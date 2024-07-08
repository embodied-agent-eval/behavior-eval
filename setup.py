# coding:utf-8

from setuptools import find_packages, setup
import os
import subprocess

def install_dependency_if_missing(repo_url, package_name):
    try:
        __import__(package_name)
    except ImportError:
        subprocess.check_call(["pip", "install", f"git+{repo_url}#egg={package_name}"])

install_dependency_if_missing('https://github.com/embodied-agent-eval/iGibson.git@master', 'igibson')
install_dependency_if_missing('https://github.com/embodied-agent-eval/bddl.git@v1.0.2', 'bddl')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='behavior-eval',
    version='1.0.1',
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
    include_package_data=True,
    package_data={
        'igibson': ['*.dll','*.pyd'],
        '': ['*.json', '*.xml', '*.md'],
    },
)
