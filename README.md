# QR Code Detector

This is Python wrapper for [QR-Code Scanner](https://github.com/PhilS94/QR-Code-Scanner):

> A QR-Code Scanner, written in C++ and using the OpenCV library, which was developed as an optional part of the university course "Computer Vision" in a small team of three.

This implementation works __substantially__ better than the `QRCodeDetector` that comes with OpenCV.


## Install


### Windows

On Windows, install `Visual Studio Build Tools 2019`:
https://visualstudio.microsoft.com/downloads/

Then install this package into your Pyhton environment:
```
pip install git+https://github.com/driedler/qrcode_detector.git
```



### Linux

Ensure the GCC build toolchain is installed:

```
sudo apt install -y build-essential ninja-build gcc-9
```

Then install this package into your Pyhton environment:
```
pip install git+https://github.com/driedler/qrcode_detector.git
```



### Raspberry PI


#### Install pre-built

A pre-built Python package for Raspberry PI3 (or Raspberry PI Zero 2 W) can be installed with (this assumes Python3.9 on Rasparian OS 11 "Bullseye"):

```
pip3 install https://github.com/driedler/qrcode_detector/raw/main/dist/qrcode_detector-0.1.0-cp39-cp39-linux_armv7l.whl
```

#### Build from source

(If on Windows, run from WSL2)

The following is tested to work with a Raspberry PI 3 (or Raspberry PI Zero 2 W)
using the `bullseye` Raspbarian OS.

Download the toolchain by running the script: [install_rpi3_bullseye_toolchain.sh](cpp/install_rpi3_bullseye_toolchain.sh)


Then build the RPI wheel
```
pip3 install wheel
export BUILD_RASPBERRY=1
python3 setup.py bdist_wheel
```

Then copy the built wheel to your raspberry PI and install with:
```
pip install <path to .whl>
```



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
