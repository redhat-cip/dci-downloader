Name:             dci-downloader
Version:          0.1.0
Release:          1.VERS%{?dist}
Summary:          DCI downloader
License:          ASL 2.0
URL:              https://github.com/redhat-cip/dci-downloader
BuildArch:        noarch
Source0:          dci-downloader-%{version}.tar.gz

Requires:         podman

%description
DCI downloader used to download Red Hat products

%prep -a
%autosetup -n %{name}-%{version}

%build

%install
install -p -D -m 644 dcirc.sh.dist %{buildroot}%{_sysconfdir}/dci-downloader/dcirc.sh.dist

%clean

%pre


%files
%{_bindir}/dci-downloader
%{_unitdir}
%{_sysconfdir}/dci-downloader/dcirc.sh.dist

%changelog
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
