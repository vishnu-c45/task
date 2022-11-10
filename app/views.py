from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse

# Create your views here.
#home
def home(request):
    return render(request,'home.html')

#signup page
def signup(request):
    std=Desigination.objects.all()
    return render(request,'signup.html',{'std':std})

#admin page
def adminhome(request):
    if 'amname' in request.session:
        std=Vehicle_registeration.objects.all()
        return render(request,'admin_home.html',{'std':std})
    return redirect('user_logout')

#load user home 
def userhome(request):
    if 'pid' in request.session:
        pk=request.session['pid']
        username=Registration.objects.get(id=pk)
        std=Vehicle_registeration.objects.all()
        return render(request,'user_home.html',{'std':std,'user':username})
    return redirect('user_logout')


#super admin page
def super_admin(request):
    if 'username' in request.session:
        userid=request.session['username']
        std=Vehicle_registeration.objects.filter(user_id=userid)
        return render(request,'super_admin.html',{'std':std})
    return redirect('user_logout')

#login user,admin,superadmin
def login_page(request):
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            # auth.login(request,user)
            request.session['username']=user.id
            return redirect('super_admin') 
        elif Registration.objects.filter(username=username,password=password,desigination=Desigination.objects.get(desigination="USER")):
            pm=Registration.objects.get(username=username,password=password)
            request.session['pid']=pm.id
            request.session['pname']=pm.username
            return redirect('userhome')
        elif Registration.objects.filter(username=username,password=password,desigination=Desigination.objects.get(desigination="ADMIN")):
            am=Registration.objects.get(username=username,password=password)
            request.session['am.id']=am.id
            request.session['amname']=am.username
            return redirect('adminhome')
        else:
            messages.error(request,'user does not exists')
            return redirect('login_page')               
    logout(request)    
    return render(request,'login.html')


#register user and admin
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
                messages.error(request,'username already exists')
                return redirect('signup')
            elif Registration.objects.filter(username=username):
                messages.error(request,'username already exists')
                return redirect('signup')
                
            else:
                user = Registration(first_name=firstname,last_name=lastname,email=email,username=username,password=password,
                                    desigination_id=desiginations)
                user.save()
                messages.success(request, 'Registration successfully completed')
                return redirect('signup')
        else:
            messages.error(request, 'password not matching')
            return redirect('registration')
   
    return redirect('signup')


  
#create vehicle registration
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
            messages.success(request,'successfully created')
            return redirect('add_vehicle')
        return render(request,'add_vehicle.html')
    return redirect('user_logout')

#add desigination in superadmin
def add_desigination(request):
    if 'username' in request.session:
        if request.method== 'POST':
            desigination=request.POST['desi']
            if Desigination.objects.filter(desigination=desigination):
                messages.warning(request,'desigination already exists')
                return redirect('add_desigination')
            else:
                #desigination saving only uppercase
                std=Desigination(desigination=desigination)
                std.save()
                messages.success(request,'desigination Add successfully')
                return redirect('add_desigination')
        return render(request,'add_desigination.html')
    return redirect('user_logout')



#update vehicle registration in super admin
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


#update vehicle registration in admin
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

#delete vehicle registration
def delete_vehicle(request,pk):
    if 'username' in request.session:
        std=Vehicle_registeration.objects.get(id=pk)
        std.delete()
        messages.error(request,'deleted successfully')
        return redirect('super_admin')
    return redirect('user_logout')

#To view user and admin accounts in super admin
def user_admin_list(request):
    if 'username' in request.session:
        std=Registration.objects.all()
        return render(request,'user_admin_action.html',{'std':std})
    return redirect('user_logout')

#delete user and admin accounts
def delete_user_admin(request,pk):
    if 'username' in request.session:
        std=Registration.objects.get(id=pk)
        std.delete()
        messages.success(request,'deleted successfully')
        return redirect('user_admin_list')
    return redirect('user_logout')

#logout function
def user_logout(request):
    logout(request)
    return redirect('login_page')  