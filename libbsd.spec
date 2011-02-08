Name:		libbsd
Version:	0.2.0
Release:	4%{?dist}
Summary:	Library providing BSD-compatible functions for portability
URL:		http://libbsd.freedesktop.org/

Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.gz

# Patch to use $(CFLAGS) when linking shared library, necessary to
# get debuginfo package.  Upstream bug 
# https://bugs.freedesktop.org/show_bug.cgi?id=26310
Patch0:		libbsd-debuginfo.patch

License:	BSD and ISC and Copyright only and Public Domain
Group:		System Environment/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package devel
Summary:	Development files for libbsd
Group:		Development/Libraries
Requires:	libbsd = %{version}-%{release}
Requires:	pkgconfig

%description devel
Development files for the libbsd library.

%prep
%setup -q
%patch0 -p1 -b .debuginfo

# fix encoding of flopen.3 man page
for f in src/flopen.3; do
  iconv -f iso8859-1 -t utf-8 $f >$f.conv
  touch -r $f $f.conv
  mv $f.conv $f
done

%build
make CFLAGS="%{optflags}" %{?_smp_mflags} \
     libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix}

%install
rm -rf %{buildroot}
make libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix} \
     DESTDIR=%{buildroot} \
     install

# don't want static library
rm %{buildroot}%{_libdir}/%{name}.a

# Shared library needs to be executable for debuginfo to be generated
# Upstream bug https://bugs.freedesktop.org/show_bug.cgi?id=26312
chmod 755 %{buildroot}%{_libdir}/%{name}.so.%{version}

# Move nlist.h into bsd directory to avoid conflict with elfutils-libelf.
# Anyone that wants that functionality should really used elfutils-libelf
# instead.
mv %{buildroot}%{_includedir}/nlist.h %{buildroot}%{_includedir}/bsd/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README TODO ChangeLog
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*.3.gz
%{_mandir}/man3/*.3bsd.gz
%{_includedir}/*.h
%{_includedir}/bsd
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 29 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-3
- changes based on review by Sebastian Dziallas

* Fri Jan 29 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-2
- changes based on review comments by Jussi Lehtola and Ralf Corsepious

* Thu Jan 28 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-1
- initial version
