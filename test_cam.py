from vilib import Vilib

def testing():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
    Vilib.image_classify_set_model(path ="./detect.tflite")
    Vilib.image_classify_set_labels(path = "./labelmap.txt")
    Vilib.image_classify_switch(True)
    
if __name__ == "__main__":
    testing()

#Environment Commnads:
#source ~/picar-env/bin/activate

