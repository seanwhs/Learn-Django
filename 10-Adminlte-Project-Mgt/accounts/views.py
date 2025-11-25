from django.shortcuts import render
from django.views.generic import View

# class DashboardView(View):    
#     def get(self, request, *args, **kwargs):
#         return render(request, 'accounts/dashboard.html')

class DashboardView(View):    
    def get(self, request, *args, **kwargs):
        context = {}
        context['name'] = 'Sean'
        context['email'] = 'Sean@email.com'
        return render(request, 'accounts/dashboard.html', context)