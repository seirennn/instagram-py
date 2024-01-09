from setuptools import setup, find_packages
from InstagramPy import __version__

with open('README.rst', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='instagram-py',
    version=__version__,
    description='Slick Instagram brute force command-line tool written in Python.',
    long_description=long_description,
    url='https://github.com/DeathSec/Instagram-Py',
    download_url=f'https://github.com/deathsec/instagram-py/archive/v{__version__}.tar.gz',
    author='DeathSec',
    author_email='antonyjr@protonmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['cli', 'hack', 'instagram', 'password', 'brute force', 'attack'],
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['requests', 'requests[socks]', 'stem'],
    entry_points={
        'console_scripts': [
            'instagram-py=InstagramPy:ExecuteInstagramPy',
        ],
    },
)
#made few changes by seirennn
