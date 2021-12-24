from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from datetime import datetime

class User(AbstractUser):
    name = models.CharField("姓名", max_length = 20, default = "")
    user_type = models.CharField("用户类型", max_length = 12, default="")
    school = models.CharField("学校", max_length=15, default="")
    img_url = models.CharField("头像地址", max_length=100, default = "")
    _class = models.CharField("班级", max_length=10, default="")
    register_time = models.DateField("注册时间", auto_now_add = True)
    force_logout_date = models.DateTimeField(null = True, blank = True)

    def force_logout(self):
        self.force_logout_date = datetime.now()
        self.save()

class Authentication(models.Model):
    authentication = models.CharField("校验码",max_length = 50, default="")

class Question(models.Model):
    type = models.CharField("问题类型", max_length = 20, default = "")
    title = models.CharField("问题名称", max_length = 30, default = "")
    abstract = models.CharField("问题摘要", max_length = 200, default = "")
    state = models.CharField("问题状态", max_length = 10, default = "unsolved")
    questioner_id = models.ForeignKey("User", db_column='questioner_id',
        related_name = "questioner_id", on_delete = models.SET_DEFAULT, default = 1)
    answerer_id = models.ForeignKey("User", db_column='answerer_id',
        related_name = "answerer_id", on_delete = models.SET_DEFAULT, default = 1)
    question_time = models.DateTimeField("提问时间", auto_now_add = True)
    is_star = models.BooleanField("是否加精", default = False)

class Reply(models.Model):
    type = models.CharField("回复类型", max_length = 10, default = "")
    content = models.CharField("回复内容", max_length = 200, default = "")
    poster_id = models.ForeignKey("User", db_column='poster_id', on_delete = models.SET_DEFAULT, default = 1)
    question_id = models.ForeignKey("Question", db_column='question_id', on_delete = models.CASCADE, default = 1)
    reply_time = models.DateTimeField("回复时间",auto_now_add = True)

class Picture_Relation(models.Model):
    url = models.ImageField("图片地址", default = "")
    reply_id = models.ForeignKey("Reply", db_column="reply_id",
        related_name = "reply_id", on_delete = models.CASCADE, default = 1)

def update_session_last_login(sender, user, request, **kwargs):
    if request:
        request.session['LAST_LOGIN_DATE'] = datetime.now()

user_logged_in.connect(update_session_last_login)