# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


setup(
    name='python-tools',
    version='0.0.1',
    description='Random tools for django.',
    long_description=open('README.md').read(),
    author='Troy Grosfield',
    author_email='troy.grosfield@gmail.com',
    url='https://pl3.projectlocker.com/tbo3champ/python/svn/trunk/django-tools',
    # license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose']
)
