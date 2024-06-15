# # def IP(request):
# #     if request.method == 'POST':
# #         name = request.session.get('first_name')
# #         date = request.POST.get('date')
# #         p_name = request.POST.get('p_name')
# #         key_person = request.POST.get('key_person')
# #         employee = Members.objects.get(member_name=name)
# #         try:
# #             user = IpData.objects.create(
# #                 name = employee,
# #                 date = date,
# #                 patient_name = p_name,
# #                 key_person = key_person,
# #             )
# #             user.save()
# #             return redirect('/app/dashboard/')
# #         except IntegrityError as e:
# #             messages.error(request, "Failed to set targets.")
# #     else:
# #         return render(request, 'app/IP.html')
    


# class IP:
#     def __init__(self, employee, date, p_name, key_person):
#         self.employee = employee 
#         self.date = date
#         self.p_name = p_name
#         self.key_person = key_person
    
#     def Main(self, request):
#         if request.method == 'POST':            
#             employee = Members.objects.get(member_name=name)
#             try:
#                 user = IpData.objects.create(
#                     name = self.employee,
#                     date = self.date,
#                     patient_name = self.p_name,
#                     key_person = self.key_person,
#                 )
#                 user.save()
#                 return redirect('/app/dashboard/')
#             except IntegrityError as e:
#                 messages.error(request, "Failed to set targets.")
#         else:
#             return render(request, 'app/IP.html')
        
# if __name__ == '__main__':
#     name = request.session.get('first_name')
#     date = request.POST.get('date')
#     p_name = request.POST.get('p_name')
#     key_person = request.POST.get('key_person')
#     obj =IP(name, date, p_name, key_person)

