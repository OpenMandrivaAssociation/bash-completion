Name:		bash-completion
Version:	2.0
Release:	2
Epoch:		2
Summary:	Programmable completion for bash
Group:		Shells
License:	GPL
URL:		http://bash-completion.alioth.debian.org/
Source0:	http://bash-completion.alioth.debian.org/files/%{name}-%{version}.tar.bz2
# ~/.bash_completion is used for completion variables setting, it has
# to be sourced from profile scriptlet instead of completion code itself
Patch10:	bash-completion-1.99-disable-user-completion.patch
BuildArch:	noarch

%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash.

%prep
%setup -q
%patch10 -p 1

%build
%configure2_5x
%make

%install
%makeinstall_std

chmod 644 %{buildroot}%_datadir/bash-completion/bash_completion

# adapt installation
rm -f %{buildroot}%_sysconfdir/profile.d/bash_completion.sh

mkdir -p %{buildroot}%_sysconfdir/profile.d/
cat <<'EOF' >> %{buildroot}%_sysconfdir/profile.d/20bash-completion.sh
# Check for interactive bash and that we haven't already been sourced.
if [ -z "$BASH_VERSION" -o -z "$PS1" -o -n "$BASH_COMPLETION_COMPAT_DIR" ]; then
    return
fi

# source system wide config file
. %_sysconfdir/sysconfig/bash-completion

# source user config file if available,
if [ -f $HOME/.bash_completion ]; then
    . $HOME/.bash_completion
fi

if [ -n "$ENABLE_BASH_COMPLETION" ]; then
    . %_datadir/bash-completion/bash_completion
fi
EOF

mkdir -p %{buildroot}%_sysconfdir/sysconfig
cat <<'EOF' >> %{buildroot}%_sysconfdir/sysconfig/bash-completion
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

mkdir -p %{buildroot}%_sysconfdir/skel
cat <<'EOF' >> %{buildroot}%_sysconfdir/skel/.bash_completion
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
Mageia RPM specific notes

Programmable bash completion is enabled by default. These settings can be
changed system-wide in /etc/sysconfig/bash-completion. Users may override these
settings in their ~/.bash_completion files. New users get a skeleton
configuration file automatically, while existing users can copy
/etc/skel/.bash_completion into their home directories if they want to edit
their completion settings.
EOF

# This comes with udevadm (systemd) these days
rm %buildroot%_datadir/bash-completion/completions/udevadm

%triggerpostun -- bash-completion < 2:1.90-3.mga2
# drop dangling symlinks resulting from previous setup
find %{_sysconfdir}/bash_completion.d -type l | xargs rm -f

%files
%doc README README.*.urpmi
%{_sysconfdir}/profile.d/20bash-completion.sh
%{_datadir}/bash-completion
%{_datadir}/pkgconfig/bash-completion.pc
%config(noreplace) %{_sysconfdir}/sysconfig/bash-completion
%config(noreplace) %{_sysconfdir}/skel/.bash_completion


%changelog

* Mon Jan 09 2012 guillomovitch <guillomovitch> 2:1.99-1.mga2
+ Revision: 193924
- new version

* Sun Dec 18 2011 doktor5000 <doktor5000> 2:1.90-5.mga2
+ Revision: 183875
- really fix XV EPS completion properly this time (mga#3329)

  + shlomif <shlomif>
    - SPEC cleanup - convert all tabs to spaces

* Fri Dec 16 2011 shlomif <shlomif> 2:1.90-4.mga2
+ Revision: 182495
- Bump the release to 4
- Add a fix for the xv EPS completion - https://bugs.mageia.org/show_bug.cgi?id=3329

* Thu Dec 08 2011 blino <blino> 2:1.90-3.mga2
+ Revision: 179336
- fix path in trigger script

* Sat Nov 26 2011 guillomovitch <guillomovitch> 2:1.90-2.mga2
+ Revision: 172320
- fix upgrade trigger (thanks Anssi)

* Sun Nov 06 2011 guillomovitch <guillomovitch> 2:1.90-1.mga2
+ Revision: 164312
- new version
- drop scp and rpm completion switch patches

* Mon Feb 28 2011 ahmad <ahmad> 2:1.3-2.mga1
+ Revision: 61773
- add patch to adjust helpers dir location to the modified layout we use (Fedora)

* Mon Feb 07 2011 ahmad <ahmad> 2:1.3-1.mga1
+ Revision: 48765
- sync with bash-completion-1.3-1.src.rpm from Mandriva:
  o revert to stable release instead of snapshots, bumping epoch for this
  o fix scp-remote-completion patch
  o fix some triggers

* Tue Jan 11 2011 blino <blino> 1:2.0-0.20101219.1.mga1
+ Revision: 5654
- remove hardcoded distro name
- imported package bash-completion


* Sun Dec 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20101219.1mdv2011.0
+ Revision: 623203
- new snapshot

* Mon Dec 06 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20101206.2mdv2011.0
+ Revision: 612560
- lsof trigger
- new version
- add missing configuration variable

* Sat Nov 06 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20101106.1mdv2011.0
+ Revision: 594337
- new snapshot
- fix modules completion activation
- drop patch4 (disable avahi completion), merged upstream with a different variable name

* Sat Sep 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100912.2mdv2011.0
+ Revision: 579571
- add missing trigger to install service completion (fix #61043)

* Sun Sep 12 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100912.1mdv2011.0
+ Revision: 577777
- new snapshot
- fix some triggers

* Sun Aug 22 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100822.1mdv2011.0
+ Revision: 571965
- new snapshot
- merge completions from different files to workaround 60699 and 60706
- new snapshot

* Mon Aug 09 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100809.1mdv2011.0
+ Revision: 568270
- new snapshot

* Thu Jun 10 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100419.3mdv2010.1
+ Revision: 547809
- really apply avahi-browse patch

* Wed May 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100419.2mdv2010.1
+ Revision: 545367
- patch4: allow to disable slow avahi-browse completion
- fix bluez-utils completion trigrer

* Mon Apr 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100419.1mdv2010.1
+ Revision: 536811
- new snapshot
- add rfkill trigger

* Mon Apr 12 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100412.1mdv2010.1
+ Revision: 533725
- new snapshot (really fix #58382)

* Sat Apr 03 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100403.1mdv2010.1
+ Revision: 530892
- new snapshot, fix #58382

* Wed Mar 31 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100331.1mdv2010.1
+ Revision: 530080
- new snapshot
- fix some triggers

* Sun Mar 21 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100321.2mdv2010.1
+ Revision: 526001
- add a trigger for cryptsetup completion
- new snapshot
- add a trigger for mkinitrd completion

* Wed Feb 03 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.20100203.1mdv2010.1
+ Revision: 500535
- new development snapshot
- no bash completion for munin package, only for munin-node

* Tue Oct 13 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1-1mdv2010.0
+ Revision: 457006
- 1.1 final
- use auto-generated triggers to configure completions

* Thu Sep 24 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1-0.20090924.1mdv2010.0
+ Revision: 448520
- new snapshot
- drop additional source, merged upstream

* Mon Sep 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1-0.20090910.2mdv2010.0
+ Revision: 441117
- fix rpm completion patch
- use a script to install relevant completions, instead of triggers

* Thu Sep 10 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1-0.20090910.1mdv2010.0
+ Revision: 437501
- new snapshot
- drop merged patches

* Sun Aug 30 2009 Eugeni Dodonov <eugeni@mandriva.com> 1:1.0-2mdv2010.0
+ Revision: 422708
- Fixed bash4 issues when path contains spaces (#53145)

* Tue May 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.0-1mdv2010.0
+ Revision: 372315
- first official upstream versionned release

* Thu Feb 12 2009 Guillaume Rousse <guillomovitch@mandriva.org> 20090212-1mdv2009.1
+ Revision: 339929
- new snapshot
- drop merged patches

* Mon Feb 09 2009 Guillaume Rousse <guillomovitch@mandriva.org> 20090209-1mdv2009.1
+ Revision: 339014
- new release
- drop _command completion patch, it breaks strace completion, but fix sudo and other similar command (bug #47517)

* Wed Feb 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 20090204-1mdv2009.1
+ Revision: 337605
- new snapshot

* Tue Feb 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 20090203-1mdv2009.1
+ Revision: 337206
- new snapshot (more patches merged)
- don't install additional completion as documentation, but in %%_datadir/bash-completion
- use trigger to symlink them under %%_sysconfdir/bash_completion.d
- drop old upgrade README

* Mon Feb 02 2009 Guillaume Rousse <guillomovitch@mandriva.org> 20090202-1mdv2009.1
+ Revision: 336665
- new snapshot

* Tue Jan 13 2009 Guillaume Rousse <guillomovitch@mandriva.org> 20090108-2mdv2009.1
+ Revision: 328902
- openssl and mkinitrd completions are now shipped in respective packages
- fix PCI id completion

* Fri Jan 09 2009 Guillaume Rousse <guillomovitch@mandriva.org> 20090108-1mdv2009.1
+ Revision: 327527
- new version
- rediff patches 1, 5, 8, 20, 23, 24, 25
- drop patch 2 (alias completion)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 20060301-23mdv2009.0
+ Revision: 264328
- rebuild early 2009.0 package (before pixel changes)

* Mon Apr 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-22mdv2009.0
+ Revision: 192686
- rediff patch 5 to fix remote host completion with scp

* Wed Mar 19 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 20060301-21mdv2008.1
+ Revision: 188796
- /usr/lib/rpm/mandriva/macros is gone, don't try look after macros in it

* Wed Mar 05 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 20060301-20mdv2008.1
+ Revision: 180166
- be sure to read all macros from /etc/rpm/macros.d/*.macros & /usr/lib/rpm/mandriva/macros (P29)
- add mp2 format as well for mplayer completion

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Dec 08 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-19mdv2008.1
+ Revision: 116509
- document configuration settings
- non-executable and versioned profile scriptlet
- uniformize patches format
- better screen completion
  fix getent completion

* Wed Sep 19 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 20060301-18mdv2008.0
+ Revision: 91004
- fix typo in P25 that broken tar lzma completion

* Wed Sep 12 2007 Anssi Hannula <anssi@mandriva.org> 20060301-17mdv2008.0
+ Revision: 84667
- update documentation, and do not show them on every upgrade

* Tue Sep 04 2007 Götz Waschk <waschk@mandriva.org> 20060301-16mdv2008.0
+ Revision: 79138
- improve rpm suggests patch

* Mon Sep 03 2007 Götz Waschk <waschk@mandriva.org> 20060301-15mdv2008.0
+ Revision: 78543
- add suggests option to rpm completion

* Mon Aug 27 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-14mdv2008.0
+ Revision: 71784
- don't call wrapped command completion twice (fix #32795)

* Thu Jul 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-13mdv2008.0
+ Revision: 53705
- make use configuration override system configuration (fix #31833)

* Sun Jul 15 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 20060301-12mdv2008.0
+ Revision: 52236
- add lzma support (P25)
- add mplayer completion for .flv (flash video), .xvid & .divx (P24)

* Fri Jun 15 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-11mdv2008.0
+ Revision: 39972
- better perl completion


* Mon Mar 05 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-10mdv2007.0
+ Revision: 133084
- add bibtex completion (#29056)

* Wed Feb 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-9mdv2007.1
+ Revision: 121134
- cdrkit completion

* Mon Jan 22 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-8mdv2007.1
+ Revision: 111626
- fix command completion for command without completion function

* Sun Jan 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-7mdv2007.1
+ Revision: 108796
- better completion for command accepting another command as argument

* Fri Dec 08 2006 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-6mdv2007.1
+ Revision: 92220
- add forgotten kernel completion patch, needed by dkms completion
- Import bash-completion

* Tue Sep 05 2006 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-5mdv2007.0
- fix .bash_completion file (COMP_IWCONFIG_SCAN -> COMP_IWLIST_SCAN)

* Tue Sep 05 2006 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-4mdv2007.0
- don't source old rpm files in /etc/bash_completion.d 
- merge mdv-specific informations in a single README.urpmi

* Tue Mar 28 2006 Guillaume Rousse <guillomovitch@mandriva.org> 20060301-3mdk
- drop additional = in alias completion (fix #21738)

* Sat Mar 11 2006 Götz Waschk <waschk@mandriva.org> 20060301-2mdk
- fix patch 17

* Wed Mar 01 2006 Götz Waschk <waschk@mandriva.org> 20060301-1mdk
- patch 17, add evince
- drop patches 6,13,14,15,16

* Wed Mar 01 2006 Götz Waschk <waschk@mandriva.org> 20060301-1mdk
- New release 20060301

* Wed Mar 01 2006 Guillaume Rousse <guillomovitch@mandriva.org> 20050721-5mdk
- add kdvi, dvipdf and advi to dvi file completion (fix bug #20947)

* Fri Jan 27 2006 Guillaume Rousse <guillomovitch@mandriva.org> 20050721-4mdk
- fix known_host completion with bash 3.1

* Thu Dec 22 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050721-3mdk
- fix installed package completion slowliness when used outside of rpm
  completion (thanx pterjan)
- rediff patch8

* Tue Oct 11 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20050721-2mdk
- fix completion for midi files ending with MID (P14)
- %%mkrel

* Sat Jul 23 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050721-1mdk 
- new version
- dropped patch 0, 6, 7, 9, 11 and 12 merged upstream

* Fri Jul 22 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050720-2mdk 
- iconv patch

* Thu Jul 21 2005 Götz Waschk <waschk@mandriva.org> 20050720-1mdk
- New release 20050720

* Thu Jul 14 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050712-1mdk 
- new release
- dropped patches 2, 3 and 4 merged upstream
- rediff patch 5, 7

* Sun Jun 26 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050121-8mdk 
- mc completion patch

* Fri Jun 24 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050121-7mdk 
- fix ssh aliases completion

* Tue Jun 14 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050121-6mdk 
- user config file is ~/.bash_completion, not ~/.bash-completion

* Tue Jun 14 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050121-5mdk 
- rework activation procedure again
- fix lilo labels completion

* Thu May 19 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050121-4mdk 
- make rpm slow database completion optional
- fix mplayer options completion

* Mon May 09 2005 Guillaume Rousse <guillomovitch@mandriva.org> 20050121-3mdk 
- add a bunch of patches waiting for upstream merge (id, getent, iwconfig)
- disable all slow completion by default, including remote scp completion
- rework activation procedure
- drop README.urpmi in favor of README.mdk
- spec cleanup

* Sat Apr 02 2005 Guillaume Rousse <guillomovitch@mandrake.org> 20050121-2mdk 
- fix tcpdump & dhclient completions
- add shellbang in profile script

* Mon Jan 24 2005 Guillaume Rousse <guillomovitch@mandrake.org> 20050121-1mdk
- New release 20050121

* Thu Jan 20 2005 Goetz Waschk <waschk@linux-mandrake.com> 20050120-1mdk
- New release 20050120

* Thu Jan 13 2005 Guillaume Rousse <guillomovitch@mandrake.org> 20050112-1mdk 
- New release
- don't tag scripts as config

* Tue Jan 04 2005 Guillaume Rousse <guillomovitch@mandrake.org> 20050103-1mdk
- New release 20050103

* Fri Oct 29 2004 Guillaume Rousse <guillomovitch@mandrake.org> 20041017-1mdk 
- New release 20041017
- /etc/profile.d config file is back, but disabled
- README.urpmi

* Mon Jul 12 2004 Guillaume Rousse <guillomovitch@mandrakesoft.com> 20040711-1mdk
- New release 20040711

* Sat Jul 10 2004 Guillaume Rousse <guillomovitch@mandrake.org> 20040704-2mdk 
- no more config file in /etc/profile.d, existing users have to 
  explicitely source /etc/bash_completion from their .bashrc now

* Mon Jul 05 2004 Guillaume Rousse <guillomovitch@mandrakesoft.com> 20040704-1mdk
- New release 20040704

* Thu May 27 2004 Götz Waschk <waschk@linux-mandrake.com> 20040526-1mdk
- fix URL
- New release 20040526

* Thu Apr 01 2004 Guillaume Rousse <guillomovitch@mandrake.org> 20040331-1mdk
- new version
- dropped mkisofs patch (merged upstream)

