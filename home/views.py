from django.shortcuts import render, redirect
from home.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def homepage(request):
    photos = Items.objects.all()
    return render(request, "index.html", {'sendpics':photos})


def registerpage(request):

    if request.method == 'POST':

        fnamev = request.POST.get('fnameh')
        lnamev = request.POST.get('lnameh')
        emailv = request.POST.get('emailh')
        passwordv = request.POST.get('passwordh')

        if User.objects.filter(username = emailv):
            messages.error(request, 'User already exists!....')
            return redirect('registerpage')
        
        user = User.objects.create(
            first_name = fnamev,
            last_name = lnamev,
            username = emailv,
        )

        user.set_password(passwordv)
        user.save()

        messages.success(request, 'Account Created Successfully!....')
        return redirect('registerpage')
    
    return render(request, "register.html")



def loginpage(request):

    if request.method == 'POST':

        emailv = request.POST.get('emailh')
        passwordv = request.POST.get('passwordh')
        
        if not User.objects.filter(username = emailv):
            messages.error(request, 'Invalid username!....')
            return redirect('loginpage')
        
        user = authenticate(username = emailv, password = passwordv)

        if user is None:
            messages.error(request, 'Invalid Password!....')
            return redirect('loginpage')
        else:
            login(request, user)
            messages.success(request, 'Login Succesfull!...')
            return redirect('homepage')

    return render(request, "login.html")


def logoutpage(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url=loginpage)
def createpage(request):
    if request.method == 'POST':
        titlev = request.POST.get('titleh')
        descv = request.POST.get('descriptionh')
        imgurlv = request.POST.get('imageh')
        insert = Items( title=titlev, descripion=descv, imgurl = imgurlv )
        insert.save()
        return redirect('displaypage')
    return render(request, "create.html")


@login_required(login_url=loginpage)
def displaypage(request):
    # featch all data from the database
    display = Items.objects.all()
    # to search any item code
    if request.GET.get('searchname'):
        display = display.filter(title__icontains = request.GET.get('searchname'))
    # end search code
    return render(request, "display.html", {'dispdata': display})



def delete_item(request, id):
    item = Items.objects.get(id=id)
    item.delete()
    return redirect('displaypage')



def update_item(request, id):
    item = Items.objects.get(id =id)
    if request.method == 'POST':
        item.title = request.POST.get('titleh')
        item.descripion = request.POST.get('descriptionh')
        item.imgurl = request.POST.get('imageh')
        item.save()
        return redirect('displaypage')

    return render(request, 'updated.html', {'item': item})
