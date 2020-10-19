from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [

    # home_page views
    path('', views.home_page_index, name='home_page_index'),

    # posts views
    path('posts', views.posts_list, name='post_list'),

    # login page view
    path('login', views.login_page, name='login_page'),

    # details page views
    path('posts/<int:poem_id>', views.details, name="details"),
    path('posts/<int:poem_id>/add-suggestion', views.details2, name="details2"),

    # path('details.html', views.details),

    # new post view
    path('new-post', views.new_post, name="new_post"),

    # search page view
    path('search-results', views.search_results, name="search_results")
]
# TODO: fix category issue in URL