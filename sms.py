# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC********************************"
auth_token = ""

def send_sms(reciever, website, co_ordinates):
	client = Client(account_sid, auth_token)

	To = reciever
	Text = "\nYour driver detect drowsy.\nYour drive current location: " + website + co_ordinates
	print ('\nSMS details:\nto = ' + To + '\nfrom = +19412709940\nbody: ' + Text)

	client.api.account.messages.create(
		to = To,
		from_ = "+19412709940",
		body = Text)

	print ('\nSMS sent successfully.')
