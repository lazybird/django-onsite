from setuptools import setup, find_packages

import onsite


setup(
    name='django-onsite',
    version=onsite.__version__,
    description=onsite.__doc__,
    packages=find_packages(),
    url='http://github.com/lazybird/django-onsite/',
    author='lazybird',
    long_description=open('README.md').read(),
    include_package_data=True,
    license='Creative Commons Attribution 3.0 Unported',
)
