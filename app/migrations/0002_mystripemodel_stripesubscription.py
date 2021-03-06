# Generated by Django 3.1.5 on 2021-01-09 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(help_text='The start date of the subscription.')),
                ('status', models.CharField(help_text='The status of this subscription.', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MyStripeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stripe_subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stripesubscription')),
            ],
        ),
    ]
