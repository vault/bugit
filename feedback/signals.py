from common.models import User
from django.core.mail import send_mail

def mail_staff(sender, **kwargs):
    message = kwargs['instance']
    if message.sent or kwargs['raw']:
        return

    staff = User.objects.filter(is_staff=True)
    emails = [u.email for u in staff]

    send_mail("[Git Feedback] " + message.subject, message.message,
            message.sender.email, emails)
    message.sent = True

