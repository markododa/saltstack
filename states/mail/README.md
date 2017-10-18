# Email

The VapourApps e-mail app uses the iRedmail open source e-mail system, which combines several open source tools for sending and receiving e-mail, webmail, mail filtering, antivirus and antispam. The virtual instance is preconfigured to work with the Directory server and will not start if a Directory instance is not running. Users and groups are managed through the directory server.

The following connections should be used for connecting to the e-mail server:

Secure POP3 - Host: %EMAIL_HOST%, Port 995;
Secure IMAP - Host: %EMAIL_HOST%, Port 993;
E-mail sending (Submission) - Host: %EMAIL_HOST%, Port 587

Through the webmail, message filters for a particular user can be created, such as automatic redirection and vacation messages. Webmail is available at https:///mail/

The MX record should contain the public IP address of the VapourApps private cloud, from which port 25 is forwarded to the e-mail instance.

SPF records should be configured accordingly into the public DNS for the domain which was configured in the VapourApps installer:

TXT record containing "v=spf1 mx -all"

DKIM records can be configured into the public DNS. The DKIM public records can be viewed with the command: # amavisd-new showkeys on the E-Mail host.