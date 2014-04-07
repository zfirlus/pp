from django.http import HttpResponse
from django.template import loader, RequestContext

# Create your views here.

def index(request):
    template = loader.get_template('base.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))