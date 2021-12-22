"""proj URL Configuration

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
from django.urls import path
from .views import (admin_views, question_views, reply_views, user_views)

urlpatterns = [
    path("register_pre_check/", user_views.register_pre_check_view),
    path("register/", user_views.register_view),
    path("login/", user_views.login_view),
    path("upload_icon/", user_views.upload_icon_view),
    path("delete_user/", user_views.delete_user_view),
    path("question/", question_views.question_view),
    path("question_list/", question_views.question_list_view),
    path("update_question_state/", question_views.update_question_view),
    path("delete_question/", question_views.delete_question_view),
    path("reply/", reply_views.reply_view),
    path("add_star/", admin_views.add_star_view),
    path("modify_info/", user_views.modify_info_view),
    path("get_info/", user_views.get_info_view),
]