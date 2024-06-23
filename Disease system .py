import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Define the DiseaseSystemApp class
class DiseaseSystemApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Disease System")

        # Initialize variables to store table dimensions, data, headers, patients, and records
        self.num_rows = 0
        self.num_cols = 0
        self.data = []
        self.headers = []
        self.patients = []
        self.records = []

        # Create and layout the widgets
        self.create_widgets()

    # Create and layout the widgets
    def create_widgets(self):
        self.master.configure(bg='#f0f0f0')
        self.master.geometry('900x600+300+100')  # Set window size and position
        self.master.iconbitmap("E:\education fils\graduation project\clipboard.ico")  # Set window icon

        # Labels and entries for number of rows and columns
        tk.Label(self.master, text="Number of Rows:", bg='#f0f0f0').place(x=20, y=10)
        self.rows_entry = tk.Entry(self.master, bg='white')
        self.rows_entry.place(x=130, y=10)

        tk.Label(self.master, text="Number of Columns:", bg='#f0f0f0').place(x=280, y=10)
        self.cols_entry = tk.Entry(self.master, bg='white')
        self.cols_entry.place(x=400, y=10)

        # Buttons for creating table, adding data, uploading XLSX, processing data, and downloading results
        self.create_table_button = tk.Button(self.master, text="Create Table", command=self.create_table, bg='#008CBA', fg='white', borderwidth=0, highlightthickness=0, cursor="hand2")
        self.create_table_button.place(x=550, y=9)

        self.add_button = tk.Button(self.master, text="Add Data", command=self.add_data, bg='#4CAF50', fg='white', borderwidth=0, highlightthickness=0, cursor="hand2")
        self.add_button.place(x=50, y=50)

        self.upload_button = tk.Button(self.master, text="Upload XLSX", command=self.upload_data, bg='#4CAF50', fg='white', borderwidth=0, highlightthickness=0, cursor="hand2")
        self.upload_button.place(x=150, y=50)

        self.process_button = tk.Button(self.master, text="Process Data", command=self.process_data, bg='#4CAF50', fg='white', borderwidth=0, highlightthickness=0, cursor="hand2")
        self.process_button.place(x=300, y=50)

        self.download_button = tk.Button(self.master, text="Download Results", command=self.download_results, bg='#4CAF50', fg='white', borderwidth=0, highlightthickness=0, cursor="hand2")
        self.download_button.place(x=450, y=50)

        # Canvas and scrollbars for table display
        self.canvas = tk.Canvas(self.master, bg='#f0f0f0', width=600)
        self.table_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        self.yscrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.xscrollbar = tk.Scrollbar(self.master, orient="horizontal", command=self.canvas.xview)

        # Configure canvas and scrollbars
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)
        self.canvas.configure(xscrollcommand=self.xscrollbar.set)

        self.canvas.place(x=25, y=100)
        self.yscrollbar.place(x=5, y=130, height=200)
        self.xscrollbar.place(x=150, y=375, width=350)

        # Bind frame configuration event to update the scroll region
        self.table_frame.bind("<Configure>", self.on_frame_configure)

        # Label to display results
        self.result_label = tk.Label(self.master, text="", justify="left", bg='#f0f0f0', wraplength=800)
        self.result_label.place(x=680, y=100)

    # Update the scroll region of the canvas when the frame is resized
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Create an empty table with the specified number of rows and columns
    def create_table(self):
        try:
            self.num_rows = int(self.rows_entry.get())
            self.num_cols = int(self.cols_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rows and columns.")
            return

        # Clear any existing table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Create a new table with the specified dimensions
        self.table = []
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                entry = tk.Entry(self.table_frame, width=20, bg='white')
                entry.grid(row=i, column=j, padx=5, pady=5)
                row.append(entry)
            self.table.append(row)

    # Add data from the table to the internal data structure
    def add_data(self):
        self.data = []
        for i in range(self.num_rows):
            row_data = []
            for j in range(self.num_cols):
                data = self.table[i][j].get()
                row_data.append(data)
            self.data.append(row_data)
        messagebox.showinfo("Success", "Data added successfully!")

    # Upload data from an XLSX file and display it in the table
    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                self.headers = df.columns.tolist()
                self.data = [self.headers] + df.values.tolist()
                self.num_rows, self.num_cols = len(self.data), len(self.headers)
                self.display_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    # Display the data in the table
    def display_data(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.table = []
        for i, row_data in enumerate(self.data):
            row = []
            for j, cell_data in enumerate(row_data):
                entry = tk.Entry(self.table_frame, width=20, bg='white')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(tk.END, cell_data)
                row.append(entry)
            self.table.append(row)

    # Process the data and display the results
    def process_data(self):
        if not self.data:
            messagebox.showerror("Error", "No data to process.")
            return

        try:
            headers, patients, records, last = self.parse_data(self.data)
            last_column_name = last[-1]  # Extract the name of the last column
            U, B, disease_yes, disease_no = self.create_sets(headers, patients, records)
            partitions = self.calculate_partitions(patients, records)

            def_yes, pos_yes = self.get_definitely_and_possibly(disease_yes, partitions)
            def_no, pos_no = self.get_definitely_and_possibly(disease_no, partitions)

            self.results = (
                ""
                f"Patients (U): {U}\n"
                f"Attributes (B): {B}\n"
                f"{last_column_name} Yes: {disease_yes}\n"
                f"{last_column_name} No: {disease_no}\n"
                f"Partitions (U|B): {partitions}\n\n"
                f"Definitively have {last_column_name} (Yes): {def_yes}\n"
                f"Possibly have {last_column_name} (Yes): {pos_yes}\n"
                f"Definitively don’t have {last_column_name} (No): {def_no}\n"
                f"Possibly don’t have {last_column_name} (No): {pos_no}\n"
            )
            self.result_label.config(text=self.results)

            self.results_df = pd.DataFrame({
                "Patients (U)": list(U),
                f"Definitively have {last_column_name} (Yes)": list(def_yes),
                f"Possibly have {last_column_name} (Yes)": list(pos_yes),
                f"Definitively don’t have {last_column_name} (No)": list(def_no),
                f"Possibly don’t have {last_column_name} (No)": list(pos_no)
            })
            # Call download_results function and pass results as an argument
            self.download_results()

        except:
            None

    # Download the results to an XLSX file
    def download_results(self):
        if not self.data:
            messagebox.showerror("Error", "No results to download.")
            return

        # Convert the table data to a DataFrame
        table_df = pd.DataFrame(self.data[1:], columns=self.data[0])

        # Initialize results_summary
        results_summary = "No results available"

        # Create a DataFrame for the detailed results summary
        if hasattr(self, 'results'):
            results_summary = self.results
            results_summary_df = pd.DataFrame({"Results Summary": [results_summary]})
        else:
            results_summary_df = pd.DataFrame({"Results Summary": [results_summary]})

        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if filename:
            with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                table_df.to_excel(writer, sheet_name='Original Data', index=False)
                if hasattr(self, 'results_df') and not self.results_df.empty:
                    self.results_df.to_excel(writer, sheet_name='Results', index=False)
                results_summary_df.to_excel(writer, sheet_name='Detailed Summary', index=False)

                # Get the xlsxwriter workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets['Detailed Summary']

                # Set the format for the cell to wrap text
                cell_format = workbook.add_format({'text_wrap': True, 'font_size': 16})
                worksheet.set_column('A:A', 100, cell_format)  # Adjust the width of the column

                # Calculate the number of rows needed for the results summary
                results_lines = results_summary.split('\n')
                num_rows = len(results_lines) + 5
                # Merge the cells to fit the detailed results summary
                worksheet.merge_range(0, 0, num_rows - 1, 0, results_summary, cell_format)  # Adjust range as needed

            messagebox.showinfo("Success", f"Results downloaded successfully to {filename}")

    # Parse the data into headers, patients, and records
    def parse_data(self, data):
        last = data[0][1:] # a variable incloud the last column
        headers = data[0][1:-1] # a variable incloud the symptoms only
        patients = [row[0] for row in data[1:]]
        records = [row[1:] for row in data[1:]]
        return headers, patients, records, last

    # Create sets of patients, attributes, and disease sets for Yes and No
    def create_sets(self, headers, patients, records):
        B = set(headers)
        U = {f"P{i+1}" for i in range(len(records))}
        disease_yes = {patients[i] for i in range(len(records)) if records[i][-1] == 'Yes'}
        disease_no = {patients[i] for i in range(len(records)) if records[i][-1] == 'No'}
        return U, B, disease_yes, disease_no

    # Calculate the partitions of the patients based on their records
    def calculate_partitions(self, patients, records):
        partitions = []
        unique_records = []
        for record in records:
            if record[:-1] not in unique_records:  # Exclude the last column
                unique_records.append(record[:-1])  # Exclude the last column
        for unique_record in unique_records:
            partition = {patients[i] for i in range(len(records)) if records[i][:-1] == unique_record}  # Exclude the last column
            partitions.append(partition)
        return partitions

    # Get the equivalence class of a patient from the partitions
    def get_equivalence_class(self, patient, partitions):
        for partition in partitions:
            if patient in partition:
                return partition
        return set()

    # Get definitely and possibly sets for disease
    def get_definitely_and_possibly(self, Fµ_set, partitions):
        definitely = set()
        possibly = set()
    
        for partition in partitions:
            if all(patient in Fµ_set for patient in partition):
                definitely.update(partition)
                possibly.update(partition)
            elif not Fµ_set.isdisjoint(partition):
                possibly.update(partition)
        return definitely, possibly

# Main function to start the application
def main():
    root = tk.Tk()
    app = DiseaseSystemApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
