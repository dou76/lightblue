import unittest

from util import check_question_info

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