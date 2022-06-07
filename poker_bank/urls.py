"""poker_bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from pages.views import about_view
from bankroll.views import (
                DataInputView,
                DataUpdateView,
                DataDetailView,
                DataDeleteView,
                home_view,
                sample_home_view,
                filter_view,
                filtered_home_view,
                    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('sample', sample_home_view, name='sample-data-list'),
    path('', home_view, name='data-list'),
    path('filter', filter_view, name='data-filter'),
    path('filtered', filtered_home_view, name='filtered-data'),
    path('input/', DataInputView.as_view(), name='data-input'),
    path('<int:pk>/', DataDetailView.as_view(), name='data-detail'),
    path('<int:pk>/delete/', DataDeleteView.as_view(), name='data-delete'),
    path('<int:pk>/update/', DataUpdateView.as_view(), name='data-update'),
    path('about/', about_view),
]


