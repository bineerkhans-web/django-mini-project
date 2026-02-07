from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from secondapp import views

app_name = 'secondapp'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('plotsale/', views.plotsale, name='plotsale'),
    path('myplot/', views.myplot, name='myplot'),
    path('myplot/<int:plot_id>/update/', views.update_plot, name='update_plot'),
    path('myplot/<int:plot_id>/delete/', views.delete_plot, name='delete_plot'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)