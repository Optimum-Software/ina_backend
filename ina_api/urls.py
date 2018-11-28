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


]