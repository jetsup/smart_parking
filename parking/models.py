from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class Subscriptions(models.Model):
    plan = models.CharField(max_length=30, unique=True)
    pricing = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserTypes(models.Model):
    USER_TYPES = (("Admin", "Admin"), ("User", "User"))
    type = models.CharField(max_length=25, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


# need to insert the user after this
# =============================================================================================================================
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone",
        "id_passport",
        "password",
    ]
    USERNAME_FIELD = "email"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13, null=True, unique=False)
    email = models.EmailField(null=True, unique=True)
    id_passport = models.PositiveBigIntegerField(null=True, unique=True)
    password = models.CharField(max_length=128)  # will use SHA256
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True
    )  # FIXME: Not good
    user_type = models.IntegerField(default=2)
    rfid = models.CharField(max_length=20, unique=True)
    parking_frequency = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.email) + " " + self.rfid

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_staff

    @is_superuser.setter
    def is_superuser(self, value):
        self.is_staff = value

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


# =============================================================================================================================


class VehicleTypes(models.Model):
    VEHICLE_TYPE = (
        ("Car", "Car"),
        ("Motorcycle", "Motorcycle"),
        ("Bicycle", "Bicycle"),
        ("TukTuk", "TukTuk"),
        ("Truck", "Truck"),
    )
    type = models.CharField(max_length=25, choices=VEHICLE_TYPE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


# populate the table with some default vehicle types
class Vehicles(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vehicle_type = models.ForeignKey(VehicleTypes, on_delete=models.SET_NULL, null=True)
    number_plate = models.CharField(max_length=10, unique=True)
    subscription = models.ForeignKey(
        Subscriptions, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Slots(models.Model):
    slot = models.IntegerField(unique=True)
    occupied = models.BooleanField(default=False)
    occupied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class RewardTypes(models.Model):
    type = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rewards(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reward_type = models.ForeignKey(RewardTypes, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
