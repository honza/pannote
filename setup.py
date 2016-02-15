from setuptools import setup

long_desc = open('README.md').read()

setup(
    name='pannote',
    version='0.2.0',
    url='https://github.com/honza/pannote',
    install_requires=[
        'click'
    ],
    description='Save notes in markdown and search them',
    long_description=long_desc,
    author='Honza Pokorny',
    author_email='me@honza.ca',
    maintainer='Honza Pokorny',
    maintainer_email='me@honza.ca',
    packages=['pannote'],
    include_package_data=True,
    scripts=['bin/pannote'],
)
