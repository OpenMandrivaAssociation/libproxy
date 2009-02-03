%define gecko_version 1.9

%define major 0
%define libname %mklibname proxy %major
%define develname %mklibname -d proxy
Name:           libproxy
Version:        0.2.3
Release:        %mkrel 2
Summary:        A library handling all the details of proxy configuration

Group:          System/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libproxy/
Source0:        http://libproxy.googlecode.com/files/libproxy-%{version}.tar.gz
Patch0:         libproxy-0.2.3-dbus.patch
Patch1:		libproxy-0.2.3-fix-linking.patch
Patch2:		libproxy-0.2.3-format-strings.patch
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
BuildRequires:  webkitgtk-devel
# kde
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

%package        webkit
Summary:        Plugin for %{name} and webkit
Group:          System/Libraries
Requires:       %{libname} = %{version}
Provides:       %{name}-pac = %{version}-%{release}

%description    webkit
The %{name}-webkit package contains the %{name} plugin for
webkit.

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
%patch0 -p1 -b .dbus
%patch1 -p1
%patch2 -p1
autoreconf -fi

%build
%configure2_5x --includedir=%{_includedir}/libproxy --disable-static --with-python
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
%dir %{_libdir}/%{name}/%{version}/plugins
%{_libdir}/%{name}/%{version}/plugins/envvar.so
%{_libdir}/%{name}/%{version}/plugins/file.so
#%{_libdir}/%{name}/%{version}/plugins/networkmanager.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/proxy

%files -n python-%name
%defattr(-,root,root,-)
%{py_puresitedir}/*

%files gnome
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/plugins/gnome.so

%files kde
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/plugins/kde.so

%files mozjs
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/plugins/mozjs.so

%files webkit
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/plugins/webkit.so

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/libproxy/
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/libproxy-1.0.pc


