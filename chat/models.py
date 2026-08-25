from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    skill_name = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:40]}"

    def is_visible_to(self, user):
        if user == self.sender and self.deleted_by_sender:
            return False
        if user == self.receiver and self.deleted_by_receiver:
            return False
        return True
