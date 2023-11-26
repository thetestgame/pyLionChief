try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pathlib import Path
repository_directory = Path(__file__).parent
long_description = (repository_directory / "README.md").read_text()

setup(
    name='pyLionChief',
    description="Module for controlling Lionel LionChief series trains",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    version='1.0.0',
    author='Jordan Maxwell',
    maintainer='Jordan Maxwell',
    url='https://github.com/thetestgame/pyLionChief',
    packages=['lionchief'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ])
