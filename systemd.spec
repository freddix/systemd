# NOTE:
# for multi-user target tty1 is not enabled by default
#
# mkdir -p ${FS_DIR}/etc/systemd/system/getty.target.wants
# ln -sf /lib/systemd/system/getty@.service \
# 	${FS_DIR}/etc/systemd/system/getty.target.wants/getty@tty1.service
#
Summary:	A System and Service Manager
Name:		systemd
Version:	220
Release:	2
Epoch:		1
License:	GPL v2+
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
# Source0-md5:	60acd92b04c0f5faa806678abd433014
# user session
Source1:	%{name}-user.pamd
Source2:	dbus.service
Source3:	dbus.socket
# misc
Source10:	%{name}-loop.conf
Source11:	%{name}-sysctl.conf
URL:		http://www.freedesktop.org/wiki/Software/systemd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cryptsetup-devel
BuildRequires:	curl-devel
BuildRequires:	dbus-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-devel
BuildRequires:	glib-gio-devel
BuildRequires:	gnutls-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gperf
BuildRequires:	intltool
BuildRequires:	kmod-devel
BuildRequires:	libblkid-devel
BuildRequires:	libcap-devel
BuildRequires:	libidn-devel
BuildRequires:	libmicrohttpd-devel
BuildRequires:	libseccomp-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	m4
BuildRequires:	pam-devel
BuildRequires:	pciutils-devel
BuildRequires:	perl-tools-devel
BuildRequires:	pkg-config
BuildRequires:	python-devel
BuildRequires:	python-lxml
BuildRequires:	python-modules
BuildRequires:	qrencode-devel
BuildRequires:	usbutils
BuildRequires:	which
BuildRequires:	xz-devel
Requires(pre,postun):	pwdutils
Requires(post,postun):	/usr/sbin/ldconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-units = %{epoch}:%{version}-%{release}
Provides:	group(systemd-journal)
Provides:	virtual(init-daemon)
Requires:	core
Requires:	dbus
Requires:	kbd
Requires:	kmod
Requires:	udev = %{epoch}:%{version}-%{release}
Requires:	util-linux
# where is systemd-boot ???
#Obsoletes:	gummiboot
Obsoletes:	nss-myhostname
Suggests:	fuse
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libnss_myhostname.so.2
%define		filterout   -march.*

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
Summary:	systemd libraries
Group:		Libraries
Requires(post,postun):	/usr/sbin/ldconfig
Requires(post,preun):	sed

%description libs
systemd libraries.

%package devel
Summary:	Header files for systemd libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files for systemd libraries.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Group:		Base
Requires(post):	coreutils

%description units
Basic configuration files, directories and installation tool for the
systemd system and service manager.

%package journal-gatewayd
Summary:	Journal Gateway Service
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description journal-gatewayd
systemd-journal-gatewayd serves journal events over the network.

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

%package -n zsh-completion-systemd
Summary:	Zsh auto-complete site functions
Group:		Documentation
Requires:	zsh

%description -n zsh-completion-systemd
Zsh auto-complete site functions.

%prep
%setup -q

# define different than upstream sysrq behaviour
%{__sed} -i "s|kernel\.sysrq.*|kernel.sysrq = 1|" \
	sysctl.d/50-default.conf

# remove pregenerated files
find src -name \*-from-name.gperf -exec rm -f {} +
find src -name \*-to-name.h -exec rm -f {} +

%build
%if 0
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%endif
./autogen.sh
%configure \
	--disable-audit		\
	--disable-ima		\
	--disable-selinux	\
	--disable-silent-rules	\
	--disable-static	\
	--enable-compat-libs	\
	--with-firmware-path=/usr/lib/firmware	\
	--with-sysvinit-path=	\
	--with-sysvrcnd-path=
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{udev/rules.d,X11/xorg.conf.d}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# Don't ship any units in /etc in the package
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/*.target.wants/*

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/systemd/*.{la,py}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{*/,}*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/bash-completion
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/initrd*

%{__rm} $RPM_BUILD_ROOT%{_bindir}/coredumpctl
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/sysctl.d/50-coredump.conf
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/systemd/systemd-coredump
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/coredump.conf

install -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/journald.conf.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/resolved.conf.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/timesyncd.conf.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/user.conf.d

install -d $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/basic.target.wants
install -d $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/dbus.target.wants
install -d $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/default.target.wants
install -d $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/network-online.target.wants
install -d $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset
install -d $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user-preset
#install -d $RPM_BUILD_ROOT/var/lib/systemd/coredump
install -d $RPM_BUILD_ROOT/var/lib/systemd/catalog
install -d $RPM_BUILD_ROOT/var/log/journal
touch $RPM_BUILD_ROOT/var/lib/systemd/catalog/database
touch $RPM_BUILD_ROOT%{_sysconfdir}/udev/hwdb.bin
touch $RPM_BUILD_ROOT%{_sysconfdir}/machine-id
touch $RPM_BUILD_ROOT%{_sysconfdir}/machine-info
touch $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/00-keyboard.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/systemd-user
install %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user

install %{SOURCE10} $RPM_BUILD_ROOT/usr/lib/modules-load.d/loop.conf
install %{SOURCE11} $RPM_BUILD_ROOT/usr/lib/sysctl.d/60-freddix.conf

ln -s %{_prefix}/lib/systemd/systemd $RPM_BUILD_ROOT%{_bindir}/systemd

ln -s systemctl $RPM_BUILD_ROOT%{_bindir}/halt
ln -s systemctl $RPM_BUILD_ROOT%{_bindir}/poweroff
ln -s systemctl $RPM_BUILD_ROOT%{_bindir}/reboot

# disable all services
echo 'disable *' > \
    $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/99-default.preset

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 112 -r -f systemd-journal
%groupadd -g 114 -r -f systemd-timesync
%groupadd -g 115 -r -f systemd-network
%groupadd -g 116 -r -f systemd-resolve
%groupadd -g 119 -r -f systemd-bus-proxy
%groupadd -g 119 -r -f systemd-bus-proxy
%groupadd -g 120 -r -f systemd-journal-gateway
%useradd -u 114 -r -d / -s /usr/bin/false -c "systemd time synchronization" -g systemd-timesync systemd-timesync
%useradd -u 115 -r -d / -s /usr/bin/false -c "systemd network managment" -g systemd-network systemd-network
%useradd -u 116 -r -d / -s /usr/bin/false -c "systemd resolver" -g systemd-resolve systemd-resolve
%useradd -u 119 -r -d / -s /usr/bin/false -c "systemd bus proxy" -g systemd-bus-proxy systemd-bus-proxy
%useradd -u 120 -r -d / -s /usr/bin/false -c "HTTP server for journal events" -g systemd-journal-gateway systemd-journal-gateway
systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service ||:

%post
systemd-machine-id-setup ||:
/usr/lib/systemd/systemd-random-seed save ||:
systemctl daemon-reexec ||:
systemctl start systemd-udev.service ||:
udevadm hwdb --update ||:
journalctl --update-catalog ||:
systemd-tmpfiles --create ||:
if [ "$1" = "1" ] ; then
    /usr/bin/systemctl enable \
	getty@tty1.service \
	remote-fs.target \
	systemd-resolved.service \
	systemd-timesyncd.service \
	systemd-networkd.service \
	systemd-networkd-wait-online.service ||:
fi

%preun
if [ "$1" = "0" ]; then
	systemctl disable \
	getty@tty1.service \
	remote-fs.target \
	systemd-resolved.service \
	systemd-timesyncd.service \
	systemd-networkd.service \
	systemd-networkd-wait-online.service ||:
fi

%postun
if [ "$1" -ge "1" ] ; then
	systemctl daemon-reload ||:
	systemctl try-restart systemd-logind.service ||:
fi
if [ "$1" = "0" ]; then
    %groupremove systemd-journal
    %userremove systemd-bus-proxy
    %groupremove systemd-bus-proxy
    %userremove systemd-network
    %groupremove systemd-network
    %userremove systemd-resolve
    %groupremove systemd-resolve
    %userremove systemd-timesync
    %groupremove systemd-timesync
    %groupremove systemd-journal-gateway
    %userremove systemd-journal-gateway
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

%pre journal-gatewayd

%postun journal-gatewayd
if [ "$1" = "0" ]; then
fi

%post	-n udev-libs -p /usr/sbin/ldconfig
%postun	-n udev-libs -p /usr/sbin/ldconfig

%post	-n udev-glib -p /usr/sbin/ldconfig
%postun	-n udev-glib -p /usr/sbin/ldconfig


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc DISTRO_PORTING README TODO
%attr(755,root,root) %{_bindir}/bootctl
%attr(755,root,root) %{_bindir}/busctl
%attr(755,root,root) %{_bindir}/hostnamectl
%attr(755,root,root) %{_bindir}/journalctl
%attr(755,root,root) %{_bindir}/localectl
%attr(755,root,root) %{_bindir}/loginctl
%attr(755,root,root) %{_bindir}/machinectl
%attr(755,root,root) %{_bindir}/networkctl
%attr(755,root,root) %{_bindir}/timedatectl

%attr(755,root,root) %{_bindir}/systemd
%attr(755,root,root) %{_bindir}/systemd-analyze
%attr(755,root,root) %{_bindir}/systemd-ask-password
%attr(755,root,root) %{_bindir}/systemd-cat
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-cgtop
%attr(755,root,root) %{_bindir}/systemd-delta
%attr(755,root,root) %{_bindir}/systemd-detect-virt
%attr(755,root,root) %{_bindir}/systemd-escape
%attr(755,root,root) %{_bindir}/systemd-firstboot
%attr(755,root,root) %{_bindir}/systemd-hwdb
%attr(755,root,root) %{_bindir}/systemd-inhibit
%attr(755,root,root) %{_bindir}/systemd-machine-id-setup
%attr(755,root,root) %{_bindir}/systemd-notify
%attr(755,root,root) %{_bindir}/systemd-nspawn
%attr(755,root,root) %{_bindir}/systemd-path
%attr(755,root,root) %{_bindir}/systemd-run
%attr(755,root,root) %{_bindir}/systemd-stdio-bridge
%attr(755,root,root) %{_bindir}/systemd-sysusers
%attr(755,root,root) %{_bindir}/systemd-tty-ask-password-agent

%attr(755,root,root) %{_bindir}/halt
%attr(755,root,root) %{_bindir}/poweroff
%attr(755,root,root) %{_bindir}/reboot

# EFI boot helper for gummiboot
%attr(755,root,root) %{_bindir}/kernel-install
%dir %{_prefix}/lib/kernel
%dir %{_prefix}/lib/kernel/install.d
%attr(755,root,root) %{_prefix}/lib/kernel/install.d/50-depmod.install
%attr(755,root,root) %{_prefix}/lib/kernel/install.d/90-loaderentry.install
%dir %{_prefix}/lib/systemd/boot
%dir %{_prefix}/lib/systemd/boot/efi
%{_prefix}/lib/systemd/boot/efi/linuxx64.efi.stub
%{_prefix}/lib/systemd/boot/efi/systemd-bootx64.efi

%attr(755,root,root) %{_prefix}/lib/systemd/systemd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-ac-power
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-activate
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-backlight
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-binfmt
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-bootchart
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-bus-proxyd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-cgroups-agent
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-cryptsetup
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-export
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-fsck
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-hibernate-resume
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-hostnamed
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-import
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-importd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-initctl
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-journald
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-localed
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-logind
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-machine-id-commit
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-machined
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-modules-load
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-networkd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-networkd-wait-online
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-pull
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-quotacheck
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-random-seed
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-remount-fs
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-reply-password
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-resolve-host
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-resolved
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-rfkill
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-shutdown
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-sleep
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-socket-proxyd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-sysctl
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-timedated
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-timesyncd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-udevd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-update-done
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-update-utmp
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-user-sessions
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-vconsole-setup

%dir %{_prefix}/lib/systemd/system-generators
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-cryptsetup-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-debug-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-efi-boot-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-fstab-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-getty-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-gpt-auto-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-hibernate-resume-generator
%attr(755,root,root) %{_prefix}/lib/systemd/system-generators/systemd-system-update-generator

%attr(755,root,root) %{_libdir}/security/pam_systemd.so

%config(noreplace) %verify(not md5 mtime size) /etc/systemd/bootchart.conf
%config(noreplace) %verify(not md5 mtime size) /etc/X11/xorg.conf.d/00-keyboard.conf
%{_prefix}/lib/modules-load.d/loop.conf
%{_prefix}/lib/sysctl.d/50-default.conf
%{_prefix}/lib/sysctl.d/60-freddix.conf

%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info

%dir %{_sysconfdir}/systemd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/user.conf

%dir %{_datadir}/systemd
%{_datadir}/systemd/kbd-model-map
%{_datadir}/systemd/language-fallback-map
%{_prefix}/lib/systemd/import-pubring.gpg

%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service

%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.import1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.network1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.resolve1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service

%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.import1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy

%{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.import1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.network1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf

%{_prefix}/lib/tmpfiles.d/etc.conf
%{_prefix}/lib/tmpfiles.d/home.conf
%{_prefix}/lib/tmpfiles.d/systemd-nologin.conf
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/var.conf
%{_prefix}/lib/tmpfiles.d/x11.conf

%{_prefix}/lib/udev/rules.d/70-uaccess.rules
%{_prefix}/lib/udev/rules.d/71-seat.rules
%{_prefix}/lib/udev/rules.d/73-seat-late.rules
%{_prefix}/lib/udev/rules.d/99-systemd.rules

%{_prefix}/lib/systemd/network/80-container-host0.network
%{_prefix}/lib/systemd/network/99-default.link
%{_prefix}/lib/systemd/network/80-container-ve.network

%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*
%exclude %{_mandir}/man1/systemctl.1*
%exclude %{_mandir}/man5/tmpfiles.d.5*
%exclude %{_mandir}/man8/systemd-tmpfiles.8*

%{_prefix}/lib/systemd/catalog/systemd.catalog
%lang(fr) %{_prefix}/lib/systemd/catalog/systemd.fr.catalog
%lang(it) %{_prefix}/lib/systemd/catalog/systemd.it.catalog
%lang(pl) %{_prefix}/lib/systemd/catalog/systemd.pl.catalog
%lang(pt_BR) %{_prefix}/lib/systemd/catalog/systemd.pt_BR.catalog
%lang(ru) %{_prefix}/lib/systemd/catalog/systemd.ru.catalog

# targets
%{_prefix}/lib/systemd/system/basic.target
%{_prefix}/lib/systemd/system/bluetooth.target
%{_prefix}/lib/systemd/system/cryptsetup-pre.target
%{_prefix}/lib/systemd/system/cryptsetup.target
%{_prefix}/lib/systemd/system/ctrl-alt-del.target
%{_prefix}/lib/systemd/system/default.target
%{_prefix}/lib/systemd/system/emergency.target
%{_prefix}/lib/systemd/system/final.target
%{_prefix}/lib/systemd/system/getty.target
%{_prefix}/lib/systemd/system/graphical.target
%{_prefix}/lib/systemd/system/halt.target
%{_prefix}/lib/systemd/system/hibernate.target
%{_prefix}/lib/systemd/system/hybrid-sleep.target
%{_prefix}/lib/systemd/system/kexec.target
%{_prefix}/lib/systemd/system/local-fs-pre.target
%{_prefix}/lib/systemd/system/local-fs.target
%{_prefix}/lib/systemd/system/machines.target
%{_prefix}/lib/systemd/system/multi-user.target
%{_prefix}/lib/systemd/system/network-online.target
%{_prefix}/lib/systemd/system/network-pre.target
%{_prefix}/lib/systemd/system/network.target
%{_prefix}/lib/systemd/system/nss-lookup.target
%{_prefix}/lib/systemd/system/nss-user-lookup.target
%{_prefix}/lib/systemd/system/paths.target
%{_prefix}/lib/systemd/system/poweroff.target
%{_prefix}/lib/systemd/system/printer.target
%{_prefix}/lib/systemd/system/reboot.target
%{_prefix}/lib/systemd/system/remote-fs-pre.target
%{_prefix}/lib/systemd/system/remote-fs.target
%{_prefix}/lib/systemd/system/rescue.target
%{_prefix}/lib/systemd/system/rpcbind.target
%{_prefix}/lib/systemd/system/shutdown.target
%{_prefix}/lib/systemd/system/sigpwr.target
%{_prefix}/lib/systemd/system/sleep.target
%{_prefix}/lib/systemd/system/slices.target
%{_prefix}/lib/systemd/system/smartcard.target
%{_prefix}/lib/systemd/system/sockets.target
%{_prefix}/lib/systemd/system/sound.target
%{_prefix}/lib/systemd/system/suspend.target
%{_prefix}/lib/systemd/system/swap.target
%{_prefix}/lib/systemd/system/sysinit.target
%{_prefix}/lib/systemd/system/system-update.target
%{_prefix}/lib/systemd/system/time-sync.target
%{_prefix}/lib/systemd/system/umount.target

# *.target.wants
%{_prefix}/lib/systemd/system/local-fs.target.wants/systemd-remount-fs.service
%{_prefix}/lib/systemd/system/local-fs.target.wants/tmp.mount
%{_prefix}/lib/systemd/system/local-fs.target.wants/var-lib-machines.mount
%{_prefix}/lib/systemd/system/multi-user.target.wants/getty.target
%{_prefix}/lib/systemd/system/multi-user.target.wants/systemd-ask-password-wall.path
%{_prefix}/lib/systemd/system/multi-user.target.wants/systemd-logind.service
%{_prefix}/lib/systemd/system/multi-user.target.wants/systemd-user-sessions.service
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-initctl.socket
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-journald-audit.socket
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-journald.socket
%{_prefix}/lib/systemd/system/sysinit.target.wants/cryptsetup.target
%{_prefix}/lib/systemd/system/sysinit.target.wants/dev-hugepages.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/dev-mqueue.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/kmod-static-nodes.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/proc-sys-fs-binfmt_misc.automount
%{_prefix}/lib/systemd/system/sysinit.target.wants/sys-fs-fuse-connections.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/sys-kernel-config.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/sys-kernel-debug.mount
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-ask-password-console.path
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-binfmt.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-firstboot.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-hwdb-update.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-journal-catalog-update.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-journal-flush.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-journald.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-machine-id-commit.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-modules-load.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-random-seed.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-sysctl.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-sysusers.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-tmpfiles-setup-dev.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-tmpfiles-setup.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-udev-trigger.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-udevd.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-update-done.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-update-utmp.service
%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-vconsole-setup.service

# mounts
%{_prefix}/lib/systemd/system/dev-hugepages.mount
%{_prefix}/lib/systemd/system/dev-mqueue.mount
%{_prefix}/lib/systemd/system/proc-sys-fs-binfmt_misc.automount
%{_prefix}/lib/systemd/system/proc-sys-fs-binfmt_misc.mount
%{_prefix}/lib/systemd/system/sys-fs-fuse-connections.mount
%{_prefix}/lib/systemd/system/sys-kernel-config.mount
%{_prefix}/lib/systemd/system/sys-kernel-debug.mount
%{_prefix}/lib/systemd/system/tmp.mount
%{_prefix}/lib/systemd/system/var-lib-machines.mount

# sockets
%{_prefix}/lib/systemd/system/syslog.socket
%{_prefix}/lib/systemd/system/systemd-initctl.socket
%{_prefix}/lib/systemd/system/systemd-journald-audit.socket
%{_prefix}/lib/systemd/system/systemd-journald-dev-log.socket
%{_prefix}/lib/systemd/system/systemd-journald.socket
%{_prefix}/lib/systemd/system/systemd-networkd.socket

# timers
%{_prefix}/lib/systemd/system/timers.target
%{_prefix}/lib/systemd/system/timers.target.wants/systemd-tmpfiles-clean.timer
%{_prefix}/lib/systemd/system/systemd-tmpfiles-clean.timer

# paths
%{_prefix}/lib/systemd/system/systemd-ask-password-console.path
%{_prefix}/lib/systemd/system/systemd-ask-password-wall.path

# services
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.hostname1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.import1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.locale1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.login1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.machine1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.network1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.resolve1.service
%{_prefix}/lib/systemd/system/dbus-org.freedesktop.timedate1.service

%{_prefix}/lib/systemd/system/autovt@.service
%{_prefix}/lib/systemd/system/console-getty.service
%{_prefix}/lib/systemd/system/console-shell.service
%{_prefix}/lib/systemd/system/container-getty@.service
%{_prefix}/lib/systemd/system/debug-shell.service
%{_prefix}/lib/systemd/system/emergency.service
%{_prefix}/lib/systemd/system/getty@.service
%{_prefix}/lib/systemd/system/kmod-static-nodes.service
%{_prefix}/lib/systemd/system/ldconfig.service
%{_prefix}/lib/systemd/system/quotaon.service
%{_prefix}/lib/systemd/system/rescue.service
%{_prefix}/lib/systemd/system/serial-getty@.service

%{_prefix}/lib/systemd/system/systemd-ask-password-console.service
%{_prefix}/lib/systemd/system/systemd-ask-password-wall.service
%{_prefix}/lib/systemd/system/systemd-backlight@.service
%{_prefix}/lib/systemd/system/systemd-binfmt.service
%{_prefix}/lib/systemd/system/systemd-bootchart.service
%{_prefix}/lib/systemd/system/systemd-firstboot.service
%{_prefix}/lib/systemd/system/systemd-fsck-root.service
%{_prefix}/lib/systemd/system/systemd-fsck@.service
%{_prefix}/lib/systemd/system/systemd-halt.service
%{_prefix}/lib/systemd/system/systemd-hibernate-resume@.service
%{_prefix}/lib/systemd/system/systemd-hibernate.service
%{_prefix}/lib/systemd/system/systemd-hostnamed.service
%{_prefix}/lib/systemd/system/systemd-hwdb-update.service
%{_prefix}/lib/systemd/system/systemd-hybrid-sleep.service
%{_prefix}/lib/systemd/system/systemd-importd.service
%{_prefix}/lib/systemd/system/systemd-initctl.service
%{_prefix}/lib/systemd/system/systemd-journal-catalog-update.service
%{_prefix}/lib/systemd/system/systemd-journal-flush.service
%{_prefix}/lib/systemd/system/systemd-journald.service
%{_prefix}/lib/systemd/system/systemd-kexec.service
%{_prefix}/lib/systemd/system/systemd-localed.service
%{_prefix}/lib/systemd/system/systemd-logind.service
%{_prefix}/lib/systemd/system/systemd-machine-id-commit.service
%{_prefix}/lib/systemd/system/systemd-machined.service
%{_prefix}/lib/systemd/system/systemd-modules-load.service
%{_prefix}/lib/systemd/system/systemd-networkd-wait-online.service
%{_prefix}/lib/systemd/system/systemd-networkd.service
%{_prefix}/lib/systemd/system/systemd-nspawn@.service
%{_prefix}/lib/systemd/system/systemd-poweroff.service
%{_prefix}/lib/systemd/system/systemd-quotacheck.service
%{_prefix}/lib/systemd/system/systemd-random-seed.service
%{_prefix}/lib/systemd/system/systemd-reboot.service
%{_prefix}/lib/systemd/system/systemd-remount-fs.service
%{_prefix}/lib/systemd/system/systemd-resolved.service
%{_prefix}/lib/systemd/system/systemd-rfkill@.service
%{_prefix}/lib/systemd/system/systemd-suspend.service
%{_prefix}/lib/systemd/system/systemd-sysctl.service
%{_prefix}/lib/systemd/system/systemd-sysusers.service
%{_prefix}/lib/systemd/system/systemd-timedated.service
%{_prefix}/lib/systemd/system/systemd-timesyncd.service
%{_prefix}/lib/systemd/system/systemd-tmpfiles-clean.service
%{_prefix}/lib/systemd/system/systemd-tmpfiles-setup-dev.service
%{_prefix}/lib/systemd/system/systemd-tmpfiles-setup.service
%{_prefix}/lib/systemd/system/systemd-update-done.service
%{_prefix}/lib/systemd/system/systemd-update-utmp-runlevel.service
%{_prefix}/lib/systemd/system/systemd-update-utmp.service
%{_prefix}/lib/systemd/system/systemd-user-sessions.service
%{_prefix}/lib/systemd/system/systemd-vconsole-setup.service

# slices
%{_prefix}/lib/systemd/system/-.slice
%{_prefix}/lib/systemd/system/machine.slice
%{_prefix}/lib/systemd/system/system.slice
%{_prefix}/lib/systemd/system/user.slice

# presets
%{_prefix}/lib/systemd/system-preset/90-systemd.preset
%{_prefix}/lib/systemd/system-preset/99-default.preset

%dir %{_datadir}/factory
%dir %{_datadir}/factory/etc
%dir %{_datadir}/factory/etc/pam.d
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth

# sysusers.d
%{_prefix}/lib/sysusers.d/basic.conf
%{_prefix}/lib/sysusers.d/systemd.conf

%if 0
%attr(755,root,root) %{_bindir}/systemd-coredumpctl
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-coredump
%dir /var/lib/systemd/coredump
%{_prefix}/lib/sysctl.d/50-coredump.conf
%endif

# systemd --user
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/systemd-user
%dir %{_prefix}/lib/systemd/user
# targets
%{_prefix}/lib/systemd/user/basic.target
%{_prefix}/lib/systemd/user/bluetooth.target
%{_prefix}/lib/systemd/user/default.target
%{_prefix}/lib/systemd/user/exit.target
%{_prefix}/lib/systemd/user/paths.target
%{_prefix}/lib/systemd/user/printer.target
%{_prefix}/lib/systemd/user/shutdown.target
%{_prefix}/lib/systemd/user/smartcard.target
%{_prefix}/lib/systemd/user/sockets.target
%{_prefix}/lib/systemd/user/sound.target
%{_prefix}/lib/systemd/user/timers.target
# services
%{_prefix}/lib/systemd/system/user@.service
%{_prefix}/lib/systemd/user/dbus.service
%{_prefix}/lib/systemd/user/dbus.socket
%{_prefix}/lib/systemd/user/systemd-exit.service

%dir /var/lib/systemd
%dir /var/lib/systemd/catalog
%dir %attr(2755,root,systemd-journal) /var/log/journal
%ghost /var/lib/systemd/catalog/database

%if 0
# there is no initrd in Freddix
%attr(755,root,root) %{_prefix}/lib/systemd/system/initrd-cleanup.service
%attr(755,root,root) %{_prefix}/lib/systemd/system/initrd-parse-etc.service
%attr(755,root,root) %{_prefix}/lib/systemd/system/initrd-switch-root.service
%attr(755,root,root) %{_prefix}/lib/systemd/system/initrd-switch-root.target
%attr(755,root,root) %{_prefix}/lib/systemd/system/initrd-udevadm-cleanup-db.service
%endif

%files units
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemctl
%attr(755,root,root) %{_bindir}/systemd-tmpfiles
%{_mandir}/man1/systemctl.1*
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man8/systemd-tmpfiles.8*

%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/sysusers.d
%dir %{_prefix}/lib/tmpfiles.d

%dir %{_prefix}/lib/systemd/catalog
%dir %{_prefix}/lib/systemd/system-preset
%dir %{_prefix}/lib/systemd/system-shutdown
%dir %{_prefix}/lib/systemd/system-sleep
%dir %{_prefix}/lib/systemd/user-generators
%dir %{_prefix}/lib/systemd/user-preset

%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/tmpfiles.d

%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/network
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user

%dir %{_sysconfdir}/systemd/journald.conf.d
%dir %{_sysconfdir}/systemd/resolved.conf.d
%dir %{_sysconfdir}/systemd/timesyncd.conf.d
%dir %{_sysconfdir}/systemd/user.conf.d

%dir %{_sysconfdir}/xdg/systemd
%{_sysconfdir}/xdg/systemd/user

%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/network
%dir %{_prefix}/lib/systemd/system

%dir %{_prefix}/lib/systemd/system/basic.target.wants
%dir %{_prefix}/lib/systemd/system/dbus.target.wants
%dir %{_prefix}/lib/systemd/system/default.target.wants
%dir %{_prefix}/lib/systemd/system/local-fs.target.wants
%dir %{_prefix}/lib/systemd/system/multi-user.target.wants
%dir %{_prefix}/lib/systemd/system/network-online.target.wants
%dir %{_prefix}/lib/systemd/system/sockets.target.wants
%dir %{_prefix}/lib/systemd/system/sysinit.target.wants
%dir %{_prefix}/lib/systemd/system/timers.target.wants

%dir %{_sysconfdir}/systemd/system/getty.target.wants
%dir %{_sysconfdir}/systemd/system/multi-user.target.wants
%dir %{_sysconfdir}/systemd/system/network-online.target.wants
%dir %{_sysconfdir}/systemd/system/sockets.target.wants
%dir %{_sysconfdir}/systemd/system/sysinit.target.wants

%files journal-gatewayd
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-journal-gatewayd
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-journal-remote
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-journal-upload
%{_datadir}/systemd/gatewayd
%{_prefix}/lib/systemd/system/systemd-journal-gatewayd.service
%{_prefix}/lib/systemd/system/systemd-journal-gatewayd.socket
%{_prefix}/lib/systemd/system/systemd-journal-remote.service
%{_prefix}/lib/systemd/system/systemd-journal-remote.socket
%{_prefix}/lib/systemd/system/systemd-journal-upload.service
%{_prefix}/lib/sysusers.d/systemd-remote.conf
%{_prefix}/lib/tmpfiles.d/systemd-remote.conf
%{_sysconfdir}/systemd/journal-remote.conf
%{_sysconfdir}/systemd/journal-upload.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libsystemd-daemon.so.?
%attr(755,root,root) %ghost %{_libdir}/libsystemd-id128.so.?
%attr(755,root,root) %ghost %{_libdir}/libsystemd-journal.so.?
%attr(755,root,root) %ghost %{_libdir}/libsystemd-login.so.?
%attr(755,root,root) %ghost %{_libdir}/libsystemd.so.?
%attr(755,root,root) %{_libdir}/libsystemd-daemon.so.*.*.*
%attr(755,root,root) %{_libdir}/libsystemd-id128.so.*.*.*
%attr(755,root,root) %{_libdir}/libsystemd-journal.so.*.*.*
%attr(755,root,root) %{_libdir}/libsystemd-login.so.*.*.*
%attr(755,root,root) %{_libdir}/libsystemd.so.*.*.*
%attr(755,root,root) %{_libdir}/libnss_myhostname.so.2
%attr(755,root,root) %{_libdir}/libnss_mymachines.so.2
%attr(755,root,root) %{_libdir}/libnss_resolve.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsystemd*.so
%{_includedir}/systemd
%{_pkgconfigdir}/*systemd*.pc
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
%dir %{_prefix}/lib/udev/rules.d

%attr(755,root,root) %{_bindir}/udevadm
%attr(755,root,root) %{_prefix}/lib/systemd/systemd-udevd

%attr(755,root,root) %{_prefix}/lib/udev/accelerometer
%attr(755,root,root) %{_prefix}/lib/udev/collect
%attr(755,root,root) %{_prefix}/lib/udev/mtd_probe

%attr(755,root,root) %{_prefix}/lib/udev/ata_id
%attr(755,root,root) %{_prefix}/lib/udev/cdrom_id
%attr(755,root,root) %{_prefix}/lib/udev/scsi_id
%attr(755,root,root) %{_prefix}/lib/udev/v4l_id

# rules
%{_prefix}/lib/udev/rules.d/42-usb-hid-pm.rules
%{_prefix}/lib/udev/rules.d/50-udev-default.rules
%{_prefix}/lib/udev/rules.d/60-block.rules
%{_prefix}/lib/udev/rules.d/60-cdrom_id.rules
%{_prefix}/lib/udev/rules.d/60-drm.rules
%{_prefix}/lib/udev/rules.d/60-evdev.rules
%{_prefix}/lib/udev/rules.d/60-persistent-alsa.rules
%{_prefix}/lib/udev/rules.d/60-persistent-input.rules
%{_prefix}/lib/udev/rules.d/60-persistent-storage-tape.rules
%{_prefix}/lib/udev/rules.d/60-persistent-storage.rules
%{_prefix}/lib/udev/rules.d/60-persistent-v4l.rules
%{_prefix}/lib/udev/rules.d/60-serial.rules
%{_prefix}/lib/udev/rules.d/61-accelerometer.rules
%{_prefix}/lib/udev/rules.d/64-btrfs.rules
%{_prefix}/lib/udev/rules.d/70-mouse.rules
%{_prefix}/lib/udev/rules.d/70-power-switch.rules
%{_prefix}/lib/udev/rules.d/70-touchpad.rules
%{_prefix}/lib/udev/rules.d/75-net-description.rules
%{_prefix}/lib/udev/rules.d/75-probe_mtd.rules
%{_prefix}/lib/udev/rules.d/78-sound-card.rules
%{_prefix}/lib/udev/rules.d/80-drivers.rules
%{_prefix}/lib/udev/rules.d/80-net-setup-link.rules
%{_prefix}/lib/udev/rules.d/90-vconsole.rules

# hwdb
%{_prefix}/lib/udev/hwdb.d/20-OUI.hwdb
%{_prefix}/lib/udev/hwdb.d/20-acpi-vendor.hwdb
%{_prefix}/lib/udev/hwdb.d/20-bluetooth-vendor-product.hwdb
%{_prefix}/lib/udev/hwdb.d/20-net-ifname.hwdb
%{_prefix}/lib/udev/hwdb.d/20-pci-classes.hwdb
%{_prefix}/lib/udev/hwdb.d/20-pci-vendor-model.hwdb
%{_prefix}/lib/udev/hwdb.d/20-sdio-classes.hwdb
%{_prefix}/lib/udev/hwdb.d/20-sdio-vendor-model.hwdb
%{_prefix}/lib/udev/hwdb.d/20-usb-classes.hwdb
%{_prefix}/lib/udev/hwdb.d/20-usb-vendor-model.hwdb
%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb
%{_prefix}/lib/udev/hwdb.d/60-keyboard.hwdb
%{_prefix}/lib/udev/hwdb.d/70-mouse.hwdb
%{_prefix}/lib/udev/hwdb.d/70-pointingstick.hwdb
%{_prefix}/lib/udev/hwdb.d/70-touchpad.hwdb

%{_sysconfdir}/udev/udev.conf
%ghost %{_sysconfdir}/udev/hwdb.bin

# systemd stuff
%{_prefix}/lib/systemd/system/sockets.target.wants/systemd-journald-dev-log.socket
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

%files -n zsh-completion-systemd
%defattr(644,root,root,755)
%{_datadir}/zsh/site-functions/_*

