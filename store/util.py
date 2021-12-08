import json
from .import models


# 检查注册用户名是否重复
def check_legal_username(username):
    return (username != None and isinstance(username, str) and len(username) <= 12 and len(username) >= 5)

# 检查注册用户名是否重复
def check_multiple_username(username):
    if(models.User.objects.filter(username = username).exists()):
        return False
    
    return True

# 检查校验码
def check_code(code):
    # if(models.Authentication.objects.filter(authentication = code).exists()):
    #     return True
    # return False

    return True

# 检查密码合法性
def check_password(password):
    if (password == None or not isinstance(password, str) or len(password) > 18 or len(password) < 6):
        return False

    lower, digit = False, False
    for letter in password:
        if letter.islower():
            lower = True
        elif letter.isdigit():
            digit = True
        
        if(lower and digit):
            return True
    
    return False

# 用户登录检验
def login_check(username, password):
    ret_dict = {"msg": "success"}
    user_dict = models.User.objects.filter(username = username)

    if(not user_dict.exists()):
        ret_dict["msg"] = "not found"

    elif (not user_dict.filter(password = password).exists()):
        ret_dict["msg"] = "error"

    else:
        user = user_dict.filter(password = password).first()
        ret_dict["id"] = user.id
        ret_dict["type"] = user.user_type

    return json.dumps(ret_dict)