from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def send_new_register_email(email, firt_name, last_name):
    htmly = get_template("email/thanks_new_register.html")
    context = {
        "email": email,
        "first_name":firt_name,
        "last_name":last_name,
        }
    to_emails = [
        email,
    ]
    subject, from_email = ("Bienvenue chez AfricaRelais", "Khadija  AfricaRelais")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)


def package_status_mail(sender_email, customer_user):
    htmly = get_template("email/package-status.html")
    context = {"sender_email": sender_email, "customer_user": customer_user}
    to_emails = [sender_email, "ahmeth.amar@gmail.com"]
    subject, from_email = ("AfricaRelais", "ahmeth mbacke amar")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)


def assign_deliverymen_email(email):
    htmly = get_template("email/thanks_new_register.html")
    context = {"email": email}
    to_emails = [
        email,
    ]
    subject, from_email = ("Bienvenue chez AfricaRelais", "Khadija  AfricaRelais")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)


# function for all notifi Except for registration notification
def send_notification_email(email, firt_name, last_name, subject, body):
    htmly = get_template("email/send_notif_email.html")
    context = {
        "subject" : subject,
        "email": email,
        "first_name":firt_name,
        "last_name":last_name,
        }
    to_emails = [
        email,
    ]
    subject, from_email = (subject, "Khadija  AfricaRelais")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)