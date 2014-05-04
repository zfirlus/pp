from datetime import datetime
from django.db.utils import ConnectionDoesNotExist
from main import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import loader, RequestContext
from main.models import Category, Project, Comment, User, Perk, Donation
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
import decimal
from decimal import Decimal

def index(request):
    template = loader.get_template('index.html')
    now = datetime.now().date()
    deadline_project_list = Project.objects.filter(deadline__gte=now).order_by('deadline')[:3]
    popular_project_list = Project.objects.filter(deadline__gte=now).order_by('-visit_counter')[:3]
    #wyswietla tylko prjekty niezakonczone, posortowane wzgledem licznika odwiedzin malejąco
    for p in deadline_project_list:
        perc = (p.money_raised / p.funding_goal) * 100
        percentage = int(perc)
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
        setattr(p, 'percentage', percentage)

    for p in popular_project_list:
        perc = (p.money_raised / p.funding_goal) * 100
        percentage = int(perc)
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
        setattr(p, 'percentage', percentage)

    context = RequestContext(request, {
        'deadline_project_list': deadline_project_list,
        'popular_project_list': popular_project_list,
    })
    return HttpResponse(template.render(context))


def projects(request):
    order_by = request.GET.get('order_by', '-visit_counter')
    key = request.GET.get('key', '')
    projects_list = Project.objects.filter(Q(title__contains=key) | Q(full_description__contains=key)).order_by(
        order_by)
    now = datetime.now().date()
    for p in projects_list:
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
    template = loader.get_template('projects.html')
    context = RequestContext(request, {
        'projects_list': projects_list,
        'key': key,
    })
    return HttpResponse(template.render(context))


def adminUsers(request):
    template = loader.get_template('admin_users.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def adminCategories(request):
    template = loader.get_template('admin_categories.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def moderator(request):
    template = loader.get_template('moderator.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def categories(request):
    order_by = request.GET.get('order_by', 'name')
    cat_list = Category.objects.annotate(count=Count('project__id')).order_by(order_by)

    template = loader.get_template('categories.html')
    context = RequestContext(request, {
        'cat_list': cat_list,
    })
    return HttpResponse(template.render(context))


def projects(request, cat_id="0"):
    order_by = request.GET.get('order_by', '-visit_counter')
    key = request.GET.get('key', '')
    projects_list = Project.objects.filter(Q(title__contains=key) | Q(full_description__contains=key)).order_by(
        order_by)
    catId = int(cat_id)
    if catId > 0:
        projects_list = Project.objects.filter(category__id=catId).order_by(order_by)
    now = datetime.now().date()
    for p in projects_list:
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
    template = loader.get_template('projects.html')
    context = RequestContext(request, {
        'projects_list': projects_list,
        'key': key,
    })
    return HttpResponse(template.render(context))


def project(request, pro_id):
    template = loader.get_template('project.html')
    pro = Project.objects.get(id=int(pro_id))
    coms = Comment.objects.filter(project=pro).order_by('-date_created')
    context = RequestContext(request, {'coms': coms, 'proid': str(pro_id)})
    return HttpResponse(template.render(context))


def UserRegister(request):
    f = forms.UserRegisterForm()
    context = RequestContext(request, {'formset': f})
    if request.method == 'POST':
        f = forms.UserRegisterForm(request.POST)
        if f.is_valid():
            login = f.cleaned_data.get("login")
            email=f.cleaned_data.get("email")
            password = f.cleaned_data.get("password")
            confirmpassword=f.cleaned_data.get("confirmpassword")
            if password == confirmpassword:
                try:
                    us = User.objects.get(login=f.data['login'])
                except:
                    f.save()
                    return redirect('/', request)
                return redirect('/rejestracja')
                return redirect('/', request)
            else:
                return redirect('/rejestracja')
    else:
        return render_to_response('register.html', context)


def AddNewProject(request):
    f = forms.ProjectRegisterForm(prefix='project')
    fr = forms.ProjectPerks(prefix='perk')
    context = RequestContext(request, {'formset': f, 'form1': fr})
    if request.method == 'POST':
        f = forms.ProjectRegisterForm(request.POST, prefix='project')
        fr = forms.ProjectPerks(request.POST, prefix='perk')
        if f.is_valid():
            p = Project()
            p.title = f.cleaned_data['title']
            p.short_description = f.cleaned_data['short_description']
            p.funding_goal = f.cleaned_data['funding_goal']
            p.full_description = f.cleaned_data['description']
            p.category = f.cleaned_data['category']
            p.user_id = 1
            Project.save(p)
            return redirect('/', request)
    else:
        return render_to_response('AddNewProject.html', context)


def EditProject(request, project_id):
    f = forms.ProjectRegisterForm()
    context = RequestContext(request, {'formset': f})
    if request.method == 'POST':
        f = forms.ProjectRegisterForm(request.POST)
        if f.is_valid():
            f.save()
        return redirect('/', request)
    return


def Signin(request):
    if request.method == 'POST':
        c = forms.Signin(request.POST)
        try:
            us = User.objects.get(login=c.data['login'],password=c.data['password'])
        except:
            return redirect('/logowanie')
        request.session['user'] = us.id
        request.session['type'] = 2
        return redirect('/')
    else:
        f = forms.Signin
        return render_to_response('signin.html', RequestContext(request, {'formset': f}))


def addcoment(request, pro_id):
    if request.method == 'POST':
        c = forms.ComentForm(request.POST)
        coment = Comment()
        coment.project = Project.objects.get(id=int(pro_id))
        coment.content = c.data['content']
        coment.user = User.objects.get(id=1)
        coment.save()
        return redirect('/project/' + str(pro_id))
    else:
        f = forms.ComentForm
        return render_to_response('comment.html', RequestContext(request, {'formset': f}))

def Support(request,pro_id):
    template = loader.get_template('support.html')
    projekt = Project.objects.get(id=int(pro_id))
    perk_list = Perk.objects.filter(project=projekt).order_by('amount')
    zmienna=perk_list[0].amount
    choice_perk_list=Perk.objects.filter(project=projekt).order_by('amount')
    context = RequestContext(request, {
            'perk_list': perk_list,
            'choice_perk_list': choice_perk_list,
            'projekt': projekt,
            'proid': str(pro_id)
            })
    if request.method == 'POST':
        f = forms.SupportForm(request.POST)
        if f.data['amount']:
            if f.is_valid:
               amount=int(f.data['amount'])
               user = request.session['user']
               if amount<zmienna:
                   f = forms.SupportForm
                   return render_to_response('support.html', RequestContext(request, {'formset': f}),context)
               else:
                   for perk in perk_list:
                    if perk.amount<=amount:
                        kwota=perk.amount
                        id=perk.id
                        donation = Donation()
                        donation.amount=decimal.Decimal(f.data['amount'])
                        donation.date=datetime.now().date()
                        donation.user= User.objects.get(id=user)
                        donation.project=Project.objects.get(id=pro_id)
                        donation.perk=Perk.objects.get(id=id)
                        donation.save()
            return redirect('/',request)
        else:
            f = forms.SupportForm
            return render_to_response('support.html', RequestContext(request, {'formset': f}),context)
    else:
        f = forms.SupportForm
        return render_to_response('support.html', RequestContext(request, {'formset': f}),context)