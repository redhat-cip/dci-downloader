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
install --preserve-timestamps -D --mode=755 bin/dci-downloader %{buildroot}%{_bindir}/dci-downloader
install --preserve-timestamps -D --mode=644 dcirc.sh.dist %{buildroot}%{_sysconfdir}/dci-downloader/dcirc.sh.dist
install --preserve-timestamps -D --mode=440 dci.sudo %{buildroot}%{_sysconfdir}/sudoers.d/dci
install --preserve-timestamps --directory --mode=755 %{buildroot}/%{_sharedstatedir}/dci

%clean

%pre
getent group dci >/dev/null || groupadd --system dci
getent passwd dci >/dev/null || useradd --system --create-home --gid dci --home-dir %{_sharedstatedir}/dci --shell /bin/bash --comment "DCI user" dci
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
