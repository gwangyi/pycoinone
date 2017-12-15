from setuptools import setup

setup(
    name='pycoinone',
    version='2017.12.05a0.dev2',
    packages=[
        'coinone',
        'coinone.api',
        'coinone.api.common',
        'coinone.api.v1',
        'coinone.api.v2'
    ],
    url='http://github.com/gwangyi/pycoinone',
    license='MIT',
    author='Sungkwang Lee',
    author_email='gwangyi.kr@gmail.com',
    description='Python Coinone API wrapper',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=['requests']
)
