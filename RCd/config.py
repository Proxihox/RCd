import os
RCNAME = "PCRC"
LOGS = False

# Mailer variables
VERIFY_MAIL = True # Do you want email verification?
MAIL_SENDER = "example@gmail.com" # The email ID from which you'll send mails like OTP for registration



# Network variables

PORT = int(os.environ.get("PORT", 8080)) # You can change the port number from 8080 to anything of your choice. 
SERVER = "0.0.0.0"

# Prevent spamming
QUERY_LIMIT = 1000

# Password Security variable
PASSWORD_SECURTIY_LEVEL=3
# 0: No checks
# 1: Minimum length
# 2: Minimum length, uppercase, lowercase
# 3: Minimum length, uppercase, lowercase, digits
# 4: Minimum length, uppercase, lowercase, digits, special symbols
# 5: Minimum length, uppercase, lowercase, digits, special symbols, username not in password
