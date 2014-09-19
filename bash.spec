# based on PLD Linux spec git://git.pld-linux.org/packages/bash.git

%define		ver		4.3
%define		patchlevel	24

Summary:	GNU Bourne Again Shell
Name:		bash
Version:	%{ver}%{?patchlevel:.%{patchlevel}}
Release:	1
License:	GPL
Group:		Core/Shells
Source0:	ftp://ftp.gnu.org/gnu/bash/%{name}-%{ver}.tar.gz
# Source0-md5:	81348932d5da294953e15d4814c74dd1
Source1:	%{name}rc
Source2:	.%{name}_logout
Source3:	.%{name}_profile
Source4:	.%{name}rc
#
Patch0:		%{name}-paths.patch
%patchset_source -f https://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-%03g 1 %{patchlevel}
URL:		http://www.gnu.org/software/bash/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel >= 6.3
BuildRequires:	texinfo
Requires(postun):	/usr/sbin/postshell
Requires:	grep
Requires:	core
Provides:	/bin/bash
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bash is an sh-compatible shell that incorporates useful features from
the Korn shell (ksh) and C shell (csh). It is intended to conform to
the IEEE POSIX P1003.2/ISO 9945.2 Shell and Tools standard. It offers
functional improvements over sh for both programming and interactive
use. In addition, most sh scripts can be run by Bash without
modification.

%prep
%setup -qn %{name}-%{ver}
%patch0 -p1
%{?patchlevel:%patchset_patch 1 %{patchlevel}}

%build
cp -f /usr/share/automake/config.* support
%{__autoconf}
%configure \
	--enable-readline		\
	--with-curses			\
	--with-installed-readline	\
	--without-bash-malloc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/etc/skel}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/bashrc
echo .so bash.1 > $RPM_BUILD_ROOT%{_mandir}/man1/rbash.1

ln -sf bash $RPM_BUILD_ROOT%{_bindir}/rbash

install %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/.bash_logout
install %{SOURCE3} $RPM_BUILD_ROOT/etc/skel/.bash_profile
install %{SOURCE4} $RPM_BUILD_ROOT/etc/skel/.bashrc

%{__rm} $RPM_BUILD_ROOT%{_bindir}/bashbug

%find_lang %{name}

%if 0
%check
%{__make} check
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p <lua>
%lua_add_etc_shells /usr/bin/bash /usr/bin/rbash
os.execute("/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1")

%preun	-p <lua>
if arg[2] == 0 then
	%lua_remove_etc_shells /usr/bin/bash /usr/bin/rbash
end

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES NEWS README doc/{FAQ,INTRO}

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bashrc
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/skel/.bash_logout
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/skel/.bash_profile
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/skel/.bashrc

%attr(755,root,root) %{_bindir}/bash
%attr(755,root,root) %{_bindir}/rbash

%{_infodir}/bash.info*
%{_mandir}/man1/*

