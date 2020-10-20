from django.shortcuts import render, redirect
from .models import poems, suggestions, regular_user, admin_user, categories


# Create your views here.

def home_page_index(request):
    return render(request, "blog/home_page/index.html", {"categories": categories})


def posts_list(request):
    return render(request, "blog/posts/list.html", {"poems": poems})


def login_page(request):
    return render(request, "blog/login/login_page.html")


def details(request, poem_id):
    poem_suggestions = []
    for poem in poems:
        if poem.id == poem_id:
            for suggestion in suggestions:
                if suggestion.poem_id == poem.id:
                    poem_suggestions.append(suggestion)
            return render(request, "blog/details/details.html", {"poem": poem, "suggestions": poem_suggestions})


def details2(request, poem_id):
    poem_suggestions = []
    for poem in poems:
        if poem.id == poem_id:
            for suggestion in suggestions:
                if suggestion.poem_id == poem.id:
                    poem_suggestions.append(suggestion)
            return render(request, "blog/details/details2.html", {"poem": poem, "suggestions": poem_suggestions})


def new_post(request):
    return render(request, "blog/new_post/new_post.html")


def search_results(request):
    return render(request, "blog/search/search_results.html")


def login(request):
    username = request.POST.get('uname')
    password = request.POST.get('psw')
    if username == regular_user['username'] and password == regular_user['password']:
        request.session['username'] = username
        request.session['role'] = 'regular'
        return redirect('blog:home_page_index')
    elif username == admin_user['username'] and password == admin_user['password']:
        request.session['username'] = username
        request.session['role'] = 'admin'
        return redirect('blog:home_page_index')
    else:
        return redirect('blog:login_page')
