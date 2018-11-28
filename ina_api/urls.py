from django.urls import path
from .controllers import DeviceController, FileController, GroupAdminController, ProjectAdminController, ProjectController, ProjectFavoriteController, ProjectFollowedController, ProjectLikedController, ProjectTagController, UserController, UserTagController, TagController

urlpatterns = [
<<<<<<< HEAD
	#DEVICE
	path('getDeviceById/<int:id>', DeviceController.getDeviceById, name="deviceById"),

	#FILE
	path('getFileById/<int:id>', FileController.getFileById, name="fileById"),

	#GROUP
	path('getGroupById/<int:user_id>', GroupController.getGroupById, name='GroupById'),
	path('getGroupByName/<slug:group_name>', GroupController.getGroupByName, name='GroupByName'),
	path('createGroup', GroupController.createGroup, name='createGroup'),
	path('deleteGroupById/<int:group_id>', GroupController.deleteGroupById, name='deleteGroupById'),
	path('deleteGroupByName/<slug:group_name>', GroupController.deleteGroupByName, name='deleteGroupByName'),

	#GROUPADMIN
	path('getGroupAdminById/<int:id>', GroupAdminController.getGroupAdminById, name="groupAdminById"),

	#MEMBER
	path('getMember/<int:group_id>/<int:user_id>', MemberController.getMember, name='getMember'),
	path('deleteMember/<int:group_id>/<int:user_id>', MemberController.deleteMember, name='deleteMember'),
	path('createMember/<int:group_id>/<int:user_id>', MemberController.createMember, name='createMember'),

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
	path('getUserById/<int:id>', UserController.getUserById, name='userById'),

	#USERTAG
	path('getUserTagById/<int:id>', UserTagController.getUserTagById, name="userTagById"),
]