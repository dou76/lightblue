import unittest

from util import check_content

class QuestionCheckTest(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()