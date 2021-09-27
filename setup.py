from setuptools import setup

setup(
    name='Genetic algorithms',
    version='1.0.0',
    install_requires=[
        'numpy',
        'rich',
        'click',
        'pygame',
    ],
    entry_points='''
        [console_scripts]
        genetic_algortihms=genetic_algorithms.main:cli
    '''
)
