from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


class User(AbstractUser, BaseModel):

    class Meta:
        db_table = "df_user"
        verbose_name = "user"
        verbose_name_plural = verbose_name


class AddressManage(models.Manager):

    def get_default_address(self, user):
        try:
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            address = None

        return address

    def get_all_address(self, user):
        try:
            have_address = self.filter(user=user)
        except self.model.DoesNotExist:
            have_address = None
        return have_address


class Address(BaseModel):

    user = models.ForeignKey(
        "User", verbose_name="user account", on_delete=models.CASCADE
    )
    receiver = models.CharField(max_length=20, verbose_name="receiver")
    addr = models.CharField(max_length=256, verbose_name="address")
    zip_code = models.CharField(max_length=6, null=True, verbose_name="zip code")
    phone = models.CharField(max_length=11, verbose_name="phone number")
    is_default = models.BooleanField(default=False, verbose_name="default or not")

    objects = AddressManage()

    class Meta:
        db_table = "df_address"
        verbose_name = "address"
        verbose_name_plural = verbose_name
