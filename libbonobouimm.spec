Summary:	A C++ interface for the libbonoboui
Summary(pl):	Interfejs C++ dla libbonoboui
Name:		libbonobouimm
Version:	1.3.6
Release:	2
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/1.3/%{name}-%{version}.tar.bz2
# Source0-md5:	ce0b37b6a92d6b9607575acae2f07af2
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	ORBit2-devel >= 2.7.6
BuildRequires:	autoconf
BuildRequires:	gtkmm-devel >= 2.2.7
BuildRequires:	libbonobomm-devel >= 1.3.7
BuildRequires:	libbonoboui-devel >= 2.3.6
BuildRequires:	orbitcpp-devel >= 1.3.7
BuildRequires:	perl >= 5.6
Requires:	cpp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a C++ interface for libbonoboui library.

%description -l pl
Ten pakiet dostarcza interfejs C++ dla biblioteki libbonoboui.

%package devel
Summary:	libbonobouimm header files, development documentation
Summary(pl):	Pliki nagłówkowe libbonobouimm, dokumentacja dla programistów
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for libbonobouimm library.

%description devel -l pl
Pliki nagłówkowe i dokumentacja dla programistów dla biblioteki
libbonobouimm.

%package static
Summary:	libbonobouimm static libraries
Summary(pl):	Biblioteki statyczne libbonobouimm
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
libbonobouimm static libraries.

%description static -l pl
Biblioteki statyczne libbonobouimm.

%prep
%setup -q

%build
# exceptions and rtti are used in this package --misiek
%configure \
	--enable-static=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

cp -dpr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/bonobo-2.0/samples/*
%{_libdir}/bonobo/servers/*
%{_datadir}/gnome/ui/*

%files devel
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS NEWS
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%dir %{_libdir}/libbonobouimm-*
%{_libdir}/libbonobouimm-*/include
%{_libdir}/gtkmm-*/proc/m4/*

%{_includedir}/libbonobouimm-2.0
%{_pkgconfigdir}/*.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
