from django.urls import path,include
from .import views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('',views.Tasklist.as_view(),name='tasklist'),
    path('task/<int:pk>/',views.TaskDetail.as_view(),name="taskdetail"),
    path('task-create/',views.TaskCreate.as_view(),name="create"),
    path('task-update/<int:pk>/',views.TaskUpdate.as_view(),name='update'),
    path('task-delete/<int:pk>/',views.TaskDelete.as_view(),name='delete'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/',views.Register.as_view()  ,name='signup'),
    
    
]
