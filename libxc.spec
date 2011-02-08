Name:		libxc
Summary:	Library of exchange and correlation functionals to be used in DFT codes
Version:	1.0
Release:	5%{?dist}
License:	LGPLv3+
Group:		Applications/Engineering
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Source:		http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-%{version}.tar.gz
URL:		http://www.tddft.org/programs/octopus/wiki/index.php/Libxc

BuildRequires:	gcc-gfortran

%description 
libxc is a library of exchange and correlation functionals. Its purpose is to
be used in codes that implement density-functional theory. For the moment, the
library includes most of the local density approximations (LDAs), generalized
density approximation (GGAs), and meta-GGAs. The library provides values for
the energy density and its 1st, 2nd, and (for the LDAs) 3rd derivatives.

%package devel
Summary:	Development library and headers for libxc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
%if 0%{?fedora} >11 || 0%{?rhel} > 5
# Old versions don't have the 32-bit gfortran compiler, and the Fortran part 
# of the multilib'd devel package won't work in any case since Fortran modules
# are architecture and compiler version dependent.
Requires:	gcc-gfortran%{_isa}
%endif

%description devel
libxc is a library of exchange and correlation functionals. Its purpose is to
be used in codes that implement density-functional theory. For the moment, the
library includes most of the local density approximations (LDAs), generalized
density approximation (GGAs), and meta-GGAs. The library provides values for
the energy density and its 1st, 2nd, and (for the LDAs) 3rd derivatives.

This package contains the development headers and library that are necessary
in order to compile programs against libxc.

%prep
%setup -q

%build
%configure --enable-shared --disable-static
# SMP make is not working.
#make %{?_smp_mflags}
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Move modules in the right place
mkdir -p %{buildroot}%{_fmoddir}
mv %{buildroot}%{_includedir}/*.mod %{buildroot}%{_fmoddir}
# Get rid of .la files
find %{buildroot}%{_libdir} -name *.la -exec rm -rf {} \;

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING AUTHORS ChangeLog TODO
%{_libdir}/libxc.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libxc.so
%{_includedir}/xc*.h
%{_fmoddir}/libxc_funcs_m.mod
%{_fmoddir}/xc_f90_*.mod
%{_libdir}/pkgconfig/libxc.pc

%changelog
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
