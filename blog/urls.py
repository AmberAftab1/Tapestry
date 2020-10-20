from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [

    # home_page views
    path('', views.home_page_index, name='home_page_index'),

    # login page views
    path('login-page', views.login_page, name='login_page'),
    path('login', views.login, name = 'login'),

    #log out page views
    path('logout', views.logout, name = 'logout'),

    # new post view
    path('new-post', views.new_post, name="new_post"),

    # search page view
    path('search-results', views.search_results, name="search_results"),

    # posts views
    path('<str:category>', views.posts_list, name='post_list'),
    # details page views
    path('<str:category>/<int:poem_id>', views.details, name="details"),
    path('<str:category>/<int:poem_id>/add-suggestion', views.details2, name="details2")
]
