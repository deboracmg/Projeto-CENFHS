from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from site_institucional import views

urlpatterns = [
    path('', views.index, name='index'),
    path('page-about-us/', views.about_us, name='about_us'),
    path('page-our-services/', views.our_services, name='our_services'),
    path('page-contact-us/', views.contact_us, name='contact_us'),
    path('entrar/', views.EntrarView.as_view(), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'recuperar-senha/',
        auth_views.PasswordResetView.as_view(
            template_name='site/password_reset_form.html',
            email_template_name='site/password_reset_email.html',
            subject_template_name='site/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'recuperar-senha/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='site/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'redefinir-senha/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='site/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'redefinir-senha/concluido/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='site/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
]
