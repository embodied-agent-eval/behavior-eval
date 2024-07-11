import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
from setuptools.command.egg_info import egg_info as _egg_info

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

def install_package(package_name, url, version=None):
    if not is_package_installed(package_name, version):
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

def custom_command():
    print("Running custom installation steps...")
    install_package("igibson", "git+https://github.com/embodied-agent-eval/iGibson.git@master#egg=igibson")
    install_package("bddl", "git+https://github.com/embodied-agent-eval/bddl.git@v1.0.2#egg=bddl")

class CustomInstallCommand(_install):
    def run(self):
        _install.run(self)
        custom_command()

class CustomDevelopCommand(_develop):
    def run(self):
        _develop.run(self)
        custom_command()

class CustomEggInfoCommand(_egg_info):
    def run(self):
        _egg_info.run(self)
        custom_command()

setup(
    name='behavior-eval',
    version='1.0.1',
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
        'igibson': ['*.dll', '*.pyd'],
        '': ['*.json', '*.xml', '*.md', '*.yaml'],
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand,
    },
)
