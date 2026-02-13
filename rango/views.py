
from rango.models import Category, Page
from django.shortcuts import render, redirect
from rango.forms import CategoryForm, PageForm

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.forms import UserForm, UserProfileForm
from django.http import HttpResponse

from datetime import datetime




from datetime import datetime
from django.shortcuts import render

from datetime import datetime
from django.shortcuts import render
from rango.models import Category, Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {
        'categories': category_list,
        'pages': page_list,
    }

    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    visitor_cookie_handler(request)
    visits = request.session.get('visits', 1)

    context_dict = {'visits': visits}
    response = render(request, 'rango/about.html', context=context_dict)
    return response


def visitor_cookie_handler(request):
    
    visits = int(request.session.get('visits', 1))
    last_visit_str = request.session.get('last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_str[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_str

    request.session['visits'] = visits



def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect('/rango/')  

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect('/rango/category/' + category_name_slug + '/')

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})



def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
              'rango/register.html',
              context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return render(request, 'rango/login.html', {'error': 'Your account is disabled.'})
        else:
            return render(request, 'rango/login.html', {'error': 'Invalid login details supplied.'})

    return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
