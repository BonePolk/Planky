from setuptools import find_packages, setup

setup(
    name='planky',
    packages=find_packages(include=['Planky']),
    version='0.0.1',
    description='Planky async tcp/tls server implementation',
    author='BonePolk',
    install_requires=[]
)