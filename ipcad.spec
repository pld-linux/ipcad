Summary:	IP Cisco-compatible Accounting Daemon
Summary(pl):	Demon do zliczania ruchu IP zgodny z Cisco
Name:		ipcad
Version:	2.6.3
Release:	0
License:	GPL
Group:		Networking/Utilities
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-conf.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IPCAD stands for IP Cisco Accounting Daemon. It runs in background and
listens traffic on the specified interfaces. It is compatible with
Cisco format of accounting tables. Same as in Cisco you can connect to
it via rsh and issue some specific command (e.g. "show ip accounting"
or "shutdown").

It has rsh support disabled by default.

%description -l pl
IPCAD to skr�t od IP Cisco Accounting Daemon. Dzia�a w tle i
nas�uchuje ruchu na wybranych interfejsach. Program jest kompatybilny
z formatem tablic zliaczania ruchu Cisco. Tak samo jak w Cisco mo�esz
si� z nim po��czy� zdalnie poprzez rsh i wydawa� r�ne polecenia (np.
"show ip accounting" czy "shutdown").

Domy�lnie zablokowano dost�p rsh.

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
install -d $RPM_BUILD_ROOT/{etc/init.d,usr/bin,usr/share/man/man{5,8},var/lib/ipcad}

%{__make} install-bin install-man DESTDIR=$RPM_BUILD_ROOT

install ipcad.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/init.d

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%preun

%post

%postun

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man5/ipcad.conf.5.gz
%{_mandir}/man8/ipcad.8.gz
%{_sysconfdir}/ipcad.conf
%dir /var/lib/ipcad
