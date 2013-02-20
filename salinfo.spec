Summary:	Decode IA64 SAL records
Summary(pl.UTF-8):	Program dekodujący rekordy SAL architektury IA64
Name:		salinfo
Version:	0.7
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://ftp.kernel.org/pub/linux/kernel/people/helgaas/%{name}-%{version}.tar.gz
# Source0-md5:	749bf802c361b3c160ed6ebfd45da3ad
ExclusiveArch:	ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The IA64 Linux kernel has a Software Abstraction Layer (SAL). One of
SAL's tasks is to record machine problems such as CMC (correctable
machine checks), CPE (correctable platform errors), MCA (machine check
architecture) and INIT (cpu initialized after boot). These records are
provided by SAL to user space. salinfo saves and decodes CMC/CPE/MCA
and INIT records.

%description -l pl.UTF-8
Jądra Linuksa na architekturze IA64 ma programową warstwę abstrakcji
SAL (Software Abstraction Layer). Jednym z jej zadań jest zapisywanie
problemów z maszyną, takich jak CMC (correctable machine check), CPE
(correctable platform error), MCA (machine check architecture) czy
INIT (inicjacja procesora po uruchomieniu). Rekordy te są przekazywane
przez SAL do przestrzeni użytkownika. salinfo zapisuje i dekoduje
rekordy CMC/CPE/MCA oraz INIT.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add salinfo_decode
%service salinfo_decode restart

%preun
if [ "$1" = "0" ]; then
	%service -q salinfo_decode stop
	/sbin/chkconfig --del salinfo_decode
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_sbindir}/salinfo_decode
%attr(755,root,root) %{_sbindir}/salinfo_decode_all
%attr(700,root,root) %dir /var/log/salinfo
%attr(700,root,root) %dir /var/log/salinfo/raw
%attr(700,root,root) %dir /var/log/salinfo/decoded
%attr(754,root,root) /etc/rc.d/init.d/salinfo_decode
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/salinfo_decode
%{_mandir}/man8/salinfo_decode.8*
