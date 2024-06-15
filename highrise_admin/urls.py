from django.urls import path
from . import views
from django.conf.urls import handler404

handler404 = 'highrise_admin.views.handler404'
urlpatterns = [
    path('', views.Login, name='Login'),
    path('admin/create-team/', views.CreateTeam, name='CreateTeam'),
    path('admin/create-member/', views.CreateMember, name='CreateMember'),
    path('', views.DropDownTeam, name='DropDownTeam'),
    path('admin/dashboard/', views.Dashboard, name='Dashboard'),
    path('admin/sign-in/', views.Sign_in, name='Sign_in'),
    path('admin/update-data/', views.UpdateData, name='UpdateData'),
    path('admin/fw-update-data/', views.FollowUploadData, name='FollowUploadData'),
    path('admin/user-logout/', views.UserLogout, name='UserLogout'),
    # path('admin/Lead-Funnel/data/', views.LeadFunnelData, name='LeadFunnelData'),
    path('admin/Lead-Funnel/', views.LeadFunnel, name='LeadFunnel'),                   
    path('admin/Daily-Report/', views.DailyPerReport, name='DailyPerReport'),
    path('admin/employee/<str:employee>', views.EmployeeData, name='EmployeeData'),
    # path('Team/wiseData/', views.TeamWiseData, name='TeamWiseData'),
    # path('Member/wiseData/', views.MemberWiseData, name='MemberWiseData'),
    # path('date/filterData/', views.DateFilterData, name='DateFilterData'),
    # path('DPR/Data', views.DPRData, name='DPRData'),
    # path('DPR/teamwiseData/', views.DPRTeamWiseData, name='DPRTeamWiseData'),
    # path('DPR/memberwiseData', views.DPRMemberWiseData, name='DPRMemberWiseData'),
    # path('lead/funnel/', views.LeadDataFilter, name='LeadDataFilter'),
    # path('DPR/filter/', views.DPRFilterData, name='DPRFilterData'),
    # path('date/DPR/', views.DateFilterDPR, name='DateFilterDPR'),
    # path('user/data', views.UserData, name='UserData'),
    # path('pdf/data', views.generate_pdf, name='generate_pdf'),
    # path('admin/pdf/',  views.PDF, name='PDF'),
    # path('LeadFunnel/', views.L_Funnel, name='L_Funnel'),
    path('LeadFunnel/Data', views.L_Funnel, name='L_Funnel'),
    path('DPR/', views.DPR, name='DPR'),
    path('admin/RPT-Team-Performance', views.RPT_team_per, name='RPT_team_per'),
    path('admin/RPT-Funnel', views.RPT_funnel, name='RPT_funnel'),
    path('admin/RPT-SM-Corp', views.RPT_sm_corp, name='RPT_sm_corp'),
    path('admin/Target-Assign/', views.Target_assign, name='Target_assign'),
    path('admin/Delete-Record/', views.Delete_Record, name='Delete_Record'),
    
]

