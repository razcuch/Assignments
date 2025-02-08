import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Button, Entry, messagebox, colorchooser

# Function to load the Excel file
def select_file():
    global file_path, data
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        file_label.config(text=f"Selected File: {file_path}")
        # Load the Excel file
        data = pd.read_excel(file_path, skiprows=3, usecols=[0, 1, 10, 11])  # Columns 1, 2, 11, 12 (0-indexed)
        data.columns = ['ml1', 'mAU1', 'ml2', 'fraction']  # Renaming columns for clarity
        # Convert 'ml1' and 'ml2' columns to numeric
        data['ml1'] = pd.to_numeric(data['ml1'], errors='coerce')
        data['ml2'] = pd.to_numeric(data['ml2'], errors='coerce')
    else:
        file_label.config(text="No file selected.")

# Function to pick a color
def pick_color():
    global fill_color
    color_code = colorchooser.askcolor(title="Choose Fill Color")
    if color_code[1]:  # If a color is selected
        fill_color = color_code[1]
        color_label.config(text=f"Selected Color: {fill_color}", bg=fill_color)

# Function to generate the graph
def generate_graph():
    try:
        # Get the input values
        ml_start = float(ml_start_entry.get())
        ml_end = float(ml_end_entry.get())
        fraction_start = fraction_start_entry.get()
        fraction_end = fraction_end_entry.get()

        # Extract data for table1 (first table)
        table1 = data.iloc[:, [0, 1]]  # Assuming ml is in the first column and mAU in the second column
        table1.columns = ['ml', 'mAU']

        # Extract data for table2 (ml2 and fraction columns)
        table2 = data.iloc[:, [2, 3]]  # ml2 is column 7, fraction is column 8
        table2.columns = ['ml2', 'fraction']

        # Filter table1 to only include data between ml_start and ml_end
        table1_filtered = table1[(table1['ml'] >= ml_start) & (table1['ml'] <= ml_end)]

        # Filter table2 to find the ml values corresponding to fraction_start and fraction_end
        if fraction_start not in table2['fraction'].values:
            raise ValueError(f"Fraction '{fraction_start}' not found in the dataset.")
        if fraction_end not in table2['fraction'].values:
            raise ValueError(f"Fraction '{fraction_end}' not found in the dataset.")

        fraction_start_ml = table2[table2['fraction'] == fraction_start]['ml2'].min()
        fraction_end_ml = table2[table2['fraction'] == fraction_end]['ml2'].max()

        # Ensure we have valid ml range for the fractions
        if fraction_start_ml > fraction_end_ml:
            raise ValueError(f"The starting fraction ml value ({fraction_start_ml}) is greater than the ending fraction ml value ({fraction_end_ml}).")

        # Filter table1 again to only include data between fraction_start_ml and fraction_end_ml for the area coloring
        table1_colored_area = table1_filtered[(table1_filtered['ml'] >= fraction_start_ml) & (table1_filtered['ml'] <= fraction_end_ml)]

        # Plot the mAU vs ml curve for the filtered range
        plt.figure(figsize=(20, 6))
        plt.plot(table1_filtered['ml'], table1_filtered['mAU'], color='black')

        # Color the area under the curve between the fraction_start_ml and fraction_end_ml
        plt.fill_between(table1_colored_area['ml'], table1_colored_area['mAU'], color=fill_color, alpha=0.6)

        # Set the y-axis to start from 0
        plt.ylim(bottom=0)

        # Set the x-axis to be exactly around the plot's range (from ml_start to ml_end)
        plt.xlim(left=ml_start, right=ml_end)

        # Add labels and title
        plt.xlabel('mL')
        plt.ylabel('A 280')
        plt.legend()

        # Ask user where to save the plot
        output_file = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg"), ("PDF files", "*.pdf")])
        if output_file:
            # Save the plot as a vector file (SVG or PDF)
            plt.savefig(output_file, format='svg')
            # Optionally, you can save as PDF if needed:
            # plt.savefig(output_file, format='pdf')
            messagebox.showinfo("Success", f"Plot saved as {output_file}")

        # Show the plot
        plt.show()

    except ValueError as ve:
        messagebox.showerror("Error", f"Invalid input: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Initialize the main window (GUI)
root = Tk()
root.title("Excel Data Visualization Tool")

file_path = ""
data = None
fill_color = "#ffcf8d"  # Default fill color

# GUI Elements
file_label = Label(root, text="No file selected.")
file_label.pack(pady=5)

select_file_button = Button(root, text="Select Excel File", command=select_file)
select_file_button.pack(pady=5)

Label(root, text="Enter starting ml value:").pack(pady=5)
ml_start_entry = Entry(root)
ml_start_entry.pack()

Label(root, text="Enter ending ml value:").pack(pady=5)
ml_end_entry = Entry(root)
ml_end_entry.pack()

Label(root, text="Enter starting fraction name:").pack(pady=5)
fraction_start_entry = Entry(root)
fraction_start_entry.pack()

Label(root, text="Enter ending fraction name:").pack(pady=5)
fraction_end_entry = Entry(root)
fraction_end_entry.pack()

color_button = Button(root, text="Pick Fill Color", command=pick_color)
color_button.pack(pady=5)

color_label = Label(root, text=f"Selected Color: {fill_color}", bg=fill_color)
color_label.pack(pady=5)

generate_button = Button(root, text="Generate Graph", command=generate_graph)
generate_button.pack(pady=10)

# Run the GUI
root.mainloop()
