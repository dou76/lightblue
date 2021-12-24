import unittest

from util import check_user_info

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

if __name__ == '__main__':
    unittest.main()