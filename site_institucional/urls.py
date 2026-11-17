from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from site_institucional import views
from site_institucional.forms import RecuperarSenhaAdminForm

urlpatterns = [
    path('', views.index, name='index'),
    path('page-about-us/', views.about_us, name='about_us'),
    path('page-our-services/', views.our_services, name='our_services'),
    path('page-contact-us/', views.contact_us, name='contact_us'),
    path('entrar/', views.EntrarView.as_view(), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'alterar-senha-obrigatoria/',
        views.alterar_senha_obrigatoria,
        name='alterar_senha_obrigatoria',
    ),
    path(
        'recuperar-senha/',
        auth_views.PasswordResetView.as_view(
            template_name='site/password_reset_form.html',
            email_template_name='site/password_reset_email.html',
            subject_template_name='site/password_reset_subject.txt',
            form_class=RecuperarSenhaAdminForm,
            success_url=reverse_lazy('password_reset_done'),
            extra_context={'active_page': 'login'},
        ),
        name='password_reset',
    ),
    path(
        'recuperar-senha/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='site/password_reset_done.html',
            extra_context={'active_page': 'login'},
        ),
        name='password_reset_done',
    ),
    path(
        'redefinir-senha/<uidb64>/<token>/',
        views.RedefinirSenhaAdminConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'redefinir-senha/concluido/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='site/password_reset_complete.html',
            extra_context={'active_page': 'login'},
        ),
        name='password_reset_complete',
    ),
]
