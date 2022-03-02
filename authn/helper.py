from django.core.mail import send_mail

from django.conf import settings 


def send_forget_password_mail(email , token ):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password https://doctor-consultationapp-shakthi.herokuapp.com/changepassword/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True