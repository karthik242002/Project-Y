from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView,  UpdateView, DetailView
from portfolio.forms import UserForm, PortfolioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from portfolio.models import Portfolio
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Feature
import openai, datetime
# Create your views here.
class personal_info(LoginRequiredMixin, CreateView):
    login_url = '/signin/'
    form_class = PortfolioForm
    model = Portfolio
    context_name = "form"
    template_name = 'portfolio/personal_info.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.username = self.request.user
        obj.save()
        return redirect('cv_template')

class UpdatePersonal_info(LoginRequiredMixin, UpdateView):
    login_url = '/signin/'
    form_class = PortfolioForm
    model = Portfolio
    context_name = "form"
    template_name = 'portfolio/personal_info.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.username = self.request.user
        obj.save()
        return redirect('cv_template')

class cv_list(ListView):
    template_name = 'portfolio/cv_list.html'
    model = Portfolio
    context_object_name = 'port'

class test_template(LoginRequiredMixin, ListView):
    login_url = '/signin/'
    model= Portfolio
    template_name = 'portfolio/templates/index_1.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username=self.request.user.username)
        return context

class text_template2(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    model = Portfolio
    template_name = 'portfolio/templates/index_2.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context

class text_template3(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = 'portfolio/templates/index_3.html'
    model = Portfolio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context  

class text_template4(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    model = Portfolio
    template_name = 'portfolio/templates/index_4.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username=self.request.user.username)
        return context

class text_template5(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = "portfolio/templates/index_5.html"
    model = Portfolio
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context
           

###############################      REGISTER    #################################
def signup_user(request):
    form_name = UserForm()
    if request.method =="POST":
        form_name = UserForm(request.POST)
        if form_name.is_valid():
            form_name.save()
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Invalid input') 
            return redirect('signup')
    else:
        context = {'form_name':form_name}
        return render(request, 'portfolio/signup.html', context)

def signin_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cv_template')
        else:
            messages.info(request, 'Invalid input.. Please try again.')
            return redirect('signin')
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'portfolio/signin.html', context)

def logout_user(request):
    logout(request)
    return redirect('signin')

# Create your views here.
def index(request):
    context={
        'name':'surya',
        'age':20,
        'nationality':'Indian'

    }#return render(request,'index.html',context)  this is to render the index.html content

    feature1=Feature()
    feature1.id =0
    feature1.name='Very Fast'
    feature1.details='it is compartively very fast then others'

    feature2=Feature()
    feature2.id =1
    feature2.name='high Transimission'
    feature2.details='it is compartively very fast then others devies'

    feature3=Feature()
    feature3.id =2
    feature3.name='responsive to all screens'
    feature3.details='it is compartively very fast then others objects'

    features=[feature1,feature2,feature3]
    
    return render(request,'index.html',{'features':features})

def counter(request):
    letters=request.POST['text']     #this is the place where the text from index.html is rendered
    amt_of_words=len(letters.split())
    return render(request,'counter.html',{'count':amt_of_words})

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home') 
        else:
            messages.info(request,'Credential are not valid')
            return redirect('login')
    else:
        return render(request,'login.html')

def studemp(request):
    return render(request,'studemp.html')

'''def store(request):
    return HttpResponse('<h1>this is surya\'s store</h1>')'''


# chatbot ...........................................
def gpt(queary):
    openai.api_key = "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"
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].get("text")

messages = []
def chatbot(request):
    times = datetime.datetime.now()
    current_time = times.strftime("%H:%M %p")
    usr_input = request.GET.get('usr_input')
    print(usr_input)
    messages.append(usr_input)
    replay=""
    try:
        replay = gpt(usr_input)
        messages.append(replay)
    except:
        replay=None
    print(replay)
    if(replay == None):
        if usr_input != None :
            replay = gpt(usr_input)
        elif(usr_input == None) :
            replay = ""
        messages.append(replay)
    makefullcode = ""
    for i,x in enumerate(messages):
        if(i != 0 and i != 1):
            if(i%2 == 0):
                user = f"""<div id="messages" class="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch">
                                <div class="chat-message">
                                    <div class="flex items-end">
                                        <div class="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-2 items-start">
                                            <div><span class="px-4 py-2 rounded-lg inline-block rounded-bl-none bg-gray-300 text-gray-600">{x}</span></div>
                                        </div>
                                        <img src="https://images.unsplash.com/photo-1549078642-b2ba4bda0cdb?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=3&amp;w=144&amp;h=144" alt="My profile" class="w-6 h-6 rounded-full order-1">
                                    </div>
                            </div>
                
                """
                makefullcode = makefullcode + user 
            else:
                system_ = f"""<div class="chat-message">
                                    <div class="flex items-end justify-end">
                                        <div class="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-1 items-end">
                                            <div><span class="px-4 py-2 rounded-lg inline-block rounded-br-none bg-blue-600 text-white ">{x}</span></div>
                                        </div>
                                        <img src="https://images.unsplash.com/photo-1590031905470-a1a1feacbb0b?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=3&amp;w=144&amp;h=144" alt="My profile" class="w-6 h-6 rounded-full order-2">
                                    </div>
                                </div>                
                """
                makefullcode = makefullcode + system_ 
    frontend = {"codes":makefullcode}

    return render(request,'chatbot/chatbot.html',frontend)
    


# ....... room chating
