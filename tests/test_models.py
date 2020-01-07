# -*- coding: UTF-8 -*-
import pytest
from unittest import TestCase as UnitTestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db import models
from django_mail_template.models import (MailTemplate, MailAttachment,
                                         Configuration)


class TestAttachment(UnitTestCase):

    def setUp(self) -> None:
        self.attachment = MailAttachment()

    def test_mail_attachment_data_model(self):
        assert isinstance(self.attachment, models.Model)

    def test_file_field_is_file_type(self):
        file = MailAttachment._meta.get_field('file')
        assert isinstance(file, models.FileField)

    def test_file_field_help_text(self):
        expected_text = _('File to be attached to a mail template.')
        actual_text = MailAttachment._meta.get_field('file').help_text
        self.assertEqual(expected_text, actual_text)


@pytest.mark.django_db
class TestMailTemplate(UnitTestCase):

    def setUp(self) -> None:
        self.mail = MailTemplate(from_email='a@b.com',
                                 subject=_('test subject'))

    def test_mail_data_model(self):
        assert isinstance(self.mail, models.Model)

    def test_required_fields(self):
        self.mail.full_clean()  # Should not fail

    def test_mail_string(self):
        expected_text = _('test subject')
        self.assertEqual(expected_text, str(self.mail))

    def test_to_field_max_length(self):
        lots = 'addresmail_test@mail.com,' * 41  # 25 character * 41 == 1025
        self.mail.to = lots[:-1]
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        ok = 'addresmail_test@mail.com,' * 40  # 25 character * 40 = 1000
        self.mail.to = ok[:-1]
        self.mail.full_clean()

    def test_to_field_help_text(self):
        expected_help_text = \
            _('A list with destiny email addresses separated with coma.')
        actual_help_text = MailTemplate._meta.get_field('to').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_to_field_do_validation(self):
        self.mail.to = 'no-mail, simple@mail.com'
        with self.assertRaises(ValidationError):
            self.mail.full_clean()

    def test_from_email_field_max_length(self):
        lots = 'a' * 250 + 'addresmail_test@mail.com'
        self.mail.from_email = lots[:-1],
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        self.mail.from_email = 'a' * 225 + 'addresmail_test@mail.com'
        self.mail.full_clean()

    def test_from_email_field_help_text(self):
        expected_help_text = _("Sender's email address.")
        actual_help_text = MailTemplate._meta.get_field('from_email').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_subject_field_max_length(self):
        big_subject = 'c' * 140 + 'exceed'  # 1 * 140 = 140 character max
        subject_ok = 'c' * 140
        self.mail.subject = big_subject
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        self.mail.subject = subject_ok
        self.mail.full_clean()

    def test_subject_field_help_text(self):
        expected_help = _('Subject text for the mail. Context variable can be '
                          'used.')
        actual_help_text = MailTemplate._meta.get_field('subject').help_text
        self.assertEqual(expected_help, actual_help_text)

    def test_body_field_max_length(self):
        big_body = 'chars' * 1000 + 'exceed'  # 5 * 1000 = 5000 character max
        body_ok = 'chars' * 1000
        self.mail.body = big_body
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        self.mail.body = body_ok
        self.mail.full_clean()

    def test_body_field_help_text(self):
        expected_help_text = _('The content of the mail. Context variable can '
                               'be used.')
        actual_help_text = MailTemplate._meta.get_field('body').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_attachments_field_help_text(self):
        expected_text = _('Select files to be sent with the mail.')
        actual_text = MailTemplate._meta.get_field('attachments').help_text
        self.assertEqual(expected_text, actual_text)

    def test_attachments_field_type(self):
        attachments = MailTemplate._meta.get_field('attachments')
        assert isinstance(attachments, models.ManyToManyField)

    def test_attachments_field_link_to_mail_attachment(self):
        attachments = MailTemplate._meta.get_field('attachments')
        assert attachments.related_model == MailAttachment


# class TestAttachFile(UnitTestCase):
#
#     def test_can_attach_two_files_to_template(self):
#         pass
#
#     def test_can_recover_files_from_template(self):
#         pass
#
#     def test_can_delete_files_from_template(self):
#         pass
#
#
# class TestSendMailTemplate(UnitTestCase):
#
#     def test_subject_replace_context_variables(self):
#         expected_subject = 'Hello Test User'
#         pass
#
#     def test_body_replace_context_variables(self):
#         expected_subject = 'Hello Test User'
#         pass
#
#     def test_can_not_send_mail_if_model_is_not_saved(self):
#         """
#         Needed to guarantee value in all required attribute to send a mail.
#         """
#         pass
#
#     def test_can_not_send_mail_without_required_attribute(self):
#         """
#         When sending an email a set of attributes will be required.
#
#         The required attributes are mainly dictated by django.core.mail.
#         Check if this test should replace upper test (if model not saved).
#         """
#         pass


class TestConfiguration(UnitTestCase):
    """
    Store dynamic configuration data used to set up django_mail_template.

    Builtin key process:

    * 'LOG_MAIL_ACTIVITY': A configuration with this value in process attribute
      will configure django_mail_template to log mail activity.?????
    """
    def setUp(self) -> None:
        self.configuration = Configuration(
            process='PROCESS_ID'
        )

    def test_required_fields(self):
        self.configuration.full_clean()

    def test_model_type_for_configuration(self):
        assert isinstance(self.configuration, models.Model)

    def test_process_field_type(self):
        field = Configuration._meta.get_field('process')
        assert isinstance(field, models.CharField)

    def test_process_field_max_length(self):
        big_data = 'chars' * 40 + 'exceed'
        data_ok = 'chars' * 40
        self.configuration.process = big_data
        with self.assertRaises(ValidationError):
            self.configuration.full_clean()
        self.configuration.process = data_ok
        self.configuration.full_clean()

    def test_mail_template_field_type(self):
        field = Configuration._meta.get_field('mail_template')
        assert isinstance(field, models.ForeignKey)

    def test_mail_template_filed_point_to_right_data_model(self):
        field = Configuration._meta.get_field('mail_template')
        assert field.related_model == MailTemplate

    def test_configuration_string_without_mail_template(self):
        expected_text = 'PROCESS_ID - ' + _('No mail template')
        assert str(self.configuration) == expected_text

    def test_configuration_string_with_mail_template(self):
        # Fixture
        mail = MailTemplate.objects.create(
            subject='test mail template subject',
            from_email='a@b.com'
        )
        self.configuration.mail_template = mail
        expected_text = _('PROCESS_ID - test mail template subject')
        assert str(self.configuration) == expected_text


class TestConfigurationBehavior(UnitTestCase):

    def setUp(self) -> None:
        self.configuration = Configuration(process='TestProcess')

    def test_get_mail_template_return_none_without_mail_template(self):
        assert Configuration.get_mail_template('') is None

    def test_get_mail_template_return_correct_mail_template(self):
        # Fixture
        mail_yes = MailTemplate.objects.create(
            subject='test mail template subject',
            from_email='a@b.com'
        )
        mail_no = MailTemplate.objects.create(
            subject='Bad mail template subject',
            from_email='a@b.com'
        )
        configuration = Configuration(process='Fake_process')
        configuration.mail_template = mail_no
        configuration.save()
        self.configuration.mail_template = mail_yes
        self.configuration.save()

        assert Configuration().get_mail_template('TestProcess') == mail_yes



# class TestLogMailTemplate(UnitTestCase):
#     """
#     Store mail activity.?????
#
#     Default implementation do not log mail activity. To log mail activity it is
#     required to create the configuration 'LOG_MAIL_ACTIVITY'.
#     """
#
#     pass
