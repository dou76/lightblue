import json

from django.http import HttpResponse

from . import util
from .. import models

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
        _type = request_dict.get("type")
        poster_id = request_dict.get("poster_id")
        poster = models.User.objects.filter(id = poster_id).first()
        question_id = request_dict.get("question_id")
        question = models.Question.objects.filter(id = question_id).first()

        if(_type == "text"):
            content = request_dict.get("content")
            new_reply = models.Reply.objects.create(type = _type, content = content)
        else:
            image = request_dict.get("image")
            new_reply = models.Reply.objects.create(type = _type, image = image)

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