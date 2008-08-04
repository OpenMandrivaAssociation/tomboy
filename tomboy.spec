%define build_dbus 1
%define external_addins 1
%define filename %name-%version

Name:           tomboy
Version: 0.11.1
Release: %mkrel 1
Summary: Desktop note-taking application for Linux and Unix
Group:          Graphical desktop/GNOME
License:        LGPL+ and GPLv2+ and MIT
# Tomboy itself is LGPL+
# libtomboy contains GPL+ code
# Mono.Addins is MIT
URL:            http://www.gnome.org/projects/tomboy/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/tomboy/%{filename}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  gtkspell-devel
BuildRequires:  gnome-sharp2-devel
BuildRequires:  libpanel-applet-devel
BuildRequires:  mono-devel
BuildRequires:  galago-sharp
BuildRequires:  gmime-sharp
%if %external_addins
BuildRequires:  mono-addins
%endif
%if %build_dbus
BuildRequires: ndesk-dbus-glib
%endif
BuildRequires: ImageMagick
BuildRequires: automake1.8
BuildRequires: intltool
BuildRequires: gnome-doc-utils
BuildRequires: desktop-file-utils
#gw we need an UTF-8 locale for gmcs to allow non-ASCII source files
BuildRequires: locales-en
#gw dllopened:
Requires: %mklibname gtkspell 0
Requires: %mklibname panel-applet-2_ 0
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
%define _requires_exceptions libtomboy.so

%description
Tomboy is a desktop note-taking application for Linux and Unix. Simple
and easy to use, but with potential to help you organize the ideas and
information you deal with every day. The key to Tomboy's usefulness
lies in the ability to relate notes and ideas together. Using a
WikiWiki-like linking system, organizing ideas is as simple as typing
a name. Branching an idea off is easy as pressing the Link button. And
links between your ideas won't break, even when renaming and
reorganizing them.

%prep
%setup -q -n %filename
rm -rf www/CVS www/img/CVS

%build
export LC_ALL=en_US.UTF-8
#gw trying to work around a build bot problem
export MONO_SHARED_DIR=`pwd`
%if %mdkversion <= 1000
%define __cputoolize true
%define __libtoolize true
%endif
%configure2_5x --enable-galago=yes --disable-scrollkeeper \
%if %external_addins
  --with-mono-addins=system \
%endif
%if !%build_dbus
  --enable-dbus=no
%endif

#gw parallel make broken in 0.11.1
make

%install

%{__rm} -rf ${RPM_BUILD_ROOT} %name.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.la
%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/*/*-{??_??,??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name.lang
done

# fix desktop entries
perl -pi -e "s^\@VERSION\@^%version^" %buildroot%_datadir/applications/*
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Accessories" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/tomboy.desktop

%clean
rm -rf ${RPM_BUILD_ROOT}

%if %mdkversion < 200900
%post
%post_install_gconf_schemas %name
%update_menus
%update_icon_cache hicolor
%update_scrollkeeper
%endif

%preun
%preun_uninstall_gconf_schemas %name

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%clean_scrollkeeper
%endif

%files -f %name.lang
%defattr(-,root,root,-)
%doc NEWS README AUTHORS
# www
%_sysconfdir/gconf/schemas/%name.schemas
%{_bindir}/%{name}
%{_bindir}/tomboy-panel
%dir %{_libdir}/%{name}
%_mandir/man1/%name.1*
%_datadir/applications/*
%_datadir/icons/hicolor/*/apps/tomboy*
%_datadir/%name
%dir %_datadir/omf/%name
%_datadir/omf/%name/tomboy-C.omf
%{_libdir}/%{name}/libtomboy.so
%{_libdir}/%{name}/Tomboy.exe
%{_libdir}/%{name}/Tomboy.exe.config
%{_libdir}/%{name}/Tomboy.exe.mdb
%{_libdir}/bonobo/servers/GNOME_TomboyApplet.server
%if !%external_addins
%{_libdir}/%{name}/Mono.Addins*
%endif
%{_libdir}/%{name}/addins/
%_libdir/pkgconfig/tomboy-addins.pc
%if %build_dbus
%_datadir/dbus-1/services/org.gnome.Tomboy.service
%endif
