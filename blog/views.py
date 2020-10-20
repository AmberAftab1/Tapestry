from django.shortcuts import render, redirect
from .models import poems, suggestions, regular_user, admin_user, categories, sorted_categories


# Create your views here.

def home_page_index(request):  # home page view
    print(request)
    print(request.POST.get("drop_categories"))
    print(request.POST.get("title"))
    print(request.POST.get("text"))
    print(request.POST.get("save"))
    return render(request, "blog/home_page/index.html", {"categories": sorted_categories})

def posts_list(request, category): #list view
    if category in categories:
        return render(request, "blog/posts/list.html", {"poems": poems, "category": category})
    else:
        return redirect('blog:home_page_index')



def login_page(request):  # login page view
    return render(request, "blog/login/login_page.html")


def details(request, poem_id, category): #details view page
    poem_suggestions = []
    for poem in poems:
        if poem.id == poem_id:
            for suggestion in suggestions:
                if suggestion.poem_id == poem.id:
                    poem_suggestions.append(suggestion)
            return render(request, "blog/details/details.html", {"poem": poem, "suggestions": poem_suggestions, "category": category})


def details2(request, poem_id, category):  # modified details page view
    poem_suggestions = []
    for poem in poems:
        if poem.id == poem_id:
            for suggestion in suggestions:
                if suggestion.poem_id == poem.id:
                    poem_suggestions.append(suggestion)
            return render(request, "blog/details/details2.html", {"poem": poem, "suggestions": poem_suggestions, "category": category})


def new_post(request):  # new post page view
    if "username" in request.session:
        return render(request, "blog/new_post/new_post.html", {"categories": sorted_categories})
    else:
        return redirect('blog:home_page_index')

def search_results(request):  # search results view
    return render(request, "blog/search/search_results.html")


def login(request):  # login view
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


def logout(request):  # logout view
    del request.session['username']
    del request.session['role']
    return redirect('blog:login_page')

# TODO: fix new post css, align login properly,