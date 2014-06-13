Summary:	Programmable completion for bash
Name:		bash-completion
Epoch:		2
Version:	2.1
Release:	10
Group:		Shells
License:	GPLv2
Url:		http://bash-completion.alioth.debian.org/
Source0:	http://bash-completion.alioth.debian.org/files/%{name}-%{version}.tar.bz2
# ~/.bash_completion is used for completion variables setting, it has
# to be sourced from profile scriptlet instead of completion code itself
Patch10:	bash-completion-1.99-disable-user-completion.patch
Patch11:        bash-completion-2.1-rpm-distsuffix.patch
Patch12:	bash-completion-2.1-util-linux-223.patch
Patch13:	bash-completion-2.1-fix-readline-quoting.patch
Patch14:	bash-completion-2.1-bad-array-subscript.patch
BuildArch:	noarch

%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash.

%package devel
Summary:	The pkgconfig for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 2:2.1-7

%description devel
The pkgconfig for %{name}.

%prep
%setup -q
%patch10 -p1
%patch11 -p1
%if "%{distepoch}" >= "2013.0"
%patch12 -p1
%endif
%if "%{distepoch}" > "2014.0"
%patch13 -p1
%endif
%patch14 -p1 -b .array~

%build
%configure2_5x
%make

%install
%makeinstall_std

chmod 644 %{buildroot}%{_datadir}/bash-completion/bash_completion

# (tpg) remove files which are in upstream packages
rm -f %{buildroot}%{_datadir}/bash-completion/completions/{nmcli,chsh,su,cal,dmesg,eject,hexdump,ionice,look,renice,hwclock,rtcwake}

# adapt installation
rm -f %{buildroot}%{_sysconfdir}/profile.d/bash_completion.sh

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
cat <<'EOF' >> %{buildroot}%{_sysconfdir}/profile.d/20bash-completion.sh
# Check for interactive bash and that we haven't already been sourced.
if [ -z "$BASH_VERSION" -o -z "$PS1" -o -n "$BASH_COMPLETION_COMPAT_DIR" ]; then
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

cat > README.install.urpmi <<EOF
Programmable bash completion is enabled by default. These settings can be
changed system-wide in /etc/sysconfig/bash-completion. Users may override these
settings in their ~/.bash_completion files. New users get a skeleton
configuration file automatically, while existing users can copy
/etc/skel/.bash_completion into their home directories if they want to edit
their completion settings.
EOF

%triggerpostun -- bash-completion < 2:1.90-3
# drop dangling symlinks resulting from previous setup
find %{_sysconfdir}/bash_completion.d -type l | xargs rm -f

%files
%doc README README.*.urpmi
%{_sysconfdir}/profile.d/20bash-completion.sh
%{_datadir}/bash-completion
%config(noreplace) %{_sysconfdir}/sysconfig/bash-completion
%config(noreplace) %{_sysconfdir}/skel/.bash_completion

%files devel
%{_datadir}/pkgconfig/bash-completion.pc

