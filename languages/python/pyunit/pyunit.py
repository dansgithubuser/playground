import unittest

class TestPlay1(unittest.TestCase):
	@classmethod
	def setUpClass(cls): print('TestPlay1 setUpClass')
	@classmethod
	def tearDownClass(cls): print('TestPlay1 tearDownClass')
	def setUp(self): print('TestPlay1 setUp')
	def tearDown(self): print('TestPlay1 tearDown')
	def test_1(self): print('TestPlay1 test_1')
	def test_2(self): print('TestPlay1 test_2')

class TestPlay2(unittest.TestCase):
	@classmethod
	def setUpClass(cls): print('TestPlay2 setUpClass')
	@classmethod
	def tearDownClass(cls): print('TestPlay2 tearDownClass')
	def setUp(self): print('TestPlay2 setUp')
	def tearDown(self): print('TestPlay2 tearDown')
	def test_1(self): print('TestPlay2 test_1')
	def test_2(self): print('TestPlay2 test_2')
