import os
import importlib.util
import sys
from pathlib import Path
sys.path.insert(0, r'C:\Users\Technical-10\AppData\Roaming\Python\Python312\site-packages')
import cv2
import numpy as np
repo = Path(r'D:\Technical\Downloads\qm vs code image processing\opencv-course')
out_dir = repo / 'Section 2 output'
out_dir.mkdir(parents=True, exist_ok=True)

orig_imread = cv2.imread

def my_imread(path, *args, **kwargs):
    p = str(path)
    if p.lower().endswith(('cats.jpg', 'park.jpg', 'cats 2.jpg')):
        return orig_imread(str(repo / 'Resources' / 'Photos' / 'momoy.jpg'), *args, **kwargs)
    return orig_imread(path, *args, **kwargs)

cv2.imread = my_imread
cv2.waitKey = lambda x=0: 1
cv2.destroyAllWindows = lambda: None

class DummyCapture:
    def __init__(self, *args, **kwargs):
        self.frame = cv2.imread(str(repo / 'Resources' / 'Photos' / 'momoy.jpg'))
        if self.frame is None:
            self.frame = np.zeros((200, 200, 3), dtype=np.uint8)
        self.frame_count = 0
    def read(self):
        self.frame_count += 1
        if self.frame_count > 1:
            return False, None
        return True, self.frame
    def release(self):
        pass
    def isOpened(self):
        return True

cv2.VideoCapture = lambda *args, **kwargs: DummyCapture()

current_script = None

def save_imshow(name, img):
    if img is None:
        return
    safe = name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    path = out_dir / f'{current_script}_{safe}.png'
    cv2.imwrite(str(path), img)
    print(f'saved {path.name}')

cv2.imshow = save_imshow

scripts = ['bitwise.py', 'blurring.py', 'colour_spaces.py', 'gradients.py', 'histogram.py', 'masking.py', 'rescale_resize.py', 'splitmerge.py']
for script in scripts:
    current_script = Path(script).stem
    print(f'RUNNING {script}')
    os.chdir(repo / 'Section #2 - Advanced')
    try:
        spec = importlib.util.spec_from_file_location(current_script, script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f'ERROR {script}: {e}')

print('DONE')
