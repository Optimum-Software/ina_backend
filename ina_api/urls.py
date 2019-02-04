from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .controllers import LoginController, DeviceController, FileController, GroupAdminController, \
    ProjectAdminController, \
    ProjectController, ProjectFavoriteController, ProjectFollowedController, ProjectLikedController, \
    ProjectTagController, UserController, UserTagController, TagController, GroupController, MemberController,  \
    MessageController, ChatController, ProjectUpdateController, NotificationController


urlpatterns = [
    # Authentication tutorial
    path('login',LoginController.LoginUser.as_view(),name='auth_user_login'),

    path('logout',LoginController.LogoutUser.as_view(),name='auth_user_logout'),

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
    path('getAllGroups', GroupController.getAllGroups, name='getAllGroups'),
    path('getMyGroups', GroupController.getMyGroups, name='getMyGroups'),

    # GROUPADMIN
    path('getGroupAdminById/<int:id>', GroupAdminController.getGroupAdminById, name="groupAdminById"),

    # MEMBER
    path('getMember', MemberController.getMember, name='getMember'),
    path('getMemberById/<int:id>', MemberController.getMemberById, name='getMemberById'),
    path('deleteMember', MemberController.deleteMember, name='deleteMember'),
    path('createMember', MemberController.createMember, name='createMember'),
    path('getMembersByProjectId/<int:project_id>', MemberController.getMembersByProjectId, name='getMembersByProjectId'),
    path('getMembersByUserId/<int:user_id>', MemberController.getMembersByUserId, name='getMembersByUserId'),

    #MESSAGE
    path('sendMessageToUserById', MessageController.sendMsgToUser, name="sendMessage"), #fields: userId, chatId

    #NOTIFICATION
    path("getNotificationByUser/<int:id>", NotificationController.getNotificationByUser, name="getNotificationByUser"),
    path("markAsRead/<int:id>", NotificationController.markAsRead, name="markAsRead"),

    # PROJECT
    path('getProjectById/<int:id>', ProjectController.getProjectById, name="projectById"),
    path('getAllProjects', ProjectController.getAllProjects, name="getAllProjects"),
    path('uploadThumbnailForProject', ProjectController.uploadThumbnailForProject, name="uploadThumbnailForProject"),
    path('getAllProjectsNewestFirst', ProjectController.getAllProjectsNewestFirst, name="getAllProjectsNewestFirst"),
    path('getAllProjectsOldestFirst', ProjectController.getAllProjectsOldestFirst, name="getAllProjectsOldestFirst"),
    path('getAllProjectsMostLikedFirst', ProjectController.getAllProjectsMostLikedFirst, name="getAllProjectsMostLikedFirst"),
    path('getAllProjectsMostFollowsFirst', ProjectController.getAllProjectsMostFollowsFirst, name="getAllProjectsMostFollowsFirst"),
    path('searchForProjects', ProjectController.searchForProjects, name="searchForProjects"),
    path('createProject', ProjectController.createProject, name="createProject"),
    path('getProjectsByTag', ProjectController.getProjectsByTag, name="getProjectsByTag"),
    path('getSwipeProjects/<int:userId>', ProjectController.getSwipeProjects, name="getSwipeProjects"),
    path('editProject', ProjectController.editProject, name="editProject"),

    # PROJECTADMIN
    path('getProjectAdminById/<int:id>', ProjectAdminController.getProjectAdminById, name="projectAdminById"),
    path('getAllProjects', ProjectController.getAllProjects, name="getAllProjects"),

    # PROJECTFAVORITE
    path('getProjectFavoriteById/<int:id>', ProjectFavoriteController.getProjectFavoriteById, name="fileById"),

    # PROJECTFOLLOWED
    path('getProjectFollowedById/<int:id>', ProjectFollowedController.getProjectFollowedById, name="projectFollowedById"),
    path('followProjectById', ProjectFollowedController.followProjectById, name="followProjectById"),
    path('getAllFollowedProjectsByUserId/<int:id>', ProjectFollowedController.getAllFollowedProjectsByUserId, name="getAllFollowedProjectsByUserId"),
    path('setCanNotificate', ProjectFollowedController.setCanNotificate, name="setCanNotificate"),

    # PROJECTLIKED
    path('getProjectLikedById/<int:id>', ProjectLikedController.getProjectLikedById, name="projectLikedById"),
    path('likeProjectById', ProjectLikedController.likeProjectById, name="likeProjectById"),
    path('getAllLikedProjectsById/<int:id>', ProjectLikedController.getAllLikedProjectsById, name="getAllLikedProjectsById"),
    path('getLikedProjectsByUserId/<int:user_id>', ProjectLikedController.getLikedProjectsByUserId, name="getLikedProjectsByUserId"),
    path('checkIfProjectLiked/<int:userId>/<int:projectId>', ProjectLikedController.checkIfProjectLiked, name="checkIfProjectLiked"),
    path('unlikeProjectById', ProjectLikedController.unlikeProjectById, name="unlikeProjectById"),

    # PROJECTTAG
    path('getProjectTagById/<int:id>', ProjectTagController.getProjectTagById, name="projectTag"),

    # PROJECTUPDATE
    path('addProjectUpdate', ProjectUpdateController.addUpdate, name="addUpdate"), #fields: project, user, title, content
    path('getProjectUpdatesByProjectId/<int:project_id>', ProjectUpdateController.getProjectUpdatesByProjectId, name="getUpdates"),

    # TAG
    path('getTagById/<int:id>', TagController.getTagById, name="tagById"),
    path('getAllTags', TagController.getAllTags, name="allTags"),
    path('getAllProjectTagsById/<int:id>', TagController.getAllProjectTagsById, name="getAllProjectTagsById"),
    path('uploadPictureForTag', TagController.uploadPictureForTag, name="uploadPictureForTag"),
    path('searchForTags', TagController.searchForTags, name="searchForTags"),

    # USER
    path('getUserById/<int:id>', UserController.getUserById, name="userById"),
    path('getUserByEmail', UserController.getUserByEmail, name="userByEmail"), #Fields: email
    path('createUser', UserController.CreateUserAPIView.as_view(), name="createUser"), # Fields: email, password, firstName, lastName, bio, mobile
    path('updateUser', UserController.updateUser, name="updateUser"),
    path('passwordForgotVerification', UserController.sendPasswordVerification, name="sendPasswordVerification"),
    path('changePassword', UserController.changePassword, name="changePassword"),
    path('getUserSettings/<int:id>', UserController.getUserSettings, name="getUserSettings"),
    path('saveUserSettings', UserController.saveUserSettings, name="saveUserSettings"), 
    path('deleteUser', UserController.deleteUser, name="deleteUser"),  # Fields: id
    path('uploadFileForUser', UserController.uploadFileForProfilePhoto, name="uploadFileForProfilePhoto"),
    path('editOptionalInfo', UserController.editOptionalInfo, name="editOptionalInfo"),

    # USERTAG
    path('getUserTagById/<int:id>', UserTagController.getUserTagById, name="userTagById"),
]
