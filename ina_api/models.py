from django.db import models
from django.utils import timezone

class User(models.Model):
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(max_length=2000)
    password = models.CharField(max_length=200)
    salt = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=22)
    organisation = models.CharField(max_length=50)  # optional, example: Hanzehogeschool Groningen
    function = models.CharField(max_length=50)  # optional, example: Docent Software Engineering
    profile_photo_path = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    passwordVerification = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return {
            "id": self.pk,
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "bio": self.bio,
            "mobile": self.mobile,
            "organisation": self.organisation,
            "function": self.function,
            "profilePhotoPath": self.profile_photo_path,
            "createdAt": self.created_at
        }


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    desc = models.TextField(max_length=2000)
    photo_path = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now())
    member_count = models.IntegerField(default=0)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "id": self.pk,
            "name": self.name,
            "desc": self.desc,
            "photo_path": self.photo_path,
            "created_at": self.created_at,
            "member_count": self.member_count,
            "public": self.public,

        }

class Project(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=3000)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())
    like_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=1000, default='no path')

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
            "id": self.pk,
            "name": self.name,
            "desc": self.desc,
            "creator": self.creator.__repr__(),
            "startDate": self.start_date,
            "endDate": self.end_date,
            "createdAt": self.created_at,
            "likeCount": self.like_count,
            "followerCount": self.follower_count,
            "location": self.location,
            "thumbnail": self.thumbnail,
        }

class Member(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.project, self.user)

    def __repr__(self):
        return {
            "id": self.pk,
            "project": self.project,
            "user": self.user
        }

class Group_Admin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.group, self.user)

    def __repr__(self):
        return {
            "id": self.pk,
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
            "id": self.pk,
            "project": self.project,
            "user": self.user
        }


class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    path = models.CharField(max_length=1000)

    def __str__(self):
        return self.path

    def __repr__(self):
        return {
            "id": self.pk,
            "project": self.project.__repr__(),
            "path": self.path
        }


class Project_Liked(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.project, self.user)

    def __repr__(self):
        return {
            "id": self.pk,
            "project": self.project,
            "user": self.user
        }

class Project_Update(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=3000)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title

    def __repr__(self):
        return {
            'id': self.pk,
            'project': self.project.__repr__(),
            'creator' : self.creator.__repr__(),
            'title': self.title,
            'content' : self.content,
            'created_at': self.created_at
        }

class Project_Favorite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.project, self.user)

    def __repr__(self):
        return {
            "id": self.pk,
            "project": self.project,
            "user": self.user
        }


class Project_Followed(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    canNotificate = models.BooleanField(default=True)

    def __str__(self):
        return '{} : {}'.format(self.project, self.user)

    def __repr__(self):
        return {
            "id": self.pk,
            "project": self.project,
            "user": self.user
        }


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    canNotificate = models.BooleanField(default=True)

    def __str__(self):
        return '{} : {}'.format(self.user, self.device_name)

    def __repr__(self):
        return {
            "id": self.pk,
            "user": self.user,
            "device_name": self.device_name,
            "canNotificate": self.canNotificate
        }


class Tag(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "id": self.pk,
            "name": self.name,
            "thumbnail": self.thumbnail
        }


class User_Tag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.tag, self.user)

    def __repr__(self):
        return {
            "id": self.pk,
            "tag": self.tag,
            "user": self.user
        }


class Project_Tag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.tag, self.project)

    def __repr__(self):
        return {
            "id": self.pk,
            "tag": self.tag,
            "project": self.project
        }

class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    chat_uid = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.chat_uid

    def __repr__(self):
        return {
            "id": self.pk,
            "user1": self.user1.__repr__(),
            "user2": self.user2.__repr__(),
            "chatUid": self.chat_uid,
            "createdAt": self.created_at
        }

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    TYPES = {
        (0, "Chat"),
        (1, "Project"),
        (2, "Group")
    }

    type = models.IntegerField(choices=TYPES)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name='project')
    groupChat = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name='groupChat')
    created_at = models.DateTimeField(default=timezone.now())
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at)

    def __repr__(self):
        return {
            "id": self.pk,
            "user": self.user.__repr__(),
            "type": self.type,
            "chat": self.chat.__repr__(),
            "project": self.project.__repr__(),
            "groupChat": self.groupChat.__repr__(),
            "createdAt": self.created_at,
            "read": self.read,
        }
