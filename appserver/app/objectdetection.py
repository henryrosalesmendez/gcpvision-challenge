#!/usr/bin/env python



from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont



def copyImageToStorage(fromF, toF):
    """
    Copying the an image from local workspace to Storage
    
    Args:
      fromF: image from local workspace
      toF: location in storage
    """
    filename = fromF.split("/")[-1]
    print("[INFO] Uploading %s from Storage to %s" %(fromF, toF))
    subprocess.run(["gsutil","-m","cp",fromF, toF])
    print("[INFO] upload ends")

class ObjectDetection:
    """
    This class aim to identify, label, and draw object from an image following the 
    falabella requirements.
    """
    def __init__(self, workspace = None):
        """
        Initializing the attributes and workspace. Here I will check and create a folder for those
        given images, and other for the output if required.
        """        
        self.DISCOVERY_URL = 'https://vision.googleapis.com/v1/images:annotate'
        if not workspace:
            workspace = "/var/www/"
            #workspace = "/home/henry/Falabella/docker/"

        self.workspace = workspace
        self.folder_in_images = workspace + "appserver/app/static/img/inImages/"
        self.folder_out_images = workspace + "appserver/app/static/img/outImages/"

        if not os.path.isdir(self.workspace):
            #os.mkdir(workspace)
            print("[INFO] You have to create %s" % (workspace))

        if not os.path.isdir(self.folder_in_images):
            #os.mkdir(self.folder_in_images)
            print("[INFO] You have to create  %s" % (self.folder_in_images))

        if not os.path.isdir(self.folder_out_images):
            #os.mkdir(self.folder_out_images)
            print("[INFO] You have to create  %s" % (self.folder_out_images))


    def get_vision_service(self):
        """
        This method obtain the credential following the strategy called Application Default Credentials
        to find your application's credentials
        """
        credentials = GoogleCredentials.get_application_default()
        print("[Credential]",credentials)
        return discovery.build('vision', 'v1', credentials=credentials,
                            discoveryServiceUrl=self.DISCOVERY_URL)


    def gs2labels(self, max_results=None):
        """
        Uses the Vision API to discover/locate objects in an image. 
        
        Args:
          max_results: number of retry 
        
        The output has the next structure:
            [{'mid': '/m/01yrx', 'name': 'Cat', 'score': 0.9555101, 'boundingPoly': {'normalizedVertices': [{'x': 0.07531861, 'y': 0.22401918}, {'x': 0.4559419, 'y': 0.22401918}, {'x': 0.4559419, 'y': 0.7658673}, {'x': 0.07531861, 'y': 0.7658673}]}} , ...]
        """
        if not max_results: max_results = 4
        
        batch_request = [{
            'image': {
                'source': {
                    'gcs_image_uri': self.gcs_uri
                }
            },
            'features': [{
                'type': 'OBJECT_LOCALIZATION',
                'maxResults': max_results,
                }]
            }]

        service = self.get_vision_service()
        print("[SERVICE]",service)
        request = service.images().annotate(body={
            'requests': batch_request,
            })
        response = request.execute()
        print("response:",type(response),response)
        if "localizedObjectAnnotations" in response["responses"][0]:
            return response["responses"][0]["localizedObjectAnnotations"]
        return []


    def copyImageToLocal(self):
        """
        Copy the targeted image to local workspace
        """
        self.filename = self.gcs_uri.split("/")[-1]
        self.pathTo = self.folder_in_images + self.filename
        print("[INFO] Downloading %s from Storage to %s" %(self.gcs_uri, self.pathTo))
        subprocess.run(["gsutil","-m","cp",self.gcs_uri, self.pathTo])
        print("[INFO] download ends")


    def draw_objects(self, poligon):
        """Draws a polygon around the faces, then saves to output_filename.

        Args:
          poligon: a list of dictionary, each of them denote an detected object in an image
        """
        im = Image.open(self.pathTo)
        width, height = im.size
        draw = ImageDraw.Draw(im)

        # Sepecify the font-family and the font-size
        #pthfont = self.workspace + "appserver/app/static/fonts/FreeMono.ttf"
        #fnt = ImageFont.truetype(pthfont, 140)
        print("==============> poligon:",poligon)
        for pol in poligon:
            box = [(width*vertex["x"], height*vertex["y"])
                   for vertex in pol["boundingPoly"]["normalizedVertices"] if "x" in vertex.keys() and "y" in vertex.keys()]

            draw.line(box + [box[0]], width=2, fill='#00ff00')
            draw.text((box[0][0], box[0][1] - 30), str(pol["name"]), fill='#FF0000')#, font=fnt)
            
        output_filename = self.folder_out_images + self.filename
        print("[INFO] Just about write to %s" %(output_filename))
        im.save(output_filename)
        print("[INFO] stored ok")

        if len(poligon) == 0:
            return [output_filename, ["No se pudo obtener información de esta imagen"]]
        return [output_filename, [pol["name"] for pol in poligon]]


    def process(self, _gcs_uri):
        """
        This is the main method for detecting/labelling/drawing the objects for a given image.
        
        Args:
          _gcs_uri: storage uri where is placed the image to process
        """
        self.gcs_uri = _gcs_uri

        # detecting objects with cloud vision API
        objs = self.gs2labels()
        print("[INFO] %d objects detected" %(len(objs)))
        
        # copying the given image locally
        self.copyImageToLocal()

        # drawing poligons
        return self.draw_objects(objs)


"""
if __name__ == '__main__':
    do = ObjectDetection()
    d = do.process("gs://image-pool-falabella-test/cat_dog.jpg")
"""
