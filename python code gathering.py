import os

def read_python_files(directory):
    # Open the output text file
    with open('python_files_output.txt', 'w') as output_file:
        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):  # Check for Python files
                    file_path = os.path.join(root, file)
                    output_file.write(f"File: {file_path}\n")
                    output_file.write("="*50 + "\n")
                    # Read and write the content of the Python file
                    with open(file_path, 'r') as f:
                        output_file.write(f.read())
                    output_file.write("\n\n" + "="*50 + "\n\n")

if __name__ == "__main__":
    directory = "../AIGraphSearchingAlgorithms"
    read_python_files(directory)
    
    print("Output saved to python_files_output.txt")
