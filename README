What is PyLXCA?
---------------
PyLXCA is Python based interface for Lenovo xClarity Administration APIs.

PyLXCA command-line interface (CLI) provides a Python-based library of 
commands to automate provisioning and resource management from an OpenStack 
environment, such as Ansible or Puppet.

The Lenovo XClarity Administrator PYLXCA CLI provide an interface to 
Lenovo XClarity Administrator REST APIs to automate functions such as:
*	Logging in to Lenovo XClarity Administrator
*	Managing and unmanaging chassis, servers, storage systems, and 
    top-of-rack switches (endpoints)
*	Viewing inventory data for endpoints and components
*	Deploying an operating-system image to one or more servers
*	Configuring servers through the use of Configuration Patterns
*	Applying firmware updates to endpoints

Whats New in 2.4.0
------------------
* 	Argument Parsing library replaced from optparse to argparse.
*	Support for subcmd under various commands.
*	New commands supported under shell
		osimages
		managementserver
		resourcegroups
* 	Better Error handling.

Installation
------------
To use the PYLXCA command-line interface (CLI), you must install the 
CLI and start a command session.

Python (including the request and logging modules) is required to use
to the PYLXCA CLI. Ensure at the following requirements are met. For 
more information about Python, see the [Link]www.python.org website. 

*	Python v2.7.x (Later versions have not been tested.)
*	Python requests v2.7.0 or later
*	Python logging v0.4.9.6 or later

Complete the following steps to install the PYLXCA CLI.

1.	Run the following command to install the module:
    pip install pylxca

2.	Start a Python shell session in Command mode.

	$lxca_shell

	--------------------------------------------------
	Welcome to PyLXCA Shell v2.4.0
	Type "help" at any time for a list of commands.
	Type "pyshell" at any time to get interactive python shell
	--------------------------------------------------

	PyLXCA >>

3. 	Start a Python LXCA Shell in Interactive mode.

	
	$lxca_shell --api
	Interactive Python Shell for Lenovo XClarity Administrator v2.4.0
	Type "dir()" or "help(lxca command object)" for more information.
	>>>

4.	Validate that the module was installed correctly by running the following command:

	In Python Shell Try to import pylxca module as follows

	>>> import pylxca

	If python able to import pylxca without any error then it is installed correctly.

	
API Reference
-------------

PyLXCA command reference is available at 
	http://ralfss30.labs.lenovo.com:8120/help/topic/com.lenovo.lxca.doc/pycli_overview.html

PyLXCA API Help can be seen from Interactive Python Shell as follows.
	
	$lxca_shell --api
	Interactive Python Shell for Lenovo XClarity Administrator v2.4.0
	Type "dir()" or "help(lxca command object)" for more information.
	>>>
	>>> help(connect)

Example
------------

	python lxca_shell
	connect -l https://10.241.106.216 -u USERID --noverify
	connect -l https://10.241.106.216 -u USERID

Example to call lxca_cmd python module from python script or Ansible module

	import pylxca
	con1 = connect("https://10.241.106.216","USERID","Passw0rd","True")

Several sample scripts are also available to help you to quickly begin using the PYLXCA command-line interface (CLI) to manage endpoints. 
The sample scripts are location in the following directory:
lib/python2.7/site-packages/pylxca-<version>-py2.7.egg/pylxca\test

License
-------
Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)
