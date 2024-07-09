import subprocess
import sys
from setuptools import setup, find_packages

def is_package_installed(package_name, version=None):
    try:
        import pkg_resources
        if version:
            pkg_resources.require(f"{package_name}=={version}")
        else:
            pkg_resources.require(package_name)
        return True
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        return False

def install_package(package_name, url):
    if not is_package_installed(package_name):
        process = subprocess.Popen([sys.executable, "-m", "pip", "install", url],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                sys.stdout.write(output)
                sys.stdout.flush()
        
        # Print any remaining stderr output
        stderr = process.communicate()[1]
        if stderr:
            sys.stderr.write(stderr)
            sys.stderr.flush()

install_package("igibson", "git+https://github.com/embodied-agent-eval/iGibson.git@master#egg=igibson")
install_package("bddl", "git+https://github.com/embodied-agent-eval/bddl.git@v1.0.2#egg=bddl")

setup(
    name='behavior-eval',
    version='1.0.0',
    author='stanford',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/embodied-agent-eval/behavior-eval",
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        "fire",
        "lark",
    ],
    include_package_data=True,
    package_data={
        'igibson': ['*.dll','*.pyd'],
        '': ['*.json', '*.xml', '*.md','*.yaml'],
    },
)
