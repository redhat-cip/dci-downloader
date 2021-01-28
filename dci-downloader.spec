%if 0%{?rhel} && 0%{?rhel} < 8
%global with_python2 1
%else
%global with_python3 1
%endif
%global srcname dci-downloader

Name:             dci-downloader
Version:          2.7.0
Release:          1.VERS%{?dist}
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
%if 0%{?with_python2}
%{python2_sitelib}/*
%else
%{python3_sitelib}/*
%endif
%{_bindir}/%{srcname}

%changelog
* Fri Jan 29 2021 Guillaume Vincent <gvincent@redhat.com> - 2.7.0-1
- Allow debug flag without a variant
* Fri Jan 29 2021 Guillaume Vincent <gvincent@redhat.com> - 2.6.1-1
- Decode compressed responses when we download a file
* Tue Dec 15 2020 Jorge A Gallegos <jgallego@redhat.com> - 2.6.0-1
- Add support for multiple setting files
* Tue Nov 03 2020 Guillaume Vincent <gvincent@redhat.com> - 2.5.0-1
- Check DCI repo is accessible on startup
* Tue Nov 03 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.6-1
- Clean cache folder with filtered files list
* Wed Oct 14 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.5-1
- Filter files only for composes
* Mon Sep 08 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.4-1
- Improve locking mechanism
- Improve Pool Executor closing
* Thu Sep 03 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.3-1
- Change open mode for file lock to w+
* Thu Sep 03 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.2-1
- Create topic folder if doesn't exists
* Wed Sep 02 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.1-1
- Add a file lock per topic to avoid race condition during the download
* Tue Aug 25 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.0-1
- Stop refreshing SSL certificates
* Thu Jul 30 2020 Guillaume Vincent <gvincent@redhat.com> - 2.3.1-1
- Fix bad exception raised
* Mon Jun 22 2020 Guillaume Vincent <gvincent@redhat.com> - 2.3.0-1
- Introduce parallel downloads to increase download speed
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
