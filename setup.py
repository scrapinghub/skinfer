#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'json-schema-generator >= 0.3'
]

test_requirements = [
    # put package test requirements here
]

setup(
    name='skinfer',
    version='0.1.1',
    description='Simple tool to merge JSON schemas',
    long_description=readme + '\n\n' + history,
    author='Scrapinghub',
    author_email='info@scrapinghub.com',
    url='https://github.com/scrapinghub/skinfer',
    packages=[
        'skinfer',
    ],
    package_dir={'skinfer':
                 'skinfer'},
    scripts=[
        'bin/schema_inferer',
        'bin/json_schema_merger',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='skinfer json-schema json schema inferer merger',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
