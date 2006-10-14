#%%define prerelease rc1

Summary:        Email filter with virus scanner and spamassassin support
Name:           amavisd-new
Version:        2.4.3
Release:        2%{?prerelease:.%{prerelease}}%{?dist}
License:        GPL
Group:          Applications/System
URL:            http://www.ijs.si/software/amavisd/
Source0:        http://www.ijs.si/software/amavisd/amavisd-new-%{version}%{?prerelease:-%{prerelease}}.tar.gz
Source1:        amavis-clamd.init
Source2:        amavis-clamd.conf
Source3:        amavis-clamd.sysconfig
Source4:        README.fedora
Source5:        README.quarantine
Source6:        amavisd.cron
Patch0:         amavisd-conf.patch
Patch1:         amavisd-init.patch
Patch2:         amavisd-condrestart.patch
Patch3:         amavisd-db.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-root/
Requires:       smtpdaemon
Requires:       /usr/sbin/clamd, /etc/clamd.d
Requires:       /usr/sbin/tmpwatch, /etc/cron.daily
Requires:       bzip2
Requires:       gzip
Requires:       arj
Requires:       cpio
Requires:       freeze
Requires:       lzop
Requires:       nomarch
Requires:       cabextract
Requires:       /usr/bin/ar
# We probably should parse the fetch_modules() code in amavisd for this list.
# These are just the dependencies that don't get picked up otherwise.
Requires:       perl(IO::Stringy)
Requires:       perl(MIME::Body)
Requires:       perl(MIME::Decoder::Base64)
Requires:       perl(MIME::Decoder::Binary)
Requires:       perl(MIME::Decoder::Gzip64)
Requires:       perl(MIME::Decoder::NBit)
Requires:       perl(MIME::Decoder::QuotedPrint)
Requires:       perl(MIME::Decoder::UU)
Requires:       perl(MIME::Head)
Requires:       perl(Mail::Field)
Requires:       perl(Mail::Header)
Requires:       perl(Mail::Internet)
Requires:       perl(Mail::SpamAssassin)
Requires:       perl(Archive::Tar)
Requires:       perl(Archive::Zip)
Requires:       perl(Convert::TNEF)
Requires:       perl(Convert::UUlib)
Requires:       perl(URI)
Requires:       perl(Net::DNS)
Requires:       perl(Net::LDAP)
Requires:       perl(DBI)
Requires:       perl(DBD::mysql)
Requires:       perl(DBD::SQLite)
Requires:       perl(Razor2::Client::Version)
Requires:       perl(Authen::SASL)
Requires:       perl(Mail::SPF::Query)
Requires:       perl(Compress::Zlib) >= 1.35
BuildArch:      noarch

%description
amavisd-new is a high-performance and reliable interface between mailer
(MTA) and one or more content checkers: virus scanners, and/or
Mail::SpamAssassin Perl module. It is written in Perl, assuring high
reliability, portability and maintainability. It talks to MTA via (E)SMTP
or LMTP, or by using helper programs. No timing gaps exist in the design
which could cause a mail loss.

%prep
%setup -q -n %{name}-%{version}%{?prerelease:-%{prerelease}}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
install -m644 %{SOURCE4} %{SOURCE5} README_FILES/

%build

%install
rm -rf "$RPM_BUILD_ROOT"

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m755 amavisd $RPM_BUILD_ROOT%{_sbindir}/
( cd $RPM_BUILD_ROOT%{_sbindir} && ln -s clamd clamd.amavisd )

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m755 amavisd-{agent,nanny} $RPM_BUILD_ROOT%{_bindir}/

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m755 amavisd_init.sh $RPM_BUILD_ROOT%{_initrddir}/amavisd
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/clamd.amavisd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/amavisd
install -m644 amavisd.conf $RPM_BUILD_ROOT%{_sysconfdir}/amavisd/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d/amavisd.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/clamd.amavisd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/amavisd

mkdir -p $RPM_BUILD_ROOT/var/spool/amavisd/{tmp,db,quarantine}
touch $RPM_BUILD_ROOT/var/spool/amavisd/clamd.sock
mkdir -p $RPM_BUILD_ROOT/var/run/amavisd/

%clean
rm -rf "$RPM_BUILD_ROOT"

%pre
if ! id amavis > /dev/null 2>&1 ; then
    useradd -r -s /sbin/nologin -d /var/spool/amavisd amavis
fi

%preun
if [ "$1" = 0 ]; then
    chkconfig --del amavisd
    chkconfig --del clamd.amavisd
fi

%post
chkconfig --add amavisd
service amavisd condrestart
chkconfig --add clamd.amavisd
service clamd.amavisd condrestart

%files
%defattr(-,root,root)
%doc AAAREADME.first LDAP.schema LICENSE RELEASE_NOTES TODO
%doc README_FILES test-messages amavisd.conf-*
%dir %{_sysconfdir}/amavisd/
%attr(755,root,root) %{_initrddir}/amavisd
%attr(755,root,root) %{_initrddir}/clamd.amavisd
%config(noreplace) %{_sysconfdir}/amavisd/amavisd.conf
%config(noreplace) %{_sysconfdir}/clamd.d/amavisd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/clamd.amavisd
%config(noreplace) %{_sysconfdir}/cron.daily/amavisd
%{_sbindir}/amavisd
%{_sbindir}/clamd.amavisd
%{_bindir}/amavisd-*
%dir %attr(700,amavis,amavis) /var/spool/amavisd
%dir %attr(700,amavis,amavis) /var/spool/amavisd/tmp
%dir %attr(700,amavis,amavis) /var/spool/amavisd/db
%dir %attr(700,amavis,amavis) /var/spool/amavisd/quarantine
%dir %attr(755,amavis,amavis) /var/run/amavisd
%ghost /var/spool/amavisd/clamd.sock

%changelog
* Sat Oct 14 2006 Steven Pritchard <steve@kspei.com> 2.4.3-2
- Fix permissions on the cron.daily script.

* Tue Oct 10 2006 Steven Pritchard <steve@kspei.com> 2.4.3-1
- Update to 2.4.3.
- Add quarantine directory and instructions for enabling it.
- Add tmpwatch cron script.

* Thu Sep 28 2006 Steven Pritchard <steve@kspei.com> 2.4.2-4
- Drop lha dependency and add arj.

* Sun Sep 17 2006 Steven Pritchard <steve@kspei.com> 2.4.2-3
- Rebuild.

* Wed Aug 02 2006 Steven Pritchard <steve@kspei.com> 2.4.2-2
- Fix path to clamd socket in amavisd-conf.patch.

* Mon Jul 31 2006 Steven Pritchard <steve@kspei.com> 2.4.2-1
- Update to 2.4.2
- Fix permissions on README.fedora (bug #200769)

* Tue Jun 20 2006 Steven Pritchard <steve@kspei.com> 2.4.1-1
- Update to 2.4.1
- Drop zoo dependency due to Extras maintainer security concerns

* Tue Apr 25 2006 Steven Pritchard <steve@kspei.com> 2.4.0-1
- Update to 2.4.0

* Thu Feb 02 2006 Steven Pritchard <steve@kspei.com> 2.3.3-5
- Add dist to Release

* Wed Sep 21 2005 Steven Pritchard <steve@kspei.com> 2.3.3-4
- Add TODO and amavisd.conf-* to %%doc

* Mon Sep 19 2005 Steven Pritchard <steve@kspei.com> 2.3.3-3
- Add amavisd-db.patch to fix the path to the db directory in
  amavisd-agent and amavisd-nanny.  (Thanks to Julien Tognazzi.)

* Fri Sep 02 2005 Steven Pritchard <steve@kspei.com> 2.3.3-2
- Requires: perl(Compress::Zlib) >= 1.35

* Thu Sep 01 2005 Steven Pritchard <steve@kspei.com> 2.3.3-1
- Update to 2.3.3
- Remove explicit dependencies on core perl modules

* Fri Aug 19 2005 Steven Pritchard <steve@kspei.com> 2.3.2-10
- Recommend using 127.0.0.1 instead of localhost in README.fedora
- .deb support requires ar

* Wed Aug 17 2005 Steven Pritchard <steve@kspei.com> 2.3.2-9
- Set $virus_admin, $mailfrom_notify_admin, $mailfrom_notify_recip,
  and $mailfrom_notify_spamadmin to undef in the default config to
  turn off notification emails

* Fri Aug 12 2005 Steven Pritchard <steve@kspei.com> 2.3.2-8
- Add dependencies for freeze, lzop, nomarch, zoo, cabextract

* Wed Jul 27 2005 Steven Pritchard <steve@kspei.com> 2.3.2-7
- Add README.fedora with simplified Postfix instructions

* Mon Jul 25 2005 Steven Pritchard <steve@kspei.com> 2.3.2-6
- Create /var/spool/amavisd/db

* Thu Jul 21 2005 Steven Pritchard <steve@kspei.com> 2.3.2-5
- Add perl(Mail::SPF::Query) (now packaged for Extras) dependency
- Drop /var/log/amavisd since we weren't using it
- Fix paths for clamd.sock and amavisd.pid in a couple of places

* Tue Jul 12 2005 Steven Pritchard <steve@kspei.com> 2.3.2-4
- Add a bunch of other missing Requires (both actually required modules
  and optional modules)

* Tue Jul 12 2005 Steven Pritchard <steve@kspei.com> 2.3.2-3
- Add missing Requires: perl(Convert::TNEF)

* Wed Jul 06 2005 Steven Pritchard <steve@kspei.com> 2.3.2-2
- Fix init script ordering
- Don't enable amavisd by default

* Wed Jul 06 2005 Steven Pritchard <steve@kspei.com> 2.3.2-1
- Update to 2.3.2

* Wed Jun 29 2005 Steven Pritchard <steve@kspei.com> 2.3.2-0.1.rc1
- Update to 2.3.2-rc1
- Fedora Extras clamav integration
- Drop amavisd-syslog.patch (Unix::Syslog is in Extras)

* Mon Feb 23 2004 Steven Pritchard <steve@kspei.com> 0.20030616.p7-0.fdr.0.1
- Add amavisd-syslog.patch to eliminate Unix::Syslog dependency
- Add in clamd helper
- Fix up init script
- Initial package
