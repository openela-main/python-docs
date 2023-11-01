%if 0%{?fedora}
%bcond_without check_links
%else
# The linkchecker executable isn't available in RHEL8, if it's provided from
# elsewhere, enable this bcond to run tests of links
%bcond_with check_links
%endif

%{!?__python_ver:%global __python_ver 3}

%if "%{__python_ver}" != "EMPTY"
%global main_python 0
%global python python%{__python_ver}
%else
%global main_python 1
%global python python
%endif

%define pybasever 3.6

Summary: Documentation for the Python 3 programming language
Name: python-docs
# The Version needs to be in-sync with the "python" package:
Version: %{pybasever}.7
Release: 2%{?dist}
License: Python
Group: Documentation
URL: https://www.python.org/
BuildArch: noarch


# The upstream tarball includes questionable executable files for Windows,
# which we should not ship even in the SRPM.
# Run the "get-source.sh" with the version as argument to download the upstream
# tarball and generate a version with the .exe files removed. For example:
# $ ./get-source.sh 3.7.0
#   (if there's a newer version of this script in the python3 component, update
#   it here)
Source: Python-%{version}-noexe.tar.xz

# A script to remove .exe files from the source distribution
# The authoritative version of this script is in the python3 component, if it's
# updated there, copy the new version here as well
Source1: get-source.sh


%package -n %{python}-docs
Summary: %{summary}

Recommends: %{python} = %{version}

BuildRequires: %{python}
BuildRequires: %{python}-sphinx
BuildRequires: %{python}-docutils
BuildRequires: %{python}-pygments

%if %{with check_links}
BuildRequires: linkchecker
%endif


%description
The python3-docs package contains documentation on the Python 3
programming language and interpreter.

Install the python3-docs package if you'd like to use the documentation
for the Python 3 language.

%description -n %{python}-docs
The python3-docs package contains documentation on the Python 3
programming language and interpreter.

Install the python3-docs package if you'd like to use the documentation
for the Python 3 language.


%prep
%setup -q -n Python-%{version}

%build
make -C Doc html SPHINXBUILD=sphinx-build-3 PYTHON=%{python}
rm Doc/build/html/.buildinfo

%install
mkdir -p $RPM_BUILD_ROOT

%check
#    NOTICE:
#        The check has been disabled by default because linkchecker isn't
#        available on RHEL8, however you can still do the check manually after
#        rebasing to a new version or enable the check_links bcond.
#
# Verify that all of the local links work (see rhbz#670493 - doesn't apply
# to python3-docs, but only to older python-docs)
#
# (we can't check network links, as we shouldn't be making network connections
# within a build.  Also, don't bother checking the .txt source files; some
# contain example URLs, which don't work)
%if %{with check_links}
linkchecker \
  --ignore-url=^mailto: --ignore-url=^http --ignore-url=^ftp \
  --ignore-url=.txt\$ --no-warnings \
  Doc/build/html/index.html
%endif

%files -n %{python}-docs
%doc Misc/NEWS Misc/HISTORY Misc/README Doc/build/html

%changelog
* Thu Apr 04 2019 Tomas Orsava <torsava@redhat.com> - 3.6.7-2
- Bumping due to problems with modular RPM upgrade path
- Resolves: rhbz#1695587

* Wed Dec 05 2018 Tomas Orsava <torsava@redhat.com> - 3.6.7-1
- Modify for RHEL8
- Update to new Python version
- Resolves: rhbz#1656044

* Thu Apr 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.5-2
- Only recommend the python3 package

* Thu Apr 05 2018 Charalampos Stratakis <cstratak@redhat.com> - 3.6.5-1
- Update to 3.6.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 3.6.4-1
- Update to version 3.6.4

* Mon Oct 09 2017 Charalampos Stratakis <cstratak@redhat.com> - 3.6.3-1
- Update to version 3.6.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Charalampos Stratakis <cstratak@redhat.com> - 3.6.2-1
- Update to version 3.6.2

* Wed Mar 22 2017 Iryna Shcherbina <ishcherb@redhat.com> - 3.6.1-1
- Update to version 3.6.1 final

* Fri Mar 17 2017 Iryna Shcherbina <ishcherb@redhat.com> - 3.6.1-0.1.rc1
- Update to 3.6.1 release candidate 1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Charalampos Stratakis <cstratak@redhat.com> - 3.6.0-1
- Update to current version

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.5.2-2
- Rebuild for Python 3.6

* Mon Aug 22 2016 Tomas Orsava <torsava@redhat.com> - 3.5.2-1
- Update to current version
- Removed use-classic-theme.patch as it was no longer necessary

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Robert Kuska <rkuska@redhat.com> - 3.5.1-1
- Update to current version

* Mon Nov 16 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.5.0-1
- Update to current version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.4.3-1
- Rebuild for Python 3.4.3

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.2-1
- Rebuilt for Python 3.4.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.1-1
- Rebuilt for Python 3.4.1

* Mon Sep 16 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-2
- Patch docs build to use locally installed python3-sphinx.

* Wed Sep 04 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-1
- Initial package, spec adapted from python-docs.
