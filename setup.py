import os
from pip.req import parse_requirements
from setuptools import setup
from rememberthematch import __version__ as version

here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements(os.path.join(here, "requirements.txt"))
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='rememberthematch',
    version=version,
    url='',
    license='',
    author='Michal Michalski',
    author_email='michal@michalski.im',
    description='A tool that will help you to remember about important matches',
    keywords='',
    packages=['rememberthematch'],
    install_requires=reqs,
    scripts=['bin/rtm'],
    test_suite = 'nose.collector',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
    ]
)