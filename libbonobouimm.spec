#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	A C++ interface for the libbonoboui
Summary(pl.UTF-8):	Interfejs C++ dla libbonoboui
Name:		libbonobouimm
Version:	1.3.7
Release:	5
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbonobouimm/1.3/%{name}-%{version}.tar.bz2
# Source0-md5:	d563938439ea59004f2bb54ad33e6d5b
Patch0:		%{name}-gtkmm24.patch
Patch1:		%{name}-uidir.patch
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtkmm-devel >= 2.4.0
BuildRequires:	libbonobomm-devel >= 1.3.8-2
BuildRequires:	libbonoboui-devel >= 2.4.0
BuildRequires:	libsigc++-devel >= 1:2.0.1
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	perl-base >= 5.6
BuildRequires:	pkgconfig
Requires:	cpp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a C++ interface for libbonoboui library.

%description -l pl.UTF-8
Ten pakiet dostarcza interfejs C++ dla biblioteki libbonoboui.

%package devel
Summary:	Header files for libbonobouimm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbonobouimm
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtkmm-devel >= 2.4.0
Requires:	libbonobomm-devel >= 1.3.8-2
Requires:	libbonoboui-devel >= 2.4.0

%description devel
Header files for libbonobouimm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbonobouimm.

%package static
Summary:	libbonobouimm static libraries
Summary(pl.UTF-8):	Biblioteki statyczne libbonobouimm
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libbonobouimm static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne libbonobouimm.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# force regeneration for libsigc++-2.0
rm -f bonobomm/servers/{control*,wrap_init.cc}
rm -f bonobomm/servers/private/control*
rm -f bonobomm/widgets/{dock*,selector*,wi*,wrap_init.cc}
rm -f bonobomm/widgets/private/{dock*,selector*,wi*}

%build
# exceptions and rtti are used in this package --misiek
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__automake}
%configure \
	--enable-maintainer-mode \
	--enable-static \
	%{!?with_static_libs:--disable-static}
# examples/creating_control/Makefile.am contains hardcoded "$(prefix)/lib/bonobo-2.0"
%{__make} \
	samplesdir=%{_libdir}/bonobo-2.0/samples

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir} \
	samplesdir=%{_libdir}/bonobo-2.0/samples

cp -dpr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS NEWS
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/bonobo-2.0/samples/*
%{_libdir}/bonobo/servers/*
%{_datadir}/gnome-2.0/ui/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/libbonobouimm-*
%{_libdir}/glibmm-*/proc/m4/*
%{_includedir}/libbonobouimm-2.0
%{_pkgconfigdir}/*.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
