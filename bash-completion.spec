%define name	bash-completion
%define version 2.0
%define snapshot 20100912
%define release %mkrel 0.%{snapshot}.2

# Usage: bashcomp_trigger PACKAGENAME [SCRIPTNAME]
%define bashcomp_trigger() \
%triggerin -- %1\
if [ ! -L %{_sysconfdir}/bash_completion.d/%{?2}%{!?2:%1} ] ; then\
    ln -sf ../..%{_datadir}/%{name}/%{?2}%{!?2:%1} %{_sysconfdir}/bash_completion.d\
fi\
%triggerun -- %1\
[ $2 -gt 0 ] || rm -f %{_sysconfdir}/bash_completion.d/%{?2}%{!?2:%1}\
%{nil}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:      1
Summary:	Programmable completion for bash
Group:		Shells
License:	GPL
URL:		http://bash-completion.alioth.debian.org/
Source0:	http://bash-completion.alioth.debian.org/files/%{name}-%{snapshot}.tar.bz2
# configuration: allow to disable slow avahi-browse completion
Patch4:		bash-completion-20100419-avahi-browse.patch
# configuration: allow to disable slow remote scp completion
Patch5:		bash-completion-20100203-scp-remote.patch
# configuration: allow to disable slow rpm database completion
Patch8:		bash-completion-20100203-rpm-database.patch
# configuration: make ~/.bash_completion sourced by profile scriptlet
Patch10:	bash-completion-20100203-disable-user-completion.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash.

%prep
%setup -q -n %{name}-%{snapshot}
%patch4 -p 1
%patch5 -p 1
%patch8 -p 1
%patch10 -p 1
autoreconf -i

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# adapt installation
rm -f %{buildroot}%_sysconfdir/profile.d/bash_completion.sh

install -d -m 755 %{buildroot}%{_datadir}/bash-completion
mv %{buildroot}%_sysconfdir/bash_completion.d/* \
    %{buildroot}%{_datadir}/bash-completion

pushd %{buildroot}%_sysconfdir/bash_completion.d
ln -s ../..%{_datadir}/bash-completion/helpers .
popd

mkdir -p %{buildroot}%_sysconfdir/profile.d/
cat <<'EOF' >> %{buildroot}%_sysconfdir/profile.d/20bash-completion.sh
#!/bin/sh
# system-wide activation
if [ "$PS1" ]  && [ -n "$BASH" ]; then
    # source system wide config file
	. %_sysconfdir/sysconfig/bash-completion
    # source user config file if available,
    if [ -f $HOME/.bash_completion ]; then
        . $HOME/.bash_completion
    fi

    if [ -n "$ENABLE_BASH_COMPLETION" ]; then
        . %_sysconfdir/bash_completion
    fi
fi
EOF

mkdir -p %{buildroot}%_sysconfdir/sysconfig
cat <<'EOF' >> %{buildroot}%_sysconfdir/sysconfig/bash-completion
# bash completion global configuration

# enable bash completion
ENABLE_BASH_COMPLETION=1
# enable remote cvs completion
COMP_CVS_REMOTE=
# enable remote scp completion
COMP_SCP_REMOTE=
# enable configure arguments completion
COMP_CONFIGURE_HINTS=
# enable tar archive internal path completion
COMP_TAR_INTERNAL_PATHS=
# enable wireless uid completion
COMP_IWLIST_SCAN=
# enable installed packages completion
COMP_RPM_DATABASE=
# enable zeroconf hostnames completion
COMP_AVAHI_BROWSE=
EOF

mkdir -p %{buildroot}%_sysconfdir/skel
cat <<'EOF' >> %{buildroot}%_sysconfdir/skel/.bash_completion
# bash completion local configuration

# enable bash completion
#ENABLE_BASH_COMPLETION=1
# enable remote cvs completion
#COMP_CVS_REMOTE=
# enable remote scp completion
#COMP_SCP_REMOTE=
# enable configure arguments completion
#COMP_CONFIGURE_HINTS=
# enable tar archive internal path completion
#COMP_TAR_INTERNAL_PATHS=
# enable wireless uid completion
#COMP_IWCONFIG_SCAN=
# enable installed packages completion
#COMP_RPM_DATABASE=
# enable zeroconf hostnames completion
#COMP_AVAHI_BROWSE=
EOF

cat > README.install.urpmi <<EOF
Mandriva RPM specific notes

Programmable bash completion except for slow completions is enabled
by default. These settings can be changed system-wide in
/etc/sysconfig/bash-completion. Users may override these settings in
their ~/.bash_completion files. New users get a skeleton
configuration file automatically, while existing users can copy
/etc/skel/.bash_completion into their home directories if they want
to edit their completion settings.
EOF

install -d -m 755 %{buildroot}%{_bindir}
install -m 755 install-completions %{buildroot}%{_bindir}/install-completions

# Combine to per-package files to work around #60699
pushd %{buildroot}%{_datadir}/bash-completion
( echo ; cat procps ) >> sysctl
rm procps
( echo ; cat chsh ; echo ; cat mount ; echo ; cat rtcwake ) >> util-linux-ng
rm chsh mount rtcwake
( echo ; cat iconv; echo ; cat getent ) >> glibc
rm iconv getent
popd

%bashcomp_trigger ant
%bashcomp_trigger apt
%bashcomp_trigger aptitude
%bashcomp_trigger aspell
%bashcomp_trigger autorpm
%bashcomp_trigger bash bash-builtins
%bashcomp_trigger bind-utils
%bashcomp_trigger bitkeeper
%bashcomp_trigger BitTorrent bittorrent
%bashcomp_trigger bluez
%bashcomp_trigger bridge-utils brctl
%bashcomp_trigger bzip2
%bashcomp_trigger cdrkit wodim
%bashcomp_trigger cdrkit-genisoimage genisoimage
%bashcomp_trigger chkconfig
%bashcomp_trigger cksfv
%bashcomp_trigger clisp
%bashcomp_trigger coreutils dd
%bashcomp_trigger cpio
%bashcomp_trigger cups-clients cups
%bashcomp_trigger cryptsetup
%bashcomp_trigger cvsnt,cvs cvs
%bashcomp_trigger dhcp-client dhclient
%bashcomp_trigger dict
%bashcomp_trigger dpkg
%bashcomp_trigger dsniff
%bashcomp_trigger expat xmlwf
%bashcomp_trigger findutils
%bashcomp_trigger freeciv-client,freeciv-server freeciv
%bashcomp_trigger gcc-ada gnatmake
%bashcomp_trigger gcc,gcc-java,fortran,gcc-c++ gcc
%bashcomp_trigger gcl
%bashcomp_trigger gdb
%bashcomp_trigger gkrellm
%bashcomp_trigger glibc
%bashcomp_trigger gnupg2 gpg2
%bashcomp_trigger gnupg gpg
%bashcomp_trigger gzip
%bashcomp_trigger heimdal-workstation heimdal
%bashcomp_trigger hping2
%bashcomp_trigger imagemagick
%bashcomp_trigger initscripts service
%bashcomp_trigger info,pinfo info
%bashcomp_trigger ipmitool
%bashcomp_trigger iptables
%bashcomp_trigger jar
%bashcomp_trigger java-sun-jre,java-gcj-compat java
%bashcomp_trigger kdelibs dcop
%bashcomp_trigger ldapvi
%bashcomp_trigger lftp
%bashcomp_trigger libxml2-progs xmllint
%bashcomp_trigger lilo
%bashcomp_trigger lilypond
%bashcomp_trigger links
%bashcomp_trigger lvm2 lvm
%bashcomp_trigger lzma,xz lzma
%bashcomp_trigger lzop
%bashcomp_trigger mailman
%bashcomp_trigger make
%bashcomp_trigger man
%bashcomp_trigger mc
%bashcomp_trigger mcrypt
%bashcomp_trigger mdadm
%bashcomp_trigger medusa
%bashcomp_trigger minicom
%bashcomp_trigger mkinitrd
%bashcomp_trigger mplayer
%bashcomp_trigger mtx
%bashcomp_trigger multisync-msynctool,msynctool msynctool
%bashcomp_trigger munin-node
%bashcomp_trigger mutt
%bashcomp_trigger mysql-client mysqladmin
%bashcomp_trigger ncftp
%bashcomp_trigger net-tools
%bashcomp_trigger nfs-utils rpcdebug
%bashcomp_trigger nmap
%bashcomp_trigger ntp-client ntpdate
%bashcomp_trigger openldap
%bashcomp_trigger openssh-clients ssh
%bashcomp_trigger openssl-tools openssl
%bashcomp_trigger pcmciautils cardctl
%bashcomp_trigger perl-base perl
%bashcomp_trigger pine
%bashcomp_trigger pkgconfig pkg-config
%bashcomp_trigger poldek
%bashcomp_trigger postfix
%bashcomp_trigger postgresql-clients postgresql
%bashcomp_trigger povray
%bashcomp_trigger procps procps
%bashcomp_trigger pwdutils shadow
%bashcomp_trigger util-linux-ng
%bashcomp_trigger python
%bashcomp_trigger qemu
%bashcomp_trigger qt4-qtdbus qdbus
%bashcomp_trigger quota-tools
%bashcomp_trigger rcs
%bashcomp_trigger rdesktop
%bashcomp_trigger resolvconf
%bashcomp_trigger rfkill
%bashcomp_trigger rpm
%bashcomp_trigger rrdtool
%bashcomp_trigger rsync
%bashcomp_trigger ruby-modules ri
%bashcomp_trigger samba-client samba
%bashcomp_trigger sbcl
%bashcomp_trigger screen
%bashcomp_trigger sitecopy
%bashcomp_trigger smartmontools smartctl
%bashcomp_trigger snownews
%bashcomp_trigger strace
%bashcomp_trigger svk
%bashcomp_trigger tar
%bashcomp_trigger tcpdump
%bashcomp_trigger tightvnc vncviewer
%bashcomp_trigger unace
%bashcomp_trigger unixODBC isql
%bashcomp_trigger unrar
%bashcomp_trigger update-alternatives
%bashcomp_trigger vpnc
%bashcomp_trigger wireless-tools
%bashcomp_trigger wvdial
%bashcomp_trigger xhost
%bashcomp_trigger xrandr
%bashcomp_trigger xen xm
%bashcomp_trigger libxml2-utils xmllint
%bashcomp_trigger xmms
%bashcomp_trigger xrandr
%bashcomp_trigger xhost
%bashcomp_trigger xz
%bashcomp_trigger yp-tools
%bashcomp_trigger yum
%bashcomp_trigger yum-arch

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README README.*.urpmi TODO
%{_bindir}/install-completions
%{_sysconfdir}/bash_completion
%{_sysconfdir}/bash_completion.d
%{_sysconfdir}/profile.d/20bash-completion.sh
%{_datadir}/bash-completion
%config(noreplace) %{_sysconfdir}/sysconfig/bash-completion
%config(noreplace) %{_sysconfdir}/skel/.bash_completion


