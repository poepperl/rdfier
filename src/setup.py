from setuptools import find_packages, setup

setup(
    name='unco',
    packages=find_packages(where='stosrc'),
    package_dir={"unco": "unco"},
    version='0.1.0',
    description='Uncertanty Coparator',
    author='Luca Pöpperl',
    license='',
)
