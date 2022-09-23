from setuptools import setup


setup(
    name='Local search',
    version='1.0.0',
    py_modules=['local_search'],
    install_requires=[
        'numpy',
        'rich',
        'click',
        'pygame',
        'Pillow',
        'mpmath',
        'pytest'
    ],
    entry_points='''
        [console_scripts]
        local_search_solver=local_search.cli.entry_point:entry_point
    '''
)
