import qrcode

url = input("Enter the URL to generate QR code: ").strip()
file_path = "/Users/abhinav/Abhinav/Mini Project/QRcode/qr_code.png"

qr = qrcode.QRCode()
qr.add_data(url)

img = qr.make_image()
img.save(file_path)

print(f"QR code generated and saved to {file_path}")