import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os

def generate_barcode_from_excel(excel_path, output_dir):
    df = pd.read_excel(excel_path)  
    
    
    os.makedirs(output_dir, exist_ok=True)
    
  
    for index, row in df.iterrows():
        barcode_number = str(row['Barcode'])  
        filename = f'{output_dir}/barcode_image_{index + 1}' 
        
        
        PRODUCT = barcode.get_barcode_class('ean13')
        product = PRODUCT(barcode_number, writer=ImageWriter())
        barcode_image = product.save(filename)
        
        print(f"Barcode {barcode_number} saved as {filename}.png")


excel_path = r'D:\PROJECT\cloud_garage_llp\Python\Barcode Excell\barcodes.xlsx' 
output_dir = r'D:\PROJECT\cloud_garage_llp\Python\Barcode Excell\barcodes'       

generate_barcode_from_excel(excel_path, output_dir)
