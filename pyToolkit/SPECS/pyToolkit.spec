#------------------------------------------------------------
# Lenovo Copyright
#
# (c) Copyright Lenovo 2016.
#
# LIMITED AND RESTRICTED RIGHTS NOTICE:
# If data or software is delivered pursuant a General Services
# Administration (GSA) contract, use, reproduction, or disclosure
# is subject to restrictions set forth in Contract No. GS-35F-05925.
#-------------------------------------------------------------



#--------------------------
# Metadata
#-------------------------- 
Name:          pytoolkit
Summary:       Python 2.7 Toolkit package
Version:       xxRELEASE_NUMBERxx
Release:       xxBUILD_NUMBERxx
BuildArch:     x86_64
License:       (C) Copyright Lenovo 2016 All Rights Reserved
Group:         Applications/Other
Vendor:        Lenovo
Packager:      LXCA Core Build Service
%description
Python 2.7 toolkit for customer to download from LXCA help menu
+ pylxca-xxRELEASE_NUMBERxx-py2.7.egg

%define _unpackaged_files_terminate_build 0

#--------------------------
# install
#-------------------------- 
%pre
exit 0

%install
exit 0

%post
exit 0

#--------------------------
# uninstall
#-------------------------- 
%preun
exit 0

%postun
# Post uninstall runs AFTER the install of a new upgrade RPM
# so we need to check for the upgrade condition and only run
# when this is not an upgrade.
# $1 == 1 on upgrade
# $1 == 0 on uninstall
#
#if [ $1 -lt 1 ] ; then
#fi
exit 0

#--------------------------
# File list
#-------------------------- 
%files

%attr(644,root,root) /opt/lenovo/lxca/resources/pylxca-xxRELEASE_NUMBERxx-py2.7.egg

