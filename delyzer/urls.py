"""
URL configuration for delyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf 
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from delyzer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('departures/', views.departure_list),
    path('departures/<int:id>', views.departure_detail),
    path('lines/', views.lines),
    path('stations/', views.stations),
    path('delay/lines', views.lines_by_delay),
    path('delay/line/<str:line>/<str:direction>', views.line_by_delay),
    path('delay/times', views.delay_at_time),
    path('delay/times/<str:line>/<str:direction>', views.line_delay_at_time),
    path('delay/stations', views.delay_at_station),
    path('delay/stations/<str:line>/<str:direction>', views.line_delay_at_station),
     path('propability/stations', views.propability_at_stations),
    path('propability/station/<str:station>', views.propability_at_station),
    path('propability/line/<str:line>/<str:direction>', views.propability_of_line),
    path('propability/lines', views.propability_of_lines),

]