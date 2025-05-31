import subprocess
import sys  # To get the current Python interpreter path

def run_script(script_name):
    print(f"\nRunning {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{script_name} ran successfully.")
    else:
        print(f"Error while running {script_name}:\n{result.stderr}")
        exit(1)

if __name__ == "__main__":
    run_script("main4.py")                 # Step 1: Split handwritten image into lines
    run_script("new_handwritten_ocr.py")   # Step 2: Perform OCR on each line
    run_script("grade_extracted_text.py")  # Step 3: Grade the OCR results against schema

    print("\n✅ All steps completed successfully.")
