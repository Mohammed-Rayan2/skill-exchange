from django.db import models
from django.conf import settings


class Skill(models.Model):
    SKILL_TYPES = [('Teach', 'Teach'), ('Learn', 'Learn')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    skill_name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=5, choices=SKILL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'skill_name', 'skill_type']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.skill_name} ({self.skill_type})"


class Connection(models.Model):
    STATUS_CHOICES = [
        ('Pending',  'Pending'),
        ('Accepted', 'Accepted'),
    ]
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_connections'
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_connections'
    )
    skill_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['requester', 'provider', 'skill_name']

    def __str__(self):
        return f"{self.requester.username} → {self.provider.username} ({self.skill_name})"
