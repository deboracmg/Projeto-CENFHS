from django.urls import path

from site_institucional import views


urlpatterns = [
    path('', views.index, name='index'),
    path('page-about-us/', views.about_us, name='about_us'),
    path('page-our-services/', views.our_services, name='our_services'),
    path('page-contact-us/', views.contact_us, name='contact_us'),
    path('entrar/', views.EntrarView.as_view(), name='login'),
]
