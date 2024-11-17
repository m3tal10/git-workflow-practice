from django.urls import path
from user import views

app_name='user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('token/', views.CreateLoginView.as_view(), name='token'),
]