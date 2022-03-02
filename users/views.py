from ast import Return
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from authn.models import userdetails
from users.models import notAvailableTablets, patientDetails
from django.db.models import Max
# Create your views here.
import datetime
from datetime import datetime
import pytz
from datetime import date



def attendant(request,pk):
    
        #print('username is...',request.user.username
        data = pk
        #print(data)
        name= userdetails.objects.get(id=data)
        """ args=patientNum.objects.filter(user=data)
        t=args.aggregate(Max('patientNum'))
        t1=t['patientNum__max']
        num = t1
        print('maximum with respect to user:',num) """
        if request.method == 'POST':
            print('hello..........')
            if 'delete' in request.POST:
                itemid = request.POST.get('id')
                print('id to be deleted is...',itemid)
                patientDetails.objects.filter(id=itemid).delete()
                #userid=patientDetails.objects.filter(id=itemid).values('userdet_id')
                #userid= userid[0]['userdet_id']
                #print('userid is...',userid)
                # id=patientDetails.objects.filter(id=itemid).values('patientNumber')
                # id=id[0]['patientNumber']
                # id1 = id+1
                # print('also to be deleted',id)
                # print('include this also',id1)
            # patientNum.objects.filter(patientNum=id).delete()
                #patientNum.objects.filter(patientNum=id1).delete()
                return redirect(request.path)
            if 'update' in request.POST:
                itemid = request.POST.get('id')
                u_name = request.POST['pname']
                u_reason = request.POST['reason']
                u_age =  request.POST['age']
                u_tel = request.POST['tel']
                u_blood = request.POST['blood']
                u_gender = request.POST['gender']
                # u_date = request.POST['date']
                # cdate =u_date
                # datetimeobject = datetime.strptime(cdate,'%Y-%m-%d')
                # new_format = datetimeobject.strftime('%d-%m-%Y') 
                #print('new date',new_format)
                print('updated name:',u_name)
                print('updated name:',u_age)
                print('updated name:',u_tel)
                #print('updated name:',u_date)
                print('id to be updated is...',itemid)
                print('gender to be updated is...',u_gender)
                patientDetails.objects.filter(id=itemid).values('patientName').update(patientName=u_name)
                patientDetails.objects.filter(id=itemid).values('generalReason').update(generalReason=u_reason)
                #userid= userid[0]['patientName']
                #print('patient Name  is...',userid)
                patientDetails.objects.filter(id=itemid).values('age').update(age=u_age)
                #userid1= userid1[0]['age']
                #print('age is...',userid1)
                patientDetails.objects.filter(id=itemid).values('contactNumber').update(contactNumber=u_tel)
                patientDetails.objects.filter(id=itemid).values('bloodGroup').update(bloodGroup=u_blood)
                patientDetails.objects.filter(id=itemid).values('gender').update(gender=u_gender)
                #userid2= userid2[0]['contactNumber']
                #print('contactNumber  is...',userid2)
                #userid3=patientDetails.objects.filter(id=itemid).values('date').update(date=new_format)
                #userid3= userid3[0]['date']
                #print('date  is...',userid3)
                #patientDetails.filter().update()
                return redirect(request.path)
            else:
                pname = request.POST['pname']
                age = request.POST['age']
                gender = request.POST['gender']
                tel = request.POST['tel']
                dat = request.POST.get('date')
                reason = request.POST.get('reason')
                blood = request.POST['blood']
                status = request.POST['status']
                print('status is...',status)
                """ args=patientNum.objects.filter(user=data)
                t=args.aggregate(Max('patientNum'))
                t1=t['patientNum__max']
                num = t1
                addnum = num+1
                args=addnum
                print('data',data) """
                print('date is',dat)
                cdate =dat
                datetimeobject = datetime.strptime(cdate,'%Y-%m-%d')
                new_format = datetimeobject.strftime('%d-%m-%Y') 
                print('new date',new_format)

                data= userdetails.objects.only('id').get(id=data) #Note this
                add = patientDetails(userdet=data,gender=gender,patientName=pname,generalReason=reason,age=age,contactNumber=tel,bloodGroup=blood,date=new_format,status=status)
                add.save()
                
                """ b=patientNum.objects.create(patientNum=args,user=data)
                b.save() """
                return redirect(request.path)
        today = date.today()
        d1= today.strftime("%d-%m-%Y")
        print("Today's date:", d1)
        details = patientDetails.objects.filter(userdet=data,status='Waiting').order_by('date')
        print('details',details)
        count = patientDetails.objects.filter(userdet=data,date=d1,status='Waiting').count()
        completed = patientDetails.objects.filter(userdet=data,date=d1,status='Diagonised').count()
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        d = now.strftime('%d/%m/%Y')
        
        context = {
            "data" : data,
            "name" : name,
            "details" :details,
            "count" : count,
            "completed":completed,
            "today":d
            
        }
        
        return render(request,'attendant.html',context)
    

from django.shortcuts import render
from json import dumps
#simple_variable = 6 
def doctor(request,pk):
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        d = now.strftime('%d/%m/%Y')
        data =pk
        request.session['data2'] = data
        name= userdetails.objects.get(id=data)
        details = patientDetails.objects.filter(userdet=data,status='Waiting',date=d)
        #count = patientDetails.objects.filter(userdet=data,status='Waiting').count()
        #global simple_variable
        #simple_variable = pk
        #print('test simple',simple_variable)
        
        name_test = name
        str_name = str(name_test)
        naming = str_name.upper()
        name = naming
        context ={
            "name": name,
            "details" :details,
            "pk":pk,
            "today":d
            #"count" : count
        }
        return render(request,'doctor.html',context)
    



def getdata(request):
    data = request.session.get('name')
    
    test = request.GET.get('attack')
    print('test value.....',test)
    #global simple_variable
    #print('Got the output', simple_variable)
    #data= simple_variable
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    d = now.strftime('%d-%m-%Y')
    name= userdetails.objects.get(id=test)
    details = patientDetails.objects.filter(userdet=test,status='Waiting',date=d)
    print('details',details)
    print('date',d)
    counti = patientDetails.objects.filter(userdet=test,status='Waiting').count()
    return JsonResponse({"details":list(details.values())}) 

"""
def test(request):
    data = request.session.get('data2')
    data = userdetails.objects.get(id=data)
    context={
        "data":data
    }
    return render(request,'test.html',context) """


def test(request,pk):
      
        data = request.session.get('data2')
        data = userdetails.objects.get(id=data)
        age=patientDetails.objects.filter(id=pk).values('age')
        age = age[0]['age']
        reason=patientDetails.objects.filter(id=pk).values('generalReason')
        reason = reason[0]['generalReason']
        name=patientDetails.objects.filter(id=pk).values('patientName')
        name = name[0]['patientName']
        blood=patientDetails.objects.filter(id=pk).values('bloodGroup')
        blood = blood[0]['bloodGroup']
        gender=patientDetails.objects.filter(id=pk).values('gender')
        gender = gender[0]['gender']
        id= patientDetails.objects.filter(id=pk).values('userdet_id')
        id = id[0]['userdet_id']
        hid=id
        id = '/doctor'+'/'+str(id)
        print('id is',id)
        request.session['u_back_session'] = id
        if request.method == 'POST':
            u_problem = request.POST.get('problem')
            u_tablet =  request.POST.get('tablet')
            u_status =  request.POST.get('status')
            print('status came....',u_status)
            patientDetails.objects.filter(id=pk).values('problem').update(problem=u_problem)
            patientDetails.objects.filter(id=pk).values('tabletsDetails').update(tabletsDetails=u_tablet)
            patientDetails.objects.filter(id=pk).values('status').update(status=u_status)
            id= patientDetails.objects.filter(id=pk).values('userdet_id')
            id = id[0]['userdet_id']
            
            testing = '/doctor'+'/'+str(id)
            
            return redirect(testing)
        tabletsdetails = notAvailableTablets.objects.filter(hospitalId=hid)
        print(tabletsdetails)
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        d = now.strftime('%d/%m/%Y')
        context ={
            "age":age,
            "name":name,
            "data":data,
            "blood":blood,
            "gender":gender,
            "id":id,
            "today":d,
            "reason":reason,
            "tabletsdetails":tabletsdetails
        }

        return render(request,'test.html',context) 
    

def medicalshop(request,pk):
   
        
        h_name=userdetails.objects.filter(id=pk).values('hospitalName')
        h_name = h_name[0]['hospitalName']
        print('printig',h_name)
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        d = now.strftime('%d/%m/%Y')
        context={
            "h_name":h_name,
            "pk":pk,
            "today":d
        }
        if request.method == 'POST':
            
            
            Tpath='notAvailTablets/'
            return redirect(Tpath)
        return render(request,'medicalshop.html',context)
    

""" def back(request):
    try:
        print('hello')
        if request.method == 'GET':
            del request.session['back']
            doc_back = request.session.get('u_back_session')
            print('Back----doc_back',doc_back)
            print('deleted......')
            return redirect(doc_back)
    except KeyError:
        return redirect('login') """ 
    
def getmedicalshop(request):
    data = request.GET.get('attack')
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    today = now.strftime('%d-%m-%Y')
    details = patientDetails.objects.filter(userdet=data,date=today,status='Diagonised',tabletsStatus__isnull=True).order_by('date')
    print('details',details)
    return JsonResponse({"details":list(details.values())})

def givetablets(request,pk):
    
        name=patientDetails.objects.filter(id=pk).values('patientName')
        name = name[0]['patientName']
        id1= patientDetails.objects.filter(id=pk).values('userdet_id')
        id1 = id1[0]['userdet_id']
        f_id = id1
        h_name=userdetails.objects.filter(id=id1).values('hospitalName')
        h_name = h_name[0]['hospitalName']
        tablets = patientDetails.objects.filter(id=pk).values('tabletsDetails')
        tablets = tablets[0]['tabletsDetails']
        problem = patientDetails.objects.filter(id=pk).values('problem')
        problem = problem[0]['problem']
        id1 = '/medicalshop'+'/'+ str(id1)
        print('id is ...',id1)
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        d = now.strftime('%d/%m/%Y')
        context ={
                
                "name":name,
                "h_name":h_name,
                "tablets":tablets,
                "problem":problem,
                "today":d
            }
        
        if request.method == 'POST':
            status = request.POST.get('status')

            print('Status is....',status)
            patientDetails.objects.filter(id=pk).values('tabletsStatus').update(tabletsStatus=status)
            Not_Available = request.POST.get('Not Available')
            if status =="Not Available":
                print('Not Available tablets details.....',Not_Available)
                data= patientDetails.objects.only('id').get(id=pk) #Note this
                add = notAvailableTablets(patientnum=data,tabletsname=Not_Available,hospitalId=f_id)
                add.save()
            return redirect(id1)
        return render(request,'tablets.html',context)
    

def notAvailTablets(request,test):
    print('test is...',test)
    data= userdetails.objects.only('id').get(id=test)
    print('another test is...',data)
    name=userdetails.objects.filter(id=test).values('hospitalName')
    name=name[0]['hospitalName']
    details = notAvailableTablets.objects.filter(hospitalId=test)
    count = notAvailableTablets.objects.filter(hospitalId=test).count()
    print('details......',details)
    context ={
        'name':name,
        'details':details,
        'count':count
    } 
    if request.method == 'POST':
        if 'add' in request.POST:
            tabletsname = request.POST.get('tablets')
            add=notAvailableTablets.objects.create(tabletsname=tabletsname,hospitalId=test)
            add.save()
            return redirect(request.path)
            
        if 'delete' in request.POST:
            itemid = request.POST.get('id')
            print('id to be deleted is...',itemid)
            notAvailableTablets.objects.filter(id=itemid).delete()
            return redirect(request.path)
    return render(request,'notAvailTablets.html',context)