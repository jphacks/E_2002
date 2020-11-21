from django.urls import path
from . import views
from . import apis
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name ='wakeup'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
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
    path("howto/", views.HowToView.as_view(), name='howto'),
    path('api/', include(apis.router.urls)),
    path('api/how_to_options/', apis.how_to_options, name='how_to_options'),
    path('api/send_out_mail/', apis.send_out_mail, name='send_out_mail'),
    path('api/send_safe_mail/', apis.send_safe_mail, name='send_safe_mail'),
    path('api/air_conditioner_options/', apis.air_conditioner_options, name='air_conditioner_options'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
