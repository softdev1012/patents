from django.db import models
from django.db.models import F


class Counter(models.Model):
    value = models.IntegerField(default=0)

    def increment(self):
        """Atomically increments the counter value."""
        self.value += 1
        self.save()
        return self.value

    def __str__(self):
        return str(self.value)
