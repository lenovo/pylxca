import os, sys

__version__ = '1.0'

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name                = "pylxca",
    version             = __version__,
    author              = "Girish Kumar",
    author_email        = "gkumar1@lenovo.com",
    description         = ("It is tool/api to connect LXCA from command line"),
    license             = "LENOVO",
    keywords            = "PYLXCA",
    url                 = "http://packages.python.org/an_example_pypi_project",
    packages            = ['pylxca','pylxca.pylxca_api','pylxca.pylxca_cmd'],
    long_description    = read('pylxca/README'),
    install_requires    = ['logging', 'requests'],
    include_package_data= True,
    scripts             = ['lxca_shell'],
#    data_files          = [('pylxca_api', ['pylxca/pylxca_api/lxca_logger.conf'])],
    
    classifiers         = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: Lenovo License",
    ],
)
