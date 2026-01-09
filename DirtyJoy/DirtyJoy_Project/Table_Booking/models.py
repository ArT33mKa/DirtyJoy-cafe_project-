from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}: - ({self.email, self.phone})"


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Столик {self.number} ({self.seats} місць)"

class Booking(models.Model):

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    guests_count = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]
        unique_together = ("table", "date", "start_time")

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Час завершення має бути пізніше часу початку")

    def __str__(self):
        return f"{self.date} {self.start_time} — Table {self.table.number}"