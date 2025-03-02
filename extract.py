import cv2
import numpy as np
from encryption import decrypt_message

def extract_data(stego_image_path):
    # Read the image
    image = cv2.imread(stego_image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open {stego_image_path}. Check if the file exists.")

    binary_message = ""
    for row in image:
        for pixel in row:
            for i in range(3):  # Extract LSBs from R, G, B
                binary_message += str(pixel[i] & 1)

    # Convert binary to bytes
    byte_array = bytearray()
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            byte_array.append(int(byte, 2))

    # Decrypt the message
    try:
        hidden_message = decrypt_message(bytes(byte_array))
        print("Hidden message:", hidden_message)
    except:
        print("Error in extracting the message. Maybe no message is hidden!")

# Example Usage:
# extract_data('stego_image.png')