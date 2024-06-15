from django.db import models
import datetime
from django.contrib.auth.models import User


class HighRiseData(models.Model):
    ROW_NUM = models.TextField(null=True, blank=True)
    Column1 = models.TextField(null=True, blank=True)

    Enquiry_id = models.TextField(null=True, blank=True)
    Enquiry_SrNo = models.TextField(null=True,  blank=True)
    # EDate = models.TextField(null=True,  blank=True)
    EDate = models.DateTimeField(null=True,  blank=True)
    Name = models.TextField(max_length=1000, null=True, blank=True)
    Project = models.TextField(max_length=1000, null=True, blank=True)
    Unit = models.TextField(max_length=1000, null=True, blank=True)
    Mobile = models.TextField(null=True, blank=True)
    Phone_Office = models.TextField(max_length=1000, null=True, blank=True)
    Email = models.TextField(max_length=1000, null=True, blank=True)
    Mobile2 = models.TextField(max_length=1000, null=True, blank=True)
    Phone_Offi2 = models.IntegerField(null=True, blank=True)
    Email2 = models.TextField(null=True, blank=True)
    Remark = models.TextField(max_length=1000, null=True, blank=True)
    Result = models.TextField(max_length=1000, null=True, blank=True)
    Final_Remark = models.TextField(max_length=1000, null=True, blank=True)
    Remark1 = models.TextField(max_length=1000, null=True, blank=True)
    Remark2 = models.TextField(max_length=1000, null=True, blank=True)
    Remark3 = models.TextField(max_length=1000, null=True, blank=True)
    HandledByEmployee = models.TextField(max_length=1000, null=True, blank=True)
    # FollowUp_Date = models.TextField(null=True)
    FollowUp_Date = models.DateTimeField(null=True, blank=True)

    Followup_Employee = models.TextField(max_length=1000, null=True, blank=True)
    Approach_Followup_Employee = models.TextField(max_length=1000, null=True, blank=True)
    FollowUp_Mode = models.TextField(max_length=1000, null=True, blank=True)
    # Next_FollowUp1 = models.TextField(max_length=1000, null=True)
    Next_FollowUp1 = models.DateTimeField(null=True, blank=True)

    Next_Followup_Employee = models.TextField(max_length=1000, null=True, blank=True)
    SourceEnquiry = models.TextField(max_length=1000, null=True, blank=True)
    CustomerGrade = models.TextField(max_length=1000, null=True, blank=True)
    Address = models.TextField(max_length=1000, null=True, blank=True)
    Address_Temp = models.TextField(max_length=1000, null=True, blank=True)
    Prospect_Location = models.TextField(max_length=1000, null=True, blank=True)
    City = models.TextField(max_length=1000, null=True, blank=True)
    Pin = models.TextField(max_length=1000, null=True, blank=True)
    NRI = models.TextField(max_length=1000, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    Phone_Resi = models.TextField(max_length=1000, null=True, blank=True)
    Phone_Resi2 = models.TextField(max_length=1000, null=True, blank=True)
    Website = models.TextField(max_length=1000, null=True, blank=True)
    Community = models.TextField(max_length=1000, null=True, blank=True)
    Nation = models.TextField(max_length=1000, null=True, blank=True)
    Family_Members = models.TextField(default=None, null=True, blank=True)
    Staying_Status = models.TextField(max_length=1000, null=True, blank=True)
    Marital_Status = models.TextField(max_length=1000, null=True, blank=True)
    Occupation = models.TextField(max_length=1000, null=True, blank=True)
    Income = models.TextField(max_length=1000, null=True, blank=True)
    Organization = models.TextField(max_length=1000, null=True, blank=True)
    Designation = models.TextField(max_length=1000, null=True, blank=True)
    Office_Address = models.TextField(max_length=1000, null=True, blank=True)
    Fax = models.TextField(max_length=1000, null=True, blank=True)
    Contact_Person = models.TextField(max_length=1000, null=True, blank=True)
    UNITTYPENM = models.TextField(max_length=1000, null=True, blank=True)
    Rooms = models.TextField(max_length=1000, null=True, blank=True)
    Toilets_Required = models.TextField(max_length=1000, null=True, blank=True)
    Area_Requirement = models.TextField(max_length=1000, null=True, blank=True)
    Parking = models.TextField(max_length=1000, null=True, blank=True)
    Location = models.TextField(max_length=1000, null=True, blank=True)
    Location2 = models.TextField(max_length=1000, null=True, blank=True)
    Location3 = models.TextField(max_length=1000, null=True, blank=True)
    Floor = models.TextField(max_length=1000, null=True, blank=True)
    Budget = models.TextField(max_length=1000, null=True, blank=True)
    SourceFunding = models.TextField(max_length=1000, null=True, blank=True)
    Loan_required = models.TextField(max_length=1000, null=True, blank=True)
    Loan_amount = models.TextField(max_length=1000, null=True, blank=True)
    Finance = models.TextField(max_length=1000, null=True, blank=True)
    Expected_Possation = models.TextField(max_length=1000, null=True, blank=True)
    Enquirytype = models.TextField(max_length=1000, null=True, blank=True)
    Broker_Name = models.TextField(max_length=1000, null=True, blank=True)
    Source = models.TextField(max_length=1000, null=True, blank=True)
    Campaign = models.TextField(max_length=1000, null=True, blank=True)
    Primary_Source = models.TextField(max_length=1000, null=True, blank=True)
    Secondary_Source = models.TextField(max_length=1000, null=True, blank=True)
    Source_Of_Information = models.TextField(max_length=1000, null=True, blank=True)
    FirstQuestion = models.TextField(max_length=1000, null=True, blank=True)
    Action_taken = models.TextField(max_length=1000, null=True, blank=True)
    Purchase_Before = models.TextField(max_length=1000, null=True, blank=True)
    Booked_upto = models.TextField(max_length=1000, null=True, blank=True)
    Projnm2 = models.TextField(max_length=1000, null=True, blank=True)
    Unitno2 = models.TextField(max_length=1000, null=True, blank=True)
    Bldg = models.TextField(max_length=1000, null=True, blank=True)
    SalesPoints = models.TextField(max_length=1000, null=True, blank=True)
    CustomerType = models.TextField(max_length=1000, null=True, blank=True)
    EnquiryStage = models.TextField(max_length=1000, null=True, blank=True)
    Enquiry_Status = models.TextField(max_length=1000, null=True, blank=True)
    Enquiry_Conclusion_Date = models.DateTimeField(null=True, blank=True)
    # StageChangeDate = models.TextField(max_length=1000, null=True, blank=True)
    StageChangeDate = models.DateTimeField(null=True, blank=True)

    Last_Approach_Date = models.TextField(max_length=1000, null=True, blank=True)
    Filtered_Date = models.TextField(max_length=1000, null=True, blank=True)
    Booking_Info = models.TextField(max_length=1000, null=True, blank=True)
    
    Account_ID = models.TextField(max_length=1000, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['HandledByEmployee']),
            models.Index(fields=['EDate']),
            models.Index(fields=['Next_FollowUp1']),
            models.Index(fields=['FollowUp_Date']),
            models.Index(fields=['StageChangeDate']),
            models.Index(fields=['EnquiryStage']),
            models.Index(fields=['Enquirytype']),
           
        ]

class Teams(models.Model):
    STATUS_CHOICES = [
        ("0", "0"),
        ("1", "1"),
    ]
    T_name = models.CharField(max_length=100, default=None)  
    #Create_by = models.CharField(max_length=100)  
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="0",  db_comment='0 = active and 1 = not active')
    team_head_id = models.IntegerField(null=True, blank=True)
    #role = models.IntegerField(null=True, default= 0)
    date = models.DateField(default=None)
   # password = models.TextField(null=True)
    def __str__(self):
        return self.T_name
    class Meta:
        indexes = [
            models.Index(fields=['T_name']),           
        ]


class Members(models.Model):
    uname = models.CharField(max_length=100, null=True, blank=True)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=None)
    member_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    pwd = models.TextField(max_length=100, null=True, blank=True)
    status = models.IntegerField(default=1)
    # role1 = models.IntegerField(default=0, db_comment='2 is team leader role')

    def __str__(self):
        return self.uname
    
    class Meta:
        indexes = [
            models.Index(fields=['uname']),           
            models.Index(fields=['member_name']),           
        ]

class CorpFormData(models.Model):
    Pre_Choice = [
        ("done", "done"),
        ("not_done", "not_done"),
    ]
    visit_date = models.DateField(default=datetime.date.today)
    name = models.CharField(max_length=255, blank=True, null=True )
    #uname = models.ForeignKey(Members, on_delete=models.CASCADE,  default=None, blank=True)
    corp_name = models.CharField(max_length=500,null=True, blank=True)
    meet_person = models.IntegerField(null=True, blank=True)
    presentation = models.CharField(max_length=500, choices=Pre_Choice,null=True, blank=True)
    cofel_name = models.CharField(max_length=500, null=True, blank=True)
    nxt_pre_date = models.DateField(null=True, blank=True)
    reason = models.TextField(max_length=500,null=True, blank=True, )
    key_person = models.CharField(null=True, max_length=255)
    images = models.ImageField(upload_to='media/', null=True, blank=True)
    key_person_contact = models.TextField(max_length=255,null=True, blank=True)
    data_collect = models.TextField(max_length=500, null=True, blank=True)
    key_person2 = models.TextField(max_length=255, null=True, blank=True)
    key_person_contact2 = models.TextField(max_length=255, null=True, blank=True)
    corp_type = models.TextField(max_length=255, null=True, blank=True)
    visit_type = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),           
            models.Index(fields=['visit_date']),           
        ]


class Sagemitra(models.Model):
    uname = models.CharField(max_length=255,null=True, blank=True)
    SM_name = models.CharField(max_length=255,null=True, blank=True)
    followUp_date = models.DateField(null=True, blank=True)
    No_leads = models.IntegerField(null=True, blank=True)
    lead_detail = models.TextField(null=True, blank=True, max_length=255)
    sm_contact = models.TextField(max_length=255, null=True, blank=True)
    new_sm_name = models.TextField(max_length=255, null=True, blank=True)
    new_sm_contact = models.TextField(max_length=255, null=True, blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['uname']),           
            models.Index(fields=['followUp_date']),           
        ]




class EventAcc(models.Model):
    Event_name = models.TextField(max_length=500, null=True, blank=True)
    # team_name = models.CharField(max_length=200, null=True, blank=True)
    # owner_name = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    # num_met = models.IntegerField(null=True, blank=True)
    # presentation = models.CharField(max_length=255, null=True, blank=True)
    num_lead = models.IntegerField(null=True, blank=True)
    event_details = models.TextField(null=True, blank=True, max_length=5000)
    name = models.TextField(null=True, blank=True, max_length=255)
    num_attendees = models.TextField(null=True, blank=True, max_length=255)

    
class Target(models.Model):
    name = models.TextField(max_length=255, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    


class Target_Assign(models.Model):
    Target = models.ForeignKey(Target, on_delete=models.CASCADE, default=None)
    Employee = models.ForeignKey(Members,  on_delete=models.CASCADE, default=None)
    target = models.IntegerField(null=True, blank=True)
    revised_target = models.IntegerField(null=True, blank=True)
    month = models.TextField(null=True, blank=True)
    year = models.TextField(null=True, blank=True)
    target_rev_date = models.DateField(null=True, blank=True)
    date = models.DateField(auto_now=True)



class EmpSetTarget(models.Model):
    Target = models.ForeignKey(Target, on_delete=models.CASCADE, default=None, related_name='Target_table')
    Employee = models.ForeignKey(Members,  on_delete=models.CASCADE, default=None, related_name='Member_table')
    target = models.IntegerField(null=True, blank=True)
    month = models.TextField(null=True, blank=True)
    year = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    target_value = models.IntegerField(null=True, blank=True)
    stage = models.IntegerField(null=True, blank=True)




class FollowUpData(models.Model):
    ROW_NUM	 = models.TextField(null=True, blank=True, max_length=500)
    Name = models.TextField(null=True, blank=True, max_length=500)
    Enquiry_SrNo = models.IntegerField(null=True, blank=True)
    Edate = models.DateTimeField(null=True, blank=True)
    GTC = models.TextField(null=True, blank=True, max_length=500)
    SourceEnquiry = models.TextField(null=True, blank=True, max_length=500)
    Source	 = models.TextField(null=True, blank=True, max_length=500)
    Employee_Name = models.TextField(null=True, blank=True, max_length=500)
    EnquiryStage = models.TextField(null=True, blank=True, max_length=500)
    FollowUp_Id	 = models.IntegerField(null=True, blank=True)
    Remark1	 = models.TextField(null=True, blank=True, max_length=500)
    Remark2	 = models.TextField(null=True, blank=True, max_length=500)
    Remark3	 = models.TextField(null=True, blank=True, max_length=500)
    Next_FollowUp1 = models.DateTimeField(null=True, blank=True)
    Status_Desc	 = models.TextField(null=True, blank=True, max_length=500)
    Mobile = models.TextField(null=True, blank=True, max_length=500)
    Phone_Office = models.TextField(null=True, blank=True, max_length=500)
    Phone_Resi	 = models.TextField(null=True, blank=True, max_length=500)
    Mobile2	 = models.TextField(null=True, blank=True, max_length=500)
    Phone_Resi2	 = models.TextField(null=True, blank=True, max_length=500)
    Phone_Offi2	 = models.TextField(null=True, blank=True, max_length=500)
    SOEnquiry_Id2	 = models.TextField(null=True, blank=True, max_length=500)
    FollowUpEmployee_Id	 = models.TextField(null=True, blank=True, max_length=500)
    EnquiryStage_Id = models.TextField(null=True, blank=True, max_length=500)
    SOEnquiry_Id = models.TextField(null=True, blank=True, max_length=500)
    Enquiry_id = models.TextField(null=True, blank=True, max_length=500)
    FollowUp_Date = models.DateTimeField(null=True, blank=True)
    Reffered_project1 = models.TextField(null=True, blank=True, max_length=500)
    Reffered_project2 = models.TextField(null=True, blank=True, max_length=500)
    CustomerGrade = models.TextField(null=True, blank=True, max_length=500)
    Priority = models.TextField(null=True, blank=True, max_length=500)
    Broker_Name	 = models.TextField(null=True, blank=True, max_length=500)
    Broker_PH = models.TextField(null=True, blank=True, max_length=500)
    Prospect_Location = models.TextField(null=True, blank=True, max_length=500)
    city = models.TextField(null=True, blank=True, max_length=500)
    Occupation = models.TextField(null=True, blank=True, max_length=500)
    SourceFunding = models.TextField(null=True, blank=True, max_length=500)
    Employee_id	 = models.TextField(null=True, blank=True, max_length=500)
    Projnm1 = models.TextField(null=True, blank=True, max_length=500)
    Projnm2 = models.TextField(null=True, blank=True, max_length=500)
    Email = models.TextField(null=True, blank=True, max_length=500)
    Email2 = models.TextField(null=True, blank=True, max_length=500)
    Remark = models.TextField(null=True, blank=True, max_length=500)
    Final_Remark = models.TextField(null=True, blank=True, max_length=500)
    UNITTYPENM = models.TextField(null=True, blank=True, max_length=500)
    Budget = models.TextField(null=True, blank=True, max_length=500)
    CustomerType = models.TextField(null=True, blank=True, max_length=500)
    Result = models.TextField(null=True, blank=True, max_length=500)
    Next_Followup_Employee = models.TextField(null=True, blank=True, max_length=500)
    FollowUp_Mode = models.TextField(null=True, blank=True, max_length=500)
    FollowUp_ModeF_Age = models.TextField(null=True, blank=True, max_length=500)
    F_Due_Age = models.TextField(null=True, blank=True, max_length=500)
    Resource_URL = models.TextField(null=True, blank=True, max_length=500)
    OverdueDays = models.TextField(null=True, blank=True, max_length=500)
    FollowUp_Count = models.TextField(null=True, blank=True, max_length=500)
    Account_ID = models.TextField(null=True, blank=True, max_length=500)
    class Meta:
        indexes = [
            models.Index(fields=['Employee_Name']),
            models.Index(fields=['Next_FollowUp1']),
            models.Index(fields=['FollowUp_Date']),
           
        ]

class IpData(models.Model):
    name = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='Ip')
    date = models.DateField(null=True, blank=True)
    patient_name = models.TextField(max_length=255, null=True, blank=True)
    key_person = models.TextField(max_length=255, null=True, blank=True)



class AdmissionData(models.Model):

    name = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='Admission')
    date = models.DateField(null=True, blank=True)
    f_name = models.TextField(max_length=255, null=True, blank=True) 
    s_name = models.TextField(max_length=255, null=True, blank=True) 
    vertical = models.TextField(max_length=255, null=True, blank=True) 
    branch_class = models.TextField(max_length=255, null=True, blank=True)


class SiteVisit(models.Model):
    name = models.TextField(max_length=255, null=True, blank=True)
    C_name = models.TextField(max_length=255, null=True, blank=True)
    C_ph = models.TextField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    detail = models.TextField(max_length=255, null=True, blank=True)
    Site_name = models.TextField(max_length=255, null=True, blank=True)
    visit_stage = models.TextField(max_length=255, null=True, blank=True)
    images = models.ImageField(upload_to='media/HomeVisit', null=True, blank=True)
    co_fellow = models.CharField(max_length=5000, null=True, blank=True)


class HomeVisit(models.Model):
    name = models.TextField(max_length=255, null=True, blank=True)
    C_name = models.TextField(max_length=255, null=True, blank=True)
    C_ph = models.TextField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    detail = models.TextField(max_length=255, null=True, blank=True)
    Site_name = models.TextField(max_length=255, null=True, blank=True)
    # visit_stage = models.TextField(max_length=255, null=True, blank=True)
    images = models.ImageField(upload_to='media/HomeVisit', null=True, blank=True)
    co_fellow = models.CharField(max_length=5000, null=True, blank=True)
    visit_type = models.CharField(max_length=250, null=True, blank=True)


class CorporatesList(models.Model):
    corpo_name = models.TextField(null=True, blank=True, max_length=255)
    status = models.TextField(default=1)

class CorporateType(models.Model):
    corpo_type = models.TextField(null=True, blank=True, max_length=255)

class EventType(models.Model):
    event_type = models.TextField(null=True, blank=True, max_length=255) 
    status = models.TextField(default=1)

class SageMitraList(models.Model):
    sm_name = models.TextField(null=True, blank=True, max_length=255)
    sm_ph = models.TextField(null=True, blank=True, max_length=255)
    status = models.TextField(default=1)