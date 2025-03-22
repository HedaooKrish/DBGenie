from setuptools import setup, find_packages

setup(
    name='sql-er-diagram-generator',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'sqlparse',
        'graphviz',
        'pydot'
    ],
    entry_points={
        'console_scripts': [
            'sql-er-diagram-generator=src.main:main',
        ],
    },
)