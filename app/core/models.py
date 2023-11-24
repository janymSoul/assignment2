from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(
            email=email, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class App_user(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    profile_description = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['given_name', 'surname', 'city', 'phone_number', 'password']
    def __str__(self):
        return f'User_id: {self.user_id} name: {self.given_name} {self.surname}'

class Caregiver(models.Model):
    caregiver_user_id = models.OneToOneField('core.App_user', on_delete=models.CASCADE, primary_key=True)
    photo = models.BinaryField()
    gender = models.CharField(max_length=10)
    caregiving_type = models.CharField(max_length=255)
    hourly_rate = models.FloatField()

    def __str__(self):
        return f'Caregiver id: {self.caregiver_user_id} caregiving_type: {self.caregiving_type}'

class Member(models.Model):
    member_user_id = models.OneToOneField('core.App_user', on_delete=models.CASCADE, primary_key=True)
    house_rules = models.CharField(max_length=255)

    def __str__(self):
        return f'Member id: {self.member_user_id}'

class Address(models.Model):
    member_user = models.OneToOneField('core.Member', on_delete=models.CASCADE, primary_key=True)
    house_number = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    town = models.CharField(max_length=255)

    def __str__(self):
        return f'Address member_id: {self.member_user_id} street: {self.street} number: {self.house_number}'

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    member_user = models.ForeignKey('core.Member', on_delete=models.CASCADE)
    required_caregiving_type = models.CharField(max_length=255)
    other_requirements = models.CharField(max_length=255)
    date_posted = models.DateField()

    def __str__(self):
        return f'Job id: {self.job_id} member_id: {self.member_user_id} required_care_type: {self.required_caregiving_type}'

class JobApplication(models.Model):
    caregiver_user = models.ForeignKey('core.Caregiver', on_delete=models.CASCADE)
    job = models.ForeignKey('core.Job', on_delete=models.CASCADE)
    date_applied = models.DateField()

    def __str__(self):
        return f'Job Application caregiver_id: {self.caregiver_user_id} job_id: {self.job_id}'

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    caregiver_user = models.ForeignKey('core.Caregiver', on_delete=models.CASCADE)
    member_user = models.ForeignKey('core.Member', on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    work_hours = models.IntegerField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f'Appointment id: {self.appointment_id} member_id: {self.member_user_id} caregiver_id: {self.caregiver_user_id}'
