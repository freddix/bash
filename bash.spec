%define		ver		4.2
%define		patchlevel	037

Summary:	GNU Bourne Again Shell (bash)
Name:		bash
Version:	%{ver}.%{patchlevel}
Release:	7
License:	GPL
Group:		Applications/Shells
Source0:	ftp://ftp.gnu.org/gnu/bash/%{name}-%{ver}.tar.gz
# Source0-md5:	3fb927c7c33022f1c327f14a81c0d4b0
Source1:	%{name}rc
Source2:	.%{name}_logout
Source3:	.%{name}_profile
Source4:	.%{name}rc
#
Patch0:		%{name}-paths.patch
Patch1000:	%{name}-patchlevel-%{patchlevel}.patch
URL:		http://www.gnu.org/software/bash/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
Requires(postun):	/usr/sbin/postshell
Requires:	grep
Requires:	core
Provides:	/bin/bash
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bash is a GNU project sh-compatible shell or command language
interpreter.

%prep
%setup -qn %{name}-%{ver}
%patch1000 -p0

%patch0 -p1

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

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_bindir}/bashbug

%find_lang %{name}

%check
#%{__make} tests

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

