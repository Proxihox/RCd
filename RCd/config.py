import os
RCNAME = "PCRC"
LOGS = False

# Mailer variables
VERIFY_MAIL = True
MAIL_SENDER = "example@gmail.com"



# Network variables

PORT = int(os.environ.get("PORT", 8080))
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
