# Fix for older setuptools
import re
import os

from setuptools import setup, find_packages


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    info = read('README.rst')
    try:
        return info + '\n\n' + read('doc/changelog.rst')
    except IOError:
        return info


# grep stargate/__init__.py since python 3.x cannot import it before using 2to3
file_text = read(fpath('stargate/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


install_requires = [
    'Flask>=0.9',
    'PyJWT==1.6.4',
    'bcrypt==3.1.4',
    'pydash==4.7.0'
]

setup(
    name='Stargate',
    version=grep('__version__'),
    url='https://github.com/msyaifullah/stargate/',
    license='MIT',
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='Simple and extensible authentication library',
    long_description=desc(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    tests_require=[
        'nose>=1.0',
        # 'coverage==4.5.1',
        'mock==2.0.0'
    ],
    classifiers=[
        'Development Status :: ' + grep('__version__') + ' - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='nose.collector'
)
