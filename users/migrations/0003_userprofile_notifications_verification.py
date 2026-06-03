from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_userprofile_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email_notifications",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="release_notifications",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="verification_requested",
            field=models.BooleanField(default=False),
        ),
    ]
