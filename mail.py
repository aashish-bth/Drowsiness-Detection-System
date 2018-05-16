import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#login with your credentials
user_name = ""
user_pwd = ""

def send_mail(to, website, co_ordinates, msg_distance):
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "About your driver"
	msg['From'] = "DDS App <" + user_name + ">"
	msg['To'] = to
	#print(msg['To'])

	# Create the body of the message (a plain-text and an HTML version).
	TEXT = "Hello,\n\nJust wanted to inform you that your driver detected drowsy.\n\nYour drive current location: "
	Disclaimer = "\n\nDisclaimer- This is an auto generated email, please do not reply to this email."
	BODY = TEXT + website + co_ordinates + "\n\n" + msg_distance + Disclaimer

	html = """\
	<html>
	  <head></head>
	  <body>
		<p><b>Hi!</b></p>
		<p>Just wanted to inform you that your driver detected drowsy.</p>
		<p>Your drive current location: <a href="https://www.google.com/maps/"""+ co_ordinates +"""">Google Map</a>.</p>
		<p>"""+ msg_distance +"""</p>
		<p><b>Disclaimer</b>- This is an auto generated email, please do not reply to this email.</p>
	  </body>
	</html>
	"""
	print ('\nEmail details:\nto = ' + to + '\nfrom = ' + user_name + '\nbody:\n' + BODY)

	part1 = MIMEText(BODY, 'plain')
	part2 = MIMEText(html, 'html')

	msg.attach(part1)
	msg.attach(part2)

	mail = smtplib.SMTP('smtp.gmail.com',587)
	#mail = smtplib.SMTP("smtp.mail.yahoo.com",587)
	mail.ehlo()
	mail.starttls()

	try:
		mail.login(user_name, user_pwd)
		mail.sendmail(msg['From'], msg['To'], msg.as_string())
		print("\nemail sent successfully")
	except smtplib.SMTPAuthenticationError:
		print ("\nInvalid user_name or password.")
	mail.close()

