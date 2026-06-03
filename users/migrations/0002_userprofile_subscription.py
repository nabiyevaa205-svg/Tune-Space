from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="subscription",
            field=models.CharField(
                choices=[("free", "Free"), ("premium", "Premium"), ("gold", "Gold")],
                default="free",
                max_length=20,
            ),
        ),
    ]
