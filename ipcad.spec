Summary:	IP Cisco-compatible Accounting Daemon
Summary(pl):	Demon do zliczania ruchu IP zgodny z Cisco
Name:		ipcad
Version:	2.6.3
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-conf.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _initdir                /etc/rc.d/init.d

%description
IPCAD stands for IP Cisco Accounting Daemon. It runs in background and
listens traffic on the specified interfaces. It is compatible with
Cisco format of accounting tables. Same as in Cisco you can connect to
it via rsh and issue some specific command (e.g. "show ip accounting"
or "shutdown").

It has rsh support disabled by default.

%description -l pl
IPCAD to skrót od IP Cisco Accounting Daemon. Dzia³a w tle i
nas³uchuje ruchu na wybranych interfejsach. Program jest kompatybilny
z formatem tablic zliaczania ruchu Cisco. Tak samo jak w Cisco mo¿esz
siê z nim po³±czyæ zdalnie poprzez rsh i wydawaæ ró¿ne polecenia (np.
"show ip accounting" czy "shutdown").

Domy¶lnie zablokowano dostêp rsh.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
#%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sysconfdir},%{_initdir},%{_sysconfdir}/sysconfig,usr/bin,usr/share/man/man{5,8},var/lib/ipcad}

%{__make} install-bin install-man DESTDIR=$RPM_BUILD_ROOT

install ipcad.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_initdir}/ipcad
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ipcad

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man5/ipcad.conf.5.gz
%{_mandir}/man8/ipcad.8.gz
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipcad.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/ipcad
%attr (755,root,root) %{_initdir}/ipcad
%dir /var/lib/ipcad
