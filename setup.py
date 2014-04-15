from time import time
from setuptools import setup, find_packages

setup(
    name='flask_chutes',
    version='1.0.0-%s' % int(time()),
    description='Flask Chutes SocketIO Messaging Mixin',
    long_description=open('README.md').read(),
    license='MIT',
    author='Adi Foulger',
    author_email='technobabelfish@gmail.com',
    zip_safe=False,
    packages=find_packages(),
    package_data={
        '': ['*.csv', '*.pem', '*.txt']
    },
    platforms='any',
)
