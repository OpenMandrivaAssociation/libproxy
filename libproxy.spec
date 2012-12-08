%define major 1
%define libname %mklibname proxy %{major}
%define devname %mklibname -d proxy

%bcond_with	bootstrap

Name:		libproxy
Version:	0.4.7
Release:	2
Summary:	A library handling all the details of proxy configuration

Group:		System/Libraries
License:	LGPLv2+
URL:		http://code.google.com/p/libproxy/
# http://code.google.com/p/libproxy/issues/detail?id=130&can=1&q=perl
Source0:	http://%{name}.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		libproxy-0.4.7-xul2.0.patch
Patch1:		libproxy-javascriptcoregtk.patch
Patch2:		libproxy-0.4.7-add-missing-linkage.patch
Patch3:		libproxy-0.4.7-url-pac.patch
Patch4:		libproxy-0.4.7-unistd.patch
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
BuildRequires:	pkgconfig(webkit-1.0)
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
Requires:	%{libname} = %{version}-%{release}

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
Requires:	%{libname} = %{version}-%{release}

%description	gnome
The %{name}-gnome package contains the %{name} plugin for gnome.

%package	kde
Summary:	Plugin for %{name} and kde
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description	kde
The %{name}-kde package contains the %{name} plugin for kde.

%package	networkmanager
Summary:	Plugin for %{name} and networkmanager
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description	networkmanager
The %{name}-networkmanager package contains the %{name} plugin for
networkmanager.
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
%patch0 -p1 -b .xul20~
%patch1 -p0 -b .webkitgtk~
%patch2 -p1 -b .linkage~
%patch3 -p1
%patch4 -p1

%build
%cmake -Dlibexecdir=%{_libexecdir} -DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DMODULE_INSTALL_DIR=%{_libdir}/%{name}/%{version}/modules \
	-DPERL_VENDORINSTALL=1 -DWITH_MOZJS=OFF
%make

%install
%makeinstall_std -C build
#gw fix pkgconfig file
sed -i -e "s^Version:.*^Version: %{version}^" %{buildroot}%{_libdir}/pkgconfig/*.pc

%check
pushd build
ctest .
popd

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
%endif

%files -n %{devname}
%{_includedir}/proxy.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%{_datadir}/cmake/Modules/Findlibproxy.cmake


%changelog
* Thu Feb 16 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.4.7-1
+ Revision: 775065
- use pkgconfig() dependencies for buildrequires
- cleanup spec
- no longer building a shared libmodman..
- fix description-line-too-long
- fix buildrequires
- fix linking
- new version
- mass rebuild of perl extensions against perl 5.14.2

  + Giuseppe Ghibò <ghibo@mandriva.com>
    - Added %%mkrel for backporting libproxy1 (needed for firefox10).

* Mon Jun 20 2011 Funda Wang <fwang@mandriva.org> 0.4.6-5
+ Revision: 686115
- rebuild for new webkit

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.6-4
+ Revision: 662409
- mass rebuild

* Sun Mar 20 2011 Funda Wang <fwang@mandriva.org> 0.4.6-3
+ Revision: 647159
- libproxy does not build with xulrunner 2.0 now, so merge all pacrunner into main

* Wed Nov 03 2010 Götz Waschk <waschk@mandriva.org> 0.4.6-2mdv2011.0
+ Revision: 592881
- rebuild for new python 2.7

* Mon Sep 06 2010 Götz Waschk <waschk@mandriva.org> 0.4.6-1mdv2011.0
+ Revision: 576217
- python module is arch-dependant
- new version
- drop patches
- new libmodman major 1

* Mon Aug 09 2010 Götz Waschk <waschk@mandriva.org> 0.4.4-3mdv2011.0
+ Revision: 568091
- disable bootstrap

* Mon Aug 09 2010 Götz Waschk <waschk@mandriva.org> 0.4.4-2mdv2011.0
+ Revision: 568077
- fix bootstrapping option
- bootstrap build
- fix pkgconfig file

* Mon Aug 09 2010 Götz Waschk <waschk@mandriva.org> 0.4.4-1mdv2011.0
+ Revision: 568003
- new version
- new major
- add libmodman
- drop patches 1,2,3
- fix build
- add perl binding

* Sat Jan 02 2010 Götz Waschk <waschk@mandriva.org> 0.3.1-2mdv2010.1
+ Revision: 485011
- don't apply patch 3 on Cooker, fixes build

* Thu Nov 26 2009 Funda Wang <fwang@mandriva.org> 0.3.1-1mdv2010.1
+ Revision: 470293
- New version 0.3.1
- fix linkage of modules

* Mon Sep 28 2009 Olivier Blin <blino@mandriva.org> 0.2.3-4mdv2010.0
+ Revision: 450562
- use libxul-unstable headers for jsapi.h, patch from upstream
  http://code.google.com/p/libproxy/issues/detail?id=44
- add bootstrap (from Arnaud Patard)
  fix loop libsoup->libproxy->webkitgtk-devel->libsoup

* Thu Mar 12 2009 Frederik Himpe <fhimpe@mandriva.org> 0.2.3-3mdv2009.1
+ Revision: 354376
- Rebuild for new webkit major

* Tue Feb 03 2009 Götz Waschk <waschk@mandriva.org> 0.2.3-2mdv2009.1
+ Revision: 336801
- remove deps from the library package

* Mon Feb 02 2009 Götz Waschk <waschk@mandriva.org> 0.2.3-1mdv2009.1
+ Revision: 336716
- fix deps
- import libproxy


* Mon Feb  2 2009 Götz Waschk <waschk@mandriva.org> 0.2.3-1mdv2009.1
- initial package based on Fedora

* Thu Jan 22 2009 kwizart < kwizart at gmail.com > - 0.2.3-8
- Merge NetworkManager module into the main libproxy package
- Main Requires the -python and -bin subpackage 
 (splitted for multilibs compliance).

* Fri Oct 24 2008 kwizart < kwizart at gmail.com > - 0.2.3-7
- Disable Gnome/KDE default support via builtin modules.
 (it needs to be integrated via Gconf2/neon instead).

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-6
- Disable Obsoletes.
- Requires ev instead of evr for optionnals sub-packages.

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-5
- Use conditionals build.

* Mon Sep 15 2008 kwizart < kwizart at gmail.com > - 0.2.3-4
- Remove plugin- in the name of the packages

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-3
- Move proxy.h to libproxy/proxy.h
  This will prevent it to be included in the default include path
- Split main to libs and util and use libproxy to install all

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-2
- Rename binding-python to python
- Add Requires: gecko-libs >= %%{gecko_version}
- Fix some descriptions
- Add plugin-webkit package
 
* Fri Jul 11 2008 kwizart < kwizart at gmail.com > - 0.2.3-1
- Convert to Fedora spec

* Fri Jun 6 2008 - dominique-rpm@leuenberger.net
- Updated to version 0.2.3
* Wed Jun 4 2008 - dominique-rpm@leuenberger.net
- Extended spec file to build all available plugins
* Tue Jun 3 2008 - dominique-rpm@leuenberger.net
- Initial spec file for Version 0.2.2

