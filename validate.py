__author__ = 'pangboww'

import threading
import re
import socks
import smtplib
import dns.resolver
from stem import Signal
from stem.control import Controller


def renew_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="pb3133962")
        controller.signal(Signal.NEWNYM)


def verify_email_in_one_domain(mx_record, emails):
    # Get local server hostname
    host = "bo.com"

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
    in_file = open("email_to_clean", "rb")

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
# for i, j in enumerate(_result):
#         if j:
#             out_file.write(_emails[i] + "\n")

def divide_array(old_array):
    length = len(old_array)
    new_array = []
    size = length / 5
    i = 0
    while i < size:
        sub_array = old_array[i * 5:(i + 1) * 5]
        new_array.append(sub_array)
        i += 1
    sub_array = old_array[i * 5:]
    new_array.append(sub_array)
    return new_array


def execute_thread(emails_by_domain):
    _threads = []
    for domain, emails in emails_by_domain.iteritems():
        if True or domain == "hotmail.com" or domain == "yahoo.com":
            divided_emails = divide_array(emails)
            for sub_emails_array in divided_emails:
                thread = EmailValidationThread(mx_record_cache[domain], sub_emails_array)
                thread.setDaemon(True)
                thread.start()
                _threads.append(thread)

    return _threads


def lookup_mx_record(domain):
    try:
        records = dns.resolver.query(domain, 'MX')
    except:
        return False
    mx_record = records[0].exchange
    return str(mx_record)

mx_record_cache = {}
validate_result = []
emails_to_verify = read_emails_by_domain()

print "Resolving mx domain..."
for i, j in emails_to_verify.iteritems():
    mx_record_cache[i] = lookup_mx_record(i)


proxy_host = "127.0.0.1"
proxy_port = 9050
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_host, proxy_port)
socks.wrap_module(smtplib)
threads = execute_thread(emails_to_verify)
for t in threads:
    t.join(20)

out_file = open("result", "wb")
for i in validate_result:
    out_file.write(i + "\n")
