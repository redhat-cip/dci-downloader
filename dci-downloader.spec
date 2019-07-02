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
install -p -D -m 644 bin/dci-downloader %{buildroot}%{_bindir}/dci-downloader
install -p -D -m 644 dcirc.sh.dist %{buildroot}%{_sysconfdir}/dci-downloader/dcirc.sh.dist
install -p -D -m 440 dci.sudo %{buildroot}%{_sysconfdir}/sudoers.d/dci
install -p -d -m 755 %{buildroot}/%{_sharedstatedir}/dci

%clean

%pre
getent group dci >/dev/null || groupadd -r dci
getent passwd dci >/dev/null || useradd -r -m -g dci -d %{_sharedstatedir}/dci -s /bin/bash -c "DCI user" dci
exit 0

%files
%{_bindir}/dci-downloader
%{_sysconfdir}/dci-downloader/dcirc.sh.dist
%dir %{_sharedstatedir}/dci
%attr(0755, dci, dci) %{_sharedstatedir}/dci
%{_sysconfdir}/sudoers.d/dci


%changelog
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
