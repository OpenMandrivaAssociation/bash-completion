%define name	bash-completion
%define version 1.1
%define snapshot 20090924
%define release %mkrel 0.%{snapshot}.1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:      1
Summary:	Programmable completion for bash
Group:		Shells
License:	GPL
URL:		http://bash-completion.alioth.debian.org/
Source0:	http://bash-completion.alioth.debian.org/files/%{name}-%{snapshot}.tar.bz2
# configuration: allow to disable slow remote scp completion
Patch5:		bash-completion-20090910-scp-remote.patch
# configuration: allow to disable slow rpm database completion
Patch8:		bash-completion-20090910-rpm-database.patch
# configuration: make ~/.bash_completion sourced by profile scriptlet
Patch10:	bash-completion-20090910-disable-user-completion.patch
Requires:	bash >= 2.05
Requires(postun):	symlinks
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash.

%prep
%setup -q -n %{name}-%{snapshot}
%patch5 -p 1
%patch8 -p 1
%patch10 -p 1

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%_sysconfdir/bash_completion.d
install -m 644 bash_completion %{buildroot}%_sysconfdir

install -d -m 755 %{buildroot}%{_datadir}/bash-completion
install -m 644 contrib/* %{buildroot}%{_datadir}/bash-completion

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

install -d -m 755 %{buildroot}%{_bindir}
install -m 755 install-completions %{buildroot}%{_bindir}/install-completions

%post
%{_bindir}/install-completions -i \
    %{_datadir}/bash-completion \
    %{_sysconfdir}/bash_completion.d

%postun
symlinks -d %{_sysconfdir}/bash_completion.d >/dev/null 2>&1

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


