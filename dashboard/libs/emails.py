from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import encoding
from OGT import settings
from dashboard.libs.utils import ErrorLogHelper
from dashboard.models import SentEmailsLog


class EmailHelper:

    def __init__(self):
        self.name = 'EmailHelper'

    def send_email(self, request, client, subject, message, from_email):
        """
        Sends a simple text email
        :param request:
        :param client:
        :param subject:
        :param message:
        :param from_email:
        :return:
        """

        try:
            mail = EmailMessage(
                self.clean_email_params(subject),
                self.clean_email_params(message),
                self.clean_email_params(from_email),
                self.clean_email_params([client.email]),
                reply_to=[from_email]
            )

            mail.send()

            try:
                # Log the sent email
                email_log = SentEmailsLog()
                email_log.user = request.user
                email_log.client = client
                email_log.subject = self.clean_email_params(subject)
                email_log.content = self.clean_email_params(message)
                email_log.to_email = str(self.clean_email_params([client.email]))
                email_log.from_email = self.clean_email_params(from_email)
                email_log.host_email = settings.EMAIL_HOST_USER
                email_log.attachments = 'No'
                email_log.save()

            except Exception, e:
                ErrorLogHelper.log_error(error_message=e, calling_function="EmailHelper.send_email")

            return True

        except Exception, e:
            ErrorLogHelper.log_error(error_message=e, calling_function="EmailHelper.send_email")

            return False

    def send_email_with_attachments(self, request, client, subject, message, attachments, from_email=settings.EMAIL_HOST_USER):
        """
        Sends a simple text mail with attachments
        :param request:
        :param client:
        :param subject:
        :param message:
        :param from_email:
        :param attachments:
        :return:
        """

        # print type(encoding.smart_bytes(attachments))
        # # for attachment in attachments:
        # #     print json.loads(attachment)
        # #
        # return False

        try:
            mail = EmailMessage(
                self.clean_email_params(subject),
                self.clean_email_params(message),
                self.clean_email_params(from_email),
                self.clean_email_params([client.email]),
                reply_to=[from_email]
            )

            for attachment in attachments.values():
                mail.attach(attachment.name, attachment.read(), attachment.content_type)

            mail.send()

            try:
                # Log the sent email
                email_log = SentEmailsLog()
                email_log.user = request.user
                email_log.client = client
                email_log.subject = self.clean_email_params(subject)
                email_log.content = self.clean_email_params(message)
                email_log.to_email = str(self.clean_email_params([client.email]))
                email_log.from_email = self.clean_email_params(from_email)
                email_log.host_email = settings.EMAIL_HOST_USER
                email_log.attachments = 'No'
                email_log.save()

            except Exception, e:
                ErrorLogHelper.log_error(error_message=e, calling_function="EmailHelper.send_email_with_attachments")

            return True

        except Exception, e:
            print e
            ErrorLogHelper.log_error(error_message=e, calling_function="EmailHelper.send_email_with_attachments")

            return False

    @staticmethod
    def clean_email_params(params):

        if type(params) != list:
            try:
                params = str(params)
                return params
            except Exception, e:
                ErrorLogHelper.log_error(error_message=e, calling_function="EmailHelper.clean_email_params")
                return None
        else:
            try:
                for param in params:
                    param_pos = params.index(param)
                    if type(param) != str:
                        params[param_pos] = str(param)

                return params

            except Exception, e:
                ErrorLogHelper.log_error(error_message=e, calling_function="EmailHelper.clean_email_params")
                return False
