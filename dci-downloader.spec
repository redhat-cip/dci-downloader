%global srcname dci-downloader

Name:             dci-downloader
Version:          2.1.3
Release:          1.VERS%{?dist}
Summary:          DCI Downloader
License:          ASL 2.0
URL:              https://github.com/redhat-cip/%{srcname}
BuildArch:        noarch
Source0:          %{srcname}-%{version}.tar.gz

BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python-requests
BuildRequires:    python-dciclient
BuildRequires:    PyYAML
Requires:         python-requests
Requires:         python-dciclient
Requires:         PyYAML

%description
DCI downloader used to download Red Hat products

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build

%install
%py2_install

%files
%license LICENSE
%doc README.md
%{python_sitelib}/*
%{_bindir}/%{srcname}

%changelog
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
