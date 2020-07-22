# Generated by Django 2.2.9 on 2020-07-21 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_mail_template', '0003_auto_20200719_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='mail_template',
            field=models.ForeignKey(
                blank=True,
                help_text='The mail template linked with this '
                          'configuration (process). When required a mail '
                          'template to this configurations this mail '
                          'template will be returned.',
                null=True, on_delete=django.db.models.deletion.SET_NULL,
                to='django_mail_template.MailTemplate',
                verbose_name='Mail template'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='process',
            field=models.CharField(
                help_text='A name to identify the process.',
                max_length=200, verbose_name='Process'),
        ),
    ]
