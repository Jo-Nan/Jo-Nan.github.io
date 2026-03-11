import qrcode
from PIL import Image

url = "https://jo-nan.github.io/"
logo_path = "assets/profile.png"
output_path = "assets/qrcode.png"

# Generate QR code
qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# Add logo if exists
try:
    logo = Image.open(logo_path)
    
    # Calculate logo size (max 1/4 of QR code width/height to ensure readability)
    basewidth = int(img.size[0] / 4)
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
    
    # Calculate position
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    
    # Create a white background for logo to stand out
    logo_bg = Image.new('RGB', (logo.size[0] + 10, logo.size[1] + 10), 'white')
    img.paste(logo_bg, (pos[0] - 5, pos[1] - 5))
    img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    print(f"✅ Generated QR code with logo from {logo_path}")
except Exception as e:
    print(f"⚠️ Could not add logo: {e}. Generating standard QR code.")

img.save(output_path)
print(f"✅ QR code saved to {output_path}")
