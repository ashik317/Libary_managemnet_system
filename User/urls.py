from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page view
    path('login/', views.user_login, name='login'),  # Login view
    path('register/', views.register, name='register'),  # Register view
    path('logout/', views.user_logout, name='logout'),  # Logout view
    path('issue/', views.issue, name='issue'),  # Issue a book view
    path('return_item/', views.return_item, name='return_item'),  # Return an item view
    path('history/', views.history, name='history'),  # User history view
]
