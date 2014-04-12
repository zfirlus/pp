from datetime import datetime, timedelta
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.template import Context
from main.models import Category, Project
from django.db.models import Q, Count


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
    projects_list = Project.objects.filter(Q(title__contains=key) | Q(full_description__contains=key)).order_by(order_by)
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
        'key' : key,
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
    projects_list = Project.objects.filter(Q(title__contains=key) | Q(full_description__contains=key)).order_by(order_by)
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
        'key' : key,
    })
    return HttpResponse(template.render(context))

