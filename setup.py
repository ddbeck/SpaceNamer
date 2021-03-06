
from setuptools import setup

setup(
    name='spacenamer',
    version='0.2',
    author='Daniel D. Beck',
    author_email='me@danieldbeck.com',
    packages=['spacenamer'],
    package_data={'spacenamer': ['data/*.json']},
    install_requires=['click', 'tweepy'],
    entry_points={
        'console_scripts': ['publish_spacename = spacenamer.__main__:publish']
    }
)
