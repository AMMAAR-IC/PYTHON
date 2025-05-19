import qrcode

# Data for SMS QR code
sms_data = "sms:?&body=hello"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)
qr.add_data(sms_data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("sms_hello_qr.png")
