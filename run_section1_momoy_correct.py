import sys
import os
import pathlib
import importlib.util
from pathlib import Path
sys.path.insert(0, r'C:\Users\Technical-10\AppData\Roaming\Python\Python312\site-packages')
import cv2
repo = Path(r'D:\Technical\Downloads\qm vs code image processing\opencv-course')
out_dir = repo / 'temp_outputs'
out_dir.mkdir(parents=True, exist_ok=True)
momoy_path = repo / 'Resources' / 'Photos' / 'momoy.jpg'
if not momoy_path.exists():
    raise FileNotFoundError(f'{momoy_path} not found')
real_imread = cv2.imread

def my_imread(path, *args, **kwargs):
    p = str(path)
    if 'cats.jpg' in p.lower() or 'park.jpg' in p.lower():
        return real_imread(str(momoy_path), *args, **kwargs)
    return real_imread(path, *args, **kwargs)

cv2.imread = my_imread

cv2.waitKey = lambda x=0: 1
cv2.destroyAllWindows = lambda: None

class DummyCapture:
    def read(self):
        return False, None
    def release(self):
        pass
    def isOpened(self):
        return False

cv2.VideoCapture = lambda *args, **kwargs: DummyCapture()

current_script = None

def my_imshow(name, img):
    global current_script
    if img is None:
        return
    safe = name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    filename = f"{current_script}_{safe}.png"
    path = out_dir / filename
    cv2.imwrite(str(path), img)
    print(f'saved {filename}')

cv2.imshow = my_imshow

scripts = ['read.py', 'basic_functions.py', 'contours.py', 'thresh.py', 'draw.py', 'transformations.py']
for script in scripts:
    current_script = Path(script).stem
    print(f'RUNNING {script}')
    os.chdir(repo / 'Section #1 - Basics')
    spec = importlib.util.spec_from_file_location(current_script, script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

print('DONE')
