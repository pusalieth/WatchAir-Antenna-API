from setuptools import setup

setup(
    name='WatchAir-Antenna-API',
    version='1.0',
    description='Web API for WatchAir Antenna',
    author='Jake Pring',
    author_email='jakepring@linux.com',
    packages=['WatchAir-Antenna-API'],
    install_requires=['xmltodict', 'requests'],
)
