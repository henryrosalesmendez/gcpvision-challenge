
import unittest
import subprocess

class TestingAPI(unittest.TestCase):

    def test_bicicle(self):
        '''
        Testing the API with the image 'https://storage.cloud.google.com/image-pool-falabella-test/bicileta.jpg' (out-gcp link) where should be output: Bicycle wheel, Bicycle, Bicycle wheel
        '''
        cmd = """curl -H "Content-Type: application/json" -X POST -d '{"inputImage":"gs://image-pool-falabella-test/bicileta.jpg", "outputImage":"gs://image-pool-falabella-test-out/bicileta.jpg"}' http://35.225.113.7/falabella/api/v1.0/detectobjects
        """

        output = eval(subprocess.check_output(cmd, shell=True))
        msg = output["msg"].split(":")[1]

        self.assertTrue(not msg.find("No se pudo obtener") == 0)
        self.assertTrue(len(set(['Bicycle wheel', 'Bicycle', 'Bicycle wheel']).difference(msg.split(", ")))==0)
    
    
    def test_cat_dog(self):
        '''
        Testing the API with the image 'https://storage.cloud.google.com/image-pool-falabella-test/cat_dog.jpg' (out-gcp link) where should be output a cat and dog
        '''
        cmd = """curl -H "Content-Type: application/json" -X POST -d '{"inputImage":"gs://image-pool-falabella-test/cat_dog.jpg", "outputImage":"gs://image-pool-falabella-test-out/cat_dog.jpg"}' http://35.225.113.7/falabella/api/v1.0/detectobjects
        """

        output = eval(subprocess.check_output(cmd, shell=True))
        msg = output["msg"].split(":")[1]

        self.assertTrue(not msg.find("No se pudo obtener") == 0)
        self.assertTrue(len(set(['Cat', 'Dog']).difference(msg.split(", ")))==0)
        
    
    def test_bedroom(self):
        '''
        Testing the API with the image 'https://storage.cloud.google.com/image-pool-falabella-test/dormitorio.jpg' (out-gcp link) where should be output: 'Wardrobe', 'Couch', 'Cabinetry', 'Bed'
        '''
        cmd = """curl -H "Content-Type: application/json" -X POST -d '{"inputImage":"gs://image-pool-falabella-test/dormitorio.jpg", "outputImage":"gs://image-pool-falabella-test-out/dormitorio.jpg"}' http://35.225.113.7/falabella/api/v1.0/detectobjects
        """

        output = eval(subprocess.check_output(cmd, shell=True))
        msg = output["msg"].split(":")[1]

        self.assertTrue(not msg.find("No se pudo obtener") == 0)
        self.assertTrue(len(set(['Wardrobe', 'Couch', 'Cabinetry', 'Bed']).difference(msg.split(", ")))==0)
        
        
    def test_no_objects(self):
        '''
        Here I specify a image without objects, so, I check that the response say that.
        '''
        cmd = """curl -H "Content-Type: application/json" -X POST -d '{"inputImage":"gs://image-pool-falabella-test/blanco.jpg", "outputImage":"gs://image-pool-falabella-test-out/blanco.jpg"}' http://35.225.113.7/falabella/api/v1.0/detectobjects
        """

        output = eval(subprocess.check_output(cmd, shell=True))
        msg = output["msg"].split(":")[1]

        self.assertTrue(msg.find("No se pudo obtener") == 0)

   

if __name__ == '__main__':
    unittest.main() 



    
