Name:             dci-downloader
Version:          0.1.0
Release:          1.VERS%{?dist}
Summary:          DCI downloader
License:          ASL 2.0
URL:              https://github.com/redhat-cip/dci-downloader
BuildArch:        noarch
Source0:          dci-downloader-%{version}.tar.gz

Requires:         podman

Requires(pre): shadow-utils

%description
DCI downloader used to download Red Hat products

%prep
%setup -qc

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 bin/dci-downloader %{buildroot}%{_bindir}/dci-downloader
mkdir -p %{buildroot}%{_sysconfdir}/dci-downloader
install -m 644 dcirc.sh.dist %{buildroot}%{_sysconfdir}/dci-downloader/dcirc.sh.dist
mkdir -p %{buildroot}%{_sharedstatedir}/dci

%clean

%pre

%files
%{_bindir}/dci-downloader
%{_sysconfdir}/dci-downloader/dcirc.sh.dist

%changelog
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
