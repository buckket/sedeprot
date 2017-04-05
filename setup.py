import ast
import re
import sys

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('sedeprot.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='sedeprot',
    version=version,

    url='https://github.com/buckket/sedeprot',

    author='buckket',
    author_email='buckket@cock.li',

    py_modules=['sedeprot'],
    include_package_data=True,
    zip_safe=False,

    description='A self-enforcing protocol for collaborative decision-making',
    license='GPLv3+',

    platforms='any',

    extras_require={
        'dev': [
            'tox',
            'pytest',
            'pytest-cov',
        ],
    },
)
