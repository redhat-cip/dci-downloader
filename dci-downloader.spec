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

%prep
%setup -qc

%build

%install
install --preserve-timestamps -D --mode=755 bin/dci-downloader %{buildroot}%{_bindir}/dci-downloader


%clean

%pre

%files
%{_bindir}/dci-downloader


%changelog
* Thu Jun 27 2019 Guillaume Vincent <gvincent@redhat.com> - 0.1.0-1
- Initial release
