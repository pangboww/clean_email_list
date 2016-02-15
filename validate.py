__author__ = 'pangboww'

from validate_email import validate_email

in_file = open("name_list", "rb")
out_file = open("valid_mail_list", "wb")

for line in in_file:
    is_valid = validate_email(line, verify=True)
    if is_valid:
        out_file.write(line)
