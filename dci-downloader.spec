%global srcname dci-downloader

Name:             dci-downloader
Version:          2.0.0
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
Requires:         python-requests
Requires:         python-dciclient

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
* Mon Sep 16 2019 Guillaume Vincent <gvincent@redhat.com> - 2.0.0-1
- Change the API and simplify dci-downloader
* Mon Jul 29 2019 Guillaume Vincent <gvincent@redhat.com> - 1.0.0-1
- Transform dci-downloader into a rpm
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
