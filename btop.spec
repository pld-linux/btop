# $Revision$, $Date$
#
# Conditional build:
%bcond_without	gpu		# GPU monitoring support
%bcond_with	rocm_static	# build and link ROCm SMI library statically
#
Summary:	Resource monitor showing usage and stats for processor, memory, disks, network and processes
Summary(pl.UTF-8):	Monitor zasobów pokazujący użycie i statystyki procesora, pamięci, dysków, sieci i procesów
Name:		btop
Version:	1.4.6
Release:	1
License:	Apache v2.0
Group:		Applications/System
Source0:	https://github.com/aristocratos/btop/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6e7c9b1fe7e1894d1e66c5557e1abf62
URL:		https://github.com/aristocratos/btop
BuildRequires:	cmake >= 3.14
BuildRequires:	gcc-c++ >= 11
BuildRequires:	libcap-devel
BuildRequires:	lowdown
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
btop++ is a C++ resource monitor and continuation of bashtop and
bpytop. It shows usage and stats for processor, memory, disks, network
and processes.

Features:
- Easy to use, with a game-inspired menu system
- Full mouse support, click to change sorting, click on graphs for
  details, drag to move and resize boxes
- Fast and responsive UI with customizable update speed
- Function as a full screen application or in a smaller window
- Supports 256-color terminals and true-color themes
- Show and filter processes, send signals and kill processes
- GPU monitoring support (requires libcap or suid bit)

%description -l pl.UTF-8
btop++ to monitor zasobów napisany w C++ i kontynuacja projektów
bashtop i bpytop. Wyświetla użycie i statystyki procesora, pamięci,
dysków, sieci i procesów.

Funkcje:
- Prosty w obsłudze system menu inspirowany grami
- Pełna obsługa myszy: klikanie do zmiany sortowania, klikanie na
  wykresy po szczegóły, przeciąganie w celu przesunięcia i zmiany
  rozmiaru okienek
- Szybki i responsywny interfejs z konfigurowalną szybkością
  odświeżania
- Tryb pełnoekranowy lub okienkowy
- Obsługa terminali 256-kolorowych i motywów true-color
- Wyświetlanie i filtrowanie procesów, wysyłanie sygnałów i
  zabijanie procesów
- Obsługa monitorowania GPU (wymaga libcap lub bitu suid)

%prep
%setup -q

%build
%cmake -B build \
	-G Ninja \
	%{cmake_on_off gpu BTOP_GPU} \
	%{cmake_on_off rocm_static BTOP_RSMI_STATIC} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix}

%{__ninja} -C build %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT %{__ninja} -C build install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE
%attr(755,root,root) %caps(cap_sys_ptrace,cap_net_admin+ep) %{_bindir}/btop
%{_datadir}/applications/btop.desktop
%{_datadir}/icons/hicolor/*/apps/btop.*
%dir %{_datadir}/btop
%dir %{_datadir}/btop/themes
%{_datadir}/btop/themes/*.theme
%{_mandir}/man1/btop.1*
