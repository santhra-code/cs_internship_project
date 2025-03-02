import cv2
import numpy as np
from encryption import encrypt_message

def embed_data(image_path, message, output_path):
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open {image_path}. Check if the file exists.")

    # Encrypt the message
    encrypted_message = encrypt_message(message)
    
    # Convert encrypted message to binary
    binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)

    # Check if the message fits in the image
    total_pixels = image.shape[0] * image.shape[1] * 3  # Total RGB values
    if len(binary_message) > total_pixels:
        raise ValueError("Message is too large for the given image!")

    # Embed message in image
    data_index = 0
    for row in image:
        for pixel in row:
            for i in range(3):  # Iterate over R, G, B values
                if data_index < len(binary_message):
                    pixel[i] = (pixel[i] & 254) | int(binary_message[data_index])  # Modify LSB
                else:
                    break

    # Save stego image
    cv2.imwrite(output_path, image)
    print(f"Message hidden successfully in {output_path}")

# Example Usage:
# embed_data('input_image.jpeg', 'Hello, this is a secret!', 'stego_image.png')