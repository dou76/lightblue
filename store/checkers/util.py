# 检查注册用户名是否合法
def check_legal_username(username):
    return (username != None and isinstance(username, str) and len(username) <= 12 and len(username) >= 5)

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

# 用户信息检验
def check_user_info(request_dict):
    username = request_dict.get("username")
    name = request_dict.get("name")
    school = request_dict.get("school")
    _class = request_dict.get("class")
        
    if(not check_legal_username(username)):
        return "illegal username"
    if(name == None or not isinstance(name, str) or len(name) > 20):
        return "illegal name"
    if(school == None or not isinstance(school, str) or len(school) > 15):
        return "illegal school"
    if(_class == None or not isinstance(_class, str) or len(_class) > 10):
        return "illegal class" 

    return "success"

# 问题信息检验
def check_question_info(request_dict):
    _type = request_dict.get("type")
    title = request_dict.get("title")
    abstract = request_dict.get("abstract")

    if(_type == None or not isinstance(_type, str) or len(_type) > 20 or len(_type) < 1):
        return "illegal type"
    if(title == None or not isinstance(title, str) or len(title) > 30 or len(title) < 4):
        return "illegal title"
    if(abstract == None or not isinstance(abstract, str) or len(abstract) > 200):
        return "illegal abstract"
    
    return "success"

# 回复内容检验
def check_content(content):
    if(content == None or not isinstance(content, str) or len(content) > 20 or len(content) < 1):
        return "illegal content"
    else:
        return "success"
# 解析日期
def parse_date(date):
    date_list = date.split("-")
    return int(date_list[0]), int(date_list[1]), int(date_list[2])