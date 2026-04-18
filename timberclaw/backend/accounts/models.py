from django.conf import settings
from django.db import models


class BuilderRole(models.TextChoices):
    """PRD §4.1–4.5：Builder 侧五类账号（业务使用者 End User 不在此体系，见 PRD §4.6）。"""

    OWNER = "owner", "Owner（工厂信息化负责人）"
    REVIEWER = "reviewer", "Reviewer（业务代表）"
    ADMIN = "admin", "Admin（平台管理员）"
    PLATFORM_ENGINEER = "platform_engineer", "Platform Engineer（工程与模板）"
    HUMAN_DEVELOPER = "human_developer", "Human Developer（人工降级通道）"


class UserProfile(models.Model):
    """与 Django User 一对一；角色用于后续「角色 × 动作」门禁。"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="builder_profile",
    )
    role = models.CharField(
        max_length=32,
        choices=BuilderRole.choices,
        default=BuilderRole.HUMAN_DEVELOPER,
    )

    class Meta:
        verbose_name = "Builder 用户档案"
        verbose_name_plural = "Builder 用户档案"

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"
