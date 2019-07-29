%global description DCI downloader used to download Red Hat products
%if 0%{?fedora}
%{!?python3_pkgversion: %global python3_pkgversion 3}
%else
%{!?python3_pkgversion: %global python3_pkgversion 34}
%endif

Name:             dci-downloader
Version:          1.0.0
Release:          1.VERS%{?dist}
Summary:          DCI downloader
License:          ASL 2.0
URL:              https://github.com/redhat-cip/dci-downloader
Source0:          dci-downloader-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python%{python3_pkgversion}-devel
BuildRequires:    python%{python3_pkgversion}-setuptools
BuildRequires:    python-requests
BuildRequires:    python-dciclient
Requires:         python-requests
Requires:         python-dciclient

%description
%{description}

%package -n python2-dcidownloader
Summary: %{description}
%{?python_provide:%python_provide python2-dcidownloader}

%description -n python2-dcidownloader
%{description}

%package -n python%{python3_pkgversion}-dcidownloader
Summary: %{description}
%{?python_provide:%python_provide python%{python3_pkgversion}-dcidownloader}

%description -n python%{python3_pkgversion}-dcidownloader
%{description}

%package -n dci-downloader
Summary: %{description}
%{?python_provide:%python_provide dci-downloader}

%description -n dci-downloader
%{description}

%prep
%autosetup -n dci-downloader-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%clean

%pre

%files -n python2-dcidownloader
%license LICENSE
%doc README.md
%{python2_sitelib}/*.egg-info
%dir %{python2_sitelib}/dcidownloader
%{python2_sitelib}/dcidownloader/*

%files -n python%{python3_pkgversion}-dcidownloader
%license LICENSE
%doc README.md
%{python3_sitelib}/*.egg-info
%dir %{python3_sitelib}/dcidownloader
%{python3_sitelib}/dcidownloader/*

%files -n dci-downloader
%license LICENSE
%doc README.md
%{python3_sitelib}/*.egg-info
%dir %{python3_sitelib}/dcidownloader
%{python3_sitelib}/dcidownloader/*

%changelog
* Mon Jun 29 2019 Guillaume Vincent <gvincent@redhat.com> - 1.0.0-1
- Transform dci-downloader into a rpm
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
