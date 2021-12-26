import json
import datetime

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.db.models import Q
from ..checkers import util
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
            2. illegal type: 类型不合规范
            3. illegal title: 标题不合规范
            4. illegal abstract: 摘要不合规范

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
        reply.poster_name: 回复者姓名
        reply.poster_school: 回复者学校
        reply.poster_type: 回复者类型
    """

    if request.method == "POST":
        request_dict = json.loads(request.body)
        ret_dict = {}
        ret_dict["msg"] = util.check_question_info(request_dict)

        if(ret_dict["msg"] == "success"):
            _type = request_dict.get("type")
            title = request_dict.get("title")
            abstract = request_dict.get("abstract")
            state = "待解决"

            questioner_id = request_dict.get("questioner_id")
            questioner = models.User.objects.filter(id = questioner_id).first()
            new_question = models.Question.objects.create(type = _type, title = title, abstract = abstract,
                state = state)
            new_question.questioner_id = questioner
            new_question.save()
            ret_dict["id"] = new_question.id

        ans = json.dumps(ret_dict)
        return HttpResponse(ans, content_type = "application/json")

    elif request.method == "GET":
        question_id = request.GET.get("id")
        reply_list = models.Reply.objects.filter(question_id = question_id).order_by("id")

        ret_dict = {}
        ret_dict["msg"] = "success"
        reply_dict_list = []
        for reply in reply_list:
            reply_dict = model_to_dict(reply)
            reply_dict["reply_time"] = reply.reply_time.strftime('%Y-%m-%d %H:%M')
            user = models.User.objects.filter(id = reply_dict["poster_id"]).first()
            reply_dict["poster_name"] = user.name
            reply_dict["poster_school"] = user.school
            reply_dict["poster_type"] = user.user_type
            reply_dict_list.append(reply_dict)
            
        ret_dict["reply_list"] = reply_dict_list
        ans = json.dumps(ret_dict)
        return HttpResponse(ans, content_type = "application/json")

    else:
        return HttpResponse(json.dumps({"msg":"method error"}), content_type = "application/json")

# 获取问题列表
def question_list_view(request):
    """ 
        接受参数：request
        request.type_list: 筛选问题的条件列表
        可加入元素有：
            1. student：        学生id
            2. teacher：        教师id
            3. question_type：  问题类型
            4. date：           起止日期
            5. is_star：         是否加精
            ...
        request.student_id_list:    查看的学生id列表
        request.teacher_id_list:    查看的教师id列表
        request.question_type_list: 问题类别列表
        request.start_date:(xxxx(y)-xx(m)-xx(d)): 查询起始时间
        request.end_date:(xxxx(y)-xx(m)-xx(d)): 查询截止时间
        request.is_star:    是否只查看加精
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. method error: 请求类型错误
            3. type error: 没有传入筛选类型
        
        ans.question_list: 问题列表

        question: 单条问题
        question.id: 问题id(数据库中主键)
        question.type: 问题类型
        question.title: 问题名称
        question.abstract: 问题摘要          
        question.questioner_id: 提问者id
        question.answerer_id: 回复者id
        question.question_time: 提问时间
    """
    ret_dict = {}
    if request.method == "GET":
        ret_dict["msg"] = "success"
        type_list = request.GET.getlist("type_list[]",[])
        if(len(type_list) == 0):
            ret_dict["msg"] = "type error"

        all_condition = Q()

        if("student" in type_list):
            query_student = Q()
            student_id_list = request.GET.getlist("student_id_list[]",[])
            query_student.connector = "OR"
            for student_id in student_id_list:
                query_student.children.append(("questioner_id", student_id))
            all_condition.add(query_student, "AND")

        if("teacher" in type_list):
            query_teacher = Q()
            teacher_id_list = request.GET.getlist("teacher_id_list[]",[])
            query_teacher.connector = "OR"
            for teacher_id in teacher_id_list:
                query_teacher.children.append(("answerer_id", teacher_id))
            all_condition.add(query_teacher, "AND")

        if("question_type" in type_list):
            query_teacher = Q()
            question_type_list = request.GET.getlist("question_type_list[]",[])
            query_teacher.connector = "OR"
            for question_type in question_type_list:
                query_teacher.children.append(("type", question_type))
            all_condition.add(query_teacher, "AND")
        
        question_list = models.Question.objects.filter(all_condition)

        if("date" in type_list):
            start_year, start_month, start_day = util.parse_date(request.GET.get("start_date"))
            end_year, end_month, end_day = util.parse_date(request.GET.get("end_date"))
            start_time = datetime.datetime(year = start_year, month = start_month, day = start_day,
                hour = 0, minute = 0, second = 0)
            end_time = datetime.datetime(year = end_year, month = end_month, day = end_day,
                hour = 23, minute = 59, second = 59)
            question_list = question_list.filter(question_time__range = (start_time, end_time))

        if("is_star" in type_list):
            if(request.GET.get("is_star") == "True"):
                question_list = question_list.filter(is_star = True).order_by("-id")

        question_dict_list = []
        for question in question_list:
            question_dict = model_to_dict(question)
            question_dict["question_time"] = question.question_time.strftime('%Y-%m-%d')
            question_dict_list.append(question_dict)
            
        ret_dict["question_list"] = question_dict_list
    else:
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

        学生会结单；教师会将问题改为解答中
    """

    if request.method == "GET":
        _type = request.GET.get("type")
        id = request.GET.get("id")
        question_id = request.GET.get("question_id")
        question = models.Question.objects.filter(id = question_id).first()
        user = models.User.objects.filter(id = id).first()

        ret_dict = {}
        ret_dict["msg"] = "success"

        if _type == "teacher":
            question.answerer_id = user
            question.state = "解决中"
            question.save()
        elif _type == "student":
            question.state = "已解决"
            question.save()
        else:
            ret_dict["msg"] = "type error"
    
    else:
        ret_dict = {}
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 删除问题
def delete_question_view(request):
    """ 
        接受参数：request
        request.question_id_list: 问题id列表
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. method error: 请求类型错误
            3. not found: 查找问题失败
    """
    ret_dict = {}
    if request.method == "GET":
        ret_dict["msg"] = "success"
        question_id_list = request.GET.getlist("question_id_list[]",[])
        for question_id in question_id_list:
            question = models.Question.objects.filter(id = question_id)
            if(not question.exists()):
                ret_dict["msg"] = "not found"
                break
            else:
                question = question.first()
                question.delete()
    else:
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")