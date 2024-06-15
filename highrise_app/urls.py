from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
handler404 = 'highrise_app.views.handler404'

urlpatterns = [
    path('login/',  views.EmployeeLogin, name='EmployeeLogin'),
    path('dashboard/', views.EmployeeDashboard, name='EmployeeDashboard'),
    path('corporate-visit/', views.EmployeeCorpoVisit, name='EmployeeCorpoVisit'),
    path('sage-mitra/', views.SageMitra, name='SageMitra'),
    path('logout/', views.Logout, name='Logout'),
    path('event/', views.AccEvent, name='AccEvent'),
    # path('user-progress/', views.UserProgress, name='UserProgress'),
    path('set-target/', views.Set_Target, name='Set_Target'),
    path('IP/', views.IP, name='IP'),
    path('Admission/', views.Admission, name='Admission'),
    path('Home-visit/', views.Home_visit, name='Home_visit'),
    path('Forget-Password/', views.Forget_password, name='Forget_password'),
    path('OTP-Verification/', views.OTP_verification, name='OTP_verification'),


]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)