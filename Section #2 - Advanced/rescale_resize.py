#pylint:disable=no-member

import cv2 as cv
from pathlib import Path

# img = cv.imread('../Resources/Photos/cat.jpg')
# cv.imshow('Cat', img)

def rescaleFrame(frame, scale=0.75):
    # Images, Videos and Live Video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def changeRes(width, height):
    # Live video
    capture.set(3, width)
    capture.set(4, height)


base_dir = Path(__file__).resolve().parent
video_path = (base_dir / '../Resources/Videos/dog.mp4').resolve()
output_dir = (base_dir / '../Section 2 output').resolve()
output_dir.mkdir(parents=True, exist_ok=True)
output_video_path = output_dir / 'rescale_resize_output.mp4'

# Reading Videos
capture = cv.VideoCapture(str(video_path))

if not capture.isOpened():
    raise FileNotFoundError(f'Could not open video: {video_path}')

fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter(str(output_video_path), fourcc, 20.0, (320, 180))

frame_count = 0
while True:
    isTrue, frame = capture.read()

    if not isTrue:
        break

    frame_resized = rescaleFrame(frame, scale=.2)
    out.write(frame_resized)

    cv.imshow('Video', frame)
    cv.imshow('Video Resized', frame_resized)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

    frame_count += 1
    if frame_count >= 60:
        break

capture.release()
out.release()
cv.destroyAllWindows()
print(f'Saved video output to {output_video_path}')