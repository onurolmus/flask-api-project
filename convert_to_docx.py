import pypandoc
import os

print("Downloading pandoc...")
pypandoc.download_pandoc()

# Paths
md_path = "/mnt/c/Users/Onur Olmuş/.gemini/antigravity/brain/7d8497b7-8792-4456-b1bf-99dccb7ea9f8/staj_raporu_taslagi.md"
docx_path = "/mnt/c/Users/Onur Olmuş/.gemini/antigravity/brain/7d8497b7-8792-4456-b1bf-99dccb7ea9f8/staj_raporu_taslagi.docx"

print(f"Converting {md_path} to docx...")
try:
    pypandoc.convert_file(md_path, 'docx', outputfile=docx_path)
    print("Success! File saved to:", docx_path)
except Exception as e:
    print("Error during conversion:", e)
