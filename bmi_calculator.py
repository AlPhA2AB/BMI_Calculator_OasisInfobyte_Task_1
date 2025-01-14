import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import datetime

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator By Ayon")
        self.data = {}

        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=10)

        tk.Label(self.info_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.info_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.info_frame, text="Height (m):").grid(row=1, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(self.info_frame)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.info_frame, text="Weight (kg):").grid(row=2, column=0, padx=5, pady=5)
        self.weight_entry = tk.Entry(self.info_frame)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        self.calculate_button = tk.Button(self.info_frame, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, columnspan=2, pady=10)

        self.output_frame = tk.Frame(root)
        self.output_frame.pack(pady=10)

        tk.Label(self.output_frame, text="BMI:").grid(row=0, column=0, padx=5, pady=5)
        self.bmi_label = tk.Label(self.output_frame, text="--")
        self.bmi_label.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.output_frame, text="Status:").grid(row=1, column=0, padx=5, pady=5)
        self.status_label = tk.Label(self.output_frame, text="--")
        self.status_label.grid(row=1, column=1, padx=5, pady=5)

        self.data_frame = tk.Frame(root)
        self.data_frame.pack(pady=10)

        self.view_data_button = tk.Button(self.data_frame, text="View Data", command=self.view_data)
        self.view_data_button.pack(side=tk.LEFT, padx=5)

        self.plot_data_button = tk.Button(self.data_frame, text="Plot Data", command=self.plot_data)
        self.plot_data_button.pack(side=tk.LEFT, padx=5)

    def calculate_bmi(self):
        name = self.name_entry.get().strip()
        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            bmi = round(weight / (height ** 2), 2)
            status = self.get_bmi_status(bmi)

            self.bmi_label.config(text=str(bmi))
            self.status_label.config(text=status)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if name not in self.data:
                self.data[name] = []
            self.data[name].append({"timestamp": timestamp, "bmi": bmi})

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for height and weight.")

    def get_bmi_status(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def view_data(self):
        if not self.data:
            messagebox.showinfo("No Data", "No data to display.")
            return

        data_window = tk.Toplevel(self.root)
        data_window.title("BMI Data")

        tree = ttk.Treeview(data_window, columns=("Name", "Timestamp", "BMI"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Timestamp", text="Timestamp")
        tree.heading("BMI", text="BMI")

        for name, records in self.data.items():
            for record in records:
                tree.insert("", tk.END, values=(name, record["timestamp"], record["bmi"]))

        tree.pack(fill=tk.BOTH, expand=True)

    def plot_data(self):
        if not self.data:
            messagebox.showinfo("No Data", "No data to plot.")
            return

        plt.figure(figsize=(10, 6))
        for name, records in self.data.items():
            try:
                timestamps = [datetime.datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S") for r in records]
                bmis = [r["bmi"] for r in records]

                sorted_data = sorted(zip(timestamps, bmis))
                sorted_timestamps, sorted_bmis = zip(*sorted_data)

                plt.plot(sorted_timestamps, sorted_bmis, label=name)
            except Exception as e:
                messagebox.showerror("Plot Error", f"Error plotting data for {name}: {str(e)}")
                return

        plt.gcf().autofmt_xdate()
        plt.xlabel("Timestamp", fontsize=12)
        plt.ylabel("BMI", fontsize=12)
        plt.title("BMI Trend Analysis", fontsize=14)
        plt.legend(title="Users")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
