import json

from django.http import HttpResponse

from .. import models

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
        user_id = request.GET.get("user_id")
        question_id_list = request.GET.getlist("question_id_list[]",[])
        user = models.User.objects.filter(id = user_id).first()

        ret_dict = {}
        ret_dict["msg"] = "success"

        if(not user.user_type == "administrator"):
            ret_dict["msg"] = "power limit"

        question_list = models.Question.objects.filter(id__in = question_id_list)
        for question in question_list:
            question.is_star = "True"
            question.save()
    else:
        ret_dict = {}
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")