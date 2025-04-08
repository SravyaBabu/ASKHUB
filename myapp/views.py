from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime

# Create your views here.

def home(request):
    return render(request,"home.html")

def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        userlogin = Login.objects.filter(username=username,viewPassword=password).first()
        if userlogin is not None:
            request.session['uid']=userlogin.id
            if userlogin.usertype=="User":
                messages.info(request,"Welcome")
                return redirect("/userdash")
            else:
                messages.info(request,"Invalid Username Or Password")
                return redirect("/login")
        else:
            messages.info(request,"Invalid Username Or Password")
            return redirect("/login")
    return render(request,'login.html')


def logout(request):
    if 'uid' in request.session:
        del request.session['uid'] 
    messages.info(request, "You have successfully logged out!")
    return redirect('login')

def register(request):
    if request.POST:
        username =  request.POST["username"]
        firstname =  request.POST["firstname"]
        lastname =  request.POST["lastname"]
        photo = request.FILES["photo"]
        mobile =  request.POST["mobile"]
        dob =  request.POST["dob"]
        address =  request.POST["address"]
        password =  request.POST["password"]
        bio = request.POST["bio"]
        if Login.objects.filter(username=username).exists():
            messages.info(request,"Already Have Registered")
        log = Login.objects.create(username=username,usertype='User',viewPassword=password)
        log.save()
        userregister = User.objects.create(loginid=log,username=username,firstname=firstname,lastname=lastname,photo=photo,mobile=mobile,dob=dob,address=address,bio=bio)
        userregister.save()
        return redirect('/login')
    return render(request,'register.html')

def termsandcondi(request):
    return render(request,'termsandcondi.html')


def dashboard(request):
    uid=request.session['uid']
    user = User.objects.get(loginid = uid)
    question = Question.objects.all()
    return render(request,'User/dashboard.html',{'user':user,'question':question})

def askquestion(request):
    today = datetime.now()
    today = today.strftime('%Y-%m-%d')
    uid=request.session['uid']
    user = User.objects.get(loginid = uid)
    if request.POST:
        title = request.POST['title']
        body = request.POST['body']
        image = request.FILES['image']
        question = Question.objects.create(user=user,title=title,body=body,image=image,date=today)
        question.save()
        messages.info(request,"Question posted")
        return redirect('/userdash')
    return render(request,'User/askquestion.html',{'user':user})

def profile(request):
    uid=request.session['uid']
    user = User.objects.get(loginid = uid)
    question = Question.objects.filter(user=user)
    return render(request,'User/profile.html',{'question':question,'user':user})

def answerquestion(request):
    today = datetime.now()
    today = today.strftime('%Y-%m-%d')
    uid=request.session['uid']
    user = User.objects.get(loginid = uid)
    id = request.GET.get('id')
    question = Question.objects.get(id=id)
    questionanswer = None
    if request.POST:
        answer = request.POST['answer']
        questionanswer = Answer.objects.create(user=user,question=question,answer=answer,date=today)
        question.countanswers += 1
        question.save()
    answers = Answer.objects.filter(question=question).order_by('-date')
    return render(request,'User/answers.html',{'question':question,'user':user,'questionanswer':questionanswer,'answers':answers})

def likes(request):
    uid=request.session['uid']
    user = User.objects.get(loginid = uid)
    ansid = request.GET.get('id')
    answer = Answer.objects.get(id=ansid)
    if request.method == 'POST':
        answer.likes += 1
        answer.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))