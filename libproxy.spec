%define major	1
%define libname %mklibname proxy %{major}
%define devname %mklibname -d proxy

%bcond_with	bootstrap

Summary:	A library handling all the details of proxy configuration
Name:		libproxy
Version:	0.4.11
Release:	15
Group:		System/Libraries
License:	LGPLv2+
Url:		http://code.google.com/p/libproxy/
# http://code.google.com/p/libproxy/issues/detail?id=130&can=1&q=perl
Source0:	http://%{name}.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		libproxy-0.4.11-add-missing-linkage.patch
Patch1:		libproxy-0.4.11-python3.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(zlib)
# perl
BuildRequires:	perl-devel
%if !%{with bootstrap}
# gnome
BuildRequires:	pkgconfig(gconf-2.0)
# NetworkManager
BuildRequires:	pkgconfig(NetworkManager)
BuildRequires:	pkgconfig(dbus-glib-1)
# webkit (gtk)
BuildRequires:	pkgconfig(webkitgtk-3.0)
# kde
BuildRequires:	kdelibs4-devel
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

%package -n	%{libname}
Group:		System/Libraries
Summary:	A library handling all the details of proxy configuration
Obsoletes:	libproxy-mozjs < 0.4.6-3
Obsoletes:	libproxy-webkit < 0.4.6-3
Provides:	libproxy-pac = %{version}-%{release}

%description -n	%{libname}
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 

%package	utils
Summary:	Binary to test %{name}
Group:		System/Configuration/Networking

%description	utils
The %{name}-utils package contains the proxy binary for %{name}

%package -n	python-%{name}
Summary:	Binding for %{name} and python
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}

%description -n python-%{name}
The python-%{name} package contains the python binding for %{name}

%package	perl
Summary:	Perl bindings for %{name}
Group:		Development/Perl
Requires:	%{libname} = %{version}-%{release}

%description	perl
This contains the perl bindings for the libproxy library.

%if !%{with bootstrap}
%package	gnome
Summary:	Plugin for %{name} and gnome
Group:		System/Libraries

%description	gnome
The %{name}-gnome package contains the %{name} plugin for gnome.

%package	kde
Summary:	Plugin for %{name} and kde
Group:		System/Libraries

%description	kde
The %{name}-kde package contains the %{name} plugin for kde.

%package	networkmanager
Summary:	Plugin for %{name} and networkmanager
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description	networkmanager
The %{name}-networkmanager package contains the %{name} plugin for
networkmanager.

%package        webkit
Summary:        Plugin for %{name} and webkit
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description    webkit
The %{name}-webkit package contains the %{name} plugin for
webkit.

%endif

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%apply_patches

%build
# BIPR=OFF so we dont end up requiring gtk/webkit just for the lib 
%cmake \
	-Dlibexecdir=%{_libexecdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DMODULE_INSTALL_DIR=%{_libdir}/%{name}/%{version}/modules \
	-DBIPR=OFF \
	-DPERL_VENDORINSTALL=1 \
	-DWITH_MOZJS=OFF \
	-DWITH_WEBKIT3=1
%make

%install
%makeinstall_std -C build
#gw fix pkgconfig file
sed -i -e "s^Version:.*^Version: %{version}^" %{buildroot}%{_libdir}/pkgconfig/*.pc

%check
#pushd build
#ctest .
#popd

%files -n %{libname}
%doc AUTHORS README
%{_libdir}/libproxy.so.%{major}*
%if !%{with bootstrap}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules
%endif

%files utils
%{_bindir}/proxy

%files -n python-%{name}
%{python_sitelib}/libproxy.py

%files perl
%{perl_vendorarch}/Net/Libproxy.pm
%{perl_vendorarch}/auto/Net/Libproxy

%if !%{with bootstrap}
%files gnome
%{_libdir}/%{name}/%{version}/modules/config_gnome3.so
%{_libexecdir}/pxgsettings

%files kde
%{_libdir}/%{name}/%{version}/modules/config_kde4.so

%files networkmanager
%{_libdir}/%{name}/%{version}/modules/network_networkmanager.so

%files webkit
%{_libdir}/%{name}/%{version}/modules/pacrunner_webkit.so

%endif

%files -n %{devname}
%{_includedir}/proxy.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%{_datadir}/cmake/Modules/Findlibproxy.cmake

