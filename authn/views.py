from email import message
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from authn.models import Profile, userdetails
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


#from users.models import bill
# Create your views here.
def login(request):
    
   if request.method == 'POST':
        if 'register' in request.POST:

            hospitalName= request.POST['h']
            email = request.POST['e']
            doctorPassword = request.POST['d']
            attendantPassword = request.POST['a']
            medicalShoppassword = request.POST['m']
            contactNumber = request.POST['c']
            print(hospitalName)

            if doctorPassword != attendantPassword and doctorPassword != medicalShoppassword and attendantPassword!= medicalShoppassword: 
                if userdetails.objects.filter(email__iexact=email).exists():
                    messages.error(request,'SignUp failed, E-Mail Id exists')
                    return redirect('login')
                elif userdetails.objects.filter(contactNumber__iexact=contactNumber).exists():
                    messages.error(request,'SignUp failed, ContactNumber exists')
                    return redirect('login')
                else:
                    doctorPassword = make_password(doctorPassword)
                    attendantPassword = make_password(attendantPassword)
                    medicalShoppassword = make_password(medicalShoppassword)
                    usr = userdetails.objects.create(hospitalName=hospitalName,email=email,doctorPassword=doctorPassword,attendantPassword=attendantPassword,medicalShoppassword=medicalShoppassword,contactNumber=contactNumber)
                    usr.save()
                    profile_obj = Profile.objects.create(user = usr)
                    profile_obj.save()
                    # num = bill.objects.create(user=usr,BillNum=1)
                    # num.save()
                    messages.error(request,'User details Saved')
                    return redirect('login')
            else:
                messages.error(request,'All passwords should be different... Signup Failed !!!')
                return redirect('login')

        if 'login' in request.POST:
            username = request.POST['email']
            password = request.POST['password']
            role = request.POST['role']
            print(role)
            if userdetails.objects.filter(email__iexact=username).exists():

                if role == 'Attendant':
                    checkpass = userdetails.objects.filter(email=username).values('attendantPassword')
                    checkpass=checkpass[0]['attendantPassword']
                    validity = check_password(password,checkpass)
                    
                    if validity:
                        #messages.success(request,'Attendant Password')
                        id=userdetails.objects.filter(email=username).values('id')
                        id=id[0]['id']
                        request.session['name'] = id
                        
                        return redirect('attendant/%d/'%id)
                    else:
                        messages.error(request,'Check the Password')
                        return redirect('login')
                if role ==  'Doctor':
                    checkpass = userdetails.objects.filter(email=username).values('doctorPassword')
                    checkpass=checkpass[0]['doctorPassword']
                    validity = check_password(password,checkpass)
                    
                    if validity:
                        #messages.error(request,'doctorPassword Password')
                        id=userdetails.objects.filter(email=username).values('id')
                        id=id[0]['id']
                        request.session['name'] = id
                        
                        return redirect('doctor/%d/'%id)
                        
                    else:
                        messages.error(request,'Check the Password')
                        return redirect('login')
                if role == 'Medical-Shop':
                    checkpass = userdetails.objects.filter(email=username).values('medicalShoppassword')
                    checkpass=checkpass[0]['medicalShoppassword']
                    validity = check_password(password,checkpass)
                    
                    if validity:
                        #messages.error(request,'medicalShoppassword Password')
                        id=userdetails.objects.filter(email=username).values('id')
                        id=id[0]['id']
                        request.session['name'] = id
                       
                        
                        return redirect('medicalshop/%d/'%id)
                    else:
                        messages.error(request,'Check the Password')
                        return redirect('login')

                """ if userdetails.objects.filter(email__iexact=username, doctorPassword=password ).exists():
                    messages.error(request,'Doctor Password')
                    return redirect('login')
                if userdetails.objects.filter(email__iexact=username,attendantPassword__iexact=password ).exists():
                    messages.error(request,'Attendant Password')
                    return redirect('login')
                if userdetails.objects.filter(email__iexact=username,medicalShoppassword__iexact=password ).exists():
                    messages.error(request,'medical Shop password Password')
                    return redirect('login') """
            else:
                messages.error(request,'Invalid Credential')
                return redirect('login')



   return render(request,'login.html')

def logout(request):
    
    return redirect('login')
   

def how(request):
    return render(request,'how.html')

import uuid
from authn.helper import send_forget_password_mail
def forget(request):
    
    if request.method == 'POST':
        username = request.POST['email']
        role = request.POST['role']

        if userdetails.objects.filter(email=username).exists():
            
            user_obj = userdetails.objects.get(email = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            profile_obj.role = role
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('forget')
        else:
            messages.error(request,'E-mail id not exists')
            return redirect('forget')
    return render(request,'forget.html')


def changepassword(request , token):
    context = {}
    profile_obj = Profile.objects.filter(forget_password_token = token).first()
    if profile_obj == None:
        messages.error(request,'Link expired!!!')
        return redirect('login')

    else: 
        print('profileObj',profile_obj)
        #print('check',profile_obj.user_id)
        print(profile_obj.user_id)
        role = Profile.objects.filter(forget_password_token = token).values('role')
        print('role',role)
        role=role[0]['role']
        context = {'user_id' : profile_obj.user.id}

        if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('reconfirm_password')
                user_id = request.POST.get('user_id')
                
                if user_id is  None:
                    messages.error(request, 'No user id found.')
                    return redirect(f'/changepassword/{token}/')
                    
                
                if  new_password != confirm_password:
                    messages.error(request, 'Password Not Matched')
                    return redirect(f'/changepassword/{token}/')
                            
                
                # user_obj = userdetails.objects.get(id = user_id)
                new_password = make_password(new_password)
                if role == 'Attendant':
                    userdetails.objects.filter(id=user_id).update(attendantPassword=new_password)
                    
                    
                if role == 'Doctor':
                    userdetails.objects.filter(id=user_id).update(doctorPassword=new_password)
                    
                if role == 'Medical-Shop':
                    userdetails.objects.filter(id=user_id).update(medicalShoppassword=new_password)
                    

                    
                messages.success(request, 'Password updated successfully!')
                return redirect('login')
                
            
            
    return render(request , 'changepassword.html' , context)

