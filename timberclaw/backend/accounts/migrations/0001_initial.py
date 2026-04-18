import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("owner", "Owner（工厂信息化负责人）"),
                            ("reviewer", "Reviewer（业务代表）"),
                            ("admin", "Admin（平台管理员）"),
                            ("platform_engineer", "Platform Engineer（工程与模板）"),
                            ("human_developer", "Human Developer（人工降级通道）"),
                        ],
                        default="human_developer",
                        max_length=32,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="builder_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Builder 用户档案",
                "verbose_name_plural": "Builder 用户档案",
            },
        ),
    ]
