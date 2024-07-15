import pandas as pd
import qrcode
import os
from datetime import datetime
import shutil

def generate_qr_codes_from_excel(excel_path, output_dir, folder_name=None):
    df = pd.read_excel(excel_path)
    
    os.makedirs(output_dir, exist_ok=True)
    
    if folder_name:
        output_subdir = os.path.join(output_dir, folder_name)
    else:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_subdir = os.path.join(output_dir, timestamp)
        
    
    if os.path.exists(output_subdir):
        print(f'Folder "{folder_name}" already exists. Deleting contents...')
        shutil.rmtree(output_subdir)  

    os.makedirs(output_subdir, exist_ok=True)

    for index, row in df.iterrows():
        qrcode_details = ', '.join(row.astype(str).values)
        filename = os.path.join(output_subdir, f'qr_code_image_{index + 1}.png')

        img = qrcode.make(qrcode_details)
        img.save(filename)

    print(f'QR codes generated successfully and saved in the "{os.path.basename(output_subdir)}" directory.')

excel_path = r'D:\PROJECT\cloud_garage_llp\Python\QR_code Excel\qrcodeS.xlsx'
output_dir = r'D:\PROJECT\cloud_garage_llp\Python\QR_code Excel\qrcodes'

folder_name = input("Enter Folder name: ")
generate_qr_codes_from_excel(excel_path, output_dir, folder_name)
