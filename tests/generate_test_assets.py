import os
from PIL import Image

def generate_assets():
    test_dir = os.path.join(os.path.dirname(__file__), 'test_images')
    os.makedirs(test_dir, exist_ok=True)
    
    # 1. Create a valid JPEG (represents real image)
    real_img_path = os.path.join(test_dir, 'test_real.jpg')
    img_real = Image.new('RGB', (224, 224), color=(34, 139, 34))  # Forest Green
    img_real.save(real_img_path, format='JPEG')
    print(f"Generated: {real_img_path}")
    
    # 2. Create a valid PNG (represents fake image)
    fake_img_path = os.path.join(test_dir, 'test_fake.png')
    img_fake = Image.new('RGB', (224, 224), color=(220, 20, 60))  # Crimson
    img_fake.save(fake_img_path, format='PNG')
    print(f"Generated: {fake_img_path}")
    
    # 3. Create a spoofed file: a plain text file disguised with a PNG extension
    # (to test magic byte signature check failure)
    malicious_path = os.path.join(test_dir, 'test_malicious.png')
    with open(malicious_path, 'w', encoding='utf-8') as f:
        f.write("This is a plain text file pretending to be a PNG. It lacks PNG magic bytes, so it should fail the signature verification.")
    print(f"Generated: {malicious_path}")

if __name__ == '__main__':
    generate_assets()
