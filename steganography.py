import cv2
import numpy as np

def embed_data(image_path, message, output_path):
    print("🔹 Loading image...")
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not open {image_path}")
        return

    print("Image loaded successfully!")

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '00000000'  # End of message delimiter

    print(f"Message to embed: {message} ({len(binary_message)} bits)")

    data_index = 0
    max_bits = image.shape[0] * image.shape[1] * 3

    if len(binary_message) > max_bits:
        print("Error: Message is too large for this image!")
        return

    print("Embedding message...")

    for row in image:
        for pixel in row:
            for i in range(3):  # Modify LSBs of RGB channels
                if data_index < len(binary_message):
                    new_value = (int(pixel[i]) & ~1) | int(binary_message[data_index])  # Fix overflow issue
                    pixel[i] = np.clip(new_value, 0, 255)  # Ensures values stay in uint8 range
                    data_index += 1
                else:
                    break

    cv2.imwrite(output_path, image)
    print(f"Message successfully hidden in {output_path}")

def extract_data(stego_image_path):
    print("🔹 Loading stego image...")
    image = cv2.imread(stego_image_path)
    if image is None:
        print(f"Error: Could not open {stego_image_path}")
        return
    
    print("Image loaded successfully!")
    
    binary_message = ""
    for row in image:
        for pixel in row:
            for i in range(3):  # Extract LSBs from R, G, B
                binary_message += str(pixel[i] & 1)

    # Convert binary to text
    byte_array = bytearray()
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            byte_array.append(int(byte, 2))
    
    # Convert to string and remove any trailing null bytes
    hidden_message = byte_array.decode(errors="ignore").rstrip("\x00")
    
    if hidden_message:
        print("Hidden message extracted:", hidden_message)
    else:
        print("No message found!")

# Example Usage:
# Run these functions separately in your script
# embed_data('input_image.jpeg', 'Hello, this is a secret!', 'stego_image.png')
# extract_data('stego_image.png')