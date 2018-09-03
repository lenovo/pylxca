'''
@since: 15 Jan 2016
@author: Girish Kumar <gkumar1@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo
@summary: Setup Script for PYLXCA
'''
import os, sys, re
from codecs import open

try:
    from setuptools import setup, find_packages
except ImportError:
    print ("setuptools is needed to run this file")
    print ("Try -- 'sudo pip install setuptools'")
    print ("Exiting ..")
    sys.exit(1)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('pylxca/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

if sys.version_info[:1] == (2,):
    setup(
        name                = "pylxca",
        version             = version,
        author              = "Girish Kumar, Prashant Bhosle",
        author_email        = "gkumar1@lenovo.com, pbhosle@lenovo.com",
        description         = ("It is tool/api to connect LXCA from command line"),
        license             = "LENOVO",
        keywords            = "PYLXCA",
        url                 = "http://www.lenovo.com",
        packages            = ['pylxca','pylxca.pylxca_api','pylxca.pylxca_cmd'],
        long_description    = read('README'),
        install_requires    = ['requests>=2.7.0', 'requests-toolbelt>=0.8.0',
            'mock>=2.0.0'],
        include_package_data= True,
        scripts             = ['lxca_shell'],
        #    data_files          = [('pylxca_api', ['pylxca/pylxca_api/lxca_logger.conf'])],
        classifiers         = [
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "License :: Apache License 2.0 ",
        ],
    )
else:
    setup(
        name="pylxca",
        version=version,
        author="Girish Kumar, Prashant Bhosle",
        author_email="gkumar1@lenovo.com, pbhosle@lenovo.com",
        description=("It is tool/api to connect LXCA from command line"),
        license="LENOVO",
        keywords="PYLXCA",
        url="http://www.lenovo.com",
        packages=['pylxca', 'pylxca.pylxca_api', 'pylxca.pylxca_cmd'],
        long_description=read('README'),
        install_requires=['requests>=2.7.0', 'requests-toolbelt>=0.8.0', 'unittest2'],
        include_package_data=True,
        scripts=['lxca_shell'],
        #    data_files          = [('pylxca_api', ['pylxca/pylxca_api/lxca_logger.conf'])],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "License :: Apache License 2.0",
        ],
    )
