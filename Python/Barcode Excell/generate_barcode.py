import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os
import shutil

class BarcodeGenerator:
    def __init__(self, excel_path, output_dir, folder_name):
        self.excel_path = excel_path
        self.output_dir = output_dir
        self.folder_name = folder_name
        self.new_output_dir = os.path.join(output_dir, folder_name)

    def read_excel(self):
        self.df = pd.read_excel(self.excel_path)

    def prepare_output_directory(self):
        if os.path.exists(self.new_output_dir):
            shutil.rmtree(self.new_output_dir)
            print(f"Existing folder '{self.new_output_dir}' deleted.")
        os.makedirs(self.new_output_dir, exist_ok=True)

    def generate_barcodes(self):
        for index, row in self.df.iterrows():
            barcode_number = str(row['Barcode'])
            filename = os.path.join(self.new_output_dir, f'barcode_image_{index + 1}')
            
            PRODUCT = barcode.get_barcode_class('ean13')
            product = PRODUCT(barcode_number, writer=ImageWriter())
            barcode_image = product.save(filename)
            
            print(f"Barcode {barcode_number} saved as {filename}.png")

    def run(self):
        self.read_excel()
        self.prepare_output_directory()
        self.generate_barcodes()


excel_path = r'D:\PROJECT\cloud_garage_llp\Python\Barcode Excell\barcodes.xlsx'
output_dir = r'D:\PROJECT\cloud_garage_llp\Python\Barcode Excell\barcodes'
folder_name = input("Enter Folder name: ")

barcode_generator = BarcodeGenerator(excel_path, output_dir, folder_name)
barcode_generator.run()
