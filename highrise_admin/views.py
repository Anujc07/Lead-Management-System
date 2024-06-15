import pandas as pd
from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from highrise_app.models import *
from datetime import datetime, timedelta
from django.db.models import Count, Case, When, IntegerField, Sum, F, Q, Exists, OuterRef, Subquery, Value, CharField, Func
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.conf import settings
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.db.models.fields import CharField
from xhtml2pdf import pisa
from io import StringIO  
import json
from django.db import transaction
import calendar
from django.contrib import messages
import time




current_da = datetime.now().date()

# Calculate yesterday's date
yesterday_date = current_da - timedelta(days=1)

# Format yesterday's date as a string in the desired format
yesterday_date_str = yesterday_date.strftime("%Y-%m-%d")

def handler404(request, exception):
    return render(request, 'Admin/404.html', status=404)
    

@login_required(login_url='')
def CreateMember(request):
    if request.method == 'POST':
        # print("==========1============")
        try:
            # print("=========2=============")
            name = request.POST['uname']
            team_name = request.POST.get('team_name')
            designation = request.POST['designation']
            ph_number = request.POST['ph_number']
            password = request.POST['password']
            try:
                create_mem = User.objects.create_user(username=name, password=password)
                
                # print("=========3=============")
            except Exception as e:
                # print("=========4=============")
                error_message = f'Thi name already taken{e}'
                return render(request, 'Admin/CreateMember.html', {'error_message': error_message})
                 
            team_instance = get_object_or_404(Teams, pk=team_name)
            crnt_user = get_user_model()
            crnt_user1 = settings.AUTH_USER_MODEL
            user_pwd = crnt_user.objects.get(username=name)
            pwd_main = user_pwd.password
            user = Members.objects.create(
                    uname=name,
                    member_name= name,
                    team=team_instance,
                    designation=designation,
                    mobile=ph_number,
                    pwd= pwd_main
                )
            user.save()
            # print("=========5=============")
            
            
            success_message = f'Member has been created: {name}.'
            return render(request, 'Admin/CreateMember.html', {'success_message': success_message})
        except KeyError as e:
            error_message = f'Missing data: {e}.'
            return render(request, 'Admin/CreateMember.html', {'error_message': error_message})
        except ValueError as e:
            error_message = f'Invalid value: Enter valid value.'
            return render(request, 'Admin/CreateMember.html', {'error_message': error_message})
        except Http404:
            error_message = 'Team not found.'
            return render(request, 'Admin/CreateMember.html', {'error_message': error_message})
    else:
        teams = Teams.objects.values('id', 'T_name')
        return render(request, 'Admin/CreateMember.html', {'teams': teams})
    
    

@login_required(login_url='/')
def CreateTeam(request):
    if request.method == 'POST':
        t_name = request.POST.get('T_name')
        
        team_head_username = request.POST.get('team_head')
        password = request.POST.get('password')
        date = request.POST.get('date')

        # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:           
            team_head = User.objects.get(username=team_head_username)
        except User.DoesNotExist:           
            try:
                team_head = User.objects.create_user(username=team_head_username, password=password)
            except Exception as e:
                error_message = 'Failed to create user. Please try again later. team_head'
                return render(request, 'app/CreateTeam.html', {'error_message': error_message})
        
        try:
            # print("===================")
            team = Teams.objects.create(
                T_name=t_name,
                
                team_head=team_head,
                date=date
            )
            # print("===================")
            team.save()
            success_message = 'Team has been created successfully.'
            return render(request, 'app/CreateTeam.html', {'success_message': success_message})
        except Exception as e:
            error_message = 'Failed to create team. Please try again later.'
            return render(request, 'app/CreateTeam.html', {'error_message': error_message})
    else:
        return render(request, 'app/CreateTeam.html')

@login_required()
def DropDownTeam(request):
    teams = Teams.objects.values('id', 'T_name')
    return render(request, 'app/CreateMember.html',{'teams':teams})


# @login_required()
# def EmployeeData(request, employee):
#     data = HighRiseData.objects.filter(HandledByEmployee=employee)
#     return render(request, 'Admin/UserData.html', {'data': data})

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')        
        if username and password:      
            #print('===========================1')
            user = authenticate(username=username, password=password)
            # request.session['username'] = username
            userna = list(Members.objects.filter(uname = username).values_list('member_name', flat=True))
            request.session['username'] = ', '.join(userna) 
            if user is not None and user.is_superuser:   
                #print('===========================2')
                login(request, user)
                return redirect('/admin/dashboard/')
            elif user is not None and user.is_staff:
                # print('==========================', user)
                teamIDs = list(Members.objects.filter(uname=user).values_list('team_id', flat=True)) 
                team_name_list = list(Teams.objects.filter(id__in=teamIDs).values_list('T_name',  flat=True)) 
                print('==========================',team_name_list)
                if teamIDs:
                    request.session['teamIDs'] = teamIDs 
                    request.session['team_name'] = ', '.join(team_name_list)   
                    
                    
               
                login(request, user)
                return redirect('/admin/dashboard/')

            else:                                
                error_message = 'Invalid username or password.'
                return render(request, 'Admin/Login.html', {'error_message': error_message})
        else:            
            error_message = 'Please provide both username and password.'
            return render(request, 'Admin/Login.html', {'error_message': error_message})
    else:
        return render(request, 'Admin/Login.html')
    

@login_required(login_url='/')
def Dashboard(request):
   
    # teamIDs = list(Members.objects.filter(uname=User).values_list('team_id', flat=True))

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    teamIDs = request.session.get('teamIDs', [])
    
    current_date = datetime.now().date().strftime("%Y-%m-%d")

    if teamIDs and start_date and end_date:    
        end_date =  datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1) 
        members = Members.objects.filter(team_id__in=teamIDs).values('member_name')
        if members.exists():
            for member in members:                
                bookings = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(Enquiry_Status='Booked') & Q(Enquiry_Conclusion_Date__range=(start_date, end_date)) ).count()
                new_leads = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(EDate__range=(start_date, end_date))).count()
                # new_leads = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(EDate__range=(start_date, end_date)) & Q(Enquiry_Status='Open')).count()
                total_leads = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(Enquiry_Status = 'Open')).count()
                site_visit = FollowUpData.objects.filter(Q(EnquiryStage='Site Visit - Done') & Q(Employee_Name=member['member_name']) & Q(FollowUp_Date__range =(start_date, end_date))).count()
                home_visit = HomeVisit.objects.filter(Q(name=member['member_name']) & Q(date__range=(start_date, end_date))).count()
                # home_visit = FollowUpData.objects.filter(Q(EnquiryStage='Home Visit - Done') & Q(Employee_Name=member['member_name']) & Q(FollowUp_Date__range =(start_date, end_date))).count()
                corporate_visit = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_date__range = (start_date, end_date))).count()
                # corpo_solo = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='solo')  & Q(visit_date__range = (start_date, end_date))).count()
                # corporate = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='team')  & Q(visit_date__range = (start_date, end_date))).values_list(
                #     'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
                # )
                
                # total_corporate_count_cofellow  = 0
                # for item in corporate:
                #     names = item[0].split(',')         
                #     for name in names:
                #         corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                #             Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                #             Q(key_person_contact=item[4]) & Q(key_person=item[5])
                #         ).count()                
                #         total_corporate_count_cofellow += corporate_count_cofellow
                # corporate_visit = corpo_solo + total_corporate_count_cofellow
        
    elif teamIDs:
        members = Members.objects.filter(team_id__in=teamIDs).values('member_name')
        if members.exists():
            for member in members:                
                bookings = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(Enquiry_Status='Booked')).count()
                new_leads = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(EDate__date=current_date)).count()              
                # new_leads = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(EDate__date=current_date) & Q(Enquiry_Status='Open')).count()              
                total_leads = HighRiseData.objects.filter(Q(HandledByEmployee=member['member_name']) & Q(Enquiry_Status = 'Open')).count()
                site_visit = FollowUpData.objects.filter(Q(EnquiryStage='Site Visit - Done') & Q(Employee_Name=member['member_name'])).count()                
                # home_visit = FollowUpData.objects.filter(Q(EnquiryStage='Home Visit - Done') & Q(Employee_Name=member['member_name'])).count()
                home_visit = HomeVisit.objects.filter(Q(name=member['member_name'])).count()
                corporate_visit = CorpFormData.objects.filter(name=member['member_name']).count()
                # corpo_solo = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='solo')).count()
                # corporate = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='team')).values_list(
                #     'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
                # )
                
                # total_corporate_count_cofellow  = 0
                # for item in corporate:
                #     names = item[0].split(',')         
                #     for name in names:
                #         corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                #             Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                #             Q(key_person_contact=item[4]) & Q(key_person=item[5])
                #         ).count()                
                #         total_corporate_count_cofellow += corporate_count_cofellow
                # corporate_visit = corpo_solo + total_corporate_count_cofellow

    elif start_date and end_date:     
        end_date =  datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)  
        bookings = HighRiseData.objects.filter(Q(Enquiry_Conclusion_Date__range=(start_date, end_date)) & Q(Enquiry_Status='Booked')).count()
        # new_leads = HighRiseData.objects.filter(Q(EDate__range=(start_date, end_date)) &  Q(Enquiry_Status='Open')).count()
        new_leads = HighRiseData.objects.filter(Q(EDate__range=(start_date, end_date))).count()
        # total_leads = HighRiseData.objects.filter(Q(EDate__range=(start_date, end_date)) &  Q(Enquiry_Status='Open')).count()
        total_leads = HighRiseData.objects.filter(Enquiry_Status = 'Open').count()
        site_visit = FollowUpData.objects.filter(Q(EnquiryStage='Site Visit - Done') & Q(FollowUp_Date__range =(start_date, end_date))).count()
        # site_visit = HighRiseData.objects.filter(Q(StageChangeDate__date__range=(start_date, end_date)) & Q(EnquiryStage='Site Visit - Done')).count()
        # home_visit = HighRiseData.objects.filter(Q(StageChangeDate__date__range=(start_date, end_date)) & Q(EnquiryStage__icontains='Home Visit - Done')).count()
        # home_visit = FollowUpData.objects.filter(Q(EnquiryStage='Home Visit - Done') & Q(FollowUp_Date__range =(start_date, end_date))).count()
        home_visit = HomeVisit.objects.filter(Q(date__range=(start_date, end_date))).count()
        corporate_visit = CorpFormData.objects.filter(visit_date__range = (start_date, end_date)).count()
        # corpo_solo = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='solo')  & Q(visit_date__range = (start_date, end_date))).count()
        # corporate = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='team')  & Q(visit_date__range = (start_date, end_date))).values_list(
        #     'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
        # )
        
        # total_corporate_count_cofellow  = 0
        # for item in corporate:
        #     names = item[0].split(',')         
        #     for name in names:
        #         corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
        #             Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
        
        #             Q(key_person_contact=item[4]) & Q(key_person=item[5])
        #         ).count()                
        #         total_corporate_count_cofellow += corporate_count_cofellow
        # corporate_visit = corpo_solo + total_corporate_count_cofellow
    else:
        site_visit = FollowUpData.objects.filter(Q(EnquiryStage='Site Visit - Done')).count()
        bookings = HighRiseData.objects.filter(Enquiry_Status='Booked').count()
        new_leads = HighRiseData.objects.filter(EDate__date=current_date).count()
        total_leads = HighRiseData.objects.filter(Enquiry_Status = 'Open').count()
        # site_visit = HighRiseData.objects.filter(EnquiryStage='Site Visit - Done').count()
        # home_visit = HighRiseData.objects.filter(EnquiryStage='Home Visit - Done').count()
        home_visit = HomeVisit.objects.filter().count()
        corporate_visit = CorpFormData.objects.all().count()
        # corporate_visit = CorpFormData.objects.filter(Q(visit_type='solo')).count()
       
    # print("========", new_leads, current_date)
    return render(request, 'Admin/dashboard.html', {'bookings': bookings, 'new_leads': new_leads,
                                                     'total_leads': total_leads, 'site_visit': site_visit,
                                                     'home_visit': home_visit, 'corporate_visit': corporate_visit, 'start_date':start_date,
                                                       'end_date':end_date})


def UserLogout(request):
    logout(request)
    return redirect('/') 


# @login_required(login_url='/admin/')
def Sign_in(request):
    if request.method == 'POST':
       
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role') 

        # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        team = User.objects.create_user(
            username=name,
            password=password,
            email=email,
            is_superuser = role
        )
        success_message = 'Team has been created successfully.'
        return render(request, 'Admin/createUser.html', {'success_message': success_message})
    else:
        return render(request, 'Admin/createUser.html')
    






@login_required(login_url='/')
def UpdateData(request):
    error_message = None
    success_message = None
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        try:
            HighRiseData.objects.all().delete()
            df = pd.read_excel(excel_file)
            
            # Disable auto-commit
            with transaction.atomic():
                batch_size = 1000 
                rows_to_insert = []
                for _, row in df.iterrows():
                    highrise_data = HighRiseData()
                    for col_name, value in row.items():
                        if pd.isna(value):
                            setattr(highrise_data, col_name, None)
                        elif col_name == 'Enquiry Conclusion Date':
                            setattr(highrise_data, 'Enquiry_Conclusion_Date', timezone.make_aware(datetime.strptime(value, '%d %b %Y %H:%M:%S')))
                        elif col_name in ['FollowUp_Date', 'Next_FollowUp1', 'EDate', 'StageChangeDate']:
                            setattr(highrise_data, col_name, timezone.make_aware(datetime.strptime(value, '%d %b %Y %H:%M:%S')))
                        else:
                            setattr(highrise_data, col_name, value)
                    rows_to_insert.append(highrise_data)
                    
                    # Save in batches
                    if len(rows_to_insert) >= batch_size:
                        HighRiseData.objects.bulk_create(rows_to_insert)
                        rows_to_insert = []
                
                # Insert any remaining rows
                if rows_to_insert:
                    HighRiseData.objects.bulk_create(rows_to_insert)
                
            messages.success(request, 'Data Uploaded Successfully')
            return redirect('/admin/dashboard/')
        except FileNotFoundError:
            error_message = 'File not found. Please upload a valid Excel file.'
            print('error_message',error_message)
            
        except pd.errors.ParserError:
            error_message = 'Error parsing Excel file. Please ensure the file format is correct.'
            print('error_message',error_message)
        except Exception as e:
            error_message = f'Error: {str(e)}'
            print('error_message',error_message)
    else:
        error_message = 'No file uploaded or invalid request method.'
    # print('error_message', message)
    return render(request, 'Admin/dashboard.html', {'error_message': error_message})



@login_required(login_url='/')
def FollowUploadData(request):
    error_message = None
    success_message = None
    
    if request.method == 'POST' and request.FILES.get('excel_file2'):
        excel_file = request.FILES['excel_file2']
        
        try:
            FollowUpData.objects.all().delete()
            df = pd.read_excel(excel_file)
            print('=======')
            # Convert date and time columns to datetime objects
            date_time_columns = ['Edate', 'Next_FollowUp1', 'FollowUp_Date']
            for col_name in date_time_columns:
                # df[col_name] = pd.to_datetime(df[col_name], format='%d/%m/%Y %H:%M:%S').dt.tz_localize('UTC')
                print(f'=====Original {col_name}=====')
                print(df[col_name].head())  # Print first few rows for checking
                
                # Convert to datetime and then extract the date
                df[col_name] = pd.to_datetime(df[col_name], format='%m/%d/%Y %I:%M:%S %p').dt.date
                
                # Print the converted dates
                print(f'=====Formatted {col_name}=====')
                print(df[col_name].head())
                # df[col_name] = pd.to_datetime(df[col_name], format='%d/%m/%Y %H:%M:%S').dt.date
            
            # Disable auto-commit
            with transaction.atomic():
                batch_size = 1000 
                rows_to_insert = []
                for _, row in df.iterrows():
                    fw_data = FollowUpData()
                    for col_name, value in row.items():
                        if pd.isna(value):
                            setattr(fw_data, col_name, None)
                        else:
                            setattr(fw_data, col_name, value)
                    rows_to_insert.append(fw_data)
                    
                    # Save in batches
                    if len(rows_to_insert) >= batch_size:
                        FollowUpData.objects.bulk_create(rows_to_insert)
                        rows_to_insert = []
                
                # Insert any remaining rows
                if rows_to_insert:
                    FollowUpData.objects.bulk_create(rows_to_insert)
                
            messages.success(request, 'Data Uploaded Successfully')
            return redirect('/admin/dashboard/')
        except FileNotFoundError:
            error_message = 'File not found. Please upload a valid Excel file.'
        except pd.errors.ParserError:
            error_message = 'Error parsing Excel file. Please ensure the file format is correct.'
        except Exception as e:
            error_message = f'Error: {str(e)}'
    else:
        error_message = 'No file uploaded or invalid request method.'
        
    return render(request, 'Admin/dashboard.html', {'error_message': error_message})








# this function run when leadfunnel page render
@login_required(login_url='/')
def LeadFunnel(request):
    teams = Teams.objects.filter(status=1).values('id', 'T_name').order_by('T_name')
    members = Members.objects.filter(status=1).values('id', 'uname', 'member_name').order_by('member_name')
    
    return render(request, 'Admin/LeadFunnel.html', {'teams':teams, 'members':members})
    
 

@login_required(login_url='/')
def DailyPerReport(request):
  
    teams = Teams.objects.filter(status=1).values('id', 'T_name').order_by('T_name')
    members = Members.objects.filter(status=1).values('id', 'uname', 'member_name').order_by('member_name')
    return render(request, 'Admin/DailyPerReport.html', {'teams': teams, 'members': members})


@login_required(login_url='/')
def EmployeeData(request, employee):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    view = request.GET.get('view')  
    
    teamid = Members.objects.filter(member_name__contains=employee, status=1).values_list('team_id', flat=True)
    team = Teams.objects.filter(id__in=teamid, status=1).values()
    
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        # end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        end_date =  datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        previous_date = end_date - timedelta(days=1)
        previous_date_str = previous_date.strftime('%Y-%m-%d')
        total_sm_leads = HighRiseData.objects.filter(HandledByEmployee=employee, EDate__date__range=(start_date, end_date), Enquirytype__contains='Sage Mitra').count()
        # total_leads = HighRiseData.objects.filter(HandledByEmployee=employee).filter(Q(FollowUp_Date__range=(start_date, end_date)) & ~Q(FollowUp_Date=F('Next_FollowUp1')) & ~Q(FollowUp_Date__time=F('Next_FollowUp1__time'))).count()
        # total_leads = HighRiseData.objects.filter(HandledByEmployee=employee).filter(Enquiry_Status='Open').count()
                
               
        # total_leads = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(FollowUp_Date__range=(start_date, end_date)) & Q(Status_Desc = 'Done')).count()                        
        total_leads = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(FollowUp_Date__range=(start_date, end_date))).count()                        
        total_bookings = HighRiseData.objects.filter(HandledByEmployee=employee, Enquiry_Conclusion_Date__range=(start_date, end_date), Enquiry_Status='Booked').count()
        # total_home_visits = HighRiseData.objects.filter(HandledByEmployee=employee, StageChangeDate__date__range=(start_date, end_date), EnquiryStage__icontains='Home Visit - Done').count()
        # total_home_visits = FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date), EnquiryStage__icontains='Home Visit - Done').count()
        total_home_visits = HomeVisit.objects.filter(Q(name=employee) & Q(date__range=(start_date, end_date))).count()
        # total_1_site_visits = HighRiseData.objects.filter(HandledByEmployee=employee, StageChangeDate__date__range=(start_date, end_date), EnquiryStage__icontains='Site Visit - Done').count()
        # total_1_site_visits = SiteVisit.objects.filter(name=employee, date__range=(start_date, end_date), visit_stage='First').count()
        total_1_site_visits = FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date), EnquiryStage__icontains='Site Visit - Done').count()
        hot_leads = HighRiseData.objects.filter(HandledByEmployee=employee, FollowUp_Date__range=(start_date, end_date), CustomerGrade='Hot', Enquiry_Status='Open').count()
        # total_2_site_visits = HighRiseData.objects.filter(HandledByEmployee=employee, StageChangeDate__date__range=(start_date, end_date), EnquiryStage='Site Visit - Revisit').count()
        total_2_site_visits =  FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date), EnquiryStage__icontains='Site Visit - Revisit').count()
        # missed_fw = HighRiseData.objects.filter(HandledByEmployee=employee, Next_FollowUp1__range=(start_date, end_date), Enquiry_Status='Open').count()
        missed_fw = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(Next_FollowUp1__date=previous_date_str)).count()
        SM_FW = Sagemitra.objects.filter(uname=employee, followUp_date__range=(start_date, end_date)).count()
        # total_corpo_visits = CorpFormData.objects.filter(name=employee, visit_date__range=(start_date, end_date)).count()
        corpo_solo = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='solo')  & Q(visit_date__range = (start_date, end_date))).count()
        corporate = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='team')  & Q(visit_date__range = (start_date, end_date))).values_list(
            'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
        )
        
        total_corporate_count_cofellow  = 0
        for item in corporate:
            names = item[0].split(',')         
            for name in names:
                corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                    Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                    Q(key_person_contact=item[4]) & Q(key_person=item[5])
                ).count()                
                total_corporate_count_cofellow += corporate_count_cofellow
        total_corpo_visits = corpo_solo + total_corporate_count_cofellow
        # data = HighRiseData.objects.filter(HandledByEmployee=employee, FollowUp_Date__date__range=(start_date, end_date)).values()
        # data = HighRiseData.objects.filter(HandledByEmployee=employee).filter(Q(FollowUp_Date__range=(start_date, end_date)) & ~Q(FollowUp_Date=F('Next_FollowUp1')) & ~Q(FollowUp_Date__time=F('Next_FollowUp1__time'))).values()
        # data = HighRiseData.objects.filter(HandledByEmployee=employee).filter(Q(FollowUp_Date__range=(start_date, end_date)) & ~Q(EDate=F('FollowUp_Date')) & Q(Enquiry_Status='Open')).values()
        # data  = FollowUpData.objects.filter(Q(Employee_Name=employee) &  Q(FollowUp_Date__range=(start_date, end_date)) & Q(Status_Desc = 'Done')).values()                        
        data  = FollowUpData.objects.filter(Q(Employee_Name=employee) &  Q(FollowUp_Date__range=(start_date, end_date))).values()                        
        # print(total_leads)
        if view == 'Bookings':
            data = HighRiseData.objects.filter(HandledByEmployee=employee, Enquiry_Conclusion_Date__range=(start_date, end_date), Enquiry_Status='Booked').values()
            # print('==============',data)
        elif view == 'Home-Visit':
            # data = HighRiseData.objects.filter(HandledByEmployee=employee, StageChangeDate__date__range=(start_date, end_date), EnquiryStage='Home Visit - Done').values()
            # data = FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date), EnquiryStage__icontains='Home Visit - Done').values()
            data = HomeVisit.objects.filter(Q(name=employee) & Q(date__range=(start_date, end_date))).values()
        elif view == 'SM-Leads':
            data = HighRiseData.objects.filter(HandledByEmployee=employee, EDate__date__range=(start_date, end_date), Enquirytype='Sage Mitra').values()
        elif view == '1Site-Visits':
            data = FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date), EnquiryStage__icontains='Site Visit - Done').values()
        elif view == 'Hot-Leads':
            data = HighRiseData.objects.filter(HandledByEmployee=employee, EDate__date__range=(start_date, end_date), CustomerGrade='Hot', Enquiry_Status='Open').values()
        elif view == '2Site-Visits':
            # data = HighRiseData.objects.filter(HandledByEmployee=employee, StageChangeDate__date__range=(start_date, end_date), EnquiryStage='Site Visit - Revisit').annotate()
            data = FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date), EnquiryStage__icontains='Site Visit - Revisit').values()
        elif view == 'Missed-FW':
            # data = HighRiseData.objects.filter(HandledByEmployee=employee, Next_FollowUp1__range=(start_date, end_date), Enquiry_Status='Open').values()
            data = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(Next_FollowUp1__date=previous_date_str)).values()
        elif view == 'SM-FW':
            data = Sagemitra.objects.filter(uname=employee, followUp_date__range=(start_date, end_date)).values()
        elif view == 'Corp-visits':
            # data = CorpFormData.objects.filter(name=employee, visit_date__range=(start_date, end_date)).values()   
            corpo_solo = CorpFormData.objects.filter(Q(employee) & Q(visit_type='solo')  & Q(visit_date__range = (start_date, end_date))).values()
            corporate = CorpFormData.objects.filter(Q(employee) & Q(visit_type='team')  & Q(visit_date__range = (start_date, end_date))).values_list(
                'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
            )
            
            total_corporate_count_cofellow  = 0
            for item in corporate:
                names = item[0].split(',')         
                for name in names:
                    corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                        Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                        Q(key_person_contact=item[4]) & Q(key_person=item[5])
                    ).values()                
                    
            data = total_corporate_count_cofellow

    else:
        # data = HighRiseData.objects.filter(HandledByEmployee=employee).filter(~Q(EDate=F('FollowUp_Date')) & Q(Enquiry_Status='Open')).values()
        # data = FollowUpData.objects.filter(Employee_Name=employee, Status_Desc = 'Done').values()
        data =FollowUpData.objects.filter(Employee_Name=employee).values()      
        total_sm_leads = HighRiseData.objects.filter(HandledByEmployee=employee, Enquirytype__contains='Sage Mitra').count()
        # total_1_site_visits = HighRiseData.objects.filter(HandledByEmployee=employee, EnquiryStage='Site Visit - Done').count()
        total_1_site_visits = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage__icontains='Site Visit - Done').count()
        # total_leads = HighRiseData.objects.filter(HandledByEmployee=employee).filter(Enquiry_Status='Open').count()
        total_leads = FollowUpData.objects.filter(Employee_Name=employee).count()      
        total_bookings = HighRiseData.objects.filter(HandledByEmployee=employee, Enquiry_Status='Booked').count()
        # total_home_visits = HighRiseData.objects.filter(HandledByEmployee=employee, EnquiryStage='Home Visit - Done').count()
        total_home_visits = HomeVisit.objects.filter(Q(name=employee)).count()
        # total_home_visits = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage__icontains='Home Visit - Done').count()
        # hot_leads = HighRiseData.objects.filter(HandledByEmployee=employee, CustomerGrade='Hot', Enquiry_Status='Open').count()
        hot_leads = HighRiseData.objects.filter(HandledByEmployee=employee, CustomerGrade='Hot', Enquiry_Status='Open').count()
        # total_2_site_visits = HighRiseData.objects.filter(HandledByEmployee=employee, EnquiryStage='Site Visit - Revisit').count()
        total_2_site_visits = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage__icontains='Site Visit - REvisit').count()
        # missed_fw = HighRiseData.objects.filter(HandledByEmployee=employee, Next_FollowUp1__date=(current_date), Enquiry_Status='Open').count()
        missed_fw = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(Next_FollowUp1__date=yesterday_date_str)).count()
        SM_FW = Sagemitra.objects.filter(uname=employee).count()
        # total_corpo_visits = CorpFormData.objects.filter(name=employee).count()  
        corpo_solo = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='solo') ).count()
        corporate = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='team')).values_list(
            'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
        )
        
        total_corporate_count_cofellow  = 0
        for item in corporate:
            names = item[0].split(',')         
            for name in names:
                corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                    Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                    Q(key_person_contact=item[4]) & Q(key_person=item[5])
                ).count()                
                total_corporate_count_cofellow += corporate_count_cofellow
        total_corpo_visits = corpo_solo + total_corporate_count_cofellow  
        
        # print('=================', employee)
        if view == 'Bookings':
            data = HighRiseData.objects.filter(HandledByEmployee=employee, Enquiry_Status='Booked').values()
        elif view == 'Home-Visit':
            # data = HighRiseData.objects.filter(HandledByEmployee=employee, EnquiryStage='Home Visit - Done').values()
            # data = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage__icontains='Home Visit - Done').values()
            data = HomeVisit.objects.filter(Q(name=employee)).values()
        elif view == 'SM-Leads':
            data = HighRiseData.objects.filter(HandledByEmployee=employee, Enquirytype__contains='Sage Mitra').values()
        elif view == '1Site-Visits':
            data = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage__icontains='Site Visit - Done').values()
        elif view == 'Hot-Leads':
            data = HighRiseData.objects.filter(HandledByEmployee=employee, CustomerGrade='Hot', Enquiry_Status='Open' ).values()
        elif view == '2Site-Visits':
            data = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage__icontains='Site Visit - Revisit').values()
        elif view == 'Missed-FW':
            # data = HighRiseData.objects.filter(HandledByEmployee=employee, Next_FollowUp1__date=(current_date), Enquiry_Status='Open').values()
            data = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(Next_FollowUp1__date=yesterday_date_str)).values()
        elif view == 'SM-FW':
            data = Sagemitra.objects.filter(uname=employee).values()
        elif view == 'Corp-visits':
            data = CorpFormData.objects.filter(name=employee).values()   
            corpo_solo = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='solo') ).values()
            corporate = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='team')).values_list(
                'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
            )
            
            total_corporate_count_cofellow  = 0
            for item in corporate:
                names = item[0].split(',')         
                for name in names:
                    corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                        Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                        Q(key_person_contact=item[4]) & Q(key_person=item[5])
                    ).values()                
                 
                 # total_corporate_count_cofellow += corporate_count_cofellow
            total_corpo_visits =  corporate_count_cofellow
    
    return render(request, 'Admin/UserData.html', {'total_corpo_visits': total_corpo_visits, 'SM_FW': SM_FW, 'missed_fw': missed_fw, 'total_2_site_visits': total_2_site_visits, 'hot_leads': hot_leads,
                                                   'view': view, 'team': team, 'start_date': start_date_str, 'end_date': end_date_str, 'data': data, 'name': employee,
                                                   'total_sm_leads': total_sm_leads, 'total_home_visits': total_home_visits, 'total_bookings': total_bookings, 'total_leads': total_leads, 'total_1_site_visits': total_1_site_visits })





def get_report_data(start_date=None, end_date=None, request=None):
    teamIDs = request.session.get('teamIDs', [])
    if teamIDs:
        teams = Teams.objects.filter(status=1, id__in=teamIDs).values('id', 'T_name')
    else:
        teams = Teams.objects.filter(status=1).values('id', 'T_name')

    # print(teams)
    team_members = {}
    team_sm_counts = {}
    team_corp_counts = {}
    current_month = datetime.now().strftime("%B")
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date =  datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        select_month = start_date.strftime("%B") 
        # cuurent_date = datetime.no
        # print(current_date)
        # e_date =  datetime.strptime(end_date, '%Y-%m-%d') 
        for team in teams:
            members = Members.objects.filter(team_id=team['id'], status=1).values('id', 'member_name').order_by('member_name')
            team_data = {}
            team_sm_count = 0
            team_corp_count = 0

            for member in members:
                target_query = EmpSetTarget.objects.filter(Employee_id=member['id'], month=select_month)
                target_values = target_query.values('target', 'Target_id')
               
                # corp = CorpFormData.objects.filter(name=member['member_name'], visit_date__range=(start_date, end_date)).count()
                corpo_solo = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='solo')  & Q(visit_date__range = (start_date, end_date))).count()
                corporate = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='team')  & Q(visit_date__range = (start_date, end_date))).values_list(
                    'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
                )
                
                total_corporate_count_cofellow  = 0
                for item in corporate:
                    names = item[0].split(',')         
                    for name in names:
                        corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                            Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                            Q(key_person_contact=item[4]) & Q(key_person=item[5])
                        ).count()                
                        total_corporate_count_cofellow += corporate_count_cofellow
                corp = corpo_solo + total_corporate_count_cofellow
                sm_sum = Sagemitra.objects.filter(uname=member['member_name'], followUp_date__range=(start_date, end_date)).count()
                high_rise_data = HighRiseData.objects.filter(HandledByEmployee=member['member_name'])            
                Home_visit = HomeVisit.objects.filter(Q(name=member['member_name']) & Q(date__range=(start_date, end_date))).count()
                # Home_visit = FollowUpData.objects.filter(Q(Employee_Name=member['member_name']) & Q(FollowUp_Date__range=(start_date, end_date)) & Q(EnquiryStage__icontains='Home Visit - Done')).count()
                # followup = FollowUpData.objects.filter(Q(Employee_Name=member['member_name']) & Q(FollowUp_Date__range=(start_date, end_date)) & Q(Status_Desc = 'Done')).count()          
                followup = FollowUpData.objects.filter(Q(Employee_Name=member['member_name']) & Q(FollowUp_Date__range=(start_date, end_date))).count()          
                
                member_data = high_rise_data.aggregate(
                    bookings=Count('Enquiry_Status', filter=Q(Enquiry_Status='Booked') & Q(Enquiry_Conclusion_Date__range=(start_date, end_date))),
                    # home_visit=Count('EnquiryStage', filter=Q(EnquiryStage='Home Visit - Done', StageChangeDate__range=(start_date, end_date))),
                    # customerfollowup=Sum(Case(When(Q(FollowUp_Date__range=(start_date, end_date)) & ~Q(EDate__date=F('FollowUp_Date')),then=1),default=0,output_field=IntegerField())),
                    # new_leads=Count('EDate', filter=Q(EDate__range=(start_date, end_date)) & Q(Enquiry_Status='Open')),
                    new_leads=Count('EDate', filter=Q(EDate__range=(start_date, end_date))),
                )
                member_data['corp_visits'] = corp
                member_data['total_sm_leads'] = sm_sum
                member_data['customerfollowup'] = followup
                member_data['home_visit'] = Home_visit
                member_data['target_values'] = target_values
                team_sm_count += sm_sum
                team_corp_count += corp
                
                team_data[member['member_name']] = member_data

            team_sm_counts[team['id']] = team_sm_count
            team_corp_counts[team['id']] = team_corp_count
            team_members[team['T_name']] = team_data

        return teams, team_members, team_sm_counts, team_corp_counts
    else:
        for team in teams:
            members = Members.objects.filter(team_id=team['id'], status=1).values('id', 'member_name').order_by('member_name')
            team_data = {}
            team_sm_count = 0
            team_corp_count = 0

            for member in members:
                target_query = EmpSetTarget.objects.filter(Employee_id=member['id'], month=current_month)
                target_values = target_query.values('target', 'Target_id')
                
                # corp = CorpFormData.objects.filter(name=member['member_name']).count()
                corpo_solo = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='solo') ).count()
                corporate = CorpFormData.objects.filter(Q(name=member['member_name']) & Q(visit_type='team')  ).values_list(
                    'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
                )
                
                total_corporate_count_cofellow  = 0
                for item in corporate:
                    names = item[0].split(',')         
                    for name in names:
                        corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                            Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                            Q(key_person_contact=item[4]) & Q(key_person=item[5])
                        ).count()                
                        total_corporate_count_cofellow += corporate_count_cofellow
                corp = corpo_solo + total_corporate_count_cofellow
                
                sm_sum = Sagemitra.objects.filter(uname=member['member_name']).count()
                # Home_visit = FollowUpData.objects.filter(Q(Employee_Name=member['member_name']) & Q(EnquiryStage__icontains='Home Visit - Done')).count()
                Home_visit = HomeVisit.objects.filter(Q(name=member['member_name'])).count()
                high_rise_data = HighRiseData.objects.filter(HandledByEmployee=member['member_name'])
                # followup = FollowUpData.objects.filter(Q(Employee_Name=member['member_name']) & Q(Status_Desc = 'Done')).count()          
                followup = FollowUpData.objects.filter(Q(Employee_Name=member['member_name'])).count()          

                member_data = high_rise_data.aggregate(
                    bookings=Count('Enquiry_Status', filter=Q(Enquiry_Status='Booked')),
                    # home_visit=Count('EnquiryStage', filter=Q(EnquiryStage='Home Visit - Done')),
                    # customerfollowup=Sum(Case(When(~Q(EDate=F('FollowUp_Date')) & Q(FollowUp_Date__isnull=False), then=1), default=0, output_field=IntegerField())),
                    new_leads=Count('EDate', filter=Q(EDate__date=current_date)),
                )
                member_data['corp_visits'] = corp
                member_data['total_sm_leads'] = sm_sum
                member_data['target_values'] = target_values
                member_data['customerfollowup'] = followup
                member_data['home_visit'] = Home_visit
                
                team_sm_count += sm_sum
                team_corp_count += corp

                team_data[member['member_name']] = member_data

            team_sm_counts[team['id']] = team_sm_count
            team_corp_counts[team['id']] = team_corp_count
            team_members[team['T_name']] = team_data

        return teams, team_members, team_sm_counts, team_corp_counts



@login_required(login_url='/')
def RPT_team_per(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    teams, team_members, team_sm_counts, team_corp_counts = get_report_data(start_date, end_date, request)
    return render(request, 'admin/RPT-Team-Performance.html', {'team': teams, 'team_members': team_members, 'start_date':start_date , 'end_date':end_date})


@login_required(login_url='/')
def RPT_sm_corp(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    teams, team_members, team_sm_counts, team_corp_counts = get_report_data(start_date, end_date, request)
    return render(request, 'admin/RPT-SM-Corp-FW.html', {'team_sm_counts':team_sm_counts,'team_corp_counts':team_corp_counts,'team': teams, 'team_members': team_members, 'start_date': start_date, 'end_date': end_date})


@login_required(login_url='/')
# def RPT_funnel(request):
#     teamIDs = request.session.get('teamIDs', [])
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     current_date = datetime.now().date().strftime("%Y-%m-%d")
#     follow = []    
#     data = []
#     if start_date and end_date:
#         end_date =  datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
#         end_date__d = datetime.strptime(end_date, '%Y-%m-%d')
#         # Subtract one day from end_date
#         previous_date = end_date__d - timedelta(days=1)
#         # Convert previous_date back to string
#         previous_date_str = previous_date.strftime('%Y-%m-%d')
#         member = Members.objects.filter(status=1).values_list('member_name')
#         print('================================',member)
#         member_names = HighRiseData.objects.values('HandledByEmployee').order_by('HandledByEmployee').distinct()
#         for member_name in member_names:       
#             missed_followUp = FollowUpData.objects.filter(Q(Employee_Name=member_name['HandledByEmployee']) & Q(Next_FollowUp1__date=previous_date_str)).count()
#             follow.append({'name': member_name['HandledByEmployee'], 'missed_followUp': missed_followUp})
#         data = HighRiseData.objects.values('HandledByEmployee').order_by('HandledByEmployee').annotate(
#             total_leads=Sum(Case(When(Enquiry_Status='Open', then=1), default=0, output_field=IntegerField())),
#             # total_call_contected=Sum(Case(When(Q(EDate__range=(start_date, end_date)) & Q(Result='Call Not Picked'), then=1), default=0, output_field=IntegerField())),
#             # total_missed_FW=Sum(Case(When(Q(Enquiry_Status='Open') & Q(EDate__range=(start_date, end_date)), then=1), default=0, output_field=IntegerField())),
         
#             total_hot_leads=Sum(Case(When(Q(CustomerGrade='Hot') & Q(FollowUp_Date__range=(start_date, end_date)) & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#             total_opportunity=Sum(Case(When(Q(CustomerGrade='Opportunity') & Q(FollowUp_Date__range=(start_date, end_date)) & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#             total_proposal=Sum(Case(When(Q(CustomerGrade='Proposal') & Q(FollowUp_Date__range=(start_date, end_date)) & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#             total_cold=Sum(Case(When(Q(CustomerGrade='Cold') & Q(FollowUp_Date__range=(start_date, end_date)) & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#             total_closed=Sum(Case(When(Q(Enquiry_Status='Closed') & Q(Enquiry_Conclusion_Date__range=(start_date, end_date)), then=1), default=0, output_field=IntegerField())),
#             total_bookings=Sum(Case(When(Q(Enquiry_Status='Booked') & Q(Enquiry_Conclusion_Date__range=(start_date, end_date)), then=1), default=0, output_field=IntegerField()))
#         )
#     else:
#         member = list(Members.objects.filter(status=1).values('member_name').order_by('member_name'))
#         # print('================================',member['member_name'])

#         # member_names = HighRiseData.objects.values('HandledByEmployee').order_by('HandledByEmployee').distinct()
#         for member_name in member:       
#             print('=============',member_name)
#             missed_followUp = FollowUpData.objects.filter(Q(Employee_Name=member_name['member_name']) & Q(Next_FollowUp1__date=yesterday_date_str)).count()
#             follow.append({'name': member_name, 'missed_followUp': missed_followUp})
#             data_m = HighRiseData.objects.filter(HandledByEmployee=member_name['member_name']).values('HandledByEmployee').order_by('HandledByEmployee').annotate(
#                 total_leads=Sum(Case(When(Enquiry_Status='Open', then=1), default=0, output_field=IntegerField())),
#                 # total_call_contected=Sum(Case(When(Result='Call Not Picked', then=1), default=0, output_field=IntegerField())),
#                 # total_missed_FW=Sum(Case(When(Q(Next_FollowUp1__date = (current_date)) & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#                 total_hot_leads=Sum(Case(When(Q(CustomerGrade='Hot') & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#                 total_opportunity=Sum(Case(When(Q(CustomerGrade='Opportunity') & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#                 total_proposal=Sum(Case(When(Q(CustomerGrade='Proposal') & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#                 total_cold=Sum(Case(When(Q(CustomerGrade='Cold') & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
#                 total_closed=Sum(Case(When(Enquiry_Status='Closed', then=1), default=0, output_field=IntegerField())),
#                 total_bookings=Sum(Case(When(Enquiry_Status='Booked', then=1), default=0, output_field=IntegerField()))
#             )
#             data.append(data_m)
#     return render(request, 'admin/RPT-Funnel.html', {'data': data, 'start_date': start_date, 'end_date': end_date,'follow': follow})

@login_required(login_url='/')
def RPT_funnel(request):
    teamIDs = request.session.get('teamIDs', [])
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    follow = []
    data = []

    if start_date and end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        end_date__d = end_date + timedelta(days=1) - timedelta(seconds=1)
        previous_date = end_date__d - timedelta(days=1)
        previous_date_str = previous_date.strftime('%Y-%m-%d')
        if teamIDs:
            members = Members.objects.filter(status=1, team_id__in=teamIDs).order_by('member_name')
        else:
            members = Members.objects.filter(status=1).order_by('member_name')

        for member in members:
            missed_followUp = FollowUpData.objects.filter(
                Q(Employee_Name=member.member_name) & Q(Next_FollowUp1__date=previous_date_str)
            ).count()
            follow.append({'name': member.member_name, 'missed_followUp': missed_followUp})

            data.append(
                {
                    'HandledByEmployee': member.member_name,
                    'total_leads': HighRiseData.objects.filter(HandledByEmployee=member.member_name, Enquiry_Status='Open').count(),
                    'total_hot_leads': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Hot', FollowUp_Date__range=(start_date, end_date), Enquiry_Status='Open').count(),
                    'total_opportunity': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Opportunity', FollowUp_Date__range=(start_date, end_date), Enquiry_Status='Open').count(),
                    'total_proposal': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Proposal', FollowUp_Date__range=(start_date, end_date), Enquiry_Status='Open').count(),
                    'total_cold': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Cold', FollowUp_Date__range=(start_date, end_date), Enquiry_Status='Open').count(),
                    'total_closed': HighRiseData.objects.filter(HandledByEmployee=member.member_name, Enquiry_Status='Closed', Enquiry_Conclusion_Date__range=(start_date, end_date)).count(),
                    'total_bookings': HighRiseData.objects.filter(HandledByEmployee=member.member_name, Enquiry_Status='Booked', Enquiry_Conclusion_Date__range=(start_date, end_date)).count(),
                }
            )
    else:
        previous_date = datetime.now() - timedelta(days=1)
        previous_date_str = previous_date.strftime('%Y-%m-%d')

        if teamIDs:
            members = Members.objects.filter(status=1, team_id__in=teamIDs).order_by('member_name')
        else:
            members = Members.objects.filter(status=1).order_by('member_name')
        for member in members:
            missed_followUp = FollowUpData.objects.filter(
                Q(Employee_Name=member.member_name) & Q(Next_FollowUp1__date=previous_date_str)
            ).count()
            follow.append({'name': member.member_name, 'missed_followUp': missed_followUp})

            data.append(
                {
                    'HandledByEmployee': member.member_name,
                    'total_leads': HighRiseData.objects.filter(HandledByEmployee=member.member_name, Enquiry_Status='Open').count(),
                    'total_hot_leads': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Hot', Enquiry_Status='Open').count(),
                    'total_opportunity': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Opportunity', Enquiry_Status='Open').count(),
                    'total_proposal': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Proposal', Enquiry_Status='Open').count(),
                    'total_cold': HighRiseData.objects.filter(HandledByEmployee=member.member_name, CustomerGrade='Cold', Enquiry_Status='Open').count(),
                    'total_closed': HighRiseData.objects.filter(HandledByEmployee=member.member_name, Enquiry_Status='Closed').count(),
                    'total_bookings': HighRiseData.objects.filter(HandledByEmployee=member.member_name, Enquiry_Status='Booked').count(),
                }
            )

    return render(request, 'admin/RPT-Funnel.html', {'data': data, 'start_date': start_date, 'end_date': end_date, 'follow': follow})




@login_required(login_url='/')
def Target_assign(request):
    emp = Members.objects.filter(status=1).all().values('member_name', 'id', 'uname').order_by('member_name')
    target = Target.objects.all().values('id', 'name').order_by('name')
    months = [calendar.month_name[i] for i in range(1, 13)]
    current_month = datetime.now().strftime("%B")
    teamIDs = request.session.get('teamIDs', [])

    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        target_id = request.POST.get('target')
        year = request.POST.get('year')
        month = request.POST.get('month')
        target_value = request.POST.get('target_value')

        target_instance = Target.objects.get(id=target_id)
        
        obj = EmpSetTarget.objects.filter(Target=target_instance, Employee_id=employee_id, month=month).first()
        
        if obj:
           
            obj.target = target_value
            obj.year = year
            obj.month = month
            obj.save()
        else:            
            set_target = EmpSetTarget.objects.create(
                Employee_id=employee_id, 
                Target=target_instance,
                target=target_value,
                year=year,
                month=month
            )
            set_target.save()
        
        return redirect('/admin/Target-Assign/')
    if teamIDs:
        print(teamIDs)
        emp_data = Members.objects.filter(status=1, team_id__in=teamIDs).values_list('member_name', 'id').order_by('member_name')
        emp = Members.objects.filter(status=1, team_id__in=teamIDs).all().values('member_name', 'id', 'uname').order_by('member_name')
    else: 
        emp_data = Members.objects.filter(status=1).values_list('member_name', 'id').order_by('member_name')
    
    target_data_list = []
    for member_tuple in emp_data:
        member_name = member_tuple[0]  
        member_id = member_tuple[1]
        target_data = EmpSetTarget.objects.filter(Employee_id=member_id, month=current_month).values('Target_id', 'target', 'month')
        target_data_list.append({'member_name': member_name, 'target_data': target_data})
    # print('=============', target_data_list)

    context = {'emp': emp, 'target': target, 'months': months, 'target_data_list': target_data_list}
    return render(request, 'Admin/TargetAssign.html', context)
    




# Lead Funnel section start 
def LF_Date_Range(emp, start_date, end_date, request):
    data = []
    teamIDs = request.session.get('teamIDs', [])
    if teamIDs:
        emp = Members.objects.filter(team_id__in=teamIDs, status=1).order_by('member_name').values_list('member_name', flat=True)
    end_d = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
    for employee in emp:
        first_site_visits = FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date),
                EnquiryStage='Site Visit - Done').count()
        second_site_visits = FollowUpData.objects.filter(Employee_Name=employee,  FollowUp_Date__range=(start_date, end_date),
                EnquiryStage='Site Visit - Revisit').count()
        employee_data = HighRiseData.objects.filter(HandledByEmployee=employee).values('HandledByEmployee').order_by('HandledByEmployee').annotate(
            total_leads=Count(Case(When(Enquiry_Status='Open', then=1), default=0, output_field=CharField())),
            hot_leads=Sum(Case(When(Q(FollowUp_Date__range=(start_date, end_date)) & Q(CustomerGrade='Hot') & Q(Enquiry_Status='Open'), then=1), default=0, output_field=CharField())),
            new_leads=Count(Case(When(Q(EDate__range=(start_date, end_date)) , then=0), output_field=CharField())),
            # new_leads=Count(Case(When(Q(EDate__range=(start_date, end_date)) & Q(Enquiry_Status='Open'), then=0), output_field=CharField())),
        )
        for item in employee_data:
            item['first_site_visits'] = first_site_visits
            item['second_site_visits'] = second_site_visits
            data.append(item)
    return data


def LF_Without_Date_Range(emp, request):
    teamIDs = request.session.get('teamIDs', [])
    if teamIDs:
        emp = Members.objects.filter(team_id__in=teamIDs, status=1).order_by('member_name').values_list('member_name', flat=True)
    
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    data = []
    for employee in emp:
        first_site_visits = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage='Site Visit - Done').count()
        second_site_visits = FollowUpData.objects.filter(Employee_Name=employee, EnquiryStage='Site Visit - Revisit').count()

        employee_data = HighRiseData.objects.filter(HandledByEmployee=employee).values('HandledByEmployee').order_by('HandledByEmployee').annotate(            
            total_leads=Sum(Case(When(Enquiry_Status='Open', then=1),default=0 ,output_field=IntegerField() )),
            hot_leads=Sum(Case(When(Q(CustomerGrade='Hot') & Q(Enquiry_Status='Open'), then=1),default=0 ,output_field=CharField() )),
            # first_site_visits=Sum(Case(When(EnquiryStage__icontains='Site Visit - Done', then=1),default=0,output_field=CharField())),
            # second_site_visits=Sum(Case(When(EnquiryStage__icontains='Site Visit - Revisit', then=1),default=0,output_field=CharField())),
            new_leads=Sum(Case(When(EDate__date=current_date,  then=1),default=0 ,output_field=IntegerField())),           
            # new_leads=Sum(Case(When(EDate__date=current_date,Enquiry_Status='Open',  then=1),default=0 ,output_field=IntegerField())),           
        )
        for item in employee_data:
            item['first_site_visits'] = first_site_visits
            item['second_site_visits'] = second_site_visits
            data.append(item)
    return data

def Filter(start_date=None, end_date=None, member=None, team=None, request=None):    
    emp = []
    members = None
    if start_date and end_date:
        if member and team:        
            # print('=======')             
            employee_queryset = Members.objects.filter(member_name=member, status=1)
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name',flat=True)

            if employee_queryset.exists():
                emp = [employee_queryset.first().member_name]
                leadfunnelData = LF_Date_Range(emp, start_date, end_date, request)

        elif member:
            employee_queryset = Members.objects.filter(member_name=member, status=1)
            members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name',flat=True)

            if employee_queryset.exists():
                emp = [employee_queryset.first().member_name]
                leadfunnelData = LF_Date_Range(emp, start_date, end_date, request)

        elif team  :
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name', flat=True)
            emp = list(members)
            leadfunnelData = LF_Date_Range(emp, start_date, end_date, request)
            
        else:           
            members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name', flat=True)
            emp = list(members)
            leadfunnelData = LF_Date_Range(emp, start_date, end_date, request)

    elif team or member:

        if member and team:
            # print('=======')
            # print(member, team,'=================')
            employee_queryset = Members.objects.filter(member_name=member, status=1)
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name',flat=True)

            if employee_queryset.exists():
                emp = [employee_queryset.first().member_name]
                leadfunnelData = LF_Without_Date_Range(emp, request)

        elif member:
            # print('======')
            employee_queryset = Members.objects.filter(member_name=member, status=1)
            members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name',flat=True)
            # print(employee_queryset)
            # print(members)
            if employee_queryset.exists():
                emp = [employee_queryset.first().member_name]
                leadfunnelData = LF_Without_Date_Range(emp, request)
        elif team:
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name', flat=True)
            emp = list(members)
            leadfunnelData = LF_Without_Date_Range(emp, request)

        else:           
            members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name', flat=True)
            emp = list(members)
            leadfunnelData = LF_Without_Date_Range(emp, request)

    else:
        
        members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name', flat=True)
        emp = list(members)
        leadfunnelData = LF_Without_Date_Range(emp, request)




    return leadfunnelData, members

def L_Funnel(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    member = request.GET.get('member')
    team = request.GET.get('team')
    
    try:
        leadfunnelData, members = Filter(start_date, end_date, member, team, request) 
        leadfunnelData_list = list(leadfunnelData)
        print(members)
        members_list = list(members)  
        return JsonResponse({'leadfunnelData': leadfunnelData_list, 'members': members_list}, safe=False)
    except Exception as e:
        print(f"Error occurred: {e}")
        return JsonResponse({'error': str(e)}, status=500)
#-===========end of lead funnel ===============



# this section for DPR functions where we get request from user and filter data here with dates, members, teams
# this funtion run when user select the dates 

def DPR_Date_Range(emp, start_date, end_date, request):
    end_date_str = datetime.strptime(end_date, '%Y-%m-%d')
    end_date_present = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
    previous_date = end_date_str - timedelta(days=1)
    previous_date_str = previous_date.strftime('%Y-%m-%d')
    current_month = datetime.now().strftime("%B")
    data = []

    emp = list(emp)
    # print('===emp===', emp)
    teamIDs = request.session.get('teamIDs', [])
    if teamIDs:
        emp = Members.objects.filter(team_id__in=teamIDs, status=1).order_by('member_name').values_list('member_name', 'id')
    for employee, employee_id  in emp:       

        target = EmpSetTarget.objects.filter(Employee_id=employee_id, month=current_month).values('Target_id', 'target')
       
        # corpo_visit = CorpFormData.objects.filter(name=employee, visit_date__range=(start_date, end_date)).count()
        corpo_solo = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='solo')).count()
        corporate = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='team')).values_list(
            'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
        )
        
        total_corporate_count_cofellow  = 0
        for item in corporate:
            names = item[0].split(',')         
            for name in names:
                corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                    Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                    Q(key_person_contact=item[4]) & Q(key_person=item[5])
                ).count()                
                total_corporate_count_cofellow += corporate_count_cofellow
        corpo_visit = corpo_solo + total_corporate_count_cofellow
        sm_followup = Sagemitra.objects.filter(uname=employee, followUp_date__range=(start_date, end_date)).count()
        lead_FW = FollowUpData.objects.filter(Employee_Name=employee, FollowUp_Date__range=(start_date, end_date_str)).count()
        missed_followUp = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(Next_FollowUp1__date=previous_date_str)).count()
        # home_visit = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(EnquiryStage='Home Visit - Done') & Q(FollowUp_Date__range=(start_date, end_date))).count()
        home_visit = HomeVisit.objects.filter(Q(name=employee) & Q(date__range=(start_date, end_date))).count()
        
        employee_data = HighRiseData.objects.filter(HandledByEmployee=employee).values('HandledByEmployee').order_by('HandledByEmployee').annotate(
            booked_count=Sum(Case(When(Q(Enquiry_Conclusion_Date__range=(start_date, end_date)) & Q(Enquiry_Status='Booked'), then=1), default=0, utput_field=IntegerField())),
            # new_leads=Sum(Case(When(Q(EDate__range=(start_date, end_date)) & Q(Enquiry_Status='Open'), then=1), default=0, output_field=IntegerField())),
            new_leads=Sum(Case(When(Q(EDate__range=(start_date, end_date)), then=1), default=0, output_field=IntegerField())),
            leadsSageMitra=Sum(Case(When(Q(EDate__range=(start_date, end_date)) & Q(Enquirytype__contains='Sage Mitra'), then=1), default=0, output_field=IntegerField())),
        )
        for ed in employee_data:
            # ed['corpo_visit'] = list(corpo_visit)
            ed['corpo_visit'] = corpo_visit
            ed['home_visit'] = home_visit
            # ed['sm_followup'] = list(sm_followup)
            ed['sm_followup'] = sm_followup
            ed['lead_FW'] = lead_FW
            ed['missed_followUp'] = missed_followUp
            data.append(ed)
            ed['target'] = list(target)
    return data


# this function run when user want data with out dates
def DPR_Without_Date_Range(emp, request):
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    yesterday_date = datetime.now() - timedelta(1)
    yesterday_date_str = yesterday_date.strftime("%Y-%m-%d")
    current_month = datetime.now().strftime("%B")
    data = []
    # print('=================',list(emp))
    emp = list(emp)
    start_time = time.time()
    teamIDs = request.session.get('teamIDs', [])
    # print('===================================',emp)
    if teamIDs:
        emp = Members.objects.filter(team_id__in=teamIDs, status=1).order_by('member_name').values_list('member_name', 'id')
        member = Members.objects.filter(team_id__in=teamIDs, status=1).order_by('member_name').values_list('member_name', 'id')
    
    for employee, employee_id in emp:

        target = EmpSetTarget.objects.filter(Employee_id=employee_id, month=current_month).values('Target_id', 'target')
        
        # corpo_visit = CorpFormData.objects.filter(name=employee).count()
        corpo_solo = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='solo') ).count()
        corporate = CorpFormData.objects.filter(Q(name=employee) & Q(visit_type='team') ).values_list(
            'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
        )
        
        total_corporate_count_cofellow  = 0
        for item in corporate:
            names = item[0].split(',')         
            for name in names:
                corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                    Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                    Q(key_person_contact=item[4]) & Q(key_person=item[5])
                ).count()                
                total_corporate_count_cofellow += corporate_count_cofellow
        corpo_visit = corpo_solo + total_corporate_count_cofellow
        sm_followup = Sagemitra.objects.filter(uname=employee).count()
        lead_FW = FollowUpData.objects.filter(Employee_Name=employee).count()
        missed_followUp = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(Next_FollowUp1__date=yesterday_date_str)).count()
        # home_visit = FollowUpData.objects.filter(Q(Employee_Name=employee) & Q(EnquiryStage='Home Visit - Done')).count()
        home_visit = HomeVisit.objects.filter(Q(name=employee)).count()
        
        employee_data = HighRiseData.objects.filter(HandledByEmployee=employee).values('HandledByEmployee').order_by('HandledByEmployee').annotate(
            booked_count=Sum(Case(When(Q(Enquiry_Status='Booked'), then=1), default=0, output_field=IntegerField())),           
            new_leads=Sum(Case(When(EDate__date=current_date, then=1), default=0, output_field=IntegerField())),
            leadsSageMitra=Sum(Case(When(Enquirytype__contains='Sage Mitra', then=1), default=0, output_field=IntegerField())),
        )
        for ed in employee_data:
            ed['corpo_visit'] = corpo_visit            
            ed['home_visit'] = home_visit            
            ed['sm_followup'] = sm_followup
            ed['lead_FW'] = lead_FW
            ed['missed_followUp'] = missed_followUp
            data.append(ed)
            ed['target'] = list(target)
    
    
    end_time = time.time()  
    query_time = end_time - start_time  
    
    # print('======================')
    # print("Query Time:", query_time)
    return data


def DPR_Filter(start_date=None, end_date=None, member=None, team=None, request=None):    
    emp = []
    members = None
    if start_date and end_date:
        # print('========', start_date, end_date)
        if member and team:            
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name','id')
            mem = Members.objects.filter(member_name=member, status=1)
            emp = list(mem.values_list('member_name','id'))
            DPR_data = DPR_Date_Range(emp, start_date, end_date, request)

        elif member:            
            mem = Members.objects.filter(member_name=member, status=1)
            members = list(mem.values_list('member_name','id'))
            if mem.exists():              
                # emp = [mem.first().member_name]             
                # print('===========',emp)   
                DPR_data = DPR_Date_Range(emp, start_date, end_date, request)


        elif team:
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name','id')
            emp = list(members)
            DPR_data = DPR_Date_Range(emp, start_date, end_date, request)
            


        else:           
            members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name','id')
            emp = list(members)                           
            DPR_data = DPR_Date_Range(emp, start_date, end_date, request)



    elif team or member:
        if member and team:            
            # print('============', member, team)
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name','id')
            mem = Members.objects.filter(member_name=member, status=1)
            emp = list(mem.values_list('member_name','id'))
            DPR_data = DPR_Without_Date_Range(emp, request)

        elif member:
            mem = Members.objects.filter(member_name=member, status=1)
            members = list(mem.values_list('member_name','id'))

            if mem.exists():               
                # emp = [mem.first().member_name]
                emp = members
                # print('===========',emp)   
                DPR_data = DPR_Without_Date_Range(emp, request)

        elif team:
            members = Members.objects.filter(team_id=team, status=1).order_by('member_name').values_list('member_name','id')
            emp = list(members)
            DPR_data = DPR_Without_Date_Range(emp, request)

        else:           
            members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name','id')
            emp = list(members)
            DPR_data = DPR_Without_Date_Range(emp, request)

    else:       
        members = Members.objects.filter(status=1).order_by('member_name').values_list('member_name','id')
        emp = list(members)
        DPR_data = DPR_Without_Date_Range(emp, request)

    return DPR_data, members  



def DPR(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    member = request.GET.get('member')
    team = request.GET.get('team')
   
   
    DPR_data, members = DPR_Filter(start_date, end_date, member, team, request)
    DPR_data = list(DPR_data)
    members = list(members)
    return JsonResponse({'DPRData': DPR_data, 'members': members}, safe=False)
   
#=====end====DPR===section====== 



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def Delete_Record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            view = data.get('view')

            
            if item_id and view == 'Corp-visits':
                
                CorpFormData.objects.filter(id=item_id).delete()
                return JsonResponse({'message': 'Record deleted successfully', 'view': view})
            elif item_id and view == 'Home-Visit':
                
                HomeVisit.objects.filter(id=item_id).delete()
                return JsonResponse({'message': 'Record deleted successfully', 'view': view})
            elif item_id and view == 'SM-FW':
                
                Sagemitra.objects.filter(id=item_id).delete()
                return JsonResponse({'message': 'Record deleted successfully', 'view': view})
            else:
                return JsonResponse({'message': 'Item ID not provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)