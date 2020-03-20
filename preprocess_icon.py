import os
import cv2
from io import BytesIO
import cairosvg
from PIL import Image

if __name__ == '__main__':
    for f in os.listdir('raw_icons/'):
        file_path = os.path.join('raw_icons', f)
        output_file_path = os.path.join('icons', os.path.splitext(f)[0] + ".png")

        if file_path.endswith('.svg'):
            out = BytesIO()
            cairosvg.svg2png(url=file_path, write_to=output_file_path)
            
            img = cv2.imread(output_file_path)
            h, w, _ = img.shape
            resized_img = cv2.resize(img, (32, 32 * h//w))
            
            cv2.imwrite(output_file_path, resized_img)
        else:                
            img = cv2.imread(file_path)
            h, w, _ = img.shape
            resized_img = cv2.resize(img, (32, 32 * h//w))
            
            cv2.imwrite(output_file_path, resized_img)
    
    print("Done!")

