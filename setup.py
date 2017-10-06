import os.path
from setuptools import setup, find_packages

__DIR__ = os.path.abspath(os.path.dirname(__file__))

setup(
    name = 'orccollector',
    version = '0.1.2',
    description = 'Handy OpenTSDB collectors',
    url = 'https://github.com/mikeshultz/opentsdb-remote-collectors',
    author = 'Mike Shultz',
    author_email = 'mike@mikeshultz.com',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords = 'opentsdb monitoring metrics collector',
    packages = find_packages(exclude = ['build', 'dist']),
    install_requires = open("requirements.txt").readlines(),
    entry_points={
        'console_scripts': [
            'orccollector=orccollector.orccollector:main',
        ],
    },
)