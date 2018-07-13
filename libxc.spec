%if 0%{?rhel} == 5
%global _fmoddir %{_libdir}/gfortran/modules
%endif
%global soversion 5

Name:           libxc
Summary:        Library of exchange and correlation functionals for density-functional theory
Version:        4.2.0
Release:        3%{?dist}
License:        MPLv2.0
Group:          Applications/Engineering
Source0:        http://www.tddft.org/programs/octopus/down.php?file=libxc/%{version}/libxc-%{version}.tar.gz
# Don't rebuild libxc for pylibxc
Patch0:         libxc-4.1.1-pylibxc.patch
# Fix incorrect version string in pylibxc
Patch1:         libxc-4.2.0-pylibxc-version.patch

URL:            http://www.tddft.org/programs/octopus/wiki/index.php/Libxc

BuildRequires:  gcc-gfortran
BuildRequires:  libtool
BuildRequires:  python2-devel
BuildRequires:  python3-devel

%description
libxc is a library of exchange and correlation functionals. Its purpose is to
be used in codes that implement density-functional theory. For the moment, the
library includes most of the local density approximations (LDAs), generalized
density approximation (GGAs), and meta-GGAs. The library provides values for
the energy density and its 1st, 2nd, and (for the LDAs) 3rd derivatives.

%package devel
Summary:        Development library and headers for libxc
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
libxc is a library of exchange and correlation functionals. Its purpose is to
be used in codes that implement density-functional theory. For the moment, the
library includes most of the local density approximations (LDAs), generalized
density approximation (GGAs), and meta-GGAs. The library provides values for
the energy density and its 1st, 2nd, and (for the LDAs) 3rd derivatives.

This package contains the development headers and library that are necessary
in order to compile programs against libxc.

%package -n python2-%{name}
Summary:        Python2 interface to libxc
BuildRequires:  python2-numpy
Requires:       python2-numpy
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
libxc is a library of exchange and correlation functionals. Its purpose is to
be used in codes that implement density-functional theory. For the moment, the
library includes most of the local density approximations (LDAs), generalized
density approximation (GGAs), and meta-GGAs. The library provides values for
the energy density and its 1st, 2nd, and (for the LDAs) 3rd derivatives.

This package contains the Python2 interface library to libxc.


%package -n python3-%{name}
Summary:        Python3 interface to libxc
BuildRequires:  python3-numpy
Requires:       python3-numpy
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
libxc is a library of exchange and correlation functionals. Its purpose is to
be used in codes that implement density-functional theory. For the moment, the
library includes most of the local density approximations (LDAs), generalized
density approximation (GGAs), and meta-GGAs. The library provides values for
the energy density and its 1st, 2nd, and (for the LDAs) 3rd derivatives.

This package contains the Python3 interface library to libxc.


%prep
%setup -q
%patch0 -p1 -b .pylibxc
%patch1 -p1 -b .pylibxcver
# Plug in library soversion
sed -i "s|@SOVERSION@|%{soversion}|g" pylibxc/core.py

%build
# Don't insert C code during preprocessing
export FCCPP="cpp -ffreestanding"
%configure --enable-shared --disable-static
# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# SMP make doesn't work
#make %{?_smp_mflags}
make

# Check we have the right soversion
if [[ ! -f src/.libs/libxc.so.%{soversion} ]]; then
    echo "soversion has changed!"
    exit
fi

# Build python interface
%{py2_build}
%{py3_build}

%install
make install DESTDIR=%{buildroot}
# Move modules in the right place
mkdir -p %{buildroot}%{_fmoddir}
mv %{buildroot}%{_includedir}/*.mod %{buildroot}%{_fmoddir}
# Get rid of .la files
find %{buildroot}%{_libdir} -name *.la -exec rm -rf {} \;

# Install python interface
%{py2_install}
%{py3_install}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README NEWS COPYING AUTHORS ChangeLog TODO
%{_bindir}/xc-info
%{_bindir}/xc-threshold
%{_libdir}/libxc.so.%{soversion}*
%{_libdir}/libxcf03.so.%{soversion}*
%{_libdir}/libxcf90.so.%{soversion}*

%files devel
%{_libdir}/libxc.so
%{_libdir}/libxcf03.so
%{_libdir}/libxcf90.so
%{_includedir}/xc*.h
%{_fmoddir}/libxc_funcs_m.mod
%{_fmoddir}/xc_f03_*.mod
%{_fmoddir}/xc_f90_*.mod
%{_libdir}/pkgconfig/libxc.pc
%{_libdir}/pkgconfig/libxcf03.pc
%{_libdir}/pkgconfig/libxcf90.pc

%files -n python2-%{name}
%{python2_sitelib}/pylibxc/
%{python2_sitelib}/pylibxc-%{version}-py*.egg-info

%files -n python3-%{name}
%{python3_sitelib}/pylibxc/
%{python3_sitelib}/pylibxc-%{version}-py*.egg-info


%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-2
- Rebuilt for Python 3.7

* Tue Jun 05 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.2.0-1
- Update to 4.2.0.

* Wed May 09 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.1.1-1
- Update to 4.1.1, changing license to MPLv2 and adding Python interface.

* Fri May 04 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0.5-1
- Update to 4.0.5.

* Wed Feb 07 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4.

* Mon Nov 20 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2.

* Mon Oct 09 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1.

* Wed Sep 27 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0, removing single precision libraries.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Feb 05 2017 Kalev Lember <klember@redhat.com> - 3.0.0-3
- Rebuilt for libgfortran soname bump

* Thu Jun 30 2016 Rafael Fonseca <rdossant@redhat.com> - 3.0.0-2
- Fix compilation on ppc64.

* Thu Apr 21 2016 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.1.2-4
- Drop gfortran requires on -devel.

* Fri Apr 24 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.1.2-3
- Patch some hybrids.

* Fri Apr 24 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.1.2-2
- Patch broken makefiles.

* Thu Feb 19 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.1.0-2
- Re-enable builds on ppc and ppc64 on EPEL.

* Fri Mar 21 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.1.0-1
- Enable single precision routines as well.
- Update to 2.1.0.

* Tue Feb 18 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3.

* Mon Feb 17 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.2-3
- Fix bug with some mgga correlation functionals.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2.

* Wed Mar 06 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.1-3
- Fix FTBFS in rawhide.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1.

* Fri Dec 7 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 13 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.0-4
- Clean buildroot at the beginning of %%install.

* Sun Jan 23 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.0-3
- Update tarball.
- Make requirement on gcc-gfortran in -devel architecture explicit.

* Sat Jan 22 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.0-2
- Minor review fixes.

* Tue Jan 18 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.0-1
- Initial specfile.
