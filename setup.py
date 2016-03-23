import os, sys
try:
        from setuptools import setup, find_packages
        from setuptools.command.install import install as _install

except ImportError:
        from distutils.core import setup

version_py = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),'__init__.py'))
execfile(version_py) # defines __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def _post_install(dir):
#    from subprocess import call
#    call([sys.executable, 'scriptname.py'],
#         cwd=os.path.join(dir, ''))
    print "I'm in _post_Install script", os.path.join(dir, '')

class install(_install):
    def run(self):
        _install.run(self)
        #self.execute(_post_install, (self.install_lib,),msg="Running post install task")

setup(
    name                = "pylxca",
    version             = __version__,
    author              = "Girish Kumar",
    author_email        = "gkumar1@lenovo.com",
    description         = ("It is tool/api to connect LXCA from command line"),
    license             = "LENOVO",
    keywords            = "PYLXCA",
    url                 = "http://packages.python.org/an_example_pypi_project",
    packages            = ['pylxca_api',  'pylxca_cmd'],
    long_description    = read('README'),
    install_requires    = ['logging', 'requests'],
    include_package_data= True,
    scripts             = ['pylxca'],
#    data_files          = [('', ['pylxca_api/pylxca_logger.conf'])],
    classifiers         = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: Lenovo License",
    ],
    cmdclass={'install': install},
)
