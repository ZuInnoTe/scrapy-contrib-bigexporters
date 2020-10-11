"""
Copyright (c) 2020 ZuInnoTe (Jörn Franke) <zuinnote@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from setuptools import setup, find_packages


install_requires = [
    'Scrapy>=2.1.0',
]
extras_require = {
    'parquet': ['fastparquet>=0.4.1'],
    'avro':['fastavro>=1.0.0.post1']
}
test_requires = {
    'scrapy': ['Scrapy>=2.1.0'],
    'parquet': ['fastparquet>=0.4.1'],
    'avro':['fastavro>=1.0.0.post1']
}

setup(
    name = 'scrapy-contrib-bigexporters',
    description = 'Scrapy exporter for Big Data formats',
    long_description=open('README.rst').read(),
    author='Jörn Franke',
    maintainer='ZuInnoTe',
    maintainer_email='zuinnote@gmail.com',
    url = 'https://github.com/zuinnote/scrapy-contrib-bigexporters',
    version='0.1.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
    extras_require=extras_require,
    test_suite="tests",
    packages=find_packages(), #include/exclude arguments take * as wildcard, . for any sub-package names
)
