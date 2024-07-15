import qrcode

def generate_qr_code(qrcode_details, filename):
    img = qrcode.make(qrcode_details)
    img.save(filename)
    print(f"QR code is created as {filename}")

generate_qr_code('Hi This Siranjeevi', 'qr_code_image2.png')