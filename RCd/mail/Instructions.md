# Setting up the email OTP verification

Recently, google has ramped up its security protection, and as a result, the seemingly simple process of automating a mail is now a bit complicated.


1. Create a new Google Cloud project on [Google Cloud Console](https://console.cloud.google.com/). Make sure you are doing this on the email ID you will use to send the automated OTP's.

2. Open the Gmail API Library (Search for it in the searchbar) and enable the Gmail API for your project.

3. Set up OAuth consent screen (search in searchbar) and add the email ID of the sender as a Tester. We won't be deploying this app, but will keep it in testing phase as that's enough for our needs.

4. Open the credentials tab on the console and create new OAuth Client ID credentials. Choose Desktop App and download the json file. Rename it to credentials.json and move into this directory. 

5. Change the 13th line of the mailer.py and set `MAIL_SENDER` in config.py to your email ID and then run the mailer.py file using `python3 RCd/mail/mailer.py` . It should open a browser which asks you to login to the mail ID and approve sending permissions. This is a one time thing as it will generate a token.json which will be used for all future purposes.

Verify that the mailer is working. You should have recieved a test email sent by the same mail ID.

