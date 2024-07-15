import cv2
from pyzbar import pyzbar

def scan_qr_code(filename):
    # Load the image
    img = cv2.imread(filename)
    
    # Decode the QR code
    decoded_objects = pyzbar.decode(img)
    
    # Process and print the decoded information
    for obj in decoded_objects:
        print("Type:", obj.type)
        print("Data:", obj.data.decode("utf-8"))
    
    # Display the image with the QR code
    cv2.imshow("QR Code", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

scan_qr_code('qr_code_image2.png')
