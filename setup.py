#!/usr/bin/env python
import os.path

import setuptools

import sprockets.mixins.cors


def read_requirements(file_name):
    requirements = []
    try:
        with open(os.path.join('requires', file_name)) as req_file:
            for req_line in req_file:
                req_line = req_line.strip()
                if '#' in req_line:
                    req_line = req_line[0:req_line.find('#')].strip()
                if req_line.startswith('-r'):
                    req_line = req_line[2:].strip()
                    requirements.extend(read_requirements(req_line))
                else:
                    requirements.append(req_line)
    except IOError:
        pass
    return requirements


install_requires = read_requirements('install.txt')
setup_requires = read_requirements('setup.txt')
tests_require = read_requirements('testing.txt')

setuptools.setup(
    name='sprockets.mixins.cors',
    version=sprockets.mixins.cors.__version__,
    description=('Tornado RequestHandler mix-in for implementing '
                 'a CORS enabled endpoint.'),
    long_description='\n'+open('README.rst').read().strip(),
    url='https://github.com/sprockets/sprockets.mixins.cors.git',
    author='AWeber Communications, Inc.',
    author_email='api@aweber.com',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=setuptools.find_packages(),
    namespace_packages=['sprockets', 'sprockets.mixins'],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    zip_safe=True)
