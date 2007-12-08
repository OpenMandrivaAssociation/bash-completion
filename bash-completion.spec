%define name	bash-completion
%define version 20060301
%define release %mkrel 18

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Programmable completion for bash
Group:		Shells
License:	GPL
URL:		http://www.caliban.org/bash/
Source0:	http://www.caliban.org/files/bash/%{name}-%{version}.tar.bz2
Patch1:		bash-completion-20050121.device_ids.patch
Patch2:		bash-completion-20060301.alias-completion.patch
Patch5:		bash-completion-20050712.scp-remote.patch
Patch8:		bash-completion-20050721.rpm-database.patch
Patch10:	bash-completion-20050121.disable-user-completion.patch
Patch17:	bash-completion-20060301.evince.patch
Patch18:	bash-completion-20060301.fix-old-rpmfiles-pattern.patch
Patch19:	bash-completion-20060301.kernel-completion.patch
Patch20:    bash-completion-20060301.better-command-completion.patch
Patch21:    bash-completion-20060301.cdrkit-completion.patch
Patch22:    bash-completion-20060301.bibtex.patch
Patch23:    bash-completion-20060301.better-perl-completion.patch
Patch24:	bash-completion-20060301-mplayer-more-completion.patch
Patch25:	bash-completion-20060301-lzma-completion.patch
Patch26: bash_completion-rpm-suggests.patch
Patch27:    bash-completion-20060301-getent-completion.patch
Patch28:    bash-completion-20060301-better-screen-completion.patch
Requires:	bash >= 2.05
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash.

%prep
%setup -q -n bash_completion
%patch1
%patch2
%patch5
%patch8
%patch10
%patch17 -p1 -b .evince
%patch18
%patch19
%patch20
%patch21
%patch22
%patch23
%patch24 -p1 -b .more_formats
%patch25 -p1 -b .lzma_support
%patch26 -p1 -b .rpm-suggests
%patch27
%patch28

chmod 644 contrib/*
rm -f contrib/dsniff
rm -f contrib/freeciv
rm -f contrib/lilypond
rm -f contrib/povray
rm -f contrib/gkrellm
rm -f contrib/cksfv
rm -f contrib/sitecopy
rm -f contrib/mcrypt
rm -f contrib/gnatmake
rm -f contrib/unace
rm -f contrib/unrar
rm -f contrib/snownews
rm -f contrib/mailman
rm -f contrib/bittorrent

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%_sysconfdir/bash_completion.d
install -m 644 bash_completion %{buildroot}%_sysconfdir

mkdir -p %{buildroot}%_sysconfdir/profile.d/
cat <<'EOF' >> %{buildroot}%_sysconfdir/profile.d/bash-completion.sh
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
chmod +x %{buildroot}%_sysconfdir/profile.d/bash-completion.sh

mkdir -p %{buildroot}%_sysconfdir/sysconfig
cat <<'EOF' >> %{buildroot}%_sysconfdir/sysconfig/bash-completion
ENABLE_BASH_COMPLETION=1
COMP_CVS_REMOTE=
COMP_SCP_REMOTE=
COMP_CONFIGURE_HINTS=
COMP_TAR_INTERNAL_PATHS=
COMP_IWLIST_SCAN=
COMP_RPM_DATABASE=
EOF

mkdir -p %{buildroot}%_sysconfdir/skel
cat <<'EOF' >> %{buildroot}%_sysconfdir/skel/.bash_completion
#ENABLE_BASH_COMPLETION=1
#COMP_CVS_REMOTE=
#COMP_SCP_REMOTE=
#COMP_CONFIGURE_HINTS=
#COMP_TAR_INTERNAL_PATHS=
#COMP_IWCONFIG_SCAN=
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

cat > README.20050121-5.upgrade.urpmi <<EOF
Starting from 20050121-5mdk, bash completion activation was modified and is now
more consistant with other user environment activation systems. New users should
automatically get a working configuration, but existing users will have to
remove the explicit sourcing of /etc/bash_completion from their ~/.bashrc.
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README Changelog contrib/* README.*.urpmi
%{_sysconfdir}/bash_completion
%{_sysconfdir}/bash_completion.d
%{_sysconfdir}/profile.d/bash-completion.sh
%config(noreplace) %{_sysconfdir}/sysconfig/bash-completion
%config(noreplace) %{_sysconfdir}/skel/.bash_completion


