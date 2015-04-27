#%%global prerelease rc2

Summary:        Email filter with virus scanner and spamassassin support
Name:           amavisd-new
Version:        2.10.1
Release:        4%{?prerelease:.%{prerelease}}%{?dist}
# LDAP schema is GFDL, some helpers are BSD, core is GPLv2+
License:        GPLv2+ and BSD and GFDL
Group:          Applications/System
URL:            http://www.ijs.si/software/amavisd/
Source0:        http://www.ijs.si/software/amavisd/amavisd-new-%{version}%{?prerelease:-%{prerelease}}.tar.xz
Source2:        amavis-clamd.conf
Source4:        README.fedora
Source5:        README.quarantine
Source8:        amavisd-new-tmpfiles.conf
Source9:        amavisd.service
Source10:       amavisd-snmp.service
Source11:       amavisd-clean-tmp.service
Source12:       amavisd-clean-tmp.timer
Source13:       amavisd-clean-quarantine.service
Source14:       amavisd-clean-quarantine.timer
Source15:       amavis-mc.service
Source16:       amavisd-snmp-zmq.service
Patch0:         amavisd-new-2.10.1-conf.patch
Patch1:         amavisd-init.patch
Patch2:         amavisd-condrestart.patch
# Don't source /etc/sysconfig/network in init script; the network check
# is commented out upstream so there's no apparent reason to source it,
# and it can't be relied upon to exist in recent Fedora builds. Mail
# sent upstream to amavis-users ML 2013-05-10. -adamw
Patch3:         amavisd-new-2.8.0-init_network.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  systemd
Requires:       clamav-server
Requires:       clamav-server-systemd
Requires:       tmpwatch
Requires:       binutils
Requires:       altermime
Requires:       arj
Requires:       bzip2
Requires:       cabextract
Requires:       pax
Requires:       file
Requires:       freeze
Requires:       gzip
Requires:       lzop
Requires:       nomarch
Requires:       p7zip, p7zip-plugins
Requires:       tar
Requires:       lrzip
Requires:       unzoo
# We probably should parse the fetch_modules() code in amavisd for this list.
# These are just the dependencies that don't get picked up otherwise.
Requires:       perl(Archive::Tar)
Requires:       perl(Archive::Zip) >= 1.14
Requires:       perl(Authen::SASL)
Requires:       perl(Compress::Zlib) >= 1.35
Requires:       perl(Compress::Raw::Zlib) >= 2.017
Requires:       perl(Convert::TNEF)
Requires:       perl(Convert::UUlib)
Requires:       perl(Crypt::OpenSSL::RSA)
Requires:       perl(DBD::SQLite)
Requires:       perl(DBI)
Requires:       perl(Digest::MD5) >= 2.22
Requires:       perl(Digest::SHA)
Requires:       perl(Digest::SHA1)
Requires:       perl(File::LibMagic)
Requires:       perl(IO::Socket::IP)
Requires:       perl(IO::Socket::SSL)
Requires:       perl(IO::Stringy)
Requires:       perl(MIME::Base64)
Requires:       perl(MIME::Body)
Requires:       perl(MIME::Decoder::Base64)
Requires:       perl(MIME::Decoder::Binary)
Requires:       perl(MIME::Decoder::Gzip64)
Requires:       perl(MIME::Decoder::NBit)
Requires:       perl(MIME::Decoder::QuotedPrint)
Requires:       perl(MIME::Decoder::UU)
Requires:       perl(MIME::Head)
Requires:       perl(MIME::Parser)
Requires:       perl(Mail::DKIM) >= 0.31
Requires:       perl(Mail::Field)
Requires:       perl(Mail::Header)
Requires:       perl(Mail::Internet) >= 1.58
Requires:       perl(Mail::SPF)
Requires:       perl(Mail::SpamAssassin)
Requires:       perl(Net::DNS)
Requires:       perl(Net::LDAP)
Requires:       perl(Net::LibIDN)
Requires:       perl(Net::SSLeay)
Requires:       perl(Net::Server) >= 2.0
Requires:       perl(NetAddr::IP)
Requires:       perl(Razor2::Client::Version)
Requires:       perl(Socket6)
Requires:       perl(Time::HiRes) >= 1.49
Requires:       perl(Unix::Syslog)
Requires:       perl(URI)
Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%package snmp
Group:          Applications/System
Summary:        Exports amavisd SNMP data
Requires:       %{name} = %{version}-%{release}
Requires:       perl(NetSNMP::OID)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%package zeromq
Group:          Applications/System
Summary:        Support for communicating through 0MQ sockets
Requires:       %{name} = %{version}-%{release}
Requires:       perl(ZMQ::Constants)
Requires:       perl(ZMQ::LibZMQ3)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%package snmp-zeromq
Group:          Applications/System
Summary:        Exports amavisd SNMP data and communicates through 0MQ sockets
Requires:       %{name}-zeromq = %{version}-%{release}
Requires:       perl(NetSNMP::OID)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
amavisd-new is a high-performance and reliable interface between mailer
(MTA) and one or more content checkers: virus scanners, and/or
Mail::SpamAssassin Perl module. It is written in Perl, assuring high
reliability, portability and maintainability. It talks to MTA via (E)SMTP
or LMTP, or by using helper programs. No timing gaps exist in the design
which could cause a mail loss.

%description snmp
This package contains the program amavisd-snmp-subagent, which can be
used as a SNMP AgentX, exporting amavisd statistical counters database
(snmp.db) as well as a child process status database (nanny.db) to a
SNMP daemon supporting the AgentX protocol (RFC 2741), such as NET-SNMP.

It is similar to combined existing utility programs amavisd-agent and
amavisd-nanny, but instead of writing results as text to stdout, it
exports data to a SNMP server running on a host (same or remote), making
them available to SNMP clients (such a Cacti or mrtg) for monitoring or
alerting purposes.

%description zeromq
This package adds support for monitoring and communicating with amavisd
and auxiliary services among themselves through 0MQ sockets (also called ZMQ
or ZeroMQ, or Crossroads I/O or XS). This method offers similar features
as current services amavisd-nanny, amavisd-agent and amavisd-snmp-subagent,
but use message passing paradigm instead of communicating through a shared
Berkeley database. This avoids locking contention, so the gain can be
significant for a busy amavisd setup with lots of child processes.

%description snmp-zeromq
This package contains the program amavisd-snmp-subagent-zmq, which can be
used as a SNMP AgentX, exporting amavisd statistical counters database
(snmp.db) as well as a child process status database (nanny.db) to a
SNMP daemon supporting the AgentX protocol (RFC 2741), such as NET-SNMP.
It supports communicating through 0MQ sockets.

%prep
%setup -q -n %{name}-%{version}%{?prerelease:-%{prerelease}}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1

install -p -m 644 %{SOURCE4} %{SOURCE5} README_FILES/
sed -e 's,/var/amavis/amavisd.sock\>,%{_localstatedir}/spool/amavisd/amavisd.sock,' -i amavisd-release

%build

%install
rm -rf $RPM_BUILD_ROOT

install -D -p -m 755 amavisd $RPM_BUILD_ROOT%{_sbindir}/amavisd
install -D -p -m 755 amavisd-snmp-subagent $RPM_BUILD_ROOT%{_sbindir}/amavisd-snmp-subagent
install -D -p -m 755 amavisd-snmp-subagent-zmq $RPM_BUILD_ROOT%{_sbindir}/amavisd-snmp-subagent-zmq

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m 755 amavisd-{agent,nanny,release,signer,status,submit} $RPM_BUILD_ROOT%{_bindir}/
install -p -m 755 amavis-mc $RPM_BUILD_ROOT%{_sbindir}/
install -p -m 755 amavis-services $RPM_BUILD_ROOT%{_bindir}/

install -D -p -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_unitdir}/amavisd.service
install -D -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}/amavisd-snmp.service
install -D -p -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_unitdir}/amavisd-clean-tmp.service
install -D -p -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/amavisd-clean-tmp.timer
install -D -p -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_unitdir}/amavisd-clean-quarantine.service
install -D -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_unitdir}/amavisd-clean-quarantine.timer
install -D -p -m 644 %{SOURCE15} $RPM_BUILD_ROOT%{_unitdir}/amavis-mc.service
install -D -p -m 644 %{SOURCE16} $RPM_BUILD_ROOT%{_unitdir}/amavisd-snmp-zmq.service

install -D -p -m 644 amavisd.conf $RPM_BUILD_ROOT%{_sysconfdir}/amavisd/amavisd.conf
install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d/amavisd.conf

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/spool/amavisd/{tmp,db,quarantine}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/{clamd.amavisd,amavisd}

install -D -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_tmpfilesdir}/amavisd-new.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group amavis > /dev/null || %{_sbindir}/groupadd -r amavis
getent passwd amavis > /dev/null || \
  %{_sbindir}/useradd -r -g amavis -d %{_localstatedir}/spool/amavisd -s /sbin/nologin \
  -c "User for amavisd-new" amavis
exit 0

%preun
%systemd_preun amavisd.service
%systemd_preun amavisd-clean-tmp.service
%systemd_preun amavisd-clean-tmp.timer
%systemd_preun amavisd-clean-quarantine.service
%systemd_preun amavisd-clean-quarantine.timer

%preun snmp
%systemd_preun amavisd-snmp.service

%preun zeromq
%systemd_preun amavis-mc.service

%preun snmp-zeromq
%systemd_preun amavisd-snmp-zmq.service

%post
%systemd_post amavisd.service
%systemd_post amavisd-clean-tmp.service
%systemd_post amavisd-clean-tmp.timer
%systemd_post amavisd-clean-quarantine.service
%systemd_post amavisd-clean-quarantine.timer

systemctl enable amavisd-clean-tmp.timer >/dev/null 2>&1 || :
systemctl start amavisd-clean-tmp.timer >/dev/null 2>&1 || :
systemctl enable amavisd-clean-quarantine.timer >/dev/null 2>&1 || :
systemctl start amavisd-clean-quarantine.timer >/dev/null 2>&1 || :

%post snmp
%systemd_post amavisd-snmp.service

%post zeromq
%systemd_post amavis-mc.service

%post snmp-zeromq
%systemd_post amavisd-snmp-zmq.service

%postun
%systemd_postun_with_restart amavisd.service
%systemd_postun_with_restart amavisd-clean-tmp.service
%systemd_postun_with_restart amavisd-clean-tmp.timer
%systemd_postun_with_restart amavisd-clean-quarantine.service
%systemd_postun_with_restart amavisd-clean-quarantine.timer

%postun snmp
%systemd_postun_with_restart amavisd-snmp.service

%postun zeromq
%systemd_postun_with_restart amavis-mc.service

%postun snmp-zeromq
%systemd_postun_with_restart amavisd-snmp-zmq.service

%files
%defattr(-,root,root,-)
%doc AAAREADME.first LDAP.schema LDAP.ldif RELEASE_NOTES TODO INSTALL
%doc README_FILES test-messages amavisd.conf-* amavisd-custom.conf
%license LICENSE
%dir %{_sysconfdir}/amavisd/
%{_unitdir}/amavisd.service
%{_unitdir}/amavisd-clean-tmp.service
%{_unitdir}/amavisd-clean-tmp.timer
%{_unitdir}/amavisd-clean-quarantine.service
%{_unitdir}/amavisd-clean-quarantine.timer
%config(noreplace) %{_sysconfdir}/amavisd/amavisd.conf
%config(noreplace) %{_sysconfdir}/clamd.d/amavisd.conf
%{_sbindir}/amavisd
%{_bindir}/amavisd-agent
%{_bindir}/amavisd-nanny
%{_bindir}/amavisd-release
%{_bindir}/amavisd-signer
%{_bindir}/amavisd-submit
%dir %attr(750,amavis,amavis) %{_localstatedir}/spool/amavisd
%dir %attr(750,amavis,amavis) %{_localstatedir}/spool/amavisd/tmp
%dir %attr(750,amavis,amavis) %{_localstatedir}/spool/amavisd/db
%dir %attr(750,amavis,amavis) %{_localstatedir}/spool/amavisd/quarantine
%{_tmpfilesdir}/amavisd-new.conf
%dir %attr(755,amavis,amavis) %{_localstatedir}/run/amavisd
%dir %attr(770,amavis,clamupdate) %{_localstatedir}/run/clamd.amavisd

%files snmp
%defattr(-,root,root,-)
%doc AMAVIS-MIB.txt
%{_unitdir}/amavisd-snmp.service
%{_sbindir}/amavisd-snmp-subagent

%files zeromq
%{_unitdir}/amavis-mc.service
%{_sbindir}/amavis-mc
%{_bindir}/amavisd-status
%{_bindir}/amavis-services

%files snmp-zeromq
%{_unitdir}/amavisd-snmp-zmq.service
%{_sbindir}/amavisd-snmp-subagent-zmq

%changelog
* Mon Apr 27 2015 Juan Orti Alcaine <jorti@fedoraproject.org> 2.10.1-4
- Move amavisd socket to /var/run/amavisd

* Thu Apr 09 2015 Juan Orti Alcaine <jorti@fedoraproject.org> 2.10.1-3
- Use license macro

* Thu Feb 26 2015 Robert Scheck <robert@fedoraproject.org> 2.10.1-2
- Replaced requirement to cpio by pax (upstream recommendation)

* Mon Oct 27 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.10.1-1
- Update to 2.10.1
- Patch5 merged upstream

* Sat Oct 25 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.10.0-2
- Improve conf patch to fix amavis-mc daemon
- Add patch to fix imports when SQL is used

* Thu Oct 23 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.10.0-1
- Update to 2.10.0
- Replace IO::Socket::INET6 with IO::Socket::IP
- Review perl dependencies minimum version
- Add subpackages amavisd-new-zeromq and amavisd-new-snmp-zeromq

* Mon Oct 20 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.10.0-0.1.rc2
- Update to 2.10.0-rc2

* Wed Aug 20 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.9.1-3
- Add ExecReload and Wants=postfix.service to systemd unit

* Sun Aug 03 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.9.1-2
- Add patch to fix releasing mail from sql quarantine

* Sat Jun 28 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.9.1-1
- New version 2.9.1

* Fri Jun 27 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.9.0-4
- Change permissions of /var/spool/amavisd folders to 750. Fix bug #906396

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.9.0-2
- Service unit files hardening

* Sun May 11 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.9.0-1
- Update to version 2.9.0
- Rework amavisd-conf.patch
- Enable and start timer units

* Wed Mar 19 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.8.1-3
- Use systemd timer units instead of cronjobs
- Add PrivateDevices to service unit

* Mon Feb 17 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.8.1-2
- Move clamd socket to /var/run/clamd.amavisd
- Add permissions to clamupdate to notify clamd

* Wed Feb 12 2014 Juan Orti Alcaine <jorti@fedoraproject.org> 2.8.1-1
- Update to version 2.8.1
- Add systemd service units
- Add missing dependencies
- Start clamd using instantiated service
- Place tmpfiles conf in _tmpfilesdir
- Use _localstatedir macro

* Mon Dec 02 2013 Robert Scheck <robert@fedoraproject.org> 2.8.0-8
- Commented ripole(1) decoder as the binary is not packaged
- Commented tnef(1) decoder as the perl module is a dependency

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.8.0-6
- Perl 5.18 rebuild

* Fri May 10 2013 Adam Williamson <awilliam@redhat.com> - 2.8.0-5
- init_network.patch: don't source /etc/sysconfig/network in initscript

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Robert Scheck <robert@fedoraproject.org> 2.8.0-3
- Added requirements to lrzip and unzoo for unpacking

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Robert Scheck <robert@fedoraproject.org> 2.8.0-1
- Upgrade to 2.8.0

* Fri Jun 29 2012 Robert Scheck <robert@fedoraproject.org> 2.6.6-3
- Various minor spec file cleanups

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep 18 2011 Steven Pritchard <steve@kspei.com> 2.6.6-1
- Update to 2.6.6.
- Make /var/spool/amavisd g+x (BZ 548234).
- %%ghost /var/run/amavisd and add /etc/tmpfiles.d/amavisd-new-tmpfiles.conf
  (BZ 656544, 676430, 710984, 734271).
- Also add /var/run/clamd.amavisd (which seems to be a bug itself).  Fixes
  BZ 696725.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov  9 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.6.4-2
- 561389 patch from Sandro Janke - change stderr to stdout

* Mon Aug 10 2009 Steven Pritchard <steve@kspei.com> 2.6.4-1
- Update to 2.6.4.
- Make a snmp sub-package for amavisd-snmp-subagent.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Robert Scheck <robert@fedoraproject.org> 2.6.2-3
- Re-diffed amavisd-new configuration patch for no fuzz

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Steven Pritchard <steve@kspei.com> 2.6.2-1
- Update to 2.6.2.
- Drop smtpdaemon dependency (BZ# 438078).

* Tue Jul 15 2008 Steven Pritchard <steve@kspei.com> 2.6.1-1
- Update to 2.6.1.
- Require Crypt::OpenSSL::RSA, Digest::SHA, Digest::SHA1, IO::Socket::SSL,
  Mail::DKIM, Net::SSLeay, NetAddr::IP, and Socket6.

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.2-3
- fix license tag
- fix db patch to apply with fuzz=0

* Sun Aug 12 2007 Steven Pritchard <steve@kspei.com> 2.5.2-2
- Fix pre/preun/post dependencies and improve scriptlets a bit.
- Drop dependencies on DBD::mysql and Mail::SPF::Query.
- Add dependencies on IO::Socket::INET6, Mail::SPF, and altermime.

* Sun Jul 08 2007 Steven Pritchard <steve@kspei.com> 2.5.2-1
- Update to 2.5.2.

* Fri Jun 22 2007 Steven Pritchard <steve@kspei.com> 2.5.2-0.1.rc2
- Update to 2.5.2-rc2.

* Fri Jun 22 2007 Steven Pritchard <steve@kspei.com> 2.5.1-1
- Update to 2.5.1.
- Fix amavis-clamd.conf (bug #237252).
- Update amavisd-conf.patch.
- Require p7zip and tar.
- Improve pre/preun/post scripts.

* Thu Feb 22 2007 Steven Pritchard <steve@kspei.com> 2.4.5-1
- Update to 2.4.5.

* Mon Dec 18 2006 Steven Pritchard <steve@kspei.com> 2.4.4-2
- Fix the path to amavisd.sock in amavisd-release.

* Tue Dec 05 2006 Steven Pritchard <steve@kspei.com> 2.4.4-1
- Update to 2.4.4.

* Fri Dec 01 2006 Steven Pritchard <steve@kspei.com> 2.4.3-5
- Add missing amavisd-release script.

* Tue Nov 14 2006 Steven Pritchard <steve@kspei.com> 2.4.3-4
- Rebuild.

* Tue Nov 14 2006 Steven Pritchard <steve@kspei.com> 2.4.3-3
- Add dependency on file. (#215492)

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
