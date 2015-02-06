%define realname netools
%define modname netools
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A17_%{modname}.ini

Summary:	Networking tools for PHP
Name:		php-%{modname}
Version:	0.2
Release:	32
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/netools
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini.bz2
Patch0:		netools-0.2-php54x.diff
Requires:	php-cli >= 3:5.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	lcrzo-devel
BuildRequires:	libpcap-devel >= 0.7.2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Netools provides tools to deal with devices, TCP and UDP clients/servers, etc.

%prep

%setup -q -n %{modname}-%{version}

%patch0 -p0

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


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.2-31mdv2012.0
+ Revision: 797059
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.2-30
+ Revision: 761273
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2-29
+ Revision: 696449
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2-28
+ Revision: 695445
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2-27
+ Revision: 646666
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2-26mdv2011.0
+ Revision: 629840
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2-25mdv2011.0
+ Revision: 628167
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2-24mdv2011.0
+ Revision: 600513
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2-23mdv2011.0
+ Revision: 588851
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2-22mdv2010.1
+ Revision: 514579
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2-21mdv2010.1
+ Revision: 485410
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2-20mdv2010.1
+ Revision: 468193
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2-19mdv2010.0
+ Revision: 451297
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.2-18mdv2010.0
+ Revision: 397330
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2-17mdv2010.0
+ Revision: 377008
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2-16mdv2009.1
+ Revision: 346521
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2-15mdv2009.1
+ Revision: 341780
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-14mdv2009.1
+ Revision: 321880
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-13mdv2009.1
+ Revision: 310289
- rebuilt against php-5.2.7

* Sat Jul 19 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-12mdv2009.0
+ Revision: 238774
- bump release
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-10mdv2009.0
+ Revision: 200252
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-9mdv2008.1
+ Revision: 162126
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-8mdv2008.1
+ Revision: 107694
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-7mdv2008.0
+ Revision: 77562
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-6mdv2008.0
+ Revision: 39510
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-5mdv2008.0
+ Revision: 33864
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-4mdv2008.0
+ Revision: 21343
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-3mdv2007.0
+ Revision: 117601
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-2mdv2007.0
+ Revision: 78092
- rebuilt for php-5.2.0
- Import php-netools

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-1
- rebuilt for php-5.1.6

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-5
- rebuilt for php-4.4.4

* Sun Aug 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-4mdv2007.0
- rebuilt for php-4.4.3

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-3mdk
- rebuild

* Mon Jan 16 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-2mdk
- rebuilt against php-4.4.2

* Wed Nov 02 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-1mdk
- rebuilt for php-4.4.1
- fix versioning

* Thu Jul 14 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0_0.2-2mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Tue Jul 12 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-1mdk
- rebuilt for php-4.4.0 final

* Wed Jul 06 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-0.RC2.1mdk
- rebuilt for php-4.4.0RC2

* Wed Jun 15 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0_0.2-0.RC1.1mdk
- rebuilt for php-4.4.0RC1

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_0.2-1mdk
- renamed to php4-*

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_0.2-1mdk
- 4.3.11

* Mon Mar 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.2-4mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.2-3mdk
- rebuilt against a non hardened-php aware php lib

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.2-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.2-1mdk
- rebuild for php 4.3.10

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_0.2-1mdk
- rebuild for php 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_0.2-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_0.2-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_0.2-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.2-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php4.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.2-1mdk
- fix url
- built for php 4.3.6

