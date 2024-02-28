from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

# Create your views here.
class Tasklist(LoginRequiredMixin,ListView):
    model =Task
    context_object_name='tasks'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
         
        context['tasks']=context['tasks'].filter(user=self.request.user)  
        context['count']=context['tasks'].filter(complete=False).count()
        
        search_input=self.request.GET.get('serach-area') or ''
        if search_input :
            
            context['tasks']=context['tasks'].filter(title__icontains=search_input)
      
           
        return context
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasklist')
    
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
    
    
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasklist')
    
class TaskDelete(LoginRequiredMixin,DeleteView):
    context_object_name='task'
    model=Task
    fields='__all__'
   
    success_url=reverse_lazy('tasklist')
    
    
   
class Login(LoginView):
       template_name='login.html'
       fields='__all__'
       redirect_authenticated_user=True
       
       
       def get_success_url(self):
           return reverse_lazy('tasklist')
       
       
class Register(FormView):
    template_name='register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasklist')
    
    def form_valid(self,form):
        
        user=form.save()
        if user is not None:
            login(self.request,user)
            
            
        return super(Register,self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(Register,self).get(*args,**kwargs)
