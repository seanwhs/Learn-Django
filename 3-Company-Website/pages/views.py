from django.shortcuts import render
from django.views.generic import TemplateView

def home_page_view(request):
    context = {
        'inventory_list' : ['widget 1', 'widget 2', 'widget 3', 'widget 4' ],
        'greeting': 'Thank yOu fOr ViSiting',
    }
    return render(request, "pages/home.html", context)

class about_page_view(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['contact_address']='123 Memory Lane'
        context['phone_number']='555-555-5555'
        return context