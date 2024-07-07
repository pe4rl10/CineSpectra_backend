from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, is_subscribed=False):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, is_subscribed=is_subscribed)

        user.set_password(password)
        user.save(using=self._db)

        # Create associated search limit instance
        SearchLimit.objects.create(user=user)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class SearchLimit(models.Model):
    user = models.OneToOneField('UserAccount', on_delete=models.CASCADE, related_name='search_limit')
    remaining_count = models.IntegerField(default=3)  # Default search count limit for unsubscribed users
    last_reset = models.DateField(auto_now=True)

    def reset_search_count(self):
        self.remaining_count = 3  # Reset to default limit
        self.save()

    def decrement_search_count(self):
        if self.remaining_count > 0:
            self.remaining_count -= 1
            self.save()


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)  # New field for subscription status

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def get_search_limit(self):
        return self.search_limit  # Access the SearchLimit instance directly

    def reset_search_count(self):
        self.search_limit.reset_search_count()

    def decrement_search_count(self):
        self.search_limit.decrement_search_count()
