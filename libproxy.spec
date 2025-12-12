%define major 1
%define libname %mklibname proxy %{major}
%define devname %mklibname -d proxy
%define _disable_lto 1
%define _disable_ld_no_undefined 1
%bcond_with bootstrap

%if %{with bootstrap}
%bcond_with gnome2
%bcond_with gnome3
%bcond_with dotnet
%bcond_with kde
%bcond_with natus
%bcond_with networkmanager
%bcond_with perl
%bcond_with python2
%bcond_with python
%bcond_with vala
%bcond_with webkit1
%bcond_with webkit
%else
%bcond_without gnome2
%bcond_without gnome3
%bcond_with dotnet
%bcond_without kde
%bcond_with natus
%bcond_without networkmanager
%bcond_without perl
%bcond_with python2
%bcond_without python
%bcond_without vala
%bcond_with webkit1
%bcond_with webkit
%endif

Summary:	A library handling all the details of proxy configuration
Name:		libproxy
Version:	0.4.18
Release:	4
Group:		System/Libraries
License:	LGPLv2+
Url:		https://github.com/libproxy/libproxy
Source0:	https://codeload.github.com/libproxy/libproxy/%{name}-%{version}.tar.xz
BuildRequires:	cmake
%if %{with python}
BuildRequires:	pkgconfig(python)
%endif
%if %{with python2}
BuildRequires:	pkgconfig(python2)
%endif
BuildRequires:	pkgconfig(zlib)
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with gnome2} || %{with gnome}
BuildRequires:	pkgconfig(gconf-2.0)
%endif
%if %{with dotnet}
BuildRequires:	pkgconfig(mono-cecil)
%endif
%if %{with natus}
BuildRequires:	pkgconfig(natus)
%endif
%if %{with networkmanager}
BuildRequires:	pkgconfig(libnm)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
%endif
%if %{with webkit1}
BuildRequires:	pkgconfig(webkit-1.0)
%endif
%if %{with webkit}
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(javascriptcoregtk-4.0)
%endif

%description
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 

#---------------------------------------------------------------------------

%package -n %{libname}
Group:		System/Libraries
Summary:	A library handling all the details of proxy configuration
Obsoletes:	%{_lib}proxy-mozjs < %{EVRD}
Obsoletes:	libproxy-webkit < 0.4.6-3
Provides:	libproxy-pac = %{version}-%{release}

%description -n %{libname}
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 

%files -n %{libname}
%{_libdir}/libproxy.so.%{major}*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules

#---------------------------------------------------------------------------

%package utils
Summary:	Binary to test %{name}
Group:		System/Configuration/Networking

%description utils
The %{name}-utils package contains the proxy binary for %{name}.

%files utils
%{_bindir}/proxy

#---------------------------------------------------------------------------

%if %{with python}
%package -n python-%{name}
Summary:	Binding for %{name} and python
Group:		Development/Python
Requires:	%{libname} = %{EVRD}

%description -n python-%{name}
The python-%{name} package contains the python binding for %{name}.

%files -n python-%{name}
%{python_sitelib}/libproxy.py
#{python_sitelib}/__pycache__/*
%endif

#---------------------------------------------------------------------------

%if %{with python2}
%package -n python2-%{name}
Summary:	Binding for %{name} and python 2.x
Group:		Development/Python
Requires:	%{libname} = %{EVRD}

%description -n python2-%{name}
The python2-%{name} package contains the python 2.x binding for %{name}.

%files -n python2-%{name}
%{py2_puresitedir}/libproxy.py*
%endif

#---------------------------------------------------------------------------

%package -n vala-%{name}
Summary:	Binding for %{name} and vala
Group:		Development/Other
Requires:	%{libname} = %{EVRD}

%description -n vala-%{name}
The vala-%{name} package contains the vala binding for %{name}.

%if %{with vala}
%files -n vala-%{name}
%{_datadir}/vala/vapi/libproxy-1.0.vapi
%endif

#---------------------------------------------------------------------------

%if %{with perl}
%package perl
Summary:	Perl bindings for %{name}
Group:		Development/Perl
Requires:	%{libname} = %{EVRD}

%description perl
This contains the perl bindings for the libproxy library.

%files perl
%{perl_vendorarch}/Net/Libproxy.pm
%{perl_vendorarch}/auto/Net/Libproxy
%endif

#---------------------------------------------------------------------------

%if %{with dotnet}
%package dotnet
Summary:	.NET bindings for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}

%description dotnet
This contains the .NET bindings for the libproxy library.

%files dotnet
%{_prefix}/lib/mono/gac/libproxy-sharp
%{_prefix}/lib/mono/libproxy-sharp
%{_libdir}/pkgconfig/libproxy-sharp-1.0.pc
%endif

#---------------------------------------------------------------------------

%if %{with gnome3}
%package gnome
Summary:	Plugin for %{name} and gnome
Group:		System/Libraries

%description gnome
The %{name}-gnome package contains the %{name} plugin for gnome.

%files gnome
%{_libdir}/%{name}/%{version}/modules/config_gnome3.so
%{_libexecdir}/pxgsettings
%endif

#---------------------------------------------------------------------------

%if %{with kde}
%package kde
Summary:	Plugin for %{name} and kde
Group:		System/Libraries
Requires:	kconfig

%description kde
The %{name}-kde package contains the %{name} plugin for kde.

%files kde
%{_libdir}/%{name}/%{version}/modules/config_kde.so
%endif

#---------------------------------------------------------------------------

%if %{with networkmanager}
%package networkmanager
Summary:	Plugin for %{name} and networkmanager
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description networkmanager
The %{name}-networkmanager package contains the %{name} plugin for
networkmanager.

%files networkmanager
%{_libdir}/%{name}/%{version}/modules/network_networkmanager.so
%endif

#---------------------------------------------------------------------------

%if %{with webkit1} || %{with webkit}
%package webkit
Summary:	Plugin for %{name} and webkit
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description webkit
The %{name}-webkit package contains the %{name} plugin for
webkit.

%files webkit
%{_libdir}/%{name}/%{version}/modules/pacrunner_webkit.so
%endif

#---------------------------------------------------------------------------

%package pacrunner
Summary:	Plugin for %{name} and PacRunner
Requires:	%{libname} = %{EVRD}

%description pacrunner
The %{name}-pacrunner package contains the %{name} plugin for
PacRunner.

%files pacrunner
%{_libdir}/%{name}/%{version}/modules/config_pacrunner.so

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files -n %{devname}
%doc AUTHORS README
%{_includedir}/proxy.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%{_datadir}/cmake/Modules/Findlibproxy.cmake

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# BIPR=OFF so we dont end up requiring gtk/webkit just for the lib
%cmake \
	-Dlibexecdir=%{_libexecdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DMODULE_INSTALL_DIR=%{_libdir}/%{name}/%{version}/modules \
	-DBIPR=OFF \
	-DWITH_PERL:BOOL=%{with perl} \
%if %{with perl}
	-DPERL_VENDORINSTALL=1 \
	-DPERL_LINK_LIBPERL=1 \
%endif
%if %{with python2}
	-DPYTHON2_EXECUTABLE:FILEPATH=%{_bindir}/python2 \
%endif
	-DWITH_GNOME2:BOOL=%{with gnome2} \
	-DWITH_GNOME3:BOOL=%{with gnome3} \
	-DWITH_KDE:BOOL=%{with kde} \
	-DWITH_DOTNET:BOOL=%{with dotnet} \
	-DWITH_PYTHON2:BOOL=%{with python2} \
	-DWITH_PYTHON3:BOOL=%{with python} \
	-DWITH_VALA:BOOL=%{with vala} \
	-DWITH_MOZJS:BOOL=OFF \
	-DWITH_WEBKIT:BOOL=%{with webkit1} \
	-DWITH_WEBKIT3:BOOL=%{with webkit} \
	-DWITH_NATUS:BOOL=%{with natus} \
	-DWITH_NM:BOOL=%{with networkmanager}

%build
%make_build -C build

%install
%make_install -C build

#gw fix pkgconfig file
sed -i -e "s^Version:.*^Version: %{version}^" %{buildroot}%{_libdir}/pkgconfig/*.pc

%check
#cd build
#ctest .
#cd -

