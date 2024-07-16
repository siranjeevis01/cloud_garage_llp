import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os
import shutil
from datetime import datetime

def generate_barcode_from_excel(excel_path, output_dir, folder_name):
    df = pd.read_excel(excel_path)
    new_output_dir = os.path.join(output_dir, folder_name)
    

    if os.path.exists(new_output_dir):
        shutil.rmtree(new_output_dir)
        print(f"Existing folder '{new_output_dir}' deleted.")
    

    os.makedirs(new_output_dir, exist_ok=True)
    
    for index, row in df.iterrows():
        barcode_number = str(row['Barcode'])  
        filename = os.path.join(new_output_dir, f'barcode_image_{index + 1}') 
        
        PRODUCT = barcode.get_barcode_class('ean13')
        product = PRODUCT(barcode_number, writer=ImageWriter())
        barcode_image = product.save(filename)
        
        print(f"Barcode {barcode_number} saved as {filename}.png")

excel_path = r'D:\PROJECT\cloud_garage_llp\Python\Barcode Excell\barcodes.xlsx' 
output_dir = r'D:\PROJECT\cloud_garage_llp\Python\Barcode Excell\barcodes'

folder_name = input("Enter Folder name: ")
generate_barcode_from_excel(excel_path, output_dir, folder_name)
