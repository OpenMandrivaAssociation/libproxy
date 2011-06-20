%define major 1
%define libname %mklibname proxy %major
%define modmanmajor 1
%define libnamemodman %mklibname modman %modmanmajor
%define develname %mklibname -d proxy

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

Name:           libproxy
Version:        0.4.6
Release:        %mkrel 5
Summary:        A library handling all the details of proxy configuration

Group:          System/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libproxy/
# http://code.google.com/p/libproxy/issues/detail?id=130&can=1&q=perl
Source0:        http://%name.googlecode.com/files/%name-%version.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  cmake
BuildRequires:  python-devel
BuildRequires:	zlib-devel
# perl
BuildRequires:  perl-devel
%if !%bootstrap
# gnome
BuildRequires:  libGConf2-devel
# NetworkManager
BuildRequires:  NetworkManager-devel
BuildRequires:  dbus-glib-devel
# webkit (gtk)
BuildRequires:	webkitgtk-devel
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

%package -n %libname
Group:System/Libraries
Summary:        A library handling all the details of proxy configuration
Obsoletes: libproxy-mozjs < 0.4.6-3
Obsoletes: libproxy-webkit < 0.4.6-3
Provides: libproxy-pac = %{version}-%{release}

%description -n %libname
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 

%package -n %libnamemodman
Group:System/Libraries
Summary:        A library handling all the details of proxy configuration

%description -n %libnamemodman
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 

%package        utils
Summary:        Binary to test %{name}
Group:          System/Configuration/Networking
Requires:       %{libname} = %{version}-%{release}

%description    utils
The %{name}-utils package contains the proxy binary for %{name}

%package -n python-%name
Summary:        Binding for %{name} and python
Group:          Development/Python
Requires:       %{libname} = %{version}-%{release}

%description -n python-%name
The python-%{name} package contains the python binding for %{name}

%package        perl
Summary:        Perl bindings for %{name}
Group:          Development/Perl
Requires:       %{libname} = %{version}-%{release}

%description    perl
This contains the perl bindings for the libproxy library.

%if !%bootstrap
%package        gnome
Summary:        Plugin for %{name} and gnome
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description    gnome
The %{name}-gnome package contains the %{name} plugin for gnome.

%package        kde
Summary:        Plugin for %{name} and kde
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description    kde
The %{name}-kde package contains the %{name} plugin for kde.

%package	networkmanager
Summary:	Plugin for %{name} and networkmanager
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description	networkmanager
The %{name}-networkmanager package contains the %{name} plugin for networkmanager.
%endif

%package -n %develname
Summary:        Development files for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Requires:       %{libnamemodman} = %{version}-%{release}
Provides:	%name-devel = %version-%release

%description -n %develname
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%cmake -Dlibexecdir=%_libexecdir -DLIBEXEC_INSTALL_DIR=%_libexecdir \
	-DMODULE_INSTALL_DIR=%_libdir/%name/%version/modules \
	-DPERL_VENDORINSTALL=1 -DWITH_MOZJS=OFF
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std -C build
#gw fix pkgconfig file
sed -i -e "s^Version:.*^Version: %version^" %buildroot%_libdir/pkgconfig/*.pc

%clean
rm -rf $RPM_BUILD_ROOT

%check
pushd build
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/libmodman ctest .
popd

%files -n %libname
%defattr(-,root,root,-)
%doc AUTHORS README
%{_libdir}/libproxy.so.%{major}*
%if !%bootstrap
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules
%endif

%files -n %libnamemodman
%defattr(-,root,root,-)
%{_libdir}/libmodman.so.%{modmanmajor}*

%files utils
%defattr(-,root,root,-)
%{_bindir}/proxy

%files -n python-%name
%defattr(-,root,root,-)
%{py_platsitedir}/*

%files perl
%defattr(-,root,root,-)
%perl_vendorarch/Net/Libproxy.pm
%perl_vendorarch/auto/Net/Libproxy

%if !%bootstrap
%files gnome
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_gnome.so
%_libexecdir/pxgconf

%files kde
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_kde4.so

%files networkmanager
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/network_networkmanager.so
%endif

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/proxy.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%_datadir/cmake/Modules/Findlibproxy.cmake
