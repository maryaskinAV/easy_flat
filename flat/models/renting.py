import typing

from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError
from django.db import models


class Renting(models.Model):
    """
    Сущность бронировки квартиры
    """

    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, related_name="rent")
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    count_guest = models.PositiveIntegerField()
    lease_duration = DateRangeField()

    def clean(self) -> None:
        if (
            Renting.objects.filter(
                user=self.user, lease_duration__overlap=self.lease_duration
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                "У вас уже есть забронированная квартира в этот период"
            )
        if self.count_guest > self.flat.max_guest:
            raise ValidationError("Слишком много гостей")
        is_booked = (
            self.flat.rent.filter(lease_duration__overlap=self.lease_duration)
            .exclude(id=self.id)
            .exists()
        )
        if is_booked:
            raise ValidationError("Квартира занята")

    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.clean()
        super().save()
