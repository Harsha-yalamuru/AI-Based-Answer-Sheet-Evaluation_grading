import os
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load model and processor from local folder
model_path = "./trocr-large-handwritten"
processor = TrOCRProcessor.from_pretrained(model_path)
model = VisionEncoderDecoderModel.from_pretrained(model_path)

def run_ocr(image_folder="C:/Users/harsh/Desktop/ASE_FINAL/results", output_file="extracted_texts.txt"):
    # Get list of image files
    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    # Prepare to write to output file
    with open(output_file, "w", encoding="utf-8") as out_file:
        # out_file.write("================ EXTRACTED TEXT ================\n")

        for filename in image_files:
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path).convert("RGB")
            pixel_values = processor(images=image, return_tensors="pt").pixel_values

            with torch.no_grad():
                generated_ids = model.generate(pixel_values)

            # Define known noise values (you can expand this list as needed)
            noise_tokens = {"1961", "0 0", "#"}

            # Extract and clean the text
            extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

            # Remove noise tokens from the text
            for token in noise_tokens:
                extracted_text = extracted_text.replace(token, "")

            # Final cleanup
            cleaned_text = extracted_text.strip()

            # Skip if empty or junk
            if not cleaned_text or (cleaned_text.isdigit() and len(cleaned_text) <= 4):
                print(f"Skipping irrelevant image: {filename} -> {cleaned_text}")
                continue

            # Print and save the result
            section = f"{cleaned_text} "
            print(section)
            out_file.write(section)

        # out_file.write("\n================================================\n")

    print(f"\nAll extracted text saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    run_ocr()
