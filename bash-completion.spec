%define name	bash-completion
%define version 20090202
%define release %mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Programmable completion for bash
Group:		Shells
License:	GPL
URL:		http://www.caliban.org/bash/
Source0:	http://www.caliban.org/files/bash/%{name}-%{version}.tar.bz2
# new helper function: completion on devices PCI and USB ids
Patch1:		bash-completion-20090108-device_ids.patch
# configuration: allow to disable slow remote scp completion
Patch5:		bash-completion-20090202-scp-remote.patch
# configuration: allow to disable slow rpm database completion
Patch8:		bash-completion-20090202-rpm-database.patch
# configuration: make ~/.bash_completion sourced by profile scriptlet
Patch10:	bash-completion-20050121-disable-user-completion.patch
# better function: set words offset before launching foreign completion
Patch20:	bash-completion-20090108-better-command-completion.patch
Patch21:	bash-completion-20060301-cdrkit-completion.patch
Patch22:	bash-completion-20090202-bibtex.patch
# cosmetic: makes _perl function use standard 'if options else' pattern
Patch23:	bash-completion-20090108-more-standard-perl-completion.patch
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
%setup -q -n bash-completion
%patch1 -p 1
%patch5 -p 1
%patch8 -p 1
%patch10
%patch20 -p 1
%patch21
%patch22 -p 1
%patch23 -p 1
%patch28
%patch30 -p 1
%patch31 -p 1

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
rm -f contrib/ssh
rm -f contrib/lzma
rm -f contrib/_subversion
rm -f contrib/svk

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%_sysconfdir/bash_completion.d
install -m 644 bash_completion %{buildroot}%_sysconfdir

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
%doc README contrib README.*.urpmi TODO
%{_sysconfdir}/bash_completion
%{_sysconfdir}/bash_completion.d
%{_sysconfdir}/profile.d/20bash-completion.sh
%config(noreplace) %{_sysconfdir}/sysconfig/bash-completion
%config(noreplace) %{_sysconfdir}/skel/.bash_completion


