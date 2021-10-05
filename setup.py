from setuptools import setup

setup(
    name='Genetic algorithms',
    version='1.0.0',
    install_requires=[
        'numpy',
        'rich',
        'click',
        'pygame',
        'Pillow'
    ],
    entry_points='''
        [console_scripts]
        genetic_algortihms=genetic_algorithms.cli.entry_point:entry_point
    '''
)
