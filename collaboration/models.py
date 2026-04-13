from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, db_index=True, blank=True)
    icon_name = models.CharField(
        max_length=80,
        help_text='圖示名稱或識別字串（供前端顯示）',
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '產業領域'
        verbose_name_plural = '產業領域'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    class Role(models.TextChoices):
        EXPERT = 'expert', 'Expert'
        ENGINEER = 'engineer', 'Engineer'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ENGINEER,
    )
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = '使用者檔案'
        verbose_name_plural = '使用者檔案'

    def __str__(self) -> str:
        return f'{self.user.username} ({self.get_role_display()})'


class PainPoint(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pain_points',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='pain_points',
    )
    title = models.CharField(max_length=200)
    context = models.TextField(verbose_name='場景描述')
    current_solution = models.TextField(verbose_name='現狀')
    pain_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    potential_value = models.TextField(verbose_name='潛在價值')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '痛點'
        verbose_name_plural = '痛點'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
