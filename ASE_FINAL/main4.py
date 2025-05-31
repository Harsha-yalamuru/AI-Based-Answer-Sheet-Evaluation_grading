import cv2
import os
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

def split_image_by_horizontal_lines(image_path, output_dir):
    print(f"Reading image from: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or failed to load.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Preprocessing
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Save edge image for debugging
    cv2.imwrite("debug_edges.jpg", edges)

    print("Running HoughLinesP...")
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=80,
        minLineLength=img.shape[1] // 4,
        maxLineGap=20
    )

    if lines is None:
        raise ValueError("No lines detected.")

    print(f"Total lines detected: {len(lines)}")

    # Filter near-horizontal lines
    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y2 - y1) < 10:
            horizontal_lines.append(int(y1))

    print(f"Horizontal lines detected at y-positions: {horizontal_lines}")

    lines_y = sorted(set(horizontal_lines))
    print(f"Unique sorted horizontal line y-values: {lines_y}")

    if len(lines_y) < 2:
        raise ValueError(f"Couldn't detect enough horizontal lines. Found only {len(lines_y)}.")

    os.makedirs(output_dir, exist_ok=True)

    # Ensure top and bottom boundaries are included
    if 0 not in lines_y:
        lines_y = [0] + lines_y
    if img.shape[0] not in lines_y:
        lines_y.append(img.shape[0])

    print(f"Final split positions (y): {lines_y}")

    # Split and save segments
    segment_index = 1
    for i in range(len(lines_y) - 1):
        top = int(lines_y[i])
        bottom = int(lines_y[i + 1])
        if bottom - top > 10:
            segment = img[top:bottom, :]
            output_file = os.path.join(output_dir, f"{segment_index}.png")
            success = cv2.imwrite(output_file, segment)
            print(f"Saving segment {segment_index}: {'Success' if success else 'Failed'}")
            segment_index += 1

    print(f"Image successfully split into {segment_index - 1} segments.")


def convert_pdf_to_image(pdf_path, output_image_path):
    print(f"Converting PDF to image: {pdf_path}")
    images = convert_from_path(pdf_path)
    if not images:
        raise ValueError("Failed to convert PDF to image.")
    images[0].save(output_image_path, 'JPEG')
    print(f"Saved first page as image: {output_image_path}")
    return output_image_path


def run_split(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    if input_path.lower().endswith(".pdf"):
        temp_image_path = os.path.join(output_dir, "converted_page.jpg")
        image_path = convert_pdf_to_image(input_path, temp_image_path)
    else:
        image_path = input_path

    split_image_by_horizontal_lines(image_path, output_dir)


# Example usage
if __name__ == "__main__":
    run_split(
        input_path="C:/Users/harsh/Desktop/ASE_FINAL/test_img.jpg",  # or PDF path
        output_dir="C:/Users/harsh/Desktop/ASE_FINAL/results"
    )
