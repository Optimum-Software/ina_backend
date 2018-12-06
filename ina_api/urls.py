from django.urls import path
from .controllers import DeviceController, FileController, GroupAdminController, ProjectAdminController, ProjectController, ProjectFavoriteController, ProjectFollowedController, ProjectLikedController, ProjectTagController, UserController, UserTagController, TagController, GroupController, MemberController

urlpatterns = [
	#DEVICE
	path('getDeviceById/<int:id>', DeviceController.getDeviceById, name="deviceById"),
	path('createDevice', DeviceController.createDevice, name="createDevice"), #Fields: userId, deviceName
	path('deleteDeviceById', DeviceController.deleteDeviceById, name="deleteDeviceById"), #Fields: id

	#FILE
	path('getFileById/<int:id>', FileController.getFileById, name="fileById"),

	#GROUP
	path('getGroupById/<int:id>', GroupController.getGroupById, name='GroupById'),
	path('getGroupByName/<slug:group_name>', GroupController.getGroupByName, name='GroupByName'),
	path('createGroup', GroupController.createGroup, name='createGroup'),
	path('deleteGroupById', GroupController.deleteGroupById, name='deleteGroupById'),
	path('deleteGroupByName', GroupController.deleteGroupByName, name='deleteGroupByName'),

	#GROUPADMIN
	path('getGroupAdminById/<int:id>', GroupAdminController.getGroupAdminById, name="groupAdminById"),

	#MEMBER
	path('getMember/<int:group_id>/<int:user_id>', MemberController.getMember, name='getMember'),
	path('getMemberById/<int:id>', MemberController.getMemberById, name='getMemberById'),
	path('deleteMemberById', MemberController.deleteMemberById, name='deleteMember'),
	path('createMember', MemberController.createMember, name='createMember'),

	#PROJECT
	path('getProjectById/<int:id>', ProjectController.getProjectById, name="projectById"),

	#PROJECTADMIN
	path('getProjectAdminById/<int:id>', ProjectAdminController.getProjectAdminById, name="projectAdminById"),

	#PROJECTFAVORITE
	path('getProjectFavoriteById/<int:id>', ProjectFavoriteController.getProjectFavoriteById, name="fileById"),

	#PROJECTFOLLOWED
	path('getProjectFollowedById/<int:id>', ProjectFollowedController.getProjectFollowedById, name="projectFollowedById"),

	#PROJECTLIKED
	path('getProjectLikedById/<int:id>', ProjectLikedController.getProjectLikedById, name="projectLikedById"),

	#PROJECTTAG
	path('getProjectTagById/<int:id>', ProjectTagController.getProjectTagById, name="projectTag"),

	#TAG
	path('getTagById/<int:id>', TagController.getTagById, name="tagById"),

	#USER
	path('getUserById/<int:id>', UserController.getUserById, name="userById"),
	path('getUserByEmail/<slug:email>', UserController.getUserByEmail, name="userByEmail"),
	path('createUser', UserController.createUser, name="createUser"), #Fields: email, password, firstName, lastName, bio, mobile, (optional => can be empty) organisation, (optional => can be empty) function
	path('deleteUser', UserController.deleteUser, name="deleteUser"), #Fields: id

	#USERTAG
	path('getUserTagById/<int:id>', UserTagController.getUserTagById, name="userTagById"),
]