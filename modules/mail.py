import salt

def send(recipient, subject, body):
	__salt__['event.send']('mail/send', subject=subject, recipient=recipient, body=body)
