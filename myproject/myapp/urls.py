from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
app_name='myapp'
urlpatterns = [

	path('', views.home, name='home'),
	path('properties/', views.properties, name='properties'),
	path('properties/<int:plot_id>/', views.property_single, name='property_single'),
	path('subscription/', views.subscription, name='subscription'),
	path('single/', views.single, name='single'),
	path('signup/', views.signup, name='signup'),
	path('signin/', views.signin, name='signin'),
	path('signout/', views.signout, name='signout'),
	path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=getattr(settings, 'STATIC_ROOT', None))
