import sys
import os
import pathlib
import importlib.util
sys.path.insert(0, r'C:\Users\Technical-10\AppData\Roaming\Python\Python312\site-packages')
import cv2
out_path = pathlib.Path(r'D:\Technical\Downloads\qm vs code image processing\opencv-course\momoy.jpg')

def imshow(name, img):
    if name == 'Momoy':
        path = out_path
    else:
        safe_name = name.replace(' ', '_').replace('/', '_')
        path = out_path.parent / f'{safe_name}.png'
    cv2.imwrite(str(path), img)
    print(f'saved {name} -> {path}')

cv2.imshow = imshow
cv2.waitKey = lambda x=0: 1
cv2.destroyAllWindows = lambda: None
os.chdir(r'D:\Technical\Downloads\qm vs code image processing\opencv-course\Section #1 - Basics')
spec = importlib.util.spec_from_file_location('contours', 'contours.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print(f'output saved to {out_path}')
