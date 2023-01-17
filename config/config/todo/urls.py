from django.urls import path
from .views import TodoDetail, TodoList, TodoCreate, TodoUpdate, TodoDelete
from . import views

urlpatterns = [
    path("list", TodoList.as_view(), name="list"),
    path("detail/<int:pk>", TodoDetail.as_view(), name="detail"),
    path("create/", TodoCreate.as_view(), name="create"),
    path("update/<int:pk>", TodoUpdate.as_view(), name="update"),
    path("delete/<int:pk>", TodoDelete.as_view(), name="delete"),
    path('',views.Login,name='Login'),
    path("logout",views.Logout,name="Logout"),
    path('register', views.AccountRegistration.as_view(), name='register'),
    #path('signup/', views.signup_view, name='signup'),
    #path('login/', views.login_view, name='login'),
    #path('logout/', views.logout_view, name='logout'),
    #path('user/', views.user_view, name='user'),
    #path('other/', views.other_view, name='other'),
    path('month', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('week/', views.WeekCalendar.as_view(), name='week'),
    path('week/<int:year>/<int:month>/<int:day>/', views.WeekCalendar.as_view(), name='week'),
    path('week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),
    path(
        'week_with_schedule/<int:year>/<int:month>/<int:day>/',
        views.WeekWithScheduleCalendar.as_view(),
        name='week_with_schedule'
    ),
    path(
        'month_with_schedule/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'month_with_schedule/<int:year>/<int:month>/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path(
        'mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'
    ),
    path('schedule/change/<int:pk>/', views.ScheduleChange.as_view(), name='schedule_change'),
    path('schedule/detail/<int:pk>/', views.ScheduleDetail.as_view(), name='schedule_detail'),
    path('schedule/delete/<int:pk>/', views.ScheduleDelete.as_view(), name='schedule_delete'),
]

