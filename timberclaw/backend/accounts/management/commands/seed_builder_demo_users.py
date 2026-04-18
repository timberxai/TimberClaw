import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import BuilderRole, UserProfile

User = get_user_model()

DEMO_USERS: tuple[tuple[str, str], ...] = (
    ("tc_owner", BuilderRole.OWNER),
    ("tc_reviewer", BuilderRole.REVIEWER),
    ("tc_admin", BuilderRole.ADMIN),
    ("tc_platform_engineer", BuilderRole.PLATFORM_ENGINEER),
    ("tc_human_developer", BuilderRole.HUMAN_DEVELOPER),
)


class Command(BaseCommand):
    help = "创建五类 Builder 演示账号（仅开发 / 内网验收；勿在生产使用默认密码）。"

    def handle(self, *args, **options):
        password = os.environ.get("TC_DEMO_PASSWORD", "changeme")
        for username, role in DEMO_USERS:
            user, created = User.objects.get_or_create(username=username)
            if created or not user.has_usable_password():
                user.set_password(password)
                user.save()
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={"role": role},
            )
            if profile.role != role:
                profile.role = role
                profile.save()
            self.stdout.write(self.style.SUCCESS(f"{username} -> {role}"))
        self.stdout.write(
            self.style.WARNING(
                f"默认密码来自环境变量 TC_DEMO_PASSWORD（未设置则为 changeme）。"
            ),
        )
