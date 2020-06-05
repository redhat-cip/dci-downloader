%if 0%{?rhel} && 0%{?rhel} < 8
%global with_python2 1
%global __python /usr/bin/python2
%else
%global with_python3 1
%global __python /usr/bin/python3
%endif
%global srcname dci-downloader

Name:             dci-downloader
Version:          2.2.0
Release:          2.VERS%{?dist}
Summary:          DCI Downloader
License:          ASL 2.0
URL:              https://github.com/redhat-cip/%{srcname}
BuildArch:        noarch
Source0:          %{srcname}-%{version}.tar.gz

%if 0%{?with_python2}
BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python-requests
BuildRequires:    python-dciclient
BuildRequires:    PyYAML
Requires:         python-requests
Requires:         python-dciclient
Requires:         PyYAML
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-requests
BuildRequires:  python3-PyYAML
Requires:       python3-PyYAML
Requires:       python3-requests
Requires:       python3-dciclient
%endif

%description
DCI downloader used to download Red Hat products

%prep
%autosetup -n %{srcname}-%{version}

%build
%if 0%{?with_python2}
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python2}
%py2_install
%endif
%if 0%{?with_python3}
%py3_install
%endif

%files
%license LICENSE
%doc README.md
%{python_sitelib}/*
%{_bindir}/%{srcname}

%changelog
* Fri Jun 05 2020 Bill Peck <bpeck@redhat.com> - 2.2.0-2
- Rebuild for RHEL-8
* Wed May 6 2020 Guillaume Vincent <gvincent@redhat.com> - 2.2.0-1
- Rollback Remove EPEL dependency because dciclient doesnt requires
  EPEL anymore
* Fri Mar 27 2020 Guillaume Vincent <gvincent@redhat.com> - 2.1.6-1
- Add missing dciauth
* Fri Mar 27 2020 Guillaume Vincent <gvincent@redhat.com> - 2.1.5-1
- Fix pypi upload issue
* Fri Mar 20 2020 Guillaume Vincent <gvincent@redhat.com> - 2.1.4-1
- Remove EPEL dependency
* Tue Mar 10 2020 Guillaume Vincent <gvincent@redhat.com> - 2.1.3-1
- Fixed disk space check
* Wed Oct 23 2019 Guillaume Vincent <gvincent@redhat.com> - 2.1.2-1
- Explicitly require PyYAML
* Thu Oct 10 2019 Haïkel Guémar <hguemar@redhat.com> - 2.1.1-1
- Fix compatibility with python3
* Tue Oct 03 2019 Guillaume Vincent <gvincent@redhat.com> - 2.1.0-1
- Add multiple topics in settings file
* Mon Sep 16 2019 Guillaume Vincent <gvincent@redhat.com> - 2.0.0-1
- Change the API and simplify dci-downloader
* Mon Jul 29 2019 Guillaume Vincent <gvincent@redhat.com> - 1.0.0-1
- Transform dci-downloader into a rpm
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
