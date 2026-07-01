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
orig_imread = cv2.imread

def my_imread(path, *args, **kwargs):
    p = str(path)
    if p.lower().endswith('cats.jpg') or p.lower().endswith('park.jpg'):
        return orig_imread(str(momoy_path), *args, **kwargs)
    return orig_imread(path, *args, **kwargs)
cv2.imread = my_imread


def safe_imwrite(path, img):
    if img is None:
        return False
    if getattr(img, 'size', 0) == 0:
        return False
    return cv2.imwrite(str(path), img)


def make_imshow(script, name, img):
    safe_name = name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    fname = f"{script}_{safe_name}.png"
    path = out_dir / fname
    if safe_imwrite(path, img):
        print(f'saved {path}')
    else:
        print(f'skipped empty {path}')

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

scripts = ['read.py','basic_functions.py','contours.py','thresh.py','draw.py','transformations.py']
for script in scripts:
    script_name = Path(script).stem
    cv2.imshow = lambda name, img, script_name=script_name: make_imshow(script_name, name, img)
    print(f'RUNNING {script}')
    os.chdir(repo / 'Section #1 - Basics')
    spec = importlib.util.spec_from_file_location(script_name, script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

print('DONE')
