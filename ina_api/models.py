from django.db import models

class User(models.Model):
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    bio = models.TextField(max_length=2000)
    password = models.CharField(max_length=200)
    salt = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=22)
    organisation = models.CharField(max_length=200) #optional, example: Hanzehogeschool Groningen
    function = models.CharField(max_length=200)     #optional, example: Docent Software Engineering
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
            "profilePhotoPath": self.profile_photo_path,
            "createdAt": self.created_at
        }

class Project(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(max_length=3000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    location = models.CharField(max_length=200)

    STATUSSES = (
        (0, 'New'),
        (1, "OnGoing"),
        (2, "Ended")
    )
    status = models.IntegerField(default=0, choices=STATUSSES)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.desc,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "createdAt": self.created_at,
            "likeCount": self.like_count,
            "followerCount": self.follower_count,
            "location": self.location
        }

class Group_Admin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.group, self.user)

    def __repr__(self):
        return {
            "group": self.group,
            "user": self.user
        }

class Project_Admin(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.project, self.user)

    def __repr__(self):
        return {
            "project": self.project,
            "user": self.user
        }