from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2 = None):
        """
        Creates and saves a User with the given email,name,tc and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            # address = address,
            tc = tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None):
        """
        Creates and saves a superuser with the given email, name, tc, and password.
        """
        user = self.create_user(
            email,
            password=password,
            name = name,
            tc = tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Coustom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length = 200)
    address = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name','tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    # is_admin=models.BooleanField(default=False)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    like = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='manuiteams')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    like = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    

class UserLikeRetaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    likedate = models.DateTimeField(auto_now_add=True)
    likes = models.BooleanField()
 
    def __str__(self):
        return self.user.name
class Userlikemenuitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE)  
    likes = models.BooleanField()
    likedate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

class Usersavemenuitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE)  
    sdate = models.BooleanField()
    adddate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


