"""
URL configuration for fedor_recipe_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from recipe_book.views import index, \
                              recipe, \
                              contacts, \
                              add_recipe_v2, \
                              recipe_search, \
                              recipe_categories


handler400 = 'recipe_book.views.my_custom_view_for_400'
handler403 = 'recipe_book.views.my_custom_view_for_403'
handler404 = 'recipe_book.views.my_custom_view_for_404'
handler500 = 'recipe_book.views.my_custom_view_for_500'


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('recipe/<int:id_recipe>', recipe, name='recipe'),

    path('recipe_categories/<int:id_recipe_categories>',
         recipe_categories, name='recipe_categories'),
    path('recipe_categories/page/<int:id_recipe_categories>/<int:page_number>/',
         recipe_categories, name='recipe_categories__page_number'),

    path("recipe_search/", recipe_search, name='recipe_search'),
    path('recipe_search/page/<str:search_query_from_page_number>/<int:page_number>/',
         recipe_search, name='recipe_search__page_number'),

    path('users/', include('users.urls', namespace='users')),

    path('add_recipe_v2/', add_recipe_v2, name='add_recipe_v2'),
    #path('__debug__/', include("debug_toolbar.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)