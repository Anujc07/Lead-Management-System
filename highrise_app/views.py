from django.shortcuts import render, HttpResponse, redirect
from .models import *
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import bcrypt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.text import slugify
import os
import calendar
from django.contrib import messages
from django.db import IntegrityError  
from django.db.models import Count, Case, When, IntegerField, Sum, F, Q, Exists, OuterRef, Subquery, Value, CharField, Func
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from Highrise.settings import EMAIL_HOST_USER
import logging

def handler404(request, exception):
    return render(request, 'app/404.html', status=404)



def EmployeeLogin(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password') 
        current_date = datetime.now().date().strftime("%Y-%m-%d")
        c_date = datetime.now().date()
        # print('===', c_date)
        first_date = datetime.now().date().replace(day=1).strftime("%Y-%m-%d")
        month = datetime.now().strftime("%B")
        year = datetime.now().year
        if username and password:      
            user = authenticate(username=username, password=password)
            if user is not None:               
                login(request, user)
                
                request.session['name'] = username
                first_name = user.first_name
                username = request.session.get('name')
                request.session['first_name'] = first_name
                team_id = list(Members.objects.filter(member_name=first_name).values_list('team_id', flat=True))
                request.session['team_id'] = team_id
                total_corp_visit = CorpFormData.objects.filter(name=first_name).count()
                userData = Members.objects.filter(member_name = first_name).values('id').first()
                user_id = userData['id']
                request.session['user_id'] = user_id
                target_booking = Target_Assign.objects.filter(Q(Employee_id = user_id) & Q(Target_id = 1) & Q(month=month)).all().values()              
                # target_corp_visit = Target_Assign.objects.filter(Q(Employee_id = user_id) & Q(Target_id = 2)).all().values()
                count_data = HighRiseData.objects.filter(HandledByEmployee=first_name)
                # total_corp_visit = CorpFormData.objects.filter(name=first_name, visit_date__range=(first_date, current_date) ).count()
                
            

                corpo_solo = CorpFormData.objects.filter(Q(name=first_name) & Q(visit_type='solo') & Q(visit_date__range = (first_date, current_date))).count()
                corporate = CorpFormData.objects.filter(Q(name=first_name) & Q(visit_type='team') & Q(visit_date__range = (first_date, current_date))).values_list(
                    'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
                )
                
                total_corporate_count_cofellow  = 0


                # for item in corporate:
                #     names = item[0].split(',')         
                #     for name in names:
                #         corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                #             Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
                #             Q(key_person_contact=item[4]) & Q(key_person=item[5])
                #         ).count()                
                #         total_corporate_count_cofellow += corporate_count_cofellow
                # total_corp_visit = corpo_solo + total_corporate_count_cofellow
                for item in corporate:
                    names = item[0].split(',')         
                    for name in names:
                        corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                            Q(visit_date=item[1])
                        ).count()                
                        total_corporate_count_cofellow += corporate_count_cofellow
                total_corp_visit = corpo_solo + total_corporate_count_cofellow



                total_followUP = FollowUpData.objects.filter(Employee_Name=first_name, FollowUp_Date__range=(first_date, current_date)).count()
                total_bookings = HighRiseData.objects.filter(Q(HandledByEmployee__icontains = first_name) & Q(Enquiry_Conclusion_Date__range=(first_date, current_date)) & Q(Enquiry_Status='Booked')).count()
             
                total_SM_FW = Sagemitra.objects.filter(uname = first_name, followUp_date__range=(first_date, current_date)).count()
                
                target_values  = EmpSetTarget.objects.filter(Q(Employee_id = user_id) & Q(month = month) & Q(year = year)).all().values()
               
                total_events = EventAcc.objects.filter(name=first_name, start_date__range=(first_date, current_date)).count()
                
              
                pand_followUP = count_data.filter(Next_FollowUp1__startswith=current_date).count()
                # bookings = Target.objects.values('name')
                # target = Target.objects.values('name').values_list()
                # total_home_visit = HighRiseData.objects.filter(Q(HandledByEmployee__icontains = first_name) & Q(StageChangeDate__range=(first_date, current_date)) & Q(EnquiryStage='Home Visit - Done')).count()
                solo_home_visit = HomeVisit.objects.filter(Q(name = first_name) & Q(date__range=(first_date, current_date))).count()  
                team_home_visit = HomeVisit.objects.filter(Q(co_fellow = first_name) & Q(date__range=(first_date, current_date)) & Q(visit_type='team')).count()
                total_home_visit = solo_home_visit + team_home_visit
                print('=================', total_home_visit)


                # total_site_visit = HighRiseData.objects.filter(Q(HandledByEmployee__icontains = first_name) & Q(StageChangeDate__range=(first_date, current_date)) & Q(EnquiryStage='Site Visit - Done')).count()
                total_site_visit = FollowUpData.objects.filter(Employee_Name=first_name, FollowUp_Date__range=(first_date, current_date),EnquiryStage='Site Visit - Done').count()      
                # total_site_visit = SiteVisit.objects.filter(Q(name = first_name) & Q(date__range=(first_date, current_date))).count()            
                ip = IpData.objects.filter(name_id=user_id, date__range=(first_date, current_date)).count()
                admission = AdmissionData.objects.filter(name_id=user_id, date__range=(first_date, current_date)).count()
                #target = T_Assign.objects.filter(T_id)
                #print("-=====================", total_bookings)
                t_value = target_booking.values_list('target',flat=True).first()
                if t_value is not None:
                    perc = (total_bookings / t_value) * 100
                    percentage = int(perc)
                else:
                    percentage = 0
                # print("======================", percentage)
                return render(request, 'app/dashboard.html',{'total_home_visit':total_home_visit,'total_site_visit':total_site_visit,'total_events':total_events, 'admission':admission, 'ip':ip,'pand_followUP':pand_followUP,
                                                             'total_SM_FW':total_SM_FW, 'target_values': target_values,  'total_corp_visit':total_corp_visit,'total_followUP':total_followUP,
                                                                 'total_bookings':total_bookings, 'percentage':percentage})
            else:                                
                error_message = 'Invalid email or password.'
                return render(request, 'app/Login.html', {'error_message': error_message})
        else:            
            error_message = 'Please provide both email and password.'
            return render(request, 'app/Login.html', {'error_message': error_message})
    else:
        return render(request, 'app/Login.html')


from django.db import connection

@login_required()
def EmployeeDashboard(request):
    c_date = datetime.now().date()
    f_date = datetime.now().date().replace(day=1)
    # print('===', c_date)
    first_date = datetime.now().date().replace(day=1).strftime("%Y-%m-%d")
    month = datetime.now().strftime("%B")
    year = datetime.now().year
    # print('=========', month)
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    first_name = request.session.get('first_name')
    
    userData = Members.objects.filter(member_name = first_name).values('id').first()
    user_id = userData['id']
    # t_booking = Target_Assign.objects.filter(Q(Employee_id = user_id) & Q(Target_id = 1)).all().values()
    # t_visit = Target_Assign.objects.filter(Q(Employee_id = user_id) & Q(Target_id = 2)).all().values()
    # home = HomeVisit.objects.filter(Q(name=first_name) & Q(co_fellow__contains=first_name)).values()
    # print(home)
    # home_solo = HomeVisit.objects.filter(Q(name=first_name) & Q(visit_type = 'solo')).count()
    # home = HomeVisit.objects.filter(Q(name=first_name) & Q(visit_type = 'team')).values_list('co_fellow', flat=True)
    # fellow_data = list(home)
    # co_fellow_data = list(set(fellow_data))
    # total_home_visit = 0
     
    # # print('============= name co_fellow:', co_fellow_data)
    # for co_fellow_str in co_fellow_data:
    #     # print(co_fellow_str)
    #     co_fellow_list = co_fellow_str.split(',')  
    #     for co_fellow_name in co_fellow_list:
    #         # print('============= name of co-fellow:', co_fellow_name)
    #         home_count = HomeVisit.objects.filter(Q(name=co_fellow_name) & Q(co_fellow__contains=first_name) | Q(co_fellow__startswith=first_name + ',') |
    #                 Q(co_fellow__endswith=',' + first_name) | Q(co_fellow__icontains=',' + first_name + ',')).count()
            
    #         total_home_visit += home_count
        
    # print(total_home_count+home_solo)


    corpo_solo = CorpFormData.objects.filter(Q(name=first_name) & Q(visit_type='solo') & Q(visit_date__range = (first_date, current_date))).count()
    corporate = CorpFormData.objects.filter(Q(name=first_name) & Q(visit_type='team') & Q(visit_date__range = (first_date, current_date))).values_list(
        'cofel_name', 'visit_date', 'visit_type', 'corp_name', 'key_person_contact', 'key_person'
    )


    
    total_corporate_count_cofellow  = 0
    for item in corporate:
        names = item[0].split(',')         
        for name in names:
            print(name)
            corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
                Q(visit_date=item[1])
            ).count()     
            print(corporate_count_cofellow)           
            total_corporate_count_cofellow += corporate_count_cofellow
    total_corp_visit = corpo_solo + total_corporate_count_cofellow
    # print(corpo_solo)
    # print(total_corporate_count_cofellow)
    # for item in corporate:
    #     names = item[0].split(',')         
    #     for name in names:
    #         corporate_count_cofellow = CorpFormData.objects.filter(Q(name=name.strip()) &
    #             Q(visit_date=item[1]) & Q(visit_type=item[2]) & Q(corp_name=item[3]) &
    #             Q(key_person_contact=item[4]) & Q(key_person=item[5])
    #         ).count()                
    #         total_corporate_count_cofellow += corporate_count_cofellow
    # total_corp_visit = corpo_solo + total_corporate_count_cofellow 
            
    # print(total_coprate_visit+corpo_solo)
    solo_home_visit = HomeVisit.objects.filter(Q(name = first_name) & Q(date__range=(first_date, current_date))).count()  
    # team_home_visit = HomeVisit.objects.filter(Q(date__range=(first_date, current_date)) & Q(visit_type='team')).count()
    # values_home_visit = HomeVisit.objects.filter(Q(date__range=(first_date, current_date)) & Q(visit_type='team')).values('co_fellow')
    home_visits = HomeVisit.objects.filter(
        Q(date__range=(first_date, current_date)) & Q(visit_type='team')
    )
    team_home_visit_count = 0
    for visit in home_visits:
        co_fellows = [name.strip() for name in visit.co_fellow.split(',')]
        
        if first_name in co_fellows:
            team_home_visit_count += 1

    print(team_home_visit_count)
    total_home_visit = solo_home_visit + team_home_visit_count
    print('=================', total_home_visit)
    count_data = HighRiseData.objects.filter(HandledByEmployee=first_name)
    # total_corp_visit = CorpFormData.objects.filter(name=first_name, visit_date__range=(first_date, current_date) ).count()
    # total_followUP = count_data.filter(Q(FollowUp_Date__range=(first_date,current_date)) & ~Q(FollowUp_Date=F('Next_FollowUp1')) & ~Q(FollowUp_Date__time=F('Next_FollowUp1__time'))).count() 
    total_followUP = FollowUpData.objects.filter(Employee_Name=first_name, FollowUp_Date__range=(first_date, current_date)).count()
    total_bookings = HighRiseData.objects.filter(Q(HandledByEmployee__icontains = first_name) & Q(Enquiry_Conclusion_Date__range=(first_date, current_date)) & Q(Enquiry_Status='Booked')).count()
    # total_home_visit = HighRiseData.objects.filter(Q(HandledByEmployee__icontains = first_name) & Q(StageChangeDate__range=(first_date, current_date)) & Q(EnquiryStage='Home Visit - Done')).count()
    # total_home_visit = HomeVisit.objects.filter(Q(name = first_name) & Q(date__range=(first_date, current_date))).count()     
    # total_home_visit = HomeVisit.objects.filter(Q(name = first_name) & Q(date__range=(first_date, current_date))).count()     
    # total_site_visit = HighRiseData.objects.filter(Q(HandledByEmployee__icontains = first_name) & Q(StageChangeDate__range=(first_date, current_date)) & Q(EnquiryStage='Site Visit - Done')).count()
    total_site_visit =  FollowUpData.objects.filter(Employee_Name=first_name, FollowUp_Date__range=(first_date, current_date),EnquiryStage='Site Visit - Done').count()      
    total_SM_FW = Sagemitra.objects.filter(uname = first_name, followUp_date__range=(first_date, current_date)).count()
    # print('==================',first_name, first_date, current_date)
    # sm_mitra = Sagemitra.objects.all().filter(uname=first_name).values('id')
    # target_values  = Target_Assign.objects.filter(Q(Employee_id = user_id)).all().values()
    # target_values  = EmpSetTarget.objects.filter(Q(Employee_id = user_id) & Q(date__range=(first_date, current_date))).all().values()
    target_values  = EmpSetTarget.objects.filter(Q(Employee_id = user_id) & Q(month = month) & Q(year = year)).all().values()
    # total_followUP = count_data.filter(Next_FollowUp1__startswith=currentdate_text).count()
    pand_followUP = count_data.filter(Next_FollowUp1__startswith=current_date).count()
    # total_SM_FW_values = Sagemitra.objects.all()
    # print(sm_mitra.queries)
    # raw_query = str(sm_mitra.query)

    
    # print('====RAW SQL QUERY====')
    # print(raw_query)
    # print('======================total_SM_FNM==================', sm_mitra)
    # target = Target.objects.values('name')
    # target_name = Target.objects.values('name')
    #target = T_Assign.objects.filter(T_id)
    #print("-=====================", total_bookings)
    total_events = EventAcc.objects.filter(name=first_name, start_date__range=(first_date, current_date)).count()
    t_value = Target_Assign.objects.filter(Q(Employee_id = user_id) & Q(Target_id = 1)).values_list('target', flat=True).first()
    ip = IpData.objects.filter(name_id=user_id, date__range=(first_date, current_date)).count()
    admission = AdmissionData.objects.filter(name_id=user_id, date__range=(first_date, current_date)).count()
    # print("======================",t_value)
    if t_value is not None:
        perc = (total_bookings / t_value) * 100
        percentage = int(perc)
    else:
        percentage = 0
    #print("======================", percentage)
    # print('================count================', total_SM_FW, first_name)
    return render(request, 'app/dashboard.html',{'total_home_visit':total_home_visit,'total_site_visit':total_site_visit, 'total_events':total_events,
                                                 'admission':admission,'ip':ip, 'pand_followUP':pand_followUP, 'total_SM_FW':total_SM_FW, 'target_values':target_values, 
                                                 'total_followUP':total_followUP,  'total_bookings':total_bookings, 'percentage':percentage,
                                                   'total_corp_visit':total_corp_visit})


@login_required()
def EmployeeCorpoVisit(request):
    currentTime  = datetime.now().strftime('%H-%M-%S')
     
    # print('===', currentTime)
    corporate_list = CorporatesList.objects.values_list('corpo_name', flat=True).order_by('corpo_name')
    corporate_type = CorporateType.objects.values_list('corpo_type', flat=True).order_by('corpo_type')
    member = Members.objects.filter(status=1).values_list('member_name', flat=True).order_by('member_name')
    if request.method == 'POST':
        try:
            name = request.session['first_name']
            corp_type = request.POST.get('corp_type')
            corp_name = request.POST.get('corp_name')
            meet_person = request.POST.get('meet_person')
            presentation = request.POST.get('presentation')
            date_str = request.POST.get('date')
            nxt_pre_date = request.POST.get('nxt_date')
            reason = request.POST.get('reason')
            key_person = request.POST.get('key_person')
            key_person_contact = request.POST.get('key_person_contact')
            key_person2 = request.POST.get('key_person2')
            key_person_contact2 = request.POST.get('key_person_contact2')
            data_collect = request.POST.get('data_collect')
            visit_type = request.POST.get('visit_type')
       
            image = request.FILES.get('image')
            if not image:
                raise ValidationError('No image file provided.')
            image_name ,image_ext = os.path.splitext(image.name)
            
            # new_filename = f"{slugify(name)}_{date_str}_{slugify(corp_name)}_{slugify(currentTime)}{image_ext}"
            new_filename = f"{slugify(name)}_{date_str}_{slugify(corp_name)}_{slugify(currentTime)}{image_ext}"
            image.name = new_filename 
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):           
                error_message = 'Invalid date format. Please enter the date in YYYY-MM-DD format.'
                return render(request, 'app/corporate-visit.html', {'error_message': error_message})

            if nxt_pre_date:
                try:
                    nxt_date = datetime.strptime(nxt_pre_date, '%Y-%m-%d').date()
                except (ValueError, TypeError):           
                    error_message = 'Invalid next date format. Please enter the date in YYYY-MM-DD format.'
                    return render(request, 'app/corporate-visit.html', {'error_message': error_message})
            else:
                nxt_date = None
            
            # co_names = [request.POST[key] for key in request.POST if key.startswith('co_name_')]
            # co_names_str = ','.join(co_names)
            co_names = [request.POST[key] for key in request.POST if key.startswith('co_name_') and request.POST[key]]
            co_names_str = ','.join(co_names) if co_names else None
           
            user = CorpFormData.objects.create(
                key_person2=key_person2,
                key_person_contact2=key_person_contact2, 
                name=name,                
                corp_name=corp_name,
                corp_type=corp_type,
                meet_person=meet_person,
                presentation=presentation,
                cofel_name=co_names_str,
                visit_date=date,
                reason=reason,
                nxt_pre_date=nxt_date,
                key_person=key_person,
                images=image,  
                data_collect=data_collect,
                key_person_contact=key_person_contact,
                visit_type=visit_type,
            )
            user.save()
            success_message = 'Your Entry Saved'
            return redirect('/app/dashboard/', {'success_message': success_message}) 
        except (ValidationError, MultiValueDictKeyError) as e:
            error_message = str(e)
            return render(request, 'app/corporate-visit.html', {'error_message': error_message})
    else:
        return render(request, 'app/corporate-visit.html', {'corporate_list':corporate_list, 'corporate_type':corporate_type, 'member':member})


def Logout(request):
    logout(request)
    return redirect('/app/login/') 


from django.utils import timezone

@login_required()
def SageMitra(request):
    sm_list = SageMitraList.objects.values_list('sm_name', 'sm_ph').order_by('sm_name')
        
 
    if request.method == 'POST':
        uname = request.session.get('first_name')
        sm_name = request.POST.get('sm_name')
        followup_date = request.POST.get('followup_date')
        no_leads = request.POST.get('no_leads')
        lead_detail = request.POST.get('lead_Detail')
        sm_contact = request.POST.get('sm_contact')
        new_sm_name = request.POST.get('new_sm_name')
        new_sm_contact = request.POST.get('new_sm_contact')
        # print('===new_sm_contact==', new_sm_contact)
        # sub_date = datetime.now()
        sub_date = timezone.now()

        # print('==================================',sub_date)
        if new_sm_name is not '':
            # print('=====================')
            new_sm = SageMitraList.objects.create(
                sm_name = new_sm_name,
                sm_ph=new_sm_contact
            )
            new_sm.save()
            # print('==================================',date)
            try:
                sage_mitra = Sagemitra.objects.create(
                    new_sm_contact=new_sm_contact,
                    uname=uname,
                    SM_name=new_sm_name,
                    followUp_date=followup_date,
                    No_leads=no_leads,
                    lead_detail=lead_detail,
                    new_sm_name=new_sm_name,
                    submission_date = sub_date,
                )
                sage_mitra.save()
                success_message = 'SageMitra Detail Added'
                return redirect('/app/dashboard/')
            except ValueError as e:
                error_message = 'Invalid input'
                return render(request, 'app/sage-mitra-followup.html', {'error_message': error_message})
        else:
            try:
                # print('==================================',sub_date)
                # print('=========', sm_contact)
                sage_mitra = Sagemitra.objects.create(
                    sm_contact=sm_contact,
                    uname=uname,
                    SM_name=sm_name,
                    followUp_date=followup_date,
                    No_leads=no_leads,
                    lead_detail=lead_detail,
                    new_sm_name=new_sm_name,
                    submission_date = sub_date,
                )
                sage_mitra.save()
                success_message = 'SageMitra Detail Added'
                return redirect('/app/dashboard/')
            except ValueError as e:
                error_message = 'Invalid input'
                return render(request, 'app/sage-mitra-followup.html', {'error_message': error_message})
    else:
        return render(request, 'app/sage-mitra-followup.html',{'sm_list':sm_list})



    
def AccEvent(request):
    event_type = EventType.objects.values_list('event_type', flat=True).order_by('event_type')
    if request.method == 'POST':
        EventName = request.POST.get('Event_name')
        # owner_name = request.POST.get('owner_name')
        name = request.session.get('first_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        Eventtype = request.POST.get('Event_type')
        # NumMeet = request.POST.get('num_met')
        # presentation = request.POST.get('presentation')
        NumLeads = request.POST.get('num_leads')
        event_details = request.POST.get('event_details')
        num_attendees = request.POST.get('num_attendees')

        try:
            eventuser = EventAcc.objects.create(
                Event_name = EventName,
                name = name,
                start_date = start_date,
                end_date = end_date,
                type = Eventtype,
                # num_met = NumMeet,
                num_attendees = num_attendees,
                # presentation = presentation,
                num_lead = NumLeads,
                event_details=event_details,
            )
            eventuser.save()
            return redirect('/app/dashboard/')
        except ValueError as e:
            error_message = 'Invalid input'
            return render(request, 'app/EventForm.html',{'error_message': error_message})    
       
    else:
        return render(request, 'app/EventForm.html',{'event_type':event_type})
    

def UserProgress(request):
    currentdate = datetime.now().date().strftime('%Y-%m-%d')
    
    username = request.session.get('name')
    count_data = HighRiseData.objects.filter(HandledByEmployee=username)
    
    # Convert currentdate to a text field
    currentdate_text = datetime.now().date().strftime('%d %b %Y')
    # print("==================", currentdate_text, type(currentdate_text))
    # Use __date lookup to compare only the date part
    total_followUP = count_data.filter(Next_FollowUp1__startswith=currentdate_text).count()
    # print("=============", total_followUP)

    return render(request, 'app/UserProgress.html', {'total_followUP': total_followUP})






def Set_Target(request):
    months = [calendar.month_name[i] for i in range(1, 13)]
    current_month = datetime.now().strftime("%B")
    user_id = request.session.get('user_id')
    data = EmpSetTarget.objects.filter(Employee_id=user_id, month=current_month).values('Target_id', 'target')
    # print('===========', data)
    if request.method == 'POST':
        employee_name = request.session.get('first_name')
        year = request.POST.get('year')
        month = request.POST.get('month')
        booking = request.POST.get('booking')
        corporate = request.POST.get('corporate')
        followup = request.POST.get('followup')
        homevisit = request.POST.get('homevisit')
        sm_mitra = request.POST.get('sm_mitra')
        sitevisit = request.POST.get('sitevisit')
        admission = request.POST.get('admission')
        ip = request.POST.get('ip')
        employee = Members.objects.get(member_name=employee_name)
        
        existing_entry = EmpSetTarget.objects.filter(Employee=employee, month=month).first()
        
        if existing_entry and existing_entry.stage == 1:
            target_ids = [1, 2, 3, 4, 5, 6, 7, 8] 
            try:
                for target_id in target_ids:
                    target_instance = Target.objects.get(id=target_id)
                    target_value = None
                    if target_id == 1:
                        target_value = booking
                    elif target_id == 2:
                        target_value = corporate
                    elif target_id == 3:
                        target_value = followup
                    elif target_id == 4:
                        target_value = homevisit
                    elif target_id == 5:
                        target_value = sm_mitra
                    elif target_id == 6:
                        target_value = sitevisit
                    elif target_id == 7:
                        target_value = admission
                    elif target_id == 8:
                        target_value = ip

                    if target_value is not None and target_value != '':
                        set_target = EmpSetTarget.objects.filter(
                            Employee=employee,
                            year=year,
                            month=month,
                            Target=target_instance
                        ).first()
                        if set_target:
                            set_target.target = target_value
                            set_target.stage = 2
                            set_target.save()
                        else:
                            messages.error(request, f"Entry for target {target_id} not found.")

            except IntegrityError as e:
                print(e) 
                messages.error(request, "Failed to update targets.")
                return redirect('/app/dashboard/')
        elif existing_entry and existing_entry.stage == 2:
            message = 'You Already Updated the target'
            return render(request, 'app/Set-Target.html', {'months': months, 'message': message})
        else:
            target_ids = Target.objects.all().values_list('id', flat=True)
            for target_id in target_ids:
                target_instance = Target.objects.get(id=target_id)
                if target_id == 1:
                    target_value = booking
                elif target_id == 2:
                    target_value = corporate
                elif target_id == 3:
                    target_value = followup
                elif target_id == 4:
                    target_value = homevisit
                elif target_id == 5:
                    target_value = sm_mitra
                elif target_id == 6:
                    target_value = sitevisit
                elif target_id == 7:
                    target_value = admission
                elif target_id == 8:
                    target_value = ip

                try:
                    set_target, created = EmpSetTarget.objects.get_or_create(
                        Employee=employee,
                        year=year,
                        month=month,
                        Target=target_instance,  
                        defaults={'target': target_value, 'stage': 1}
                    )
                    if not created:
                        set_target.target = target_value
                        set_target.save()
                except IntegrityError as e:
                    # print(e) 
                    messages.error(request, "Failed to set targets.")
                    return redirect('/app/dashboard/')
        return redirect('/app/dashboard/')
        
    else:      
        
        return render(request, 'app/Set-Target.html', {'months': months, 'data': data, 'current_month':current_month})




def IP(request):
    if request.method == 'POST':
        name = request.session.get('first_name')
        date = request.POST.get('date')
        p_name = request.POST.get('p_name')
        key_person = request.POST.get('key_person')
        employee = Members.objects.get(member_name=name)
        try:
            user = IpData.objects.create(
                name = employee,
                date = date,
                patient_name = p_name,
                key_person = key_person,
            )
            user.save()
            return redirect('/app/dashboard/')
        except IntegrityError as e:
            messages.error(request, "Failed to set targets.")
    else:
        return render(request, 'app/IP.html')
    

def Admission(request):
    if request.method == 'POST':
        name = request.session.get('first_name')
        date = request.POST.get('date')
        f_name = request.POST.get('f_name')
        s_name = request.POST.get('s_name')
        vertical = request.POST.get('vertical')
        branch_class = request.POST.get('branch_class')

        employee = Members.objects.get(member_name=name)
        try:
            user = AdmissionData.objects.create(
                name = employee,
                date = date,
                f_name = f_name,
                s_name = s_name,
                vertical = vertical,
                branch_class = branch_class,
            )
            user.save()
            return redirect('/app/dashboard/')
        except IntegrityError as e:
            messages.error(request, "Failed to set targets.")
    else:
      return render(request, 'app/Admission.html')        
    


def Home_visit(request):
    currentTime  = datetime.now().strftime('%H-%M-%S')
    member = Members.objects.filter(status=1).values_list('member_name', flat=True).order_by('member_name')
    if request.method == 'POST':
        name = request.session.get('first_name')
        customer_name = request.POST.get('customer_name')
        customer_contact = request.POST.get('customer_contact')
        date = request.POST.get('date')
        visit_details = request.POST.get('visit_details')
        site_visit_name = request.POST.get('site_visit_name')       
        image = request.FILES.get('image')
        visit_type = request.POST.get('visit_type')       
        # print('=========', image)
        if not image:
            raise ValidationError('No image file provided.')
        image_name ,image_ext = os.path.splitext(image.name)
        new_filename = f"{slugify(name)}_{date}_{slugify(site_visit_name)}_{slugify(currentTime)}{image_ext}"
        image.name = new_filename 
        co_names = [request.POST[key] for key in request.POST if key.startswith('co_name_') and request.POST[key]]
        co_names_str = ','.join(co_names) if co_names else None
        try:
            user = HomeVisit.objects.create(
                name = name,
                C_name = customer_name,
                C_ph = customer_contact,
                date = date,
                detail = visit_details,
                Site_name = site_visit_name,
                images = image,  
                co_fellow = co_names_str,
                visit_type = visit_type,
                
            )
            user.save()
            return redirect('/app/dashboard/')
        except IntegrityError as e:
            messages.error(request, "Failed to set targets.")
    else:
      return render(request, 'app/Site-visit.html', {'member': member})
    



logger = logging.getLogger(__name__)

def Forget_password(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        email = request.POST.get('email')

        # Validate email and username
        if not uname or not email:
            message = 'Please provide both username and email.'
            return render(request, 'app/Forget_password.html', {'message': message})

        # Check if the username and email combination exists
        try:
            user = User.objects.get(username=uname, email=email)
        except User.DoesNotExist:
            message = 'No user found with the provided username and email.'
            return render(request, 'app/Forget_password.html', {'message': message})

        otp = get_random_string(length=6, allowed_chars='1234567890')
        
        try:
            send_mail(
                'OTP Verification For Acc Tracker',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            request.session['otp'] = otp
            request.session['uname'] = uname
            request.session['email'] = email
            request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=5)).timestamp()
            return render(request, 'app/OTP.html', {'email': email})
        except Exception as e:
            logger.error(f'Error sending OTP email: {e}')
            message = 'Error sending OTP. Please try again later.'
            # print(message)
            return render(request, 'app/Forget_password.html', {'message': message})
    else:
        return render(request, 'app/Forget_password.html')
    




def OTP_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        session_otp = request.session.get('otp')
        otp_expiry = request.session.get('otp_expiry')
        email = request.session.get('email')  
        uname = request.session.get('uname')  

        if not otp or not session_otp or not otp_expiry or not email:
            message = 'Invalid session or OTP.'
            return redirect('Forget_password')

        if datetime.now().timestamp() > otp_expiry:
            message = 'OTP has expired. Please request a new one.'
            return render(request, 'app/OTP.html', {'message': message})

        if otp == session_otp:
            if password != confirm_password:
                message = 'Passwords do not match.'
                return render(request, 'app/OTP.html', {'message': message})

            try:
                user = User.objects.get(email=email, username=uname)
                user.password = make_password(password)
                # print(make_password(password))
                user.save()
                # print('===========')
               
                del request.session['otp']
                del request.session['otp_expiry']
                del request.session['email'] 

                messages.success(request, 'Password updated successfully. Please log in.')
                return redirect('EmployeeLogin')
            except User.DoesNotExist:
                message = 'User not found.'
                return render(request, 'app/OTP.html', {'message': message})
        else:
            message = 'Invalid OTP. Please try again.'
            return render(request, 'app/OTP.html', {'message': message})
    else:
        return redirect('EmployeeLogin')
    



