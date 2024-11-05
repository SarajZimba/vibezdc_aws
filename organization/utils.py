from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_mail_to_receipients(data, mail_list, sender):
    email_body = render_to_string('organization/mail_template.html', data)
    try:
        send_mail(
            'End Day Report',
            '',
            sender,
            mail_list,
            fail_silently=False,
            html_message=email_body
        )
    except Exception as e:
        print("Exception Occured", e)

def send_combined_mail_to_receipients(combine_data, terminals_data,mail_list, sender):
    email_body = render_to_string('organization/combined_end_day_report_list.html', {'combine_data':combine_data, 'terminals_data':terminals_data})
    try:
        send_mail(
            'End Day Report',
            '',
            sender,
            mail_list,
            fail_silently=False,
            html_message=email_body
        )
    except Exception as e:
        print("Exception Occured", e)

from .models import Organization

# def get_cron_job_time():
#     # Fetch the stored time from the database
#     organization = Organization.objects.first()
#     if organization:
#         return organization.end_day_time.strftime('%H:%M')
#     else:
#         # Return a default time if no time is stored
#         return '23:59'  # Default time

def get_cron_job_time():
    # Fetch the stored time from the database
    organization = Organization.objects.first()
    if organization and organization.end_day_time:
        # Assuming organization.end_day_time is a string like '6:40'
        # Split the string into hours and minutes
        hours = organization.end_day_time.hour
        minutes = organization.end_day_time.minute
         # Format the time as '%M %H'
        return '{:02d} {:02d} * * *'.format(int(minutes), int(hours))
    else:
        # Return a default time if no time is stored
        return '59 23 * * *'  # Default time
