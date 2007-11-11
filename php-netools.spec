%define realname netools
%define modname netools
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A17_%{modname}.ini

Summary:	Networking tools for PHP
Name:		php-%{modname}
Version:	0.2
Release:	%mkrel 8
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/netools
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini.bz2
Requires:	php-cli >= 3:5.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	lcrzo-devel
BuildRequires:	libpcap-devel >= 0.7.2
BuildRoot:	%{_tmppath}/%{name}-root

%description
Netools provides tools to deal with devices, TCP and UDP clients/servers, etc.

%prep

%setup -q -n %{modname}-%{version}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS netools.php README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
