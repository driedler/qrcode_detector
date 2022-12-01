
import numpy as np
from . import _qrcode_detector


def find_and_decode(image:np.ndarray) -> str:
    """Attempt to decode the data in the QR code in the given image.
    
    Return:
        The decoded data as a string if found, or empty string if not found
    """
   

    decoded_data = _qrcode_detector.find_and_decode(image)
    return decoded_data
