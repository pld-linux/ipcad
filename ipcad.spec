Summary:	IP Cisco-compatible Accounting Daemon
Summary(pl):	Demon do zliczania ruchu IP zgodny z Cisco
Name:		ipcad
Version:	3.6.5
Release:	0.1
License:	GPL
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	40fd71336cf00300d720b05f6e2d5362
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Requires(post,preun):	/sbin/chkconfig
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
z formatem tablic zliczania ruchu Cisco. Tak samo jak w Cisco mo¿na
siê z nim po³±czyæ zdalnie poprzez rsh i wydawaæ ró¿ne polecenia (np.
"show ip accounting" czy "shutdown").

Domy¶lnie zablokowano dostêp rsh.

%prep
%setup -q

%build
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_initdir},/etc/sysconfig} \
	$RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{5,8},/var/lib/ipcad}

%{__make} install-bin install-man DESTDIR=$RPM_BUILD_ROOT

install ipcad.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/ipcad.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_initdir}/ipcad
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ipcad

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
%attr(754,root,root) %{_initdir}/ipcad
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ipcad
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipcad.conf
%{_mandir}/man5/ipcad.conf.5*
%{_mandir}/man8/ipcad.8*
%dir /var/lib/ipcad
