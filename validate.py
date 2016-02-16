__author__ = 'pangboww'

import threading
import re
import socket
import smtplib
import dns.resolver


def verify_email_in_one_domain(domain, emails):
    # MX record lookup
    records = dns.resolver.query(domain, 'MX')
    mx_record = records[0].exchange
    mx_record = str(mx_record)

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mx_record)
    print "connect to " + mx_record
    server.helo(host)
    server.mail("me@me.com")
    for email in emails:
        code, message = server.rcpt(email)
        print message
        if code == 250:
            validate_result.append(email)
    server.quit()


def read_emails_by_domain():
    in_file = open("email", "rb")

    emails = {}
    for item in in_file:
        email = item.rstrip()
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match:
            domain = email.split('@')[1]
            if domain in emails:
                emails[domain].append(email)
            else:
                emails[domain] = []
                emails[domain].append(email)

    in_file.close()
    return emails


class EmailValidationThread(threading.Thread):
    def __init__(self, domain, emails):
        threading.Thread.__init__(self)
        self.domain = domain
        self.emails = emails

    def run(self):
        print "Starting verify " + str(self.domain)
        verify_email_in_one_domain(self.domain, self.emails)
        print "Exiting " + str(self.domain)


# def write_result(_emails, _result):
#     for i, j in enumerate(_result):
#         if j:
#             out_file.write(_emails[i] + "\n")


def execute_thread(emails_by_domain):
    _threads = []
    for i, j in emails_by_domain.iteritems():
        if i == "hotmail.com" or i == "yahoo.com":
            thread = EmailValidationThread(i, j)
            thread.start()
            _threads.append(thread)
    return _threads

validate_result = []
emails_to_verify = read_emails_by_domain()
threads = execute_thread(emails_to_verify)
for t in threads:
    t.join()

out_file = open("valid_mail_list", "wb")
for i in validate_result:
    out_file.write(i + "\n")
