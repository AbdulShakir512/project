from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('login/', views.login, name='site-login'),
    path('signup/', views.signup, name='site-signup'),
    path('dashboard/', views.index, name='site-dashboard'),
    path('form1/', views.form1, name='site-form1'),
    path('form1/<int:form_id>', views.form1email, name='site-form1-email'),
    path('form1/<int:form_id>/0/<int:user_id>/', views.form1check1, name='site-form1-check1'),
    path('form1/<int:form_id>/1/<int:user_id>/', views.form1check2, name='site-form1-check2'),
    path('form2/', views.form2, name='site-form2'),
    path('form2/<int:form_id>', views.form2email, name='site-form1-email'),
    path('form2/<int:form_id>/0/<int:user_id>/', views.form2check1, name='site-form2-check1'),
    path('form2/<int:form_id>/1/<int:user_id>/', views.form2check2, name='site-form2-check2'),
]