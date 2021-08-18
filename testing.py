import unittest
import functions 

class TestGetDirs(unittest.TestCase):
    def test_empty_dir(self):
        module_res = functions.get_dirs(path='./empty_dir')
        sol = []
        self.assertEqual(module_res, sol, 
                f'Your solution is {module_res} rather than {sol}')
    def test_folders_dir(self):
        module_res = functions.get_dirs(path='./Referencias')
        sol = ['AI','cripto','desarrollo'] 
        self.assertEqual(module_res, sol, 
                f'Your solution is {module_res} rather than {sol}')
    



if __name__ == '__main__':
    unittest.main()    