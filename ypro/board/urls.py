from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('login/', views.login, name='login'),
  path('logout/',views.logout, name='logout'),
  path('list/liga', views.LigaBoardList.as_view(), name='list_liga'),
  path('list/premier', views.PremierBoardList.as_view(), name='list_premier'),
  path('list/serie', views.SerieBoardList.as_view(), name='list_serie'),
  path('list/bundes', views.BundesBoardList.as_view(), name='list_bundes'),
  path('list/liegue', views.LigueBoardList.as_view(), name='list_ligue'),
  path('detail/<int:pk>', views.BoardDetail.as_view(), name='detail'),
  path('update/<int:pk>', views.BoardUpdate.as_view(), name='update'),
  path('create/', views.BoardCreate.as_view(), name='create'),
  path('delete/<int:pk>', views.BoardDelete.as_view(), name='delete'),
]
