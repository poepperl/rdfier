from setuptools import find_packages, setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='rdfier',
    packages=find_packages(),
    package_dir={"rdfier": "rdfier"},
    version='1.0.0',
    description='The RDFier takes data in CSV files and builds the appropriate rdf graph.',
    author='Luca Poepperl',
    author_email = "luca.poepperl@gmail.com",
    url = "https://github.com/poepperl/rdfier",
    long_description=read('../README.md'),
)
