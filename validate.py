__author__ = 'pangboww'

from validate_email import validate_email
import threading
import timeit

AMOUNT = 100

start = timeit.timeit()
print "Program start"

in_file = open("email", "rb")
out_file = open("valid_mail_list", "wb")

validate_result = [None] * AMOUNT


class EmailValidationThread(threading.Thread):
    def __init__(self, email, index):
        threading.Thread.__init__(self)
        self.email = email
        self.index = index

    def run(self):
        print "Starting verify " + str(self.index) + " email: " + str(self.email)
        is_valid = validate_email(self.email, verify=True)
        validate_result[self.index] = is_valid
        print "Exiting " + str(self.index) + "email: " + str(self.email)


def read_email(amount):
    mail_list = []
    i = 0
    for line in in_file:
        mail_list.append(line.rstrip())
        i += 1
        if i >= amount:
            break

    return mail_list


def write_result(_emails, _result):
    for i, j in enumerate(_result):
        if j:
            out_file.write(_emails[i] + "\n")


def execute_thread(_emails):
    _threads = []
    for index, email in enumerate(_emails):
        thread = EmailValidationThread(email, index)
        thread.start()
        _threads.append(thread)
    return _threads


emails = read_email(AMOUNT)
threads = execute_thread(emails)
for t in threads:
    t.join()

write_result(emails, validate_result)
end = timeit.timeit()
time = end - start
print "Program end"
print "Execution time: " + str(time)