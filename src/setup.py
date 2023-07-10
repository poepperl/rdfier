from setuptools import find_packages, setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='unco',
    packages=find_packages(),
    package_dir={"unco": "unco"},
    version='0.2.0',
    description='The Uncertainty Comparator compares diffrent models of uncertain rdf data.',
    author='Luca Poepperl',
    author_email = "luca.poepperl@gmail.com",
    url = "https://github.com/UncertaintyC/unco",
    long_description=read('../README.md'),
)
