from PIL import Image

# Load the image
image_path = '84d69a73-48a8-4b51-a75c-fa93bba9bdcc.png'
try:
    with Image.open(image_path) as img:
        print(f"Image dimensions: {img.size}")  # Print the dimensions
except Exception as e:
    print(f"Error loading image: {e}")
