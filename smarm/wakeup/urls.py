from django.urls import path
from . import views
from . import apis
from django.conf.urls import include
app_name ='wakeup'

urlpatterns = [
    path('', views.top, name='top'),
    #path("schedule/", views.schedule, name='schedule'),
    path('schedule/', views.MonthCalendar.as_view(), name='month'),
    path('schedule/month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('schedule/week/', views.WeekCalendar.as_view(), name='week'),
    path('schedule/week/<int:year>/<int:month>/<int:day>/', views.WeekCalendar.as_view(), name='week'),
    path('schedule/week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),
    path(
        'schedule/week_with_schedule/<int:year>/<int:month>/<int:day>/',
        views.WeekWithScheduleCalendar.as_view(),
        name='week_with_schedule'
    ),
    path(
        'schedule/month_with_schedule/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'schedule/month_with_schedule/<int:year>/<int:month>/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path('schedule/mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path(
        'schedule/mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'
    ),
    path(
        'schedule/month_with_forms/',
        views.MonthWithFormsCalendar.as_view(), name='month_with_forms'
    ),
    path(
        'schedule/month_with_forms/<int:year>/<int:month>/',
        views.MonthWithFormsCalendar.as_view(), name='month_with_forms'
    ),
    path("howto/", views.howto, name='howto'),
    path('api/', include(apis.router.urls)),
    path('api/options/', apis.options, name='options'),
]
