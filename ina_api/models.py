from django.db import models


class User(models.Model):
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=2000)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=22)
    organisation = models.CharField(max_length=100)  # optional, example: Hanzehogeschool Groningen
    function = models.CharField(max_length=100)  # optional, example: Docent Software Engineering
    profile_photo_path = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return {
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.lastName,
            "bio": self.bio,
            "password": self.password,
            "salt": self.salt,
            "mobile": self.mobile,
            "organisation": self.organisation,
            "function": self.function,
            "profilePhotoPath": self.profile_photo_path
        }


class Project(models.Model):
    name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    desc = models.TextField(max_length=2000)
    photo_path = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    member_count = models.IntegerField(default=0)
    public = models.BooleanField(default=True)
