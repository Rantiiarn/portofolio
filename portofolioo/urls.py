from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('Posts/', views.posts, name="Posts"),
	path('Post/<slug:slug>', views.post, name="Post"),
	path('profile/', views.profile, name="profile"),
    
	#crud path

	path('create_Post/', views.createPost, name="create_Post"),
	path('update_Post/<slug:slug>/', views.updatePost, name="update_Post"),
	path('delet_Post/<slug:slug>/', views.deletPost, name="delete_Post"),


	path('send_Email/', views.sendEmail, name="send_Email"),
]