#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='skinfer',
    version='0.2.0',
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
        'bin/skinfer',
        'bin/schema_merger',
        'bin/json_validator'
    ],
    include_package_data=True,
    install_requires=[
        'jsonschema >= 0.8.0',
        'json-schema-generator >= 0.3',
    ],
    license="BSD",
    zip_safe=False,
    keywords='skinfer json-schema json schema inferer merger',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
