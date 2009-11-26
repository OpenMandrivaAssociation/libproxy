%define gecko_version 1.9

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

%define major 0
%define libname %mklibname proxy %major
%define develname %mklibname -d proxy
Name:           libproxy
Version:        0.3.1
Release:        %mkrel 1
Summary:        A library handling all the details of proxy configuration

Group:          System/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libproxy/
Source0:        http://libproxy.googlecode.com/files/libproxy-%{version}.tar.bz2
Patch1:		libproxy-0.3.1-fix-linking.patch
Patch2:		libproxy-0.3.1-format-strings.patch
Patch3:		libproxy-0.3.1-jsapi-unstable.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  python-devel
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
Requires: %{name}-pac >= %{version}
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
Provides:	%name-devel = %version-%release

%description -n %develname
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
autoreconf -fi

%build
export CFLAGS="%{optflags} -fPIC"
export CPPFLAGS="%{optflags} -fPIC"
%configure2_5x \
	--includedir=%{_includedir}/libproxy \
	--disable-static --with-python \
	--without-networkmanager
%make


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdvver < 200900
%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root,-)
%doc AUTHORS README
%{_libdir}/libproxy.so.%{major}*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules
%{_libdir}/%{name}/%{version}/modules/config_direct.so
%{_libdir}/%{name}/%{version}/modules/config_envvar.so
%{_libdir}/%{name}/%{version}/modules/config_file.so
%{_libdir}/%{name}/%{version}/modules/config_wpad.so
%{_libdir}/%{name}/%{version}/modules/ignore_domain.so
%{_libdir}/%{name}/%{version}/modules/ignore_ip.so
%{_libdir}/%{name}/%{version}/modules/wpad_dnsdevolution.so
%{_libdir}/%{name}/%{version}/modules/wpad_dns.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/proxy

%files -n python-%name
%defattr(-,root,root,-)
%{py_puresitedir}/*

%files gnome
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_gnome.so

%files kde
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_kde4.so

%files mozjs
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/pacrunner_mozjs.so

%if !%bootstrap
%files webkit
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/pacrunner_webkit.so
%endif

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/libproxy/
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/libproxy-1.0.pc
