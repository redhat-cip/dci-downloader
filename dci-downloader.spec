%global summary DCI downloader used to download Red Hat products
%global srcname dci-downloader

Name:             %{srcname}
Version:          3.2.0
Release:          2.VERS%{?dist}
Summary:          %{summary}

License:          ASL 2.0
URL:              https://github.com/redhat-cip/%{srcname}
Source0:          %{srcname}-%{version}.postDATE.tar.gz

BuildArch:        noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?rhel} < 8
BuildRequires:  python36-requests
Requires:       python36-requests
%else
BuildRequires:  python3-requests
Requires:       python3-requests
%endif
BuildRequires:  python3-PyYAML
Requires:       python3-PyYAML
Requires:       python3-dciclient
Requires:       skopeo >= 0.1.41

%description
%{summary}

%prep
%autosetup -n %{srcname}-%{version}.postDATE

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/*
%{_bindir}/%{srcname}

%changelog
* Wed Nov 15 2023 Haïkel Guémar <hguemar@redhat.com> - 3.2.0-2
- use the new build process compatible with PEP-0440
* Tue May 23 2023 Guillaume Vincent <gvincent@redhat.com> - 3.2.0-1
- Added parallel download
* Thu Feb 09 2023 Guillaume Vincent <gvincent@redhat.com> - 3.1.0-1
- Download component on s3 if available
- Build only for python3
* Tue Jan 10 2023 Guillaume Vincent <gvincent@redhat.com> 3.0.0-1
- Build also python3-dci-downloader on EL7
* Tue Jul 05 2022 Guillaume Vincent <fcharlie@redhat.com> - 2.9.0-1
- Make dci repo url configurable
* Wed Apr 14 2021 François Charlier <fcharlie@redhat.com> - 2.8.0-2
- Fix a problem with container images mirrorring trigerred even if no registry
  was specified
* Mon Mar 22 2021 François Charlier <fcharlie@redhat.com> - 2.8.0-1
- Add container images mirroring for supported topics
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
* Tue Sep 08 2020 Guillaume Vincent <gvincent@redhat.com> - 2.4.4-1
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
* Thu Oct 03 2019 Guillaume Vincent <gvincent@redhat.com> - 2.1.0-1
- Add multiple topics in settings file
* Mon Sep 16 2019 Guillaume Vincent <gvincent@redhat.com> - 2.0.0-1
- Change the API and simplify dci-downloader
* Mon Jul 29 2019 Guillaume Vincent <gvincent@redhat.com> - 1.0.0-1
- Transform dci-downloader into a rpm
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
