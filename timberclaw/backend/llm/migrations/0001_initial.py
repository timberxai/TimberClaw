from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LLMCallLog",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("provider", models.CharField(max_length=32)),
                ("success", models.BooleanField(default=False)),
                ("prompt_tokens", models.PositiveIntegerField(default=0)),
                ("completion_tokens", models.PositiveIntegerField(default=0)),
                ("latency_ms", models.PositiveIntegerField(default=0)),
                ("error_message", models.TextField(blank=True, default="")),
            ],
            options={
                "verbose_name": "LLM 调用记录",
                "verbose_name_plural": "LLM 调用记录",
                "ordering": ("-created_at",),
            },
        ),
    ]
