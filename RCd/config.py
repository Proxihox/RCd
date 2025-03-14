import os
RCNAME = "PCRC"
LOGS = True

# Mailer variables
VERIFY_MAIL = True
MAIL_SENDER = "programmingclubiitm.noreply@gmail.com"



# Network variables

PORT = int(os.environ.get("PORT", 8080))
SERVER = "0.0.0.0"

# Password Security variable
PASSWORD_SECURTIY_LEVEL=1
QUERY_LIMIT = 1000
# 1: No checks 
# 2: Min length of 8 use uppercase and lowercase characters,
# 3: 2 + use digits and special characters and don't use username as password

