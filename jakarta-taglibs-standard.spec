# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name       standard
%define short_name      taglibs-%{base_name}

Name:           jakarta-taglibs-standard
Version:        1.1.1
Release:        11.4%{?dist}
Epoch:          0
Summary:        An open-source implementation of the JSP Standard Tag Library
License:        ASL 2.0
Group:          Development/Libraries/Java
URL:            http://jakarta.apache.org/taglibs/
Source:         http://archive.apache.org/dist/jakarta/taglibs/standard/source/jakarta-taglibs-standard-1.1.1-src.tar.gz
Patch0:         jakarta-taglibs-standard-%{version}-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.5.30
BuildRequires:  ant
BuildRequires:  apache-tomcat-apis
BuildRequires:  xalan-j2 >= 2.6.0
Requires:       apache-tomcat-apis
Requires:       xalan-j2 >= 2.6.0

%description
This package contains Jakarta Taglibs's open-source implementation of the 
JSP Standard Tag Library (JSTL), version 1.1. JSTL is a standard under the
Java Community Process.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
BuildRequires:  java-javadoc

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{name}-%{version}-src
%patch0 -b .orig
cat > build.properties <<EOBP
build.dir=build
dist.dir=dist
servlet24.jar=$(build-classpath apache-tomcat-apis/tomcat-servlet2.4-api)
jsp20.jar=$(build-classpath apache-tomcat-apis/tomcat-jsp2.0-api)
jaxp-api.jar=$(build-classpath xalan-j2)
EOBP

%build

ant \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -f standard/build.xml \
  dist


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p standard/dist/standard/lib/jstl.jar $RPM_BUILD_ROOT%{_javadir}/jakarta-taglibs-core-%{version}.jar
cp -p standard/dist/standard/lib/standard.jar $RPM_BUILD_ROOT%{_javadir}/jakarta-taglibs-standard-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr standard/dist/standard/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc standard/README_src.txt standard/README_bin.txt standard/dist/doc/doc/standard-doc/*.html
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Tue Feb 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.1-11.4
- Drop gcj_support.
- Use apache-tomcat-apis instead of tomcat5-*.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.1.1-11.3
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-11.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-10.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1.1-9.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.1.1-9jpp.1
- Autorebuild for GCC 4.3

* Wed Mar 21 2007 Matt Wringe <mwringe@redhat.com> 0:1.1.1-8jpp.1
- Merge with latest jpp version
- Fix various rpmlint warnings

* Wed Mar 21 2007 Matt Wringe <mwringe@redhat.com> 0:1.1.1-8jpp
- Fix empty javadoc post and postun rpmlint warnings
- Update copyright year

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> 0:1.1.1-7jpp.1
- Merge with upstream version
 - Add missing javadoc postun
 - Add missing javadoc requires

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 1.1.1-6jpp_3fc
- Requires(post): coreutils

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.1.1-6jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> 0:1.1.1-6jpp_1fc
- Merge with upstream version
- Natively compile package

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> 0:1.1.1-6jpp
- Add conditional native compilation
- Add missing BuildRequires and Requires for tomcat5-jsp-2.0-api and xalan-j2
  (from Deepak Bhole <dbhole at redhat.com>)

* Thu Apr 27 2006 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-5jpp
- First JPP 1.7 build

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-4jpp
- Rebuild to replace incorrect patch file

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-3jpp
- Remove hack for 1.3 Java that would break building with an IBM SDK.

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.1.1-2jpp
- Rebuild with ant-1.6.2

* Tue Jul 27 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.1.1-1jpp
- 1.1.1

* Tue Feb 17 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.1.0-1jpp
- 1.1.0 final

* Wed Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.1.0-0.B1.2jpp
- change URL
- fix description

* Fri Jan  9 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.1.0-0.B1.1jpp
- First build for JPackage

* Mon Dec 22 2003 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.1.0-0.B1.1
- First build
- Skip examples for now

