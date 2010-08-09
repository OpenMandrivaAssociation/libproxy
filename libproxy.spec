%define gecko_version 1.9

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

%define major 1
%define libname %mklibname proxy %major
%define modmanmajor 0
%define libnamemodman %mklibname modman %modmanmajor
%define develname %mklibname -d proxy
Name:           libproxy
Version:        0.4.4
Release:        %mkrel 3
Summary:        A library handling all the details of proxy configuration

Group:          System/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libproxy/
# http://code.google.com/p/libproxy/issues/detail?id=130&can=1&q=perl
Source0:        http://%name.googlecode.com/files/%name-%version.tar.gz
Patch0: libproxy-r698-fix-modman-build.patch
Patch1: libproxy-r706-fix-pkgconfig-generation.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  cmake
BuildRequires:  python-devel
#perl
BuildRequires:  perl-devel
# gnome
BuildRequires:  libGConf2-devel
# mozjs
BuildRequires:  xulrunner-devel >= %{gecko_version}
# NetworkManager
#gw disabled, it is in contrib
#BuildRequires:  NetworkManager-devel
BuildRequires:  dbus-glib-devel
# webkit (gtk)
%if !%bootstrap
BuildRequires:  webkitgtk-devel
%endif
# kde
BuildRequires:	kdelibs4-devel
BuildRequires:  libxmu-devel


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
#Virtual Provides - We need either mozjs or WebKit
%if !%bootstrap
Requires: %{name}-pac >= %{version}
%endif
#

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

%package        mozjs
Summary:        Plugin for %{name} and mozjs
Group:          System/Libraries
Requires:       %{libname} = %{version}
#Tweak this according to the current gecko-libs version
Requires:       libxulrunner >= %{gecko_version}
Provides:       %{name}-pac = %{version}-%{release}

%description    mozjs
The %{name}-mozjs package contains the %{name} plugin for mozjs.

%if !%bootstrap
%package        webkit
Summary:        Plugin for %{name} and webkit
Group:          System/Libraries
Requires:       %{libname} = %{version}
Provides:       %{name}-pac = %{version}-%{release}

%description    webkit
The %{name}-webkit package contains the %{name} plugin for
webkit.
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
%patch0 -p0
%patch1 -p0

%build
%if %bootstrap
export CC="gcc -L$(pkg-config --variable sdkdir libxul)/lib"
%endif
%cmake -Dlibexecdir=%_libexecdir -DLIBEXEC_INSTALL_DIR=%_libexecdir \
-DMODULE_INSTALL_DIR=%_libdir/%name/%version/modules \
-DPERL_VENDORINSTALL=1
%make

%install
rm -rf $RPM_BUILD_ROOT
cd build
%makeinstall_std
rm -f %buildroot%_libdir/libproxy/%version/modules/network_networkmanager.so
#gw fix pkgconfig file
sed -i -e "s^Version:.*^Version: %version^" %buildroot%_libdir/pkgconfig/*.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %libname
%defattr(-,root,root,-)
%doc AUTHORS README
%{_libdir}/libproxy.so.%{major}*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules

%files -n %libnamemodman
%defattr(-,root,root,-)
%{_libdir}/libmodman.so.%{modmanmajor}*


%files utils
%defattr(-,root,root,-)
%{_bindir}/proxy

%files -n python-%name
%defattr(-,root,root,-)
%{py_puresitedir}/*

%files perl
%defattr(-,root,root,-)
%perl_vendorarch/Net/Libproxy.pm
%perl_vendorarch/auto/Net/Libproxy

%files gnome
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_gnome.so
%_libexecdir/pxgconf

%files kde
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_kde4.so

%if !%bootstrap
%files mozjs
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/pacrunner_mozjs.so

%files webkit
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/pacrunner_webkit.so
%endif

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/proxy.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%_datadir/cmake/Modules/Findlibproxy.cmake
