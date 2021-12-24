import unittest
from util import check_content
from util import check_password
from util import check_user_info
from util import check_question_info

# check_content 函数单元测试
class ContentCheckTest(unittest.TestCase):
    def setUp(self):
        print('content test start')

    def test_void_condition(self):
        right_content = "C++"
        keyerror_content = 121
        short_content = ""
        long_content = "21" * 100 +  "C"

        self.assertEqual(check_content(None), "illegal content", "空数据测试失败")
        self.assertEqual(check_content(right_content), "success", "正常内容测试失败")
        self.assertEqual(check_content(keyerror_content), "illegal content", "内容数据类型错误测试失败")
        self.assertEqual(check_content(short_content), "illegal content", "内容过短测试失败")
        self.assertEqual(check_content(long_content), "illegal content", "内容过长测试失败")

    def tearDown(self):
        print('content test end')
        
# check_password 函数单元测试
class PasswordCheckTest(unittest.TestCase):
    def setUp(self):
        print('password test start')

    def test_void_condition(self):
        right_password = "zys123456"
        keyerror_password = 121
        short_password = "z2345"
        long_password = "z21" * 10
        numerical_password = "12121211"
        letter_password = "zazazaz"
        illegal_password = "#!@%z121"

        self.assertEqual(check_password(right_password), True, "正常密码测试失败")
        self.assertEqual(check_password(keyerror_password), False, "类型错误密码测试失败")
        self.assertEqual(check_password(short_password), False, "过短密码测试失败")
        self.assertEqual(check_password(long_password), False, "过长密码测试失败")
        self.assertEqual(check_password(numerical_password), False, "纯数字密码测试失败")
        self.assertEqual(check_password(letter_password), False, "纯字母密码测试失败")
        self.assertEqual(check_password(illegal_password), False, "非法字符密码测试失败")

    def tearDown(self):
        print('password test end')
        
# check_user_info 函数单元测试
class InfoCheckTest(unittest.TestCase):
    def setUp(self):
        print('info test start')

    def test_void_condition(self):
        right_username = "zys996"
        right_name = "zys"
        right_school = "tsinghua"
        right_class = "92"

        self.assertEqual(check_user_info({}), "illegal username", "空数据测试失败")
        self.assertEqual(check_user_info({
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "illegal username", "空数据测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "school": right_school,
            "class": right_class
            }), "illegal name", "空数据测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "class": right_class
            }), "illegal school", "空数据测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": right_school,
            }), "illegal class", "空数据测试失败")
    
    def test_user_check(self):
        keyerror_username = 12121
        short_username = "zys"
        long_username = "zys999999999999"

        right_username = "zys996"
        right_name = "zys"
        right_school = "tsinghua"
        right_class = "92"

        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "success", "正常用户名测试失败")
        self.assertEqual(check_user_info({
            "username": keyerror_username,
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "illegal username", "用户名类型错误测试失败")
        self.assertEqual(check_user_info({
            "username": short_username,
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "illegal username", "短用户名测试失败")
        self.assertEqual(check_user_info({
            "username": long_username,
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "illegal username", "长用户名测试失败")
            
    def test_name_check(self):
        keyerror_name = 12121
        short_name = "z"
        long_name = "zys999999999999999999"

        right_username = "zys996"
        right_name = "zys"
        right_school = "tsinghua"
        right_class = "92"

        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "success", "正常姓名测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : keyerror_name,
            "school": right_school,
            "class": right_class
            }), "illegal name", "姓名类型错误测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : short_name,
            "school": right_school,
            "class": right_class
            }), "illegal name", "短姓名测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : long_name,
            "school": right_school,
            "class": right_class
            }), "illegal name", "长姓名测试失败")

    def test_school_check(self):
        keyerror_school = 12121
        long_school = "tsinghuatsinghuatsinghuatsinghua"

        right_username = "zys996"
        right_name = "zys"
        right_school = "tsinghua"
        right_class = "92"

        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "success", "正常学校名测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": keyerror_school,
            "class": right_class
            }), "illegal school", "学校名类型错误测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": long_school,
            "class": right_class
            }), "illegal school", "长学校名测试失败")

    def test_class_check(self):
        keyerror_class = 12121
        long_class = "tsinghuatsinghuatsinghuatsinghua"

        right_username = "zys996"
        right_name = "zys"
        right_school = "tsinghua"
        right_class = "92"

        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": right_school,
            "class": right_class
            }), "success", "正常班级名测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": right_school,
            "class": keyerror_class
            }), "illegal class", "班级名类型错误测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": right_school,
            "class": long_class
            }), "illegal class", "班级学校名测试失败")

    def test_cross_condition(self):
        wrong_username = "11"
        wrong_name = "zys999999999999999999"
        wrong_school = "tsinghuatsinghuatsinghua"
        wrong_class = "tsinghuatsinghuatsinghuatsinghua"

        right_username = "zys996"
        right_name = "zys"
        right_school = "tsinghua"
        right_class = "92"

        self.assertEqual(check_user_info({
            "username": wrong_username,
            "name" : wrong_name,
            "school": wrong_school,
            "class": wrong_class
            }), "illegal username", "多数据错误测试失败")
        self.assertEqual(check_user_info({
            "username": wrong_username,
            "name" : wrong_name,
            "school": wrong_school,
            "class": right_class
            }), "illegal username", "多数据错误测试失败")
        self.assertEqual(check_user_info({
            "username": wrong_username,
            "name" : wrong_name,
            "school": right_school,
            "class": right_class
            }), "illegal username", "多数据错误测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : wrong_name,
            "school": wrong_school,
            "class": wrong_class
            }), "illegal name", "多数据错误测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : wrong_name,
            "school": wrong_school,
            "class": right_class
            }), "illegal name", "多数据错误测试失败")
        self.assertEqual(check_user_info({
            "username": right_username,
            "name" : right_name,
            "school": wrong_school,
            "class": wrong_class
            }), "illegal school", "多数据错误测试失败")

    def tearDown(self):
        print('info test end')

# check_question_info 函数单元测试
class QuestionCheckTest(unittest.TestCase):
    def setUp(self):
        print('question test start')

    def test_void_condition(self):
        right_type = "C++"
        right_title = "C++ compile error"
        right_abstract = "couldn't compile"

        self.assertEqual(check_question_info({}), "illegal type", "空数据测试失败")
        self.assertEqual(check_question_info({
            "title": right_title,
            "abstract": right_abstract
            }), "illegal type", "空数据测试失败")
        self.assertEqual(check_question_info({
            "type" : right_type,
            "abstract": right_abstract
            }), "illegal title", "空数据测试失败")
        self.assertEqual(check_question_info({
            "type" : right_type,
            "title": right_title,
            }), "illegal abstract", "空数据测试失败")

    def test_type(self):
        keyerror_type = 12121
        short_type = ""
        long_type = "C++" * 10 + "C"

        right_type = "C++"
        right_title = "C++ compile error"
        right_abstract = "couldn't compile"

        self.assertEqual(check_question_info({
            "type": right_type,
            "title": right_title,
            "abstract": right_abstract
            }), "success", "正常问题类型测试失败")
        self.assertEqual(check_question_info({
            "type": keyerror_type,
            "title": right_title,
            "abstract": right_abstract
            }), "illegal type", "问题类型数据类型错误测试失败")
        self.assertEqual(check_question_info({
            "type": short_type,
            "title": right_title,
            "abstract": right_abstract
            }), "illegal type", "问题类型过短测试失败")
        self.assertEqual(check_question_info({
            "type": long_type,
            "title": right_title,
            "abstract": right_abstract
            }), "illegal type", "问题类型过长测试失败")

    def test_title(self):
        keyerror_title = 12121
        short_title = "C"
        long_title = "C++" * 10 + "C"

        right_type = "C++"
        right_title = "C++ compile error"
        right_abstract = "couldn't compile"

        self.assertEqual(check_question_info({
            "type": right_type,
            "title": right_title,
            "abstract": right_abstract
            }), "success", "正常标题测试失败")
        self.assertEqual(check_question_info({
            "type": right_type,
            "title": keyerror_title,
            "abstract": right_abstract
            }), "illegal title", "标题类型错误测试失败")
        self.assertEqual(check_question_info({
            "type": right_type,
            "title": short_title,
            "abstract": right_abstract
            }), "illegal title", "标题过短测试失败")
        self.assertEqual(check_question_info({
            "type": right_type,
            "title": long_title,
            "abstract": right_abstract
            }), "illegal title", "标题过长测试失败")

    def test_abstract(self):
        keyerror_abstract = 12121
        long_abstract = "C+" * 100 + "C"

        right_type = "C++"
        right_title = "C++ compile error"
        right_abstract = "couldn't compile"

        self.assertEqual(check_question_info({
            "type": right_type,
            "title": right_title,
            "abstract": right_abstract
            }), "success", "正常摘要测试失败")
        self.assertEqual(check_question_info({
            "type": right_type,
            "title": right_title,
            "abstract": keyerror_abstract
            }), "illegal abstract", "摘要类型错误测试失败")
        self.assertEqual(check_question_info({
            "type": right_type,
            "title": right_title,
            "abstract": long_abstract
            }), "illegal abstract", "摘要过长测试失败")

    def test_cross_condition(self):
        wrong_type = 12121
        wrong_title = "C"
        wrong_abstract = "C+" * 100 + "C"

        right_type = "C++"
        right_title = "C++ compile error"
        right_abstract = "couldn't compile"
        self.assertEqual(check_question_info({
            "type": wrong_type,
            "title": wrong_title,
            "abstract": wrong_abstract
            }), "illegal type", "多数据错误测试失败")
        self.assertEqual(check_question_info({
            "type": right_type,
            "title": wrong_title,
            "abstract": wrong_abstract
            }), "illegal title", "多数据错误测试失败")
        self.assertEqual(check_question_info({
            "type": wrong_type,
            "title": right_title,
            "abstract": wrong_abstract
            }), "illegal type", "多数据错误测试失败")
        self.assertEqual(check_question_info({
            "type": wrong_type,
            "title": wrong_title,
            "abstract": right_abstract
            }), "illegal type", "多数据错误测试失败")
    def tearDown(self):
        print('question test end')

if __name__ == '__main__':
    unittest.main()