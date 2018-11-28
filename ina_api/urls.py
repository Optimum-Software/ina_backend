from django.urls import path

urlpatterns = [

	#GROUP
	path('getGroupById/<int:user_id>', GroupController.getGroupById, name='GroupById'),

	#GROUP
	path('getGroupByName/<slug:group_name>', GroupController.getGroupByName, name='GroupByName'),

	#GROUP
	path('createGroup', GroupController.createGroup, name='createGroup'),

	#GROUP
	path('deleteGroupById/<int:group_id>', GroupController.deleteGroupById, name='deleteGroupById'),

	#GROUP
	path('deleteGroupByName/<slug:group_name>', GroupController.deleteGroupByName, name='deleteGroupByName'),

	#MEMBER
	path('getMember/<int:group_id>/<int:user_id>', MemberController.getMember, name='getMember'),

	#MEMBER
	path('deleteMember/<int:group_id>/<int:user_id>', MemberController.deleteMember, name='deleteMember'),

	#MEMBER
	path('createMember/<int:group_id>/<int:user_id>', MemberController.createMember, name='createMember'),






]