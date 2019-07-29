Name:             dci-downloader
Version:          1.0.0
Release:          1.VERS%{?dist}
Summary:          DCI downloader
License:          ASL 2.0
URL:              https://github.com/redhat-cip/dci-downloader
BuildArch:        noarch
Source0:          dci-downloader-%{version}.tar.gz

BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python-requests
BuildRequires:    python-dciclient
Requires:         python-requests
Requires:         python-dciclient

%{?python_provide:%python_provide dci-downloader}

%description
DCI downloader used to download Red Hat products

%prep
%autosetup -n dci-downloader-%{version}

%build
%py2_build

%install
%py2_install

%files
%license LICENSE
%doc README.md
%{python2_sitelib}/*.egg-info
%dir %{python2_sitelib}/dci_downloader
%{python2_sitelib}/dci_downloader/*
%{_bindir}/dci-downloader

%changelog
* Mon Jun 29 2019 Guillaume Vincent <gvincent@redhat.com> - 1.0.0-1
- Transform dci-downloader into a rpm
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
