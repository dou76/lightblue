import json

from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from . import util
from .. import models

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
        _type = request_dict.get("type")

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
                school = school, _class = _class, user_type = _type)
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

# 获取信息 
def get_info_view(request):
    """
        接受参数：request
        request.id: 用户id
        
        返回参数: ans
        ans.msg：消息
            1. method error: 表单提交类型错误;
            2. not found: 查找失败;
            3. success: 成功
        ans.username: 用户名
        ans.name: 姓名
        ans.school: 学校
        ans.class: 班级
        ans.img_url: 头像地址
        ans.register_time: 注册日期
    """
    ret_dict = {"msg": "success"}

    if request.method == "GET":
        id = request.GET.get("id")
        user = models.User.objects.filter(id = id)

        if(not user.exists()):
            ret_dict["msg"] = "not found"

        else:
            user = user.first()
            ret_dict["username"] = user.username
            ret_dict["name"] = user.name
            ret_dict["school"] = user.school
            ret_dict["class"] = user._class
            ret_dict["img_url"] = user.img_url
            ret_dict["register_time"] =user.register_time.strftime('%Y-%m-%d')

    else:
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 修改信息
def modify_info_view(request):
    """
        接受参数：request
        request.id: 用户id
        request.username: 用户名
        request.name: 姓名
        request.school: 学校
        request.class: 班级
        
        返回参数: ans
        ans.msg：消息
            1. method error: 表单提交类型错误;
            2. not found: 查找用户失败
            3. multiple user: 用户名重复;
            3. illegal user: 非法用户名;
            5. password error: 密码不合规范;
            6. success: 成功
    """
    ret_dict = {"msg": "success"}

    if request.method == "POST":
        request_dict = json.loads(request.body)
        id = request_dict.get("id")
        username = request_dict.get("username")
        name = request_dict.get("name")
        school = request_dict.get("school")
        _class = request_dict.get("class")

        user = models.User.objects.filter(id = id)
        if(not user.exists()):
            ret_dict["msg"] = "not found"
        else:
            user = user.first()
            if(not util.check_multiple_username(username) and not user.id == id):
                ret_dict['msg'] = "multiple user"
            elif(not util.check_legal_username(username)):
                ret_dict['msg'] = "illegal user"
            else:
                user.username = username
                user.name = name
                user.school = school
                user._class = _class
                user.save()
    else:
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 修改密码
def change_password(request):
    """
        接受参数：request
        request.id: 用户id
        request.old_password: 旧密码
        request.new_password: 新密码

        返回参数: ans
        ans.msg：消息
            1. method error: 表单提交类型错误;
            2. not found: 查找用户失败
            3. wrong password: 旧密码错误
            5. illegal password: 新密码不合规范
            6. success: 成功
    """

    ret_dict = {"msg": "success"}
    if request.method == "POST":
        request_dict = json.loads(request.body)
        id = request_dict.get("id")
        old_password = request_dict.get("old_password")
        new_password = request_dict.get("new_password")

        user = models.User.objects.filter(id = id)
        if(not user.exists()):
            ret_dict["msg"] = "not found"
        else:
            user = user.first()
            if(not old_password == user.password):
                ret_dict['msg'] = "wrong password"
            elif(not util.check_password(new_password)):
                ret_dict['msg'] = "illegal password"
            else:
                user.password = new_password
                user.save()
    else:
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 上传头像
def upload_icon_view(request):
    """
    POST:
        接受参数：request
        request.id: 用户id
        request.img: 图片
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. not found: 查找用户失败
        ans.img_url: 图片路由
    """

    ret_dict = {"msg": "success"}
    if request.method == "POST":
        request_dict = json.loads(request.body)
        id = request_dict.get("id")

        user = models.User.objects.filter(id = id)
        if(not user.exists()):
            ret_dict["msg"] = "not found"
        else:
            user = user.first()
            img = request.FILES.get("img")
            default_storage.save("../static/icon/"+img.name, ContentFile(img.read()))
            ret_dict["url"] = "/static/icon/"+img.name
            user.img_url = ret_dict["img_url"]
            user.save()
    else:
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")

# 注销用户
def delete_user_view(request):
    """
    GET:
        接受参数：request
        request.id: 用户id
        返回参数: ans
        ans.msg：消息
            1. success: 成功
            2. not found: 查找用户失败
    """

    ret_dict = {"msg": "success"}
    if request.method == "GET":
        id = request.GET.get("id")
        print("!!")
        user = models.User.objects.filter(id = id)
        if(not user.exists()):
            ret_dict["msg"] = "not found"
        else:
            user = user.first()
            user.delete()
    else:
        ret_dict["msg"] = "method error"

    ans = json.dumps(ret_dict)
    return HttpResponse(ans, content_type = "application/json")