import numpy as np
import cv2

def text_to_binary(msg):
    if isinstance(msg, str):
        return ''.join([format(ord(i), "08b") for i in msg])
    elif isinstance(msg, (bytes, np.ndarray)):
        return [format(i, "08b") for i in msg]
    elif isinstance(msg, int) or isinstance(msg, np.uint8):
        return format(msg, "08b")
    else:
        raise TypeError("Input type is not supported in this function")

def encode_image_data(img, data):
    if len(data) == 0:
        raise ValueError('Data entered to be encoded is empty')
    
    name_of_file = input("\nEnter the name of the New Image (Stego Image) after Encoding (with extension): ")
    
    no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8
    
    print("\t\nMaximum bytes to encode in Image:", no_of_bytes)
    
    if len(data) > no_of_bytes:
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
    
    data += '*^*^*'
    
    binary_data = text_to_binary(data)
    print("\n")
    print(binary_data)
    length_data = len(binary_data)
    
    print("\nThe Length of Binary data", length_data)
    
    index_data = 0
    
    for i in img:
        for pixel in i:
            r, g, b = text_to_binary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(name_of_file, img)
    print("\nEncoded the data successfully in the Image, and the image is successfully saved with name ", name_of_file)

def decode_image_data(img):
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = text_to_binary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    print("\n\nThe Encoded data which was hidden in the Image was: ", decoded_data[:-5])
                    return

def main():
    while True:
        print("IMAGE STEGANOGRAPHY LSB\n")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit\n")
        choice = int(input("Enter the Choice: "))
        
        if choice == 1:
            image = cv2.imread("./asset/img.jpg")
            data = input("\nEnter the data to be Encoded in Image: ")
            encode_image_data(image, data)
        elif choice == 2:
            image_path = input("Enter the Image you need to Decode to get the Secret message: ")
            image = cv2.imread(image_path)
            decode_image_data(image)
        elif choice == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

if __name__ == "__main__":
    main()