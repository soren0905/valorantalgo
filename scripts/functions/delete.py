import os

def delete_excel_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

def main():
    directory = r'C:\Users\soren\Projects\ValAlgo\data\Excel'  # Update this path to where your Excel files are stored
    delete_excel_files(directory)
    print("All Excel files have been deleted.")

if __name__ == '__main__':
    main()
