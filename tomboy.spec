%define build_dbus 1
%define filename %name-%version

Name:           tomboy
Version: 0.6.1
Release: %mkrel 3
Summary: Tomboy is a desktop note-taking application for Linux and Unix
Group:          Graphical desktop/GNOME
License:        LGPL
URL:            http://www.gnome.org/projects/tomboy/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/tomboy/%{filename}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  gtkspell-devel
BuildRequires:  gnome-sharp2
BuildRequires:  libpanel-applet-devel
BuildRequires:  libgnomeprintui-devel
BuildRequires:  mono-devel
BuildRequires:  galago-sharp
BuildRequires:  gmime-sharp
%if %build_dbus
BuildRequires:  dbus-glib-devel
%endif
BuildRequires: perl-XML-Parser
BuildRequires: ImageMagick
BuildRequires: automake1.8
BuildRequires: intltool
BuildRequires: gnome-doc-utils libxslt-proc
BuildRequires: desktop-file-utils
#gw we need an UTF-8 locale for gmcs to allow non-ASCII source files
BuildRequires: locales-en
#gw dllopened:
Requires: %mklibname gtkspell 0
Requires: %mklibname panel-applet-2_ 0
Requires: %mklibname dbus-1_ 3
Requires: %mklibname dbus-glib-1_ 2
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

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
%if !%build_dbus
  --enable-dbus=no
%endif

%make

%install

%{__rm} -rf ${RPM_BUILD_ROOT} %name.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
install -m 644 Tomboy/Plugins/NoteOfTheDay.dll $RPM_BUILD_ROOT%{_libdir}/%{name}/Plugins/
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.la
%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/*/*-{??_??,??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name.lang
done

# menu
mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{_bindir}/%name --tray-icon" \
title="Tomboy" \
longtitle="Desktop note-taking application" \
section="Office/Accessories" \
needs="x11" \
icon="%name.png" \
startup_notify="true" xdg="true"
EOF
# fix desktop entries
perl -pi -e "s^\@VERSION\@^%version^" %buildroot%_datadir/applications/*
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Accessories" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/tomboy.desktop

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
%post_install_gconf_schemas %name
%update_menus
%update_icon_cache hicolor
%update_scrollkeeper

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_menus
%clean_icon_cache hicolor
%clean_scrollkeeper

%files -f %name.lang
%defattr(-,root,root,-)
%doc ChangeLog NEWS README AUTHORS
# www
%_sysconfdir/gconf/schemas/%name.schemas
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%_mandir/man1/%name.1*
%_datadir/applications/*
%_datadir/icons/hicolor/*/apps/tomboy*
%_datadir/pixmaps/tomboy.png
%dir %_datadir/omf/%name
%_datadir/omf/%name/tomboy-C.omf
%{_libdir}/%{name}/libtomboy.so
%{_libdir}/%{name}/Tomboy.exe
%{_libdir}/%{name}/Tomboy.exe.config
%{_libdir}/bonobo/servers/GNOME_TomboyApplet.server
%{_libdir}/tomboy/Plugins/*
%_libdir/pkgconfig/tomboy-plugins.pc
%if %build_dbus
%_datadir/dbus-1/services/org.gnome.Tomboy.service
%endif
%{_menudir}/%{name}

