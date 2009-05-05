%define name	bash-completion
%define version 1.0
%define release %mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:      1
Summary:	Programmable completion for bash
Group:		Shells
License:	GPL
URL:		http://bash-completion.alioth.debian.org/
Source0:	http://bash-completion.alioth.debian.org/files/%{name}-%{version}.tar.gz
Source1:	to_review.tar.bz2
# configuration: allow to disable slow remote scp completion
Patch5:		bash-completion-20090202-scp-remote.patch
# configuration: allow to disable slow rpm database completion
Patch8:		bash-completion-20090202-rpm-database.patch
# configuration: make ~/.bash_completion sourced by profile scriptlet
Patch10:	bash-completion-20050121-disable-user-completion.patch
Patch28:	bash-completion-20060301-better-screen-completion.patch
Patch30:	bash-completion-20090108-externalise-openssl-completion.patch
Patch31:	bash-completion-20090108-externalise-mkinitrd-completion.patch
Requires:	bash >= 2.05
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash.

%prep
%setup -q
%setup -q -a 1 -T -D
%patch5 -p 1
%patch8 -p 1
%patch10
%patch28
%patch30 -p 1
%patch31 -p 1

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%_sysconfdir/bash_completion.d
install -m 644 bash_completion %{buildroot}%_sysconfdir

install -d -m 755 %{buildroot}%{_datadir}/bash-completion
install -m 644 contrib/* %{buildroot}%{_datadir}/bash-completion
install -m 644 to_review/* %{buildroot}%{_datadir}/bash-completion

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

%triggerin -- bittorent > 5.2.2-3mdv2009.1
ln -sf %{_datadir}/bash-completion/bittorent %{_sysconfdir}/bash_completion.d

%triggerun -- bittorent > 5.2.2-3mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/bittorent
fi

%triggerin -- bluez > 4.27-1mdv2009.1
ln -sf %{_datadir}/bash-completion/bluez-utils %{_sysconfdir}/bash_completion.d

%triggerun -- bluez > 4.27-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/bluez-utils
fi

%triggerin -- bridge-utils > 1.4-2mdv2009.1
ln -sf %{_datadir}/bash-completion/brctl %{_sysconfdir}/bash_completion.d

%triggerun -- bridge-utils > 1.4-2mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/brctl
fi

%triggerin -- cksfv
ln -sf %{_datadir}/bash-completion/cksfv %{_sysconfdir}/bash_completion.d

%triggerun -- cksfv
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/cksfv
fi

%triggerin -- clisp
ln -sf %{_datadir}/bash-completion/clisp %{_sysconfdir}/bash_completion.d

%triggerun -- clisp
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/clisp
fi

%triggerin -- cowsay > 3.03-15mdv2009.1
ln -sf %{_datadir}/bash-completion/cowsay %{_sysconfdir}/bash_completion.d

%triggerun -- cowsay > 3.03-15mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/cowsay
fi

%triggerin -- dsniff > 2.4-0.b2.8mdv2009.1
ln -sf %{_datadir}/bash-completion/dsniff %{_sysconfdir}/bash_completion.d

%triggerun -- dsniff > 2.4-0.b2.8mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/dsniff
fi

%triggerin -- freeciv > 2.1.8-1mdv2009.1
ln -sf %{_datadir}/bash-completion/freeciv %{_sysconfdir}/bash_completion.d

%triggerun -- freeciv > 2.1.8-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/freeciv
fi

%triggerin -- gnupg2
ln -sf %{_datadir}/bash-completion/gpg2 %{_sysconfdir}/bash_completion.d

%triggerun -- gnupg2
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/gpg2
fi

%triggerin -- gkrellm > 2.3.2-1mdv2009.1
ln -sf %{_datadir}/bash-completion/gkrellm %{_sysconfdir}/bash_completion.d

%triggerun -- gkrellm > 2.3.2-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/gkrellm
fi

%triggerin -- heimdal-workstation
ln -sf %{_datadir}/bash-completion/heimdal %{_sysconfdir}/bash_completion.d

%triggerun -- heimdal-workstation
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/heimdal
fi

%triggerin -- unixODBC
ln -sf %{_datadir}/bash-completion/isql %{_sysconfdir}/bash_completion.d

%triggerun -- unixODBC
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/isql
fi

%triggerin -- ldapvi > 1.7-6mdv2009.0
ln -sf %{_datadir}/bash-completion/ldapvi %{_sysconfdir}/bash_completion.d

%triggerun -- ldavpi > 1.7-6mdv2009.0
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/ldapvi
fi

%triggerin -- lilypond > 2.12.2-1mdv2009.1
ln -sf %{_datadir}/bash-completion/lilypond %{_sysconfdir}/bash_completion.d

%triggerun -- lilypond > 2.12.2-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/lilypond
fi

%triggerin -- lzop
ln -sf %{_datadir}/bash-completion/lzop %{_sysconfdir}/bash_completion.d

%triggerun -- lzop
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/lzop
fi

%triggerin -- mcrypt > 2.6.8-1mdv2009.1
ln -sf %{_datadir}/bash-completion/mcrypt %{_sysconfdir}/bash_completion.d

%triggerun -- mcrypt > 2.6.8-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/mcrypt
fi

%triggerin -- minicom > 2.3-5mdv2009.1
ln -sf %{_datadir}/bash-completion/minicom %{_sysconfdir}/bash_completion.d

%triggerun -- minicom > 2.3-5mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/minicom
fi

%triggerin -- monodevelop
ln -sf %{_datadir}/bash-completion/monodevelop %{_sysconfdir}/bash_completion.d

%triggerun -- monodevelop
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/monodevelop
fi

%triggerin -- munin-node > 1.3.4-4mdv2009.1
ln -sf %{_datadir}/bash-completion/munin-node %{_sysconfdir}/bash_completion.d

%triggerun -- munin-node > 1.3.4-4mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/munin-node
fi

%triggerin -- mkinitrd > 6.0.63-9mnb2
ln -sf %{_datadir}/bash-completion/mkinitrd %{_sysconfdir}/bash_completion.d

%triggerun -- mkinitrd > 6.0.63-9mnb2
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/mkinitrd
fi

%triggerin -- net-tools > 1.60-29mdv2009.1
ln -sf %{_datadir}/bash-completion/net-tools %{_sysconfdir}/bash_completion.d

%triggerun -- net-tools > 1.60-29mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/net-tools
fi

%triggerin -- msynctool > 0.22-7mdv2009.0
ln -sf %{_datadir}/bash-completion/msynctool %{_sysconfdir}/bash_completion.d

%triggerun -- msynctool > 0.22-7mdv2009.0
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/msynctool
fi

%triggerin -- nfs-utils > 1:1.1.4-2mdv2009.1
ln -sf %{_datadir}/bash-completion/rpcdebug %{_sysconfdir}/bash_completion.d

%triggerun -- nfs-utils > 1:1.1.4-2mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/rpcdebug
fi

%triggerin -- openldap-clients > 2.4.13-4mdv2009.1
ln -sf %{_datadir}/bash-completion/openldap %{_sysconfdir}/bash_completion.d

%triggerun -- openldap-clients > 2.4.13-4mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/openldap
fi

%triggerin -- openssh-clients
ln -sf %{_datadir}/bash-completion/ssh %{_sysconfdir}/bash_completion.d

%triggerun -- openssh-clients
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/ssh
fi

%triggerin -- openssl > 0.9.8i-4mdv2009.1
ln -sf %{_datadir}/bash-completion/openssl %{_sysconfdir}/bash_completion.d

%triggerun -- openssl > 0.9.8i-4mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/openssl
fi

%triggerin -- perl-CPANPLUS > 0.84-3mdv2009.1
ln -sf %{_datadir}/bash-completion/cpan2dist %{_sysconfdir}/bash_completion.d

%triggerun -- perl-CPANPLUS > 0.84-3mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/cpan2dist
fi

%triggerin -- qemu > 0.9.1-0.r5137.1mdv2009.0
ln -sf %{_datadir}/bash-completion/qemu %{_sysconfdir}/bash_completion.d

%triggerun -- qemu > 0.9.1-0.r5137.1mdv2009.0
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/qemu
fi

%triggerin -- quota > 3.16-4mdv2009.1
ln -sf %{_datadir}/bash-completion/quota-tools %{_sysconfdir}/bash_completion.d

%triggerun -- quota > 3.16-4mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/quota-tools
fi

%triggerin -- rdesktop > 1.6.0-6mdv2009.1
ln -sf %{_datadir}/bash-completion/rdesktop %{_sysconfdir}/bash_completion.d

%triggerun -- rdesktop > 1.6.0-6mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/rdesktop
fi

%triggerin -- rpmcheck > 0.0.2368-7mdv2009.1
ln -sf %{_datadir}/bash-completion/rpmcheck %{_sysconfdir}/bash_completion.d

%triggerun -- rpmcheck > 0.0.2368-7mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/rpmcheck
fi

%triggerin -- samba-clients > 3.2.7-1mdv2009.1
ln -sf %{_datadir}/bash-completion/samba %{_sysconfdir}/bash_completion.d

%triggerun -- samba-clients > 3.2.7-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/samba
fi

%triggerin -- sitecopy
ln -sf %{_datadir}/bash-completion/sitecopy %{_sysconfdir}/bash_completion.d

%triggerun -- sitecopy
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/sitecopy
fi

%triggerin -- smartmontools > 5.38-3mdv2009.0
ln -sf %{_datadir}/bash-completion/smartctl %{_sysconfdir}/bash_completion.d

%triggerun -- smartmontools > 5.38-3mdv2009.0
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/smartctl
fi

%triggerin -- strace > 4.5.18-1mdv2009.1
ln -sf %{_datadir}/bash-completion/strace %{_sysconfdir}/bash_completion.d

%triggerun -- strace > 4.5.18-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/strace
fi

%triggerin -- tightvnc > 1.3.9-17mdv2009.1
ln -sf %{_datadir}/bash-completion/vncviewer %{_sysconfdir}/bash_completion.d

%triggerun -- tightvnc > 1.3.9-17mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/vncviewer
fi

%triggerin -- vpnc > 0.5.3-1mdv2009.1
ln -sf %{_datadir}/bash-completion/vpnc %{_sysconfdir}/bash_completion.d

%triggerun -- vpnc 0.5.3-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/vpnc
fi

%triggerin -- unace
ln -sf %{_datadir}/bash-completion/unace %{_sysconfdir}/bash_completion.d

%triggerun -- unace
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/unace
fi

%triggerin -- unrar > 3.80-1mdv2009.1
ln -sf %{_datadir}/bash-completion/unrar %{_sysconfdir}/bash_completion.d

%triggerun -- unrar > 3.80-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/unrar
fi

%triggerin -- xz
ln -sf %{_datadir}/bash-completion/lzma %{_sysconfdir}/bash_completion.d

%triggerun -- xz
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/lzma
fi

%triggerin -- xen > 3.3.1-1mdv2009.1
ln -sf %{_datadir}/bash-completion/xm %{_sysconfdir}/bash_completion.d

%triggerun -- xen > 3.3.1-1mdv2009.1
if [ $2 = 0 ]; then
    rm -f %{_sysconfdir}/bash_completion.d/xm
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README README.*.urpmi TODO
%{_sysconfdir}/bash_completion
%{_sysconfdir}/bash_completion.d
%{_sysconfdir}/profile.d/20bash-completion.sh
%{_datadir}/bash-completion
%config(noreplace) %{_sysconfdir}/sysconfig/bash-completion
%config(noreplace) %{_sysconfdir}/skel/.bash_completion


