from locust import task, FastHttpUser
from PIL import Image
import io

class TestUser(FastHttpUser):
    # @task()
    def only_cloth(self):
        cloth = Image.open("service/back-end/sample_images/warmup_sample/cloth.jpg").convert('RGB').resize((768, 1024))
        
        clothByteArr = io.BytesIO()
        cloth.save(clothByteArr, format='JPEG')
        clothByteArr = clothByteArr.getvalue()
        
        files = [
            ("cloth", ("dummy", clothByteArr, "image/jpeg")),
            ("avatar_path", ("upper/long/Man_c.jpg")),
        ]
        
        self.client.post("http://localhost:8501/cloth-tryon", files=files)
    
    @task()
    def cloth_human(self):
        cloth = Image.open("service/back-end/sample_images/warmup_sample/cloth.jpg").convert('RGB').resize((768, 1024))
        human = Image.open("service/back-end/sample_images/warmup_sample/human.jpg").convert('RGB').resize((768, 1024))

        clothByteArr = io.BytesIO()
        cloth.save(clothByteArr, format='JPEG')
        clothByteArr = clothByteArr.getvalue()

        humanByteArr = io.BytesIO()
        human.save(humanByteArr, format='JPEG')
        humanByteArr = humanByteArr.getvalue()

        files = [
            ("part", ("upper")),
            ("cloth", ("dummy", clothByteArr, "image/jpeg")),
            ("human", ("dummy", humanByteArr, "image/jpeg")),
        ]
        
        self.client.post("http://localhost:8501/all-tryon", files=files)
    
    def on_start(self):
        print("Start Load Test.")

    def on_stop(self):
        print("Stop Load Test.s")
    