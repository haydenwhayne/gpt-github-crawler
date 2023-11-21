from setuptools import setup, find_packages

setup(
    name='gpt-github-crawler',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gpt-github-crawler=src.main:main',
        ],
    },
    # Add other setup parameters as needed
)
