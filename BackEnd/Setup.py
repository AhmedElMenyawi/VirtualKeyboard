import sys
from setuptools import setup, find_packages

include_files = ['svm.sav','Dictionary.txt','simTest.txt']
setup(
    name='EOG Virtual Keyboard',
    version='1.0',
    long_description= "",
    packages= find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)