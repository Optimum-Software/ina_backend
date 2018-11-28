from django.urls import path

urlpatterns = [
	path('user/<int:user_id>', UserController.getUser, name='user'),
]