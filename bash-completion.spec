%define _python_bytecompile_errors_terminate_build 0
%undefine _debugsource_packages

Summary:	Programmable completion for bash
Name:		bash-completion
Epoch:		2
Version:	2.16.0
Release:	1
Group:		Shells
License:	GPLv2
Url:		https://github.com/scop/bash-completion/releases
Source0:	https://github.com/scop/bash-completion/releases/download/%{version}/%{name}-%{version}.tar.xz
# libarchive tar is better than gtar in many ways -- among other things
# its ability to un"tar" zip files, iso files and more. Let's teach
# bash-completions what our tar can do.
Patch11:	bash-completion-2.10-tar-libarchive-extras.patch
BuildArch:	noarch
BuildSystem:	autotools

%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash.

%package devel
Summary:	Development files for for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 2:2.1-7

%description devel
Development files and headers files for %{name}.

%install -a
chmod 644 %{buildroot}%{_datadir}/bash-completion/bash_completion

# (tpg) remove files which are in upstream packages
rm -f %{buildroot}%{_datadir}/bash-completion/completions/{nmcli,chsh,su,cal,dmesg,eject,hexdump,ionice,look,mount,umount,renice,hwclock,rtcwake,rfkill}

# adapt installation
rm -f %{buildroot}%{_sysconfdir}/profile.d/bash_completion.sh

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
cat <<'EOF' >> %{buildroot}%{_sysconfdir}/profile.d/20bash-completion.sh
# Check for interactive bash and that we haven't already been sourced.
if [ -z "$BASH_VERSION" ] || [ -z "$PS1" ] || [ -n "$BASH_COMPLETION_COMPAT_DIR" ]; then
    return
fi

# source system wide config file
. %{_sysconfdir}/sysconfig/bash-completion

# source user config file if available,
if [ -f $HOME/.bash_completion ]; then
    . $HOME/.bash_completion
fi

if [ -n "$ENABLE_BASH_COMPLETION" ]; then
    . %{_datadir}/bash-completion/bash_completion
fi
EOF

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat <<'EOF' >> %{buildroot}%{_sysconfdir}/sysconfig/bash-completion
# bash completion global configuration

# enable bash completion
ENABLE_BASH_COMPLETION=1
# enable remote cvs completion
COMP_CVS_REMOTE=
# enable configure arguments completion
COMP_CONFIGURE_HINTS=
# enable tar archive internal path completion
COMP_TAR_INTERNAL_PATHS=
# enable wireless uid completion
COMP_IWLIST_SCAN=
# enable zeroconf hostnames completion
COMP_KNOWN_HOSTS_WITH_AVAHI=
# enable hostfile hostnames completion
COMP_KNOWN_HOSTS_WITH_HOSTFILE=1
EOF

mkdir -p %{buildroot}%{_sysconfdir}/skel
cat <<'EOF' >> %{buildroot}%{_sysconfdir}/skel/.bash_completion
# bash completion local configuration

# enable bash completion
#ENABLE_BASH_COMPLETION=1
# enable remote cvs completion
#COMP_CVS_REMOTE=
# enable configure arguments completion
#COMP_CONFIGURE_HINTS=
# enable tar archive internal path completion
#COMP_TAR_INTERNAL_PATHS=
# enable wireless uid completion
#COMP_IWCONFIG_SCAN=
# enable zeroconf hostnames completion
#COMP_AVAHI_BROWSE=
EOF

%files
%doc README*
%{_sysconfdir}/profile.d/20bash-completion.sh
%{_sysconfdir}/bash_completion.d
%{_datadir}/bash-completion
%config(noreplace) %{_sysconfdir}/sysconfig/bash-completion
%config(noreplace) %{_sysconfdir}/skel/.bash_completion

%files devel
%{_datadir}/pkgconfig/bash-completion.pc
%{_datadir}/cmake/bash-completion/*.cmake
