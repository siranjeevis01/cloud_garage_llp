import barcode
from barcode.writer import ImageWriter


def generate_barcode(barcode_number, filename):
    PRODUCT = barcode.get_barcode_class('ean13')
    product = PRODUCT(barcode_number, writer=ImageWriter())
    barcode_image = product.save(filename)
    print(f"Barcode saved as {barcode_image}.png")

generate_barcode('909654321098', 'barcode_image5')

generate_barcode('987658921098', 'barcode_image6')