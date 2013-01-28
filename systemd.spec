# NOTE:
# for multi-user target tty1 is not enabled by default
#
# mkdir -p ${FS_DIR}/etc/systemd/system/getty.target.wants
# ln -sf /lib/systemd/system/getty@.service \
# 	${FS_DIR}/etc/systemd/system/getty.target.wants/getty@tty1.service
#
Summary:	A System and Service Manager
Name:		systemd
Version:	197
Release:	3
Epoch:		1
License:	GPL v2+
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
# Source0-md5:	56a860dceadfafe59f40141eb5223743
Source10:	00-keyboard.conf
Source11:	%{name}-loop.conf
Source12:	%{name}-sysctl.conf
Source20:	dbus.service
Source21:	dbus.socket
Source22:	%{name}-user
Source23:	%{name}-stop-user-sessions.service
# udev stuff
Source30:	udev-65-permissions.rules
#
Patch0:		%{name}-localectl-lib64.patch
Patch1:		0001-dbus-fix-serialization-of-calendar-timers.patch
URL:		http://www.freedesktop.org/wiki/Software/systemd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cryptsetup-devel
BuildRequires:	dbus-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	gobject-introspection-devel
BuildRequires:	gperf
BuildRequires:	kmod-devel
BuildRequires:	libblkid-devel
BuildRequires:	libcap-devel
BuildRequires:	libmicrohttpd-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	m4
BuildRequires:	pam-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkg-config
BuildRequires:	qrencode-devel
BuildRequires:	usbutils
BuildRequires:	vala
Requires(post,postun):	/usr/sbin/ldconfig
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-units = %{epoch}:%{version}-%{release}
Provides:	virtual(init-daemon)
Requires:	core
Requires:	dbus
Requires:	kbd
Requires:	kmod
Requires:	python-pygobject3
Requires:	udev = %{epoch}:%{version}-%{release}
Requires:	util-linux
Obsoletes:	nss-myhostname
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
systemd is a system and service manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package libs
Summary:        systemd libraries
Group:          Libraries
Requires(post,postun):	/usr/sbin/ldconfig
Requires(post,preun):	sed

%description libs
systemd libraries.

%package devel
Summary:        Header files for systemd libraries
Group:          Development/Libraries
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files for systemd libraries.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Group:		Base
Requires(post):	coreutils

%description units
Basic configuration files, directories and installation tool for the
systemd system and service manager.

%package -n python-%{name}
Summary:	Python support for systemd
Group:		Libraries/Python
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-%{name}
Python support for systemd.

%package -n udev
Summary:	udev is the device manager for the Linux kernel.
Group:		Base
Requires:	udev-libs = %{epoch}:%{version}-%{release}
Requires:	pciutils
Requires:	usbutils

%description -n udev
udev is the device manager for the Linux kernel.

%package -n udev-libs
Summary:	Udev library
Group:		Libraries

%description -n udev-libs
Udev library.

%package -n udev-devel
Summary:	Header files for libvolume_id library
Group:		Development/Libraries
Requires:	udev-libs = %{epoch}:%{version}-%{release}

%description -n udev-devel
this is the package containing the header files for udev library.

%package -n udev-glib
Summary:	gudev library
Group:		Libraries
Requires:	udev-libs = %{epoch}:%{version}-%{release}

%description -n udev-glib
gudev library.

%package -n udev-glib-devel
Summary:	Header files for libvolume_id library
Group:		Development/Libraries
Requires:	udev-glib = %{epoch}:%{version}-%{release}

%description -n udev-glib-devel
This is the package containing the header files for gudev library.

%package -n udev-apidocs
Summary:	udev API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description -n udev-apidocs
udev API documentation.

%prep
%setup -q
%if %{_lib} == "lib64"
%patch0 -p1
%endif
%patch1 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-audit		\
	--disable-selinux	\
	--disable-silent-rules	\
	--disable-static	\
	--disable-tcpwrap	\
	--with-sysvinit-path=	\
	--with-sysvrcnd-path=
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{udev/rules.d,X11/xorg.conf.d},%{_sbindir}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

rm -f $RPM_BUILD_ROOT%{_libdir}/{*/,}*.la

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/*.target.wants

touch $RPM_BUILD_ROOT%{_sysconfdir}/machine-id
touch $RPM_BUILD_ROOT%{_sysconfdir}/machine-info

install %{SOURCE10} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
install %{SOURCE11} $RPM_BUILD_ROOT/usr/lib/modules-load.d/loop.conf
install %{SOURCE12} $RPM_BUILD_ROOT/usr/lib/sysctl.d/sysctl.conf

install %{SOURCE20} %{SOURCE21} $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user
install %{SOURCE22} $RPM_BUILD_ROOT%{_prefix}/lib/systemd
install %{SOURCE23} $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system
ln -s ../systemd-stop-user-sessions.service \
	$RPM_BUILD_ROOT/usr/lib/systemd/system/shutdown.target.wants/systemd-stop-user-sessions.service

install %{SOURCE30} $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/65-permissions.rules

ln -s %{_prefix}/lib/systemd/systemd $RPM_BUILD_ROOT%{_sbindir}/init
ln -s %{_prefix}/lib/systemd/systemd $RPM_BUILD_ROOT%{_bindir}/systemd

cat > $RPM_BUILD_ROOT%{systemdtmpfilesdir}/console.conf <<EOF
d /run/console 0755 root root

EOF

rm -f $RPM_BUILD_ROOT%{py_sitedir}/systemd/*.{la,py}

%clean
rm -rf $RPM_BUILD_ROOT

%post
systemd-machine-id-setup > /dev/null 2>&1 || :
/usr/lib/systemd/systemd-random-seed save > /dev/null 2>&1 || :
systemctl daemon-reexec > /dev/null 2>&1 || :
systemctl start systemd-udev.service > /dev/null 2>&1 || :
udevadm hwdb --update > /dev/null 2>&1 || :
journalctl --update-catalog > /dev/null 2>&1 || :

%post units
if [ "$1" = "1" ] ; then
    /usr/bin/systemctl enable getty@.service
    ln -sf /usr/lib/systemd/system/multi-user.target \
    	/etc/systemd/system/default.target
fi

%preun units
if [ "$1" = "0" ]; then
    systemctl disable getty@.service
    rm -f %{_sysconfdir}/systemd/system/default.target > /dev/null 2>&1 || :
fi

%postun
if [ "$1" -ge "1" ] ; then
	systemctl daemon-reload > /dev/null 2>&1 || :
	systemctl try-restart systemd-logind.service >/dev/null 2>&1 || :
fi

%post libs
/usr/sbin/ldconfig
if [ -f %{_sysconfdir}/nsswitch.conf ]; then
    %{__sed} -i -e '
    /^hosts:/ !b
    /\<myhostname\>/ b
    s/[[:blank:]]*$/ myhostname/
    ' %{_sysconfdir}/nsswitch.conf
fi

%preun libs
if [ "$1" -eq 0 -a -f %{_sysconfdir}/nsswitch.conf ] ; then
    %{__sed} -i -e '
    /^hosts:/ !b
    s/[[:blank:]]\+myhostname\>//
    ' %{_sysconfdir}/nsswitch.conf
fi

%postun	libs -p /usr/sbin/ldconfig

%post	-n udev-libs -p /usr/sbin/ldconfig
%postun	-n udev-libs -p /usr/sbin/ldconfig

%post	-n udev-glib -p /usr/sbin/ldconfig
%postun	-n udev-glib -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc DISTRO_PORTING README TODO
%attr(755,root,root) %{_bindir}/hostnamectl
%attr(755,root,root) %{_bindir}/journalctl
%attr(755,root,root) %{_bindir}/localectl
%attr(755,root,root) %{_bindir}/loginctl
%attr(755,root,root) %{_bindir}/systemd
%attr(755,root,root) %{_bindir}/systemd-analyze
%attr(755,root,root) %{_bindir}/systemd-ask-password
%attr(755,root,root) %{_bindir}/systemd-cat
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-cgtop
%attr(755,root,root) %{_bindir}/systemd-coredumpctl
%attr(755,root,root) %{_bindir}/systemd-delta
%attr(755,root,root) %{_bindir}/systemd-detect-virt
%attr(755,root,root) %{_bindir}/systemd-inhibit
%attr(755,root,root) %{_bindir}/systemd-machine-id-setup
%attr(755,root,root) %{_bindir}/systemd-notify
%attr(755,root,root) %{_bindir}/systemd-nspawn
%attr(755,root,root) %{_bindir}/systemd-stdio-bridge
%attr(755,root,root) %{_bindir}/systemd-tty-ask-password-agent
%attr(755,root,root) %{_bindir}/timedatectl
%attr(755,root,root) %{_sbindir}/init

%attr(755,root,root) %{_prefix}/lib/systemd/systemd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-ac-power
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-binfmt
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-bootchart
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-cgroups-agent
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-coredump
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-cryptsetup
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-fsck
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-hostnamed
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-initctl
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-journald
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-localed
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-logind
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-modules-load
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-multi-seat-x
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-quotacheck
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-random-seed
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-readahead
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-remount-fs
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-reply-password
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-shutdown
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-shutdownd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-sleep
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-sysctl
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-timedated
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-timestamp
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-udevd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-update-utmp
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-user
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-user-sessions
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-vconsole-setup

%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-cryptsetup-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-fstab-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-getty-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-system-update-generator

%attr(755,root,root) %{_libdir}/security/pam_systemd.so

%config(noreplace) %verify(not md5 mtime size) /etc/X11/xorg.conf.d/00-keyboard.conf
%{_prefix}/lib/modules-load.d/loop.conf
%{_prefix}/lib/sysctl.d/sysctl.conf
%{_prefix}/lib/sysctl.d/coredump.conf

%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info

%dir %{_sysconfdir}/systemd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/user.conf

%dir %{_datadir}/systemd
%{_datadir}/systemd/kbd-model-map

%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service

%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy

%{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf

%{_prefix}/lib/tmpfiles.d/console.conf
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/x11.conf

%{_prefix}/lib/udev/rules.d/70-uaccess.rules
%{_prefix}/lib/udev/rules.d/71-seat.rules
%{_prefix}/lib/udev/rules.d/73-seat-late.rules
%{_prefix}/lib/udev/rules.d/99-systemd.rules

%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*
%exclude %{_mandir}/man1/systemctl.1*
%exclude %{_mandir}/man5/tmpfiles.d.5*
%exclude %{_mandir}/man8/systemd-tmpfiles.8*

# gatewayd
%{_datadir}/systemd/gatewayd
%{_prefix}/lib/systemd/system/systemd-journal-gatewayd.service
%{_prefix}/lib/systemd/system/systemd-journal-gatewayd.socket
%{_prefix}/lib/systemd/systemd-journal-gatewayd

%files units
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemctl
%attr(755,root,root) %{_bindir}/systemd-tmpfiles

%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/tmpfiles.d

%dir %{_prefix}/lib/systemd/catalog
%{_prefix}/lib/systemd/catalog/systemd.catalog

%dir %{_prefix}/lib/systemd/ntp-units.d
%dir %{_prefix}/lib/systemd/system-generators
%dir %{_prefix}/lib/systemd/system-shutdown
%dir %{_prefix}/lib/systemd/system-sleep
%dir %{_prefix}/lib/systemd/user-generators

%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/tmpfiles.d

%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/ntp-units.d
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user

%dir %{_sysconfdir}/xdg/systemd
%{_sysconfdir}/xdg/systemd/user

%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/system

%dir %{_prefix}/lib/systemd/system/basic.target.wants
%{_prefix}/lib/systemd/system/basic.target
%{_prefix}/lib/systemd/system/basic.target.wants/systemd-tmpfiles-clean.timer

%dir %{_prefix}/lib/systemd/system/graphical.target.wants

%dir %{_prefix}/lib/systemd/system/local-fs.target.wants
%{_prefix}/lib/systemd/system/local-fs-pre.target
%{_prefix}/lib/systemd/system/local-fs.target
%{_prefix}/lib/systemd/system/local-fs.target.wants/systemd-fsck-root.service
%{_prefix}/lib/systemd/system/local-fs.target.wants/systemd-remount-fs.service
%{_prefix}/lib/systemd/system/local-fs.target.wants/tmp.mount

%dir %{_prefix}/lib/systemd/system/multi-user.target.wants
%{_prefix}/lib/systemd/system/multi-user.target
%{_prefix}/lib/systemd/system/multi-user.target.wants/getty.target
%{_prefix}/lib/systemd/system/multi-user.target.wants/systemd-ask-password-wall.path
%{_prefix}/lib/systemd/system/multi-user.target.wants/systemd-logind.service
%{_prefix}/lib/systemd/system/multi-user.target.wants/systemd-user-sessions.service

%dir %{_prefix}/lib/systemd/system/runlevel1.target.wants
%dir %{_prefix}/lib/systemd/system/runlevel2.target.wants
%dir %{_prefix}/lib/systemd/system/runlevel3.target.wants
%dir %{_prefix}/lib/systemd/system/runlevel4.target.wants
%dir %{_prefix}/lib/systemd/system/runlevel5.target.wants
%{_prefix}/lib/systemd/system/runlevel1.target.wants/systemd-update-utmp-runlevel.service
%{_prefix}/lib/systemd/system/runlevel2.target.wants/systemd-update-utmp-runlevel.service
%{_prefix}/lib/systemd/system/runlevel3.target.wants/systemd-update-utmp-runlevel.service
%{_prefix}/lib/systemd/system/runlevel4.target.wants/systemd-update-utmp-runlevel.service
%{_prefix}/lib/systemd/system/runlevel5.target.wants/systemd-update-utmp-runlevel.service
%{_prefix}/lib/systemd/system/runlevel0.target
%{_prefix}/lib/systemd/system/runlevel1.target
%{_prefix}/lib/systemd/system/runlevel2.target
%{_prefix}/lib/systemd/system/runlevel3.target
%{_prefix}/lib/systemd/system/runlevel4.target
%{_prefix}/lib/systemd/system/runlevel5.target
%{_prefix}/lib/systemd/system/runlevel6.target

%dir %{_prefix}/lib/systemd/system/shutdown.target.wants
%{_prefix}/lib/systemd/system/shutdown.target
%{_prefix}/lib/systemd/system/shutdown.target.wants/systemd-random-seed-save.service
%{_prefix}/lib/systemd/system/shutdown.target.wants/systemd-stop-user-sessions.service
%{_prefix}/lib/systemd/system/shutdown.target.wants/systemd-update-utmp-shutdown.service

%dir %{_prefix}/lib/systemd/system/sockets.target.wants
%{_prefix}/lib/systemd/system/sockets.target
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-initctl.socket
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-journald.socket
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-shutdownd.socket

%dir %{_prefix}/lib/systemd/system/sysinit.target.wants
%{_prefix}/lib/systemd/system/sysinit.target
%{_prefix}/lib/systemd/system/sysinit.target.wants/cryptsetup.target
%{_prefix}/lib/systemd/system/sysinit.target.wants/dev-hugepages.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/dev-mqueue.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/proc-sys-fs-binfmt_misc.automount
%{_prefix}/lib/systemd/system/sysinit.target.wants/sys-fs-fuse-connections.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/sys-kernel-config.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/sys-kernel-debug.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-ask-password-console.path
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-binfmt.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-journal-flush.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-journald.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-modules-load.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-random-seed-load.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-sysctl.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-tmpfiles-setup.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-udev-trigger.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-udevd.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-vconsole-setup.service

# targets
%{_prefix}/lib/systemd/system/bluetooth.target
%{_prefix}/lib/systemd/system/cryptsetup.target
%{_prefix}/lib/systemd/system/ctrl-alt-del.target
%{_prefix}/lib/systemd/system/default.target
%{_prefix}/lib/systemd/system/emergency.target
%{_prefix}/lib/systemd/system/final.target
%{_prefix}/lib/systemd/system/getty.target
%{_prefix}/lib/systemd/system/graphical.target
%{_prefix}/lib/systemd/system/halt.target
%{_prefix}/lib/systemd/system/hibernate.target
%{_prefix}/lib/systemd/system/kexec.target
%{_prefix}/lib/systemd/system/mail-transfer-agent.target
%{_prefix}/lib/systemd/system/network.target
%{_prefix}/lib/systemd/system/nss-lookup.target
%{_prefix}/lib/systemd/system/nss-user-lookup.target
%{_prefix}/lib/systemd/system/poweroff.target
%{_prefix}/lib/systemd/system/printer.target
%{_prefix}/lib/systemd/system/reboot.target
%{_prefix}/lib/systemd/system/remote-fs-pre.target
%{_prefix}/lib/systemd/system/remote-fs.target
%{_prefix}/lib/systemd/system/rescue.target
%{_prefix}/lib/systemd/system/rpcbind.target
%{_prefix}/lib/systemd/system/sigpwr.target
%{_prefix}/lib/systemd/system/sleep.target
%{_prefix}/lib/systemd/system/smartcard.target
%{_prefix}/lib/systemd/system/sound.target
%{_prefix}/lib/systemd/system/suspend.target
%{_prefix}/lib/systemd/system/swap.target
%{_prefix}/lib/systemd/system/syslog.target
%{_prefix}/lib/systemd/system/system-update.target
%{_prefix}/lib/systemd/system/time-sync.target
%{_prefix}/lib/systemd/system/umount.target
%{_prefix}/lib/systemd/system/hybrid-sleep.target

# mounts
%{_prefix}/lib/systemd/system/dev-hugepages.mount
%{_prefix}/lib/systemd/system/dev-mqueue.mount
%{_prefix}/lib/systemd/system/proc-sys-fs-binfmt_misc.automount
%{_prefix}/lib/systemd/system/proc-sys-fs-binfmt_misc.mount
%{_prefix}/lib/systemd/system/sys-fs-fuse-connections.mount
%{_prefix}/lib/systemd/system/sys-kernel-config.mount
%{_prefix}/lib/systemd/system/sys-kernel-debug.mount
%{_prefix}/lib/systemd/system/tmp.mount

# sockets
%{_prefix}/lib/systemd/system/systemd-initctl.socket
%{_prefix}/lib/systemd/system/systemd-journald.socket
%{_prefix}/lib/systemd/system/systemd-shutdownd.socket
%{_prefix}/lib/systemd/system/syslog.socket

# timers
%{_prefix}/lib/systemd/system/systemd-readahead-done.timer
%{_prefix}/lib/systemd/system/systemd-tmpfiles-clean.timer

# paths
%{_prefix}/lib/systemd/system/systemd-ask-password-console.path
%{_prefix}/lib/systemd/system/systemd-ask-password-wall.path

# services
%{_prefix}/lib/systemd/system/autovt@.service
%{_prefix}/lib/systemd/system/console-getty.service
%{_prefix}/lib/systemd/system/console-shell.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.hostname1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.locale1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.login1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.timedate1.service
%{_prefix}/lib/systemd/system/debug-shell.service
%{_prefix}/lib/systemd/system/emergency.service
%{_prefix}/lib/systemd/system/getty@.service
%{_prefix}/lib/systemd/system/quotaon.service
%{_prefix}/lib/systemd/system/rescue.service
%{_prefix}/lib/systemd/system/serial-getty@.service
%{_prefix}/lib/systemd/system/systemd-ask-password-console.service
%{_prefix}/lib/systemd/system/systemd-ask-password-wall.service
%{_prefix}/lib/systemd/system/systemd-binfmt.service
%{_prefix}/lib/systemd/system/systemd-fsck-root.service
%{_prefix}/lib/systemd/system/systemd-fsck@.service
%{_prefix}/lib/systemd/system/systemd-halt.service
%{_prefix}/lib/systemd/system/systemd-hibernate.service
%{_prefix}/lib/systemd/system/systemd-hostnamed.service
%{_prefix}/lib/systemd/system/systemd-hybrid-sleep.service
%{_prefix}/lib/systemd/system/systemd-initctl.service
%{_prefix}/lib/systemd/system/systemd-journal-flush.service
%{_prefix}/lib/systemd/system/systemd-journald.service
%{_prefix}/lib/systemd/system/systemd-kexec.service
%{_prefix}/lib/systemd/system/systemd-localed.service
%{_prefix}/lib/systemd/system/systemd-logind.service
%{_prefix}/lib/systemd/system/systemd-modules-load.service
%{_prefix}/lib/systemd/system/systemd-poweroff.service
%{_prefix}/lib/systemd/system/systemd-quotacheck.service
%{_prefix}/lib/systemd/system/systemd-random-seed-load.service
%{_prefix}/lib/systemd/system/systemd-random-seed-save.service
%{_prefix}/lib/systemd/system/systemd-readahead-collect.service
%{_prefix}/lib/systemd/system/systemd-readahead-done.service
%{_prefix}/lib/systemd/system/systemd-readahead-drop.service
%{_prefix}/lib/systemd/system/systemd-readahead-replay.service
%{_prefix}/lib/systemd/system/systemd-reboot.service
%{_prefix}/lib/systemd/system/systemd-remount-fs.service
%{_prefix}/lib/systemd/system/systemd-shutdownd.service
%{_prefix}/lib/systemd/system/systemd-stop-user-sessions.service
%{_prefix}/lib/systemd/system/systemd-suspend.service
%{_prefix}/lib/systemd/system/systemd-sysctl.service
%{_prefix}/lib/systemd/system/systemd-timedated.service
%{_prefix}/lib/systemd/system/systemd-tmpfiles-clean.service
%{_prefix}/lib/systemd/system/systemd-tmpfiles-setup.service
%{_prefix}/lib/systemd/system/systemd-update-utmp-runlevel.service
%{_prefix}/lib/systemd/system/systemd-update-utmp-shutdown.service
%{_prefix}/lib/systemd/system/systemd-user-sessions.service
%{_prefix}/lib/systemd/system/systemd-vconsole-setup.service
%{_prefix}/lib/systemd/system/user@.service

# systemd --user
%dir %{_prefix}/lib/systemd/user
%{_prefix}/lib/systemd/user/bluetooth.target
%{_prefix}/lib/systemd/user/dbus.service
%{_prefix}/lib/systemd/user/dbus.socket
%{_prefix}/lib/systemd/user/default.target
%{_prefix}/lib/systemd/user/exit.target
%{_prefix}/lib/systemd/user/printer.target
%{_prefix}/lib/systemd/user/shutdown.target
%{_prefix}/lib/systemd/user/sockets.target
%{_prefix}/lib/systemd/user/sound.target
%{_prefix}/lib/systemd/user/systemd-exit.service

%{_mandir}/man1/systemctl.1*
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man8/systemd-tmpfiles.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libsystemd-daemon.so.?
%attr(755,root,root) %ghost %{_libdir}/libsystemd-id128.so.?
%attr(755,root,root) %ghost %{_libdir}/libsystemd-journal.so.?
%attr(755,root,root) %ghost %{_libdir}/libsystemd-login.so.?
%attr(755,root,root) %{_libdir}/libsystemd-daemon.so.*.*.*
%attr(755,root,root) %{_libdir}/libsystemd-id128.so.*.*.*
%attr(755,root,root) %{_libdir}/libsystemd-journal.so.*.*.*
%attr(755,root,root) %{_libdir}/libsystemd-login.so.*.*.*

%attr(755,root,root) %{_libdir}/libnss_myhostname.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsystemd-*.so
%{_datadir}/dbus-1/interfaces/*.xml
%{_includedir}/systemd
%{_npkgconfigdir}/systemd.pc
%{_pkgconfigdir}/libsystemd-*.pc
%{_mandir}/man3/*.3*

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/systemd
%attr(755,root,root) %{py_sitedir}/systemd/*.so
%attr(755,root,root) %{py_sitedir}/systemd/*.py[co]

# UDev ------------------------------------------

%files -n udev
%defattr(644,root,root,755)

# dirs
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_prefix}/lib/udev
%dir %{_prefix}/lib/udev/hwdb.d
%dir %{_prefix}/lib/udev/keymaps
%dir %{_prefix}/lib/udev/rules.d

%attr(755,root,root) %{_bindir}/udevadm
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-udevd

%attr(755,root,root) %{_prefix}/lib/udev/accelerometer
%attr(755,root,root) %{_prefix}/lib/udev/collect
%attr(755,root,root) %{_prefix}/lib/udev/findkeyboards
%attr(755,root,root) %{_prefix}/lib/udev/keyboard-force-release.sh
%attr(755,root,root) %{_prefix}/lib/udev/keymap
%attr(755,root,root) %{_prefix}/lib/udev/mtd_probe

%attr(755,root,root) %{_prefix}/lib/udev/ata_id
%attr(755,root,root) %{_prefix}/lib/udev/cdrom_id
%attr(755,root,root) %{_prefix}/lib/udev/scsi_id
%attr(755,root,root) %{_prefix}/lib/udev/v4l_id

# rules
%{_prefix}/lib/udev/rules.d/42-usb-hid-pm.rules
%{_prefix}/lib/udev/rules.d/50-udev-default.rules
%{_prefix}/lib/udev/rules.d/60-cdrom_id.rules
%{_prefix}/lib/udev/rules.d/60-persistent-alsa.rules
%{_prefix}/lib/udev/rules.d/60-persistent-input.rules
%{_prefix}/lib/udev/rules.d/60-persistent-serial.rules
%{_prefix}/lib/udev/rules.d/60-persistent-storage-tape.rules
%{_prefix}/lib/udev/rules.d/60-persistent-storage.rules
%{_prefix}/lib/udev/rules.d/60-persistent-v4l.rules
%{_prefix}/lib/udev/rules.d/61-accelerometer.rules
%{_prefix}/lib/udev/rules.d/64-btrfs.rules
%{_prefix}/lib/udev/rules.d/65-permissions.rules
%{_prefix}/lib/udev/rules.d/70-power-switch.rules
%{_prefix}/lib/udev/rules.d/75-net-description.rules
%{_prefix}/lib/udev/rules.d/75-probe_mtd.rules
%{_prefix}/lib/udev/rules.d/75-tty-description.rules
%{_prefix}/lib/udev/rules.d/78-sound-card.rules
%{_prefix}/lib/udev/rules.d/80-drivers.rules
%{_prefix}/lib/udev/rules.d/80-net-name-slot.rules
%{_prefix}/lib/udev/rules.d/95-keyboard-force-release.rules
%{_prefix}/lib/udev/rules.d/95-keymap.rules
%{_prefix}/lib/udev/rules.d/95-udev-late.rules

# hwdb
%{_prefix}/lib/udev/hwdb.d/20-OUI.hwdb
%{_prefix}/lib/udev/hwdb.d/20-acpi-vendor.hwdb
%{_prefix}/lib/udev/hwdb.d/20-bluetooth-vendor-product.hwdb
%{_prefix}/lib/udev/hwdb.d/20-pci-classes.hwdb
%{_prefix}/lib/udev/hwdb.d/20-pci-vendor-product.hwdb
%{_prefix}/lib/udev/hwdb.d/20-usb-classes.hwdb
%{_prefix}/lib/udev/hwdb.d/20-usb-vendor-product.hwdb

%{_sysconfdir}/udev/udev.conf

%{_prefix}/lib/udev/keymaps/*

# systemd stuff
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-udevd-control.socket
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-udevd-kernel.socket
%{_prefix}/lib/systemd/system/systemd-udev-settle.service
%{_prefix}/lib/systemd/system/systemd-udev-trigger.service
%{_prefix}/lib/systemd/system/systemd-udevd-control.socket
%{_prefix}/lib/systemd/system/systemd-udevd-kernel.socket
%{_prefix}/lib/systemd/system/systemd-udevd.service

%{_mandir}/man7/*
%{_mandir}/man8/*

%files -n udev-libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libudev.so.?
%attr(755,root,root) %{_libdir}/libudev.so.*.*.*

%files -n udev-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudev.so
%{_datadir}/gir-1.0/GUdev-1.0.gir
%{_includedir}/libudev.h
%{_npkgconfigdir}/udev.pc
%{_pkgconfigdir}/libudev.pc

%files -n udev-glib
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgudev-1.0.so.?
%attr(755,root,root) %{_libdir}/libgudev-1.0.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files -n udev-glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgudev-1.0.so
%{_includedir}/gudev-1.0
%{_pkgconfigdir}/gudev-1.0.pc

%if 0
%files -n udev-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gudev
%{_gtkdocdir}/libudev
%endif

