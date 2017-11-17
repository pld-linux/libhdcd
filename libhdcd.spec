#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library for High Definition Compatible Digital (HDCD) decoding and analysis
Summary(pl.UTF-8):	Biblioteka do dekodowania i analizy HDCD (High Definition Compatible Digital)
Name:		libhdcd
Version:	1.3
Release:	1
License:	BSD (library), Apache v2.0 (hdcd-detect tool)
Group:		Libraries
#Source0Download: https://github.com/bp0/libhdcd/releases
Source0:	https://github.com/bp0/libhdcd/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f9d93bedd53ceae27db98968a493ec22
URL:		https://github.com/bp0/libhdcd
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1.6
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libtool >= 2:2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A stand-alone library for High Definition Compatible Digital (HDCD)
decoding and analysis based on foo_hdcd and ffmpeg's af_hdcd.

Features:
- HDCD decoding
- Optional HDCD detection code
- Optional Analyze mode
- Optional logging callback interface

%description -l pl.UTF-8
Samodzielna biblioteka do dekodowania i analizy HDCD (High Definition
Compatible Digital) oparta na foo_hdcd i af_hdcd z ffmpega.

Możliwości:
- dekodowanie HDCD
- opcjonalny kod wykrywający HDCD
- opcjonalny tryb analizy
- opcjonalny interfejs wywołań wstecznych do logowania

%package devel
Summary:	Header files for HDCD library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HDCD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for HDCD library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HDCD.

%package static
Summary:	Static HDCD library
Summary(pl.UTF-8):	Statyczna biblioteka HDCD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HDCD library.

%description static -l pl.UTF-8
Statyczna biblioteka HDCD.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhdcd.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{_bindir}/hdcd-detect
%attr(755,root,root) %{_libdir}/libhdcd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhdcd.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhdcd.so
%{_includedir}/hdcd
%{_pkgconfigdir}/libhdcd.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libhdcd.a
%endif
