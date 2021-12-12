import json
import datetime

from django.http import HttpResponse
from django.forms.models import model_to_dict

from . import util
from .. import models

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
        question_id = request.GET.get("id")
        reply_list = models.Reply.objects.filter(question_id = question_id).order_by("id")

        ret_dict = {}
        ret_dict["msg"] = "success"
        ret_dict["reply_list"] = [model_to_dict(reply) for reply in reply_list]
        ans = json.dumps(ret_dict)
        return HttpResponse(ans, content_type = "application/json")

    else:
        return HttpResponse(json.dumps({"msg":"method error"}), content_type = "application/json")

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
        request.question_type: 筛选问题的类别
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
        type = request.GET.get("type")
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