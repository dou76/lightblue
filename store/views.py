from django.http import HttpResponse
from django.forms.models import model_to_dict

import json
import datetime
from . import util
from . import models

# 检查用户名和密码
def register_pre_check_view(request):
    """
        接受参数：request
        request.username: 用户名
        request.password: 密码        
        
        返回参数: ans
        ans.msg：消息
            1. method error: 表单提交类型错误
            3. illegal user: 非法用户名
            3. multiple user: 用户名重复
            4. password error: 密码不符合规范
            5. success: 成功
    """
    ret_dict = {"msg": "success"}

    if request.method == "POST":
        request_dict = json.loads(request.body)
        username = request_dict.get("username")
        password = request_dict.get("password")

        if(not util.check_legal_username(username)):
            ret_dict["msg"] = "illegal user"
        elif(not util.check_multiple_username(username)):
            ret_dict["msg"] = "multiple user"
        elif(not util.check_password(password)):
            ret_dict["msg"] = "password error"

    else:
        ret_dict["msg"] = "method error"
    ans = json.dumps(ret_dict)
    print(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 用户注册
def register_view(request):
    """
        接受参数：request
        request.username: 用户名
        request.password: 密码
        request.code: 校验码
        request.type: 用户类型
        request.name: 姓名
        request.school: 学校
        request.class: 班级
        
        返回参数: ans
        ans.msg：消息
            1. method error: 表单提交类型错误
            2. code error: 校验码错误
            3. illegal user: 非法用户名
            3. multiple user: 用户名重复
            4. password error: 密码不符合规范
            5. success: 成功

        ans.id: 用户id(数据库中主键)
    """

    ret_dict = {"msg": "success"}

    if request.method == "POST":
        request_dict = json.loads(request.body)
        code = request_dict.get("code")
        username = request_dict.get("username")
        password = request_dict.get("password")
        name = request_dict.get("name")
        school = request_dict.get("school")
        _class = request_dict.get("class")
        type = request_dict.get("type")

        if(not util.check_code(code)):
            ret_dict["msg"] = "code error"
        elif(not util.check_legal_username(username)):
            ret_dict["msg"] = "illegal user"
        elif(not util.check_multiple_username(username)):
            ret_dict["msg"] = "multiple user"
        elif(not util.check_password(password)):
            ret_dict["msg"] = "password error"
        else:
            new_user = models.User.objects.create(username = username, password = password, name = name,
                school = school, _class = _class, user_type = type)
            new_user.save()
            ret_dict["id"] = new_user.id
    else:
        ret_dict["msg"] = "method error"
    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")
    
# 用户登录
def login_view(request):
    """
        接受参数：request
        request.username: 用户名
        request.password: 密码
        
        返回参数: ans
        ans.msg：消息
            1. method error: 表单提交类型错误;
            2. not found: 用户名错误;
            3. error: 密码错误;
            4. success: 成功
        ans.id: 用户id(数据库中主键)
        ans.type: 用户类型(student, teacher, admin)
    """
    if request.method == "POST":
        request_dict = json.loads(request.body)
        username = request_dict.get("username")
        password = request_dict.get("password")
        ans = util.login_check(username, password)
    else:
        ans = json.dumps({"msg": "method error"})
    return HttpResponse(ans, content_type = "application/json")

# 创建问题(post) / 获取问题信息(get)
def question_view(request):
    """
    POST:
        接受参数：request
        request.type: 问题类型
        request.title: 问题名称
        request.abstract: 问题摘要
        request.questioner_id:提问者id
        返回参数: ans
        ans.msg：消息
            1. success: 成功

        ans.id: 问题id(数据库中主键)
        
    GET:
        接受参数：request
        request.id: 问题id(数据库中主键)
        返回参数: ans
        ans.msg：消息
            1. success: 成功

        ans.reply_list: 历史记录列表
        
        reply: 单条回复
        reply.id: 回复id(数据库中主键)
        reply.type: 回复类型
        reply.content: 回复内容
        reply.image: 回复图片           ##尚未实现##
        reply.poster_id: 回复者的id
        reply.reply_time: 回复时间
    """

    if request.method == "POST":
        request_dict = json.loads(request.body)
        type = request_dict.get("type")
        title = request_dict.get("title")
        abstract = request_dict.get("abstract")
        state = "待解决"

        questioner_id = request_dict.get("questioner_id")
        questioner = models.User.objects.filter(id = questioner_id).first()
        new_question = models.Question.objects.create(type = type, title = title, abstract = abstract,
            state = state)
        new_question.questioner = questioner
        new_question.save()
        
        ret_dict = {}
        ret_dict["msg"] = "success"
        ret_dict["id"] = new_question.id

        ans = json.dumps(ret_dict)
        return HttpResponse(ans, content_type = "application/json")

    elif request.method == "GET":
        request_dict = json.loads(request.body)
        question_id = request_dict.get("id")
        reply_list = models.Reply.objects.filter(question_id = question_id).order_by("id")

        ret_dict = {}
        ret_dict["msg"] = "success"
        ret_dict["reply_list"] = [model_to_dict(reply) for reply in reply_list]
        ans = json.dumps(ret_dict)
        return HttpResponse(ans, content_type = "application/json")

    else:
        return HttpResponse(json.dumps({"msg":"method error"}), content_type = "application/json")

# 创建回复条
def reply_view(request):
    """ 
        接受参数：request
        request.type: 回复类型
        request.content: 回复内容
        request.image: 回复图片           ##尚未实现##
        request.poster_id: 回复者的id
        request.question_id: 问题的id
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. method error: 请求类型错误
        ans.id: 回复id(数据库中主键)
    """

    if request.method == "POST":
        request_dict = json.loads(request.body)
        type = request_dict.get("type")
        poster_id = request_dict.get("poster_id")
        poster = models.User.objects.filter(id = poster_id).first()
        question_id = request_dict.get("question_id")
        question = models.Question.objects.filter(id = question_id).first()

        if(type == "text"):
            content = request_dict.get("content")
            new_reply = models.Reply.objects.create(type = type, content = content)
        else:
            image = request_dict.get("image")
            new_reply = models.Reply.objects.create(type = type, image = image)

        new_reply.poster_id = poster
        new_reply.question_id = question
        new_reply.save()

        ret_dict = {}
        ret_dict["msg"] = "success"
        ret_dict["id"] = new_reply.id

    else:
        ret_dict = {}
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 获取问题列表
def question_list_view(request):
    """ 
        接受参数：request
        request.type: 查询问题方式
            1. student
            2. teacher
            3. question_type
            4. date
            ...
        request.id: 对应查询对象的id(如果是查询老师/学生的问题)
        request.quetion_type: 筛选问题的类别
        request.start_date:(xxxx(y)-xx(m)-xx(d)): 查询起始时间
        request.end_date:(xxxx(y)-xx(m)-xx(d)): 查询截止时间
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. method error: 请求类型错误
        
        ans.question_list: 问题列表

        question: 单条问题
        question.id: 问题id(数据库中主键)
        question.type: 问题类型
        question.title: 问题名称
        question.abstract: 问题摘要          
        question.questioner_id: 提问者id
        question.answerer_id: 回复者id
        question.question_time: 回复者id
    """
    if request.method == "GET":
        question_list = []
        if(type == "type"):
            question_type = request.GET.get("question_type")
            question_list = models.Question.objects.filter(type = question_type, state = "unsolved").order_by("-id")
        elif(type == "student"):
            questioner_id = request.GET.get("id")
            question_list = models.Question.objects.filter(questioner_id = questioner_id).order_by("-id")
        elif(type == "teacher"):
            answerer_id = request.GET.get("id")
            question_list = models.Question.objects.filter(answerer_id = answerer_id).order_by("-id")
        elif(type == "date"):
            start_year, start_month, start_day = util.parse_date(request.GET.get("start_date"))
            end_year, end_month, end_day = util.parse_date(request.GET.get("end_date"))
            start_time = datetime.datetime(year = start_year, month = start_month, day = start_day,
                hour = 0, minute = 0, second = 0)
            end_time = datetime.datetime(year = end_year, month = end_month, day = end_day,
                hour = 23, minute = 59, second = 59)
            question_list = models.Question.objects.filter(question_time__range = (start_time, end_time)).order_by("id")

        ret_dict = {}
        ret_dict["msg"] = "success"
        ret_dict["question_list"] = [model_to_dict(question) for question in question_list]
    else:
        ret_dict = {}
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 更新问题状态
def update_question_view(request):
    """ 
        接受参数：request
        request.type: 更新状态的人
            1. student
            2. teacher
        request.id: 对应对象的id
        request.question_id: 问题的id
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. method error: 请求类型错误
            3. type error

        ans.question_list: 问题列表

        学生会结单；教师会将问题改为解答中
    """

    if request.method == "GET":
        request_dict = json.loads(request.body)
        type = request_dict.get("type")
        id = request_dict.get("id")
        question_id = request_dict.get("question_id")
        question = models.Question.objects.filter(id = question_id).first()
        user = models.User.objects.filter(id = id).first()

        ret_dict = {}
        ret_dict["msg"] = "success"

        if type == "teacher":
            question.answerer_id = user
            question.state = "solving"
            question.save()
        elif type == "student":
            question.state = "closed"
            question.save()
        else:
            ret_dict["msg"] = "type error"
    
    else:
        ret_dict = {}
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 管理员加精
def add_star_view(request):
    """ 
        接受参数：request
        request.user_id: 加精管理员id
        request.question_id_list: 待加精问题列表
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. method error: 请求类型错误
            3. power limit: 无权限加精
    """

    if request.method == "GET":
        request_dict = json.loads(request.body)
        type = request_dict.get("type")
        user_id = request_dict.get("user_id")
        question_id_list = request_dict.get("question_id_list")
        user = models.User.objects.filter(id = user_id).first()

        ret_dict = {}
        ret_dict["msg"] = "success"

        if(not user.type == "admin"):
            ret_dict["msg"] = "power limit"

        question_list = models.Question.objects.filter(id__in = question_id_list)
        for question in question_list:
            question.is_star = True
            question.save()
    else:
        ret_dict = {}
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

def modify_info_view(request):
    """ 
        接受参数：request
        request.user_id: 加精管理员id
        request.question_id_list: 待加精问题列表
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. method error: 请求类型错误
            3. power limit: 无权限加精
    """

    