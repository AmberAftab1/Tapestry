from django.shortcuts import render, redirect
from django.contrib import messages
from .models import regular_user, admin_user, Poem, Category, Suggestion
from django.http import JsonResponse


# Create your views here.

def home_page_index(request):  # home page view
    sorted_categories = Category.objects.all()
    return render(request, "blog/home_page/index.html", {"categories": sorted_categories})


def posts_list(request, category, sort_param="date"):  # list view

    if request.method == 'POST':
        if 'delete-poem' in request.POST.keys():  # check if delete-poem form has been submitted
            poem_id = request.POST.get('delete-poem')
            to_delete = Poem.objects.get(id=poem_id)
            name = to_delete.title
            to_delete.delete()

            # warning message that poem has been deleted
            messages.add_message(request, messages.WARNING, "Poem has been deleted: %s" % name)
            return redirect('blog:post_list', category)

    categories = Category.objects.all()
    category_names = []
    for obj in categories:
        category_names.append(obj.name)
    if category in category_names:
        poems = Poem.objects.filter(category_id=category).order_by("-" + sort_param)
        if not poems:
            messages.add_message(request, messages.ERROR, "There are no posts yet for the category: %s" % category)
        return render(request, "blog/posts/list.html", {"poems": poems, "category": category})
    else:
        return redirect('blog:home_page_index')


def login_page(request):  # login page view
    return render(request, "blog/login/login_page.html")


def details(request, poem_id, category):  # details view page
    poem = Poem.objects.get(id=poem_id)
    poem_suggestions = Suggestion.objects.filter(poem_id=poem_id)
    return render(request, "blog/details/details.html",
                  {"poem": poem, "suggestions": poem_suggestions, "category": category})


def details2(request, poem_id, category):  # modified details page view
    poem = Poem.objects.get(id=poem_id)
    poem_suggestions = Suggestion.objects.filter(poem_id=poem_id)
    return render(request, "blog/details/details2.html",
                  {"poem": poem, "suggestions": poem_suggestions, "category": category})


def new_post(request):  # new post page view
    sorted_categories = Category.objects.all()
    if "username" in request.session:  # checks if user is logged in

        if request.method == 'POST':  # process the form
            title = request.POST.get('title')
            description = request.POST.get('text')
            category = request.POST.get('drop_categories')

            # creating an object of class poem to add to database
            new_poem = Poem(
                title=title,
                description=description,
                category_id=category,
                author=request.session.get('username'),
            )
            new_poem.save()  # saves new poem to database

            # success message for new post
            messages.add_message(request, messages.SUCCESS, "New post has been created: %s" % new_poem.title)

            # returns detail view of added item
            return redirect('blog:details', category, new_poem.id)

        else:  # show the form
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


def poems_vote(request, category):  # view for upvoting/downvoting poems
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        poem_id = request.POST.get('poem_id')
        action = request.POST.get('action')
        try:
            poem = Poem.objects.get(pk=poem_id)
            if action == 'upvote':
                poem.score += 1
            elif action == 'downvote':
                poem.score -= 1
            poem.save()
            return JsonResponse({'success': 'success', 'score': poem.score}, status=200)
        except Poem.DoesNotExist:
            return JsonResponse({'error': 'No poem found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax  request.'}, status=400)


def suggestions_vote(request, category, poem_id):  # view for upvoting/downvoting suggestions
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        suggestion_id = request.POST.get('suggestion_id')
        action = request.POST.get('action')
        try:
            # poem = Poem.objects.get(pk=poem_id)
            suggestion = Suggestion.objects.get(pk=suggestion_id)
            if action == 'upvote':
                suggestion.score += 1
            elif action == 'downvote':
                suggestion.score -= 1
            suggestion.save()
            return JsonResponse({'success': 'success', 'score': suggestion.score}, status=200)
        except Poem.DoesNotExist:
            return JsonResponse({'error': 'No poem found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax  request.'}, status=400)


def add_suggestion(request):  # view to handle user adding suggestions
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        poem_id = request.POST.get('poem_id')
        suggestion = request.POST.get('suggestion')
        try:
            poem = Poem.objects.get(pk=poem_id)
            toAdd = Suggestion(
                line=suggestion,
                poem_id=poem,
            )
            toAdd.save()
            return JsonResponse({'success': 'success', 'suggestion': toAdd.line}, status=200)
        except Poem.DoesNotExist:
            return JsonResponse({'error': 'No poem found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax  request.'}, status=400)


def edit_edit(request, category, poem_id):  # view for edit post
    sorted_categories = Category.objects.all()
    edited_poem = Poem.objects.get(pk=poem_id)
    if "username" in request.session:  # checks if user is logged in
        if request.method == 'POST':  # process the form
            title = request.POST.get('title')
            description = request.POST.get('text')
            category = request.POST.get('drop_categories')
            edited_poem.title = title
            edited_poem.description = description
            edited_poem.category_id = category
            edited_poem.score = 0
            author = request.session.get('username')

            edited_poem.save()  # saves new poem to database

            # success message for new post
            messages.add_message(request, messages.INFO, "Post has been edited: %s" % edited_poem.title)

            # returns detail view of added item
            return redirect('blog:details', category, edited_poem.id)

        else:  # show the form
            return render(request, "blog/edit/edit.html",
                          {"poem": edited_poem, "categories": sorted_categories, "category": category})
    else:
        return redirect('blog:home_page_index')


# shows details of poem if one hovers over it
def show_poem(request, category):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        poem_id = request.POST.get('poem_id')
        try:
            poem = Poem.objects.get(pk=poem_id)
            details = poem.description
            return JsonResponse({'success': 'success', 'details': details}, status=200)
        except Poem.DoesNotExist:
            return JsonResponse({'error': 'No poem found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax  request.'}, status=400)

# TODO: sort drop down menu in list view, edit view and message, new post and top post templates and views, vote for detail view
