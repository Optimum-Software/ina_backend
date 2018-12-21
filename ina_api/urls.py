from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .controllers import LoginController, DeviceController, FileController, GroupAdminController, \
    ProjectAdminController, \
    ProjectController, ProjectFavoriteController, ProjectFollowedController, ProjectLikedController, \
    ProjectTagController, UserController, UserTagController, TagController, GroupController, MemberController, MessageController, ChatController

urlpatterns = [
    # Authentication tutorial
    path('login',LoginController.LoginUser.as_view(),name='auth_user_login'),

    path('logout',LoginController.LogoutUser.as_view(),name='auth_user_logout'),

    # BESTE FUNCTIE OOIT
    path('test/', UserController.test, name="test"),

    #CHAT
    path("createChat", ChatController.createChat, name="createChat"), #Fields: user1Id, user2Id, chatUid
    path("getChatsForUser/<int:id>", ChatController.getChatsForUser, name="getChatsForUser"),

    # DEVICE
    path('getDeviceById/<int:id>', DeviceController.getDeviceById, name="deviceById"),
    path('createDevice', DeviceController.createDevice, name="createDevice"),  # Fields: userId, deviceId
    path('deleteDeviceById', DeviceController.deleteDeviceById, name="deleteDeviceById"),  # Fields: id

    # FILE
    path('getFileById/<int:id>', FileController.getFileById, name="fileById"),
    path('uploadFileForProject', FileController.uploadFileForProject, name="uploadFileForProject"),

    # GROUP
    path('getGroupById/<int:id>', GroupController.getGroupById, name='GroupById'),
    path('getGroupByName/<slug:group_name>', GroupController.getGroupByName, name='GroupByName'),
    path('createGroup', GroupController.createGroup, name='createGroup'),
    path('uploadGroupPhoto', GroupController.uploadGroupPhoto, name='uploadGroupPhoto'),
    path('deleteGroupById', GroupController.deleteGroupById, name='deleteGroupById'),
    path('deleteGroupByName', GroupController.deleteGroupByName, name='deleteGroupByName'),

    # GROUPADMIN
    path('getGroupAdminById/<int:id>', GroupAdminController.getGroupAdminById, name="groupAdminById"),

    # MEMBER
    path('getMember/<int:group_id>/<int:user_id>', MemberController.getMember, name='getMember'),
    path('getMemberById/<int:id>', MemberController.getMemberById, name='getMemberById'),
    path('deleteMemberById', MemberController.deleteMemberById, name='deleteMember'),
    path('createMember', MemberController.createMember, name='createMember'),

    #MESSAGE
    path('sendMessageToUserById', MessageController.sendMsgToUser, name="sendMessage"), #fields: userId

    # PROJECT
    path('getProjectById/<int:id>', ProjectController.getProjectById, name="projectById"),
    path('getAllProjects', ProjectController.getAllProjects, name="getAllProjects"),

    # PROJECTADMIN
    path('getProjectAdminById/<int:id>', ProjectAdminController.getProjectAdminById, name="projectAdminById"),
    path('getAllProjects', ProjectController.getAllProjects, name="getAllProjects"),

    # PROJECTFAVORITE
    path('getProjectFavoriteById/<int:id>', ProjectFavoriteController.getProjectFavoriteById, name="fileById"),

    # PROJECTFOLLOWED
    path('getProjectFollowedById/<int:id>', ProjectFollowedController.getProjectFollowedById, name="projectFollowedById"),
    path('followProjectById', ProjectFollowedController.followProjectById, name="followProjectById"),
    path('getAllFollowedProjectsById/<int:id>', ProjectFollowedController.getAllFollowedProjectsById, name="getAllFollowedProjectsById"),

    # PROJECTLIKED
    path('getProjectLikedById/<int:id>', ProjectLikedController.getProjectLikedById, name="projectLikedById"),
    path('likeProjectById', ProjectLikedController.likeProjectById, name="likeProjectById"),
    path('getAllLikedProjectsById/<int:id>', ProjectLikedController.getAllLikedProjectsById, name="getAllLikedProjectsById"),

    # PROJECTTAG
    path('getProjectTagById/<int:id>', ProjectTagController.getProjectTagById, name="projectTag"),

    # TAG
    path('getTagById/<int:id>', TagController.getTagById, name="tagById"),

    # USER
    path('getUserById/<int:id>', UserController.getUserById, name="userById"),
    path('getUserByEmail', UserController.getUserByEmail, name="userByEmail"), #Fields: email
    path('createUser', UserController.CreateUserAPIView.as_view(), name="createUser"),
    path('updateUser', UserController.updateUser, name="updateUser"),
    path('passwordForgotVerification', UserController.sendPasswordVerification, name="sendPasswordVerification"),
    path('changePassword', UserController.changePassword, name="changePassword"),
    # Fields: email, password, firstName, lastName, bio, mobile, (optional => can be empty) organisation, (optional => can be empty) function

    path('deleteUser', UserController.deleteUser, name="deleteUser"),  # Fields: id
    path('uploadFileForUser', UserController.uploadFileForProfilePhoto, name="uploadFileForProfilePhoto"),
    path('editOptionalInfo', UserController.editOptionalInfo, name="editOptionalInfo"),

    # USERTAG
    path('getUserTagById/<int:id>', UserTagController.getUserTagById, name="userTagById"),
]
