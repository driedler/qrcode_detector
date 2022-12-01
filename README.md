# QR Code Detector

This is Python wrapper for [QR-Code Scanner](https://github.com/PhilS94/QR-Code-Scanner):

> A QR-Code Scanner, written in C++ and using the OpenCV library, which was developed as an optional part of the university course "Computer Vision" in a small team of three.

This implementation works __substantially__ better than the `QRCodeDetector` that comes with OpenCV.


## Install

On Windows, install `Visual Studio Build Tools 2019`:
https://visualstudio.microsoft.com/downloads/

Then run the command:
```
pip install git+https://github.com/driedler/qrcode_detector.git
```

which will build the Python wrapper and install the Python package into the Python environment.



## Usage

```python

# import the QR code detector wrapper
import qrcode_detector

# import the opencv library
try:
    from cv2 import cv2
except:
    import cv2

# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv2.imshow('video', frame)

    # decode the qrcode in the given image
    data = qrcode_detector.find_and_decode(frame)
    if data:
        # Print the decoded data if it was successfully found
        print(f'Decoded: {data}')
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()

```
