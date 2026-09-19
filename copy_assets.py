import os
import glob
from PIL import Image

brain_dir = r"C:\Users\Avinash\.gemini\antigravity\brain\aeb3f2b1-b6cc-4b77-b0aa-a223f41cd68d"
dest_dir = r"C:\Users\Avinash\Desktop\superapps\frontend\public\assets\products"
os.makedirs(dest_dir, exist_ok=True)

mapping = {
    "rice_bag": "rice.png",
    "dal_lentils": "dal.png",
    "cooking_oil": "cooking_oil.png",
    "sugar_bowl": "sugar.png",
    "biscuits_packet": "biscuits.png",
    "soap_bar": "soap.png",
    "salt_packet": "salt.png",
    "tea_powder": "tea_powder.png",
    "atta_flour": "atta.png",
    "detergent_powder": "detergent_powder.png",
    "unknown_product": "unknown.png",
}

for prefix, dest_name in mapping.items():
    matches = glob.glob(os.path.join(brain_dir, f"{prefix}*.*"))
    if matches:
        src = matches[0]
        dest_path = os.path.join(dest_dir, dest_name)
        img = Image.open(src)
        img.save(dest_path, "PNG")
        print(f"Copied {os.path.basename(src)} -> {dest_name}")
        if "_" in dest_name:
            dash_name = dest_name.replace("_", "-")
            img.save(os.path.join(dest_dir, dash_name), "PNG")
            print(f"Also saved alias: {dash_name}")
    else:
        print(f"NOT FOUND: {prefix}")

print("Assets copying completed!")
