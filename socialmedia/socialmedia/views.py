from django.views import generic

class HomePage(generic.TemplateView):
    template_name = 'index.html'

class Test(generic.TemplateView):
    template_name = 'log_confirm.html'

class LogOut_confirm(generic.TemplateView):
    template_name = 'log_out_confirm.html'