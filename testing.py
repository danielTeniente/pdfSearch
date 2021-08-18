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
        sol = ['AI','cripto','desarrollo','no_pdfs'] 
        self.assertEqual(module_res, sol, 
                f'Your solution is {module_res} rather than {sol}')

class TestGetPDFs(unittest.TestCase):
    def test_no_pdfs(self):
        module_res = functions.get_PDFs(path='./Referencias/no_pdfs')
        sol = []
        self.assertEqual(module_res, sol, 
                f'Your solution is {module_res} rather than {sol}')
    def test_pdfs_names(self):
        module_res = functions.get_PDFs(path='./Referencias/AI')
        sol = ['./Referencias/AI/Book1.pdf','./Referencias/AI/Book2.pdf','./Referencias/AI/Book3.pdf'] 
        self.assertEqual(module_res, sol, 
                f'Your solution is {module_res} rather than {sol}')

class TestGetPDFsText(unittest.TestCase):
    def test_pdfs_text(self):
        module_res = functions.get_PDF_content(path='./Referencias/test.pdf')
        #elimino los espacios en blanco esperando que el contenido
        #sea el mismo en esencia
        module_res = module_res.replace(' ','')
        sol = 'Hello to everyone'.replace(' ','')
        self.assertEqual(module_res, sol, 
                f'Your solution is {module_res} rather than {sol}')



if __name__ == '__main__':
    unittest.main()    