from django.urls import path, reverse_lazy

from .views import (LoginView, LogoutView, SignUpView, UsersListView,
                    UserUpdate, UpdateLackeyView)


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True,
                                    next_page=reverse_lazy('hits_list')),
                                    name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register'),
    path('hitmen/', UsersListView.as_view(), name='hitmen'),
    path('hitmen/<int:pk>/', UserUpdate.as_view(), name='update'),
    path('lackey/<int:pk>/', UpdateLackeyView.as_view(), name='update_lackey'),
]
