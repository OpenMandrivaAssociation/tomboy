%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		tomboy
Version:	1.15.9
Release:	1
Summary:	Desktop note-taking application for Linux and Unix
Group:		Graphical desktop/GNOME
# Tomboy itself is LGPL+
# libtomboy contains GPL+ code
License:	LGPL+ and GPLv2+
URL:		http://www.gnome.org/projects/tomboy/
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
#gw we need an UTF-8 locale for gmcs to allow non-ASCII source files
BuildRequires:	locales-en
###
#for autoreconf
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
###
#BuildRequires:	mono(gmcs)
BuildRequires:	mono
BuildRequires:	pkgconfig(mono) >= 1.9.1
BuildRequires:	pkgconfig(mono-addins)
#BuildRequires:  pkgconfig(mono-nunit)
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.14.0
BuildRequires:	pkgconfig(dbus-sharp-glib-1.0) >= 0.3
BuildRequires:	pkgconfig(gconf-sharp-2.0)
BuildRequires:	pkgconfig(gtkspell-2.0) >= 2.0.9
BuildRequires:	pkgconfig(gmime-sharp-2.6)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(galago-sharp) >= 0.5.0

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
%setup -q

%build
%configure2_5x \
	--enable-galago=no \
	--enable-panel-applet=no \
	--disable-scrollkeeper \
	--disable-update-mimedb \
	--disable-schemas-install \
	--enable-gnome=no \
	--enable-tests=no
make

%install
%makeinstall_std

%find_lang %{name} --with-gnome

#we don't want these
rm -f %{buildroot}%{_libdir}/tomboy/libtomboy.la

%preun
%preun_uninstall_gconf_schemas %{name}

%files -f %{name}.lang
%doc NEWS README AUTHORS
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_mandir}/man1/%name.1*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/tomboy*
%{_datadir}/icons/hicolor/*/mimetypes/application-x-note.*
%{_datadir}/mime/packages/tomboy.xml
%{_datadir}/%{name}
%{_libdir}/%{name}/libtomboy.so
%{_libdir}/%{name}/Tomboy.exe
%{_libdir}/%{name}/Tomboy.exe.config
%{_libdir}/%{name}/Tomboy.exe.mdb
%{_libdir}/%{name}/addins/
%{_libdir}/pkgconfig/tomboy-addins.pc
%{_datadir}/dbus-1/services/org.gnome.Tomboy.service
