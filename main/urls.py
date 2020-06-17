from django.urls import path
from . import views
urlpatterns = [
path("maintain/",views.maintainLists,name="maintainLists"),
path("",views.home,name="home"),
path("create/",views.create,name="create"),
path('api/', views.apiOverview, name='overview'),
path('api/task-list/', views.taskList, name='list'),
path('api/task-detail/<str:pk>/', views.detailList, name='details'),
path('api/item-create/', views.itemCreate, name='create'),
path('api/item-update/<str:pk>', views.itemUpdate, name='update'),
path('api/item-delete/<str:pk>', views.itemDelete, name='delete'),
]