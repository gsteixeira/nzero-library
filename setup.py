# This file is part of nzero-library
#
#    nzero-library is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nzero-library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nzero-library. If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='nzerolib',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GNU License',
    description='Library to control NearZero Brushless Motor Controller',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/gsteixeira',
    author='Gustavo Selbach Teixeira',
    author_email='gsteixei@gmail.com',
    zip_safe=False,
    classifiers=[],
    install_requires=[
        'pylibi2c @ git+https://github.com/amaork/libi2c',
        ],
    package_data={},
)
