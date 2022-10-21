from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'home.html')


def signup(request):
    std=Desigination.objects.all()
    return render(request,'signup.html',{'std':std})


def adminhome(request):
    if 'amname' in request.session:
        std=Vehicle_registeration.objects.all()
        return render(request,'admin_home.html',{'std':std})
    return redirect('user_logout')


def userhome(request):
    if 'pid' in request.session:
        pk=request.session['pid']
        username=Registration.objects.get(id=pk)
        std=Vehicle_registeration.objects.all()
        return render(request,'user_home.html',{'std':std,'user':username})
    return redirect('user_logout')

def super_admin(request):
    if 'username' in request.session:
        userid=request.session['username']
        std=Vehicle_registeration.objects.filter(user_id=userid)
        return render(request,'super_admin.html',{'std':std})
    return redirect('user_logout')

def login_page(request):
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            # auth.login(request,user)
            request.session['username']=user.id
            return redirect('super_admin') 
        elif Registration.objects.filter(username=username,password=password,desigination_id=1):
            pm=Registration.objects.get(username=username,password=password)
            request.session['pid']=pm.id
            request.session['pname']=pm.username
            return redirect('userhome')
        elif Registration.objects.filter(username=username,password=password,desigination_id=2):
            am=Registration.objects.get(username=username,password=password)
            request.session['am.id']=am.id
            request.session['amname']=am.username
            return redirect('adminhome')
        else:
            messages.error(request,'username does not exists')
            return redirect('login_page')       
    logout(request)    
    return render(request,'login.html')



def registration(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['cpassword']
        desiginations=request.POST['desiginations']
        
        if password == confirmpassword:
            if  User.objects.filter(username=username):
                messages.info(request,'username already exists')
                return redirect('registration')
            elif Registration.objects.filter(username=username):
                messages.info(request,'username already exists')
                return redirect('registration')
                
            else:
                user = Registration(first_name=firstname,last_name=lastname,email=email,username=username,password=password,
                                    desigination_id=desiginations)
                user.save()
                print('hi')
                msg_success = "Registration Successfull"
                messages.info(request, 'Registration successfully completed')
                return render(request,'signup.html',{'msg_success':msg_success})
        else:
            messages.info(request, 'password not matching')
            return redirect('registration')
   
    return redirect('signup')






# def user_logout(request):
#     if 'username' in request.session:
#         request.session.flush()
#     return redirect('login_page')    

def add_vehicle(request):
    if 'username' in request.session:
        userid=request.session['username']
        if request.method=='POST':
            vehicle_number=request.POST['vehicle_number']
            vehicle_Type=request.POST['type']
            vehicle_model=request.POST['model']
            vehicle_description=request.POST['description']
            stm=Vehicle_registeration(vehicle_number=vehicle_number,
                                      vehicle_type=vehicle_Type,
                                      vehicle_model=vehicle_model,
                                      vehicle_description=vehicle_description,
                                      user_id=userid)
            stm.save()
            print('hi')
            return redirect('super_admin')
        return render(request,'add_vehicle.html')
    return redirect('user_logout')

def update_vehicle(request,pk):
    if 'username' in request.session:
        std=Vehicle_registeration.objects.get(id=pk)
        if request.method=='POST':
            std.vehicle_number=request.POST['vehicle_number']
            std.vehicle_type=request.POST['type']
            std.vehicle_model=request.POST['model']
            std.vehicle_description=request.POST['description']
            std.save()
            return redirect('super_admin')
        return render(request,'vehicle_update.html',{'std':std})
    return redirect('user_logout')



def update_vehicle_admin(request,pk):
    if 'amname' in request.session:
        std=Vehicle_registeration.objects.get(id=pk)
        if request.method=='POST':
            std.vehicle_number=request.POST['vehicle_number']
            std.vehicle_type=request.POST['type']
            std.vehicle_model=request.POST['model']
            std.vehicle_description=request.POST['description']
            std.save()
            return redirect('adminhome')
        return render(request,'admin_update.html',{'std':std})
    return redirect('user_logout')


def delete_vehicle(request,pk):
    if 'username' in request.session:
        std=Vehicle_registeration.objects.get(id=pk)
        std.delete()
        return redirect('super_admin')
    return redirect('user_logout')


def user_logout(request):
    logout(request)
    return redirect('login_page')  