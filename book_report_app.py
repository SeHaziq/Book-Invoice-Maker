import os
from docx import Document
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QMessageBox
)
from PyQt5.QtGui import QColor, QFont
import sys
from datetime import datetime

class BookReportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sebut Harga Generator")
        self.setGeometry(100, 100, 950, 700)  # Window position (x=100, y=100) and size (width=900, height=500)
        self.book_details = []
        self.selected_row = None  # To track the selected row for editing
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

       # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Book Name")
        self.name_input.setFont(QFont("Arial", 12))  # Make font larger for book name input
        self.name_input.returnPressed.connect(self.focus_next_input)  # Automatically move to the next input when Enter is pressed
        
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        self.quantity_input.setFont(QFont("Arial", 12))  # Set a larger font for better readability
        self.quantity_input.returnPressed.connect(self.focus_next_input)
        
        self.price_first_input = QLineEdit()
        self.price_first_input.setPlaceholderText("Price per unit (AIFARNIS, RM)")
        self.price_first_input.setFont(QFont("Arial", 12))  # Set font size
        self.price_first_input.returnPressed.connect(self.focus_next_input)

        self.price_second_input = QLineEdit()
        self.price_second_input.setPlaceholderText("Price per unit (Pustaka Alamanda, RM)")
        self.price_second_input.setFont(QFont("Arial", 12))  # Set font size
        self.price_second_input.returnPressed.connect(self.focus_next_input)

        self.price_third_input = QLineEdit()
        self.price_third_input.setPlaceholderText("Price per unit (Pustaka Dagang, RM)")
        self.price_third_input.setFont(QFont("Arial", 12))  # Set font size
        self.price_third_input.returnPressed.connect(self.focus_next_input)

        # Buttons
        add_button = QPushButton("Add Book")
        add_button.clicked.connect(self.add_book)
        
        update_button = QPushButton("Update Book")
        update_button.clicked.connect(self.update_book)
        
        delete_button = QPushButton("Delete Book")
        delete_button.clicked.connect(self.delete_book)
        delete_button.setStyleSheet("background-color: red; color: white;")  # Set button color to red

        generate_button = QPushButton("Generate Report")
        generate_button.clicked.connect(self.generate_report)
        generate_button.setStyleSheet("background-color: green; color: white;")  # Set button color to red

        # Button layout (Add, Update, Delete)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "Book Name", "Quantity", "Harga (Aifarnis)", 
            "Price (Alamanda)", "Price (Dagang)"
        ])
        self.table.cellClicked.connect(self.select_row)

        # Set column widths
        self.table.setColumnWidth(0, 400)  # "Book Name" column
        self.table.setColumnWidth(1, 70)   # "Quantity" column
        self.table.setColumnWidth(2, 140)  # "Harga (Aifarnis)" column
        self.table.setColumnWidth(3, 140)  # "Price (Alamanda)" column
        self.table.setColumnWidth(4, 140)  # "Price (Dagang)" column

        # Add to layout
        layout.addWidget(QLabel("Enter book details:"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.price_first_input)
        layout.addWidget(self.price_second_input)
        layout.addWidget(self.price_third_input)
        layout.addLayout(button_layout)  # Add button layout
        layout.addWidget(self.table)
        layout.addWidget(generate_button)
        self.setLayout(layout)

    def focus_next_input(self):
        # Move focus to the next input when Enter is pressed
        current_widget = self.focusWidget()
        if current_widget == self.name_input:
            self.quantity_input.setFocus()
        elif current_widget == self.quantity_input:
            self.price_first_input.setFocus()
        elif current_widget == self.price_first_input:
            self.price_second_input.setFocus()
        elif current_widget == self.price_second_input:
            self.price_third_input.setFocus()
        else:
            self.add_book()  # If on last field, add the book

    def add_book(self):
        # Gather data
        name = self.name_input.text().strip()
        quantity_text = self.quantity_input.text().strip()
        price_first_text = self.price_first_input.text().strip()
        price_second_text = self.price_second_input.text().strip()
        price_third_text = self.price_third_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter the book name.")
            return

        try:
            quantity = int(quantity_text)
            price_first = float(price_first_text)
            price_second = float(price_second_text)
            price_third = float(price_third_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for quantity and prices.")
            return

        # Add to table and book list
        self.book_details.append({
            "name": name, 
            "quantity": quantity, 
            "price_first": price_first,
            "price_second": price_second,
            "price_third": price_third
        })
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(str(quantity)))
        self.table.setItem(row, 2, QTableWidgetItem(f"RM {price_first:.2f}"))
        self.table.setItem(row, 3, QTableWidgetItem(f"RM {price_second:.2f}"))
        self.table.setItem(row, 4, QTableWidgetItem(f"RM {price_third:.2f}"))

        # Clear inputs
        self.clear_inputs()
        self.name_input.setFocus()  # Focus back to Book Name

    def select_row(self, row, column):
        # Select the row for editing
        self.selected_row = row
        book = self.book_details[row]

        # Fill inputs with selected book details
        self.name_input.setText(book["name"])
        self.quantity_input.setText(str(book["quantity"]))
        self.price_first_input.setText(str(book["price_first"]))
        self.price_second_input.setText(str(book["price_second"]))
        self.price_third_input.setText(str(book["price_third"]))

    def update_book(self):
        if self.selected_row is None:
            QMessageBox.warning(self, "No Selection", "Please select a book to update.")
            return

        # Get the updated details from inputs
        name = self.name_input.text().strip()
        quantity_text = self.quantity_input.text().strip()
        price_first_text = self.price_first_input.text().strip()
        price_second_text = self.price_second_input.text().strip()
        price_third_text = self.price_third_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter the book name.")
            return

        try:
            quantity = int(quantity_text)
            price_first = float(price_first_text)
            price_second = float(price_second_text)
            price_third = float(price_third_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for quantity and prices.")
            return

        # Update book details
        self.book_details[self.selected_row] = {
            "name": name, 
            "quantity": quantity, 
            "price_first": price_first,
            "price_second": price_second,
            "price_third": price_third
        }
        
        # Update table display
        self.table.setItem(self.selected_row, 0, QTableWidgetItem(name))
        self.table.setItem(self.selected_row, 1, QTableWidgetItem(str(quantity)))
        self.table.setItem(self.selected_row, 2, QTableWidgetItem(f"RM {price_first:.2f}"))
        self.table.setItem(self.selected_row, 3, QTableWidgetItem(f"RM {price_second:.2f}"))
        self.table.setItem(self.selected_row, 4, QTableWidgetItem(f"RM {price_third:.2f}"))

        # Clear selection and inputs
        self.selected_row = None
        self.clear_inputs()

    def delete_book(self):
        if self.selected_row is None:
            QMessageBox.warning(self, "No Selection", "Please select a book to delete.")
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Are you sure you want to delete the book '{self.book_details[self.selected_row]['name']}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Remove from book_details and table
            del self.book_details[self.selected_row]
            self.table.removeRow(self.selected_row)
            self.selected_row = None
            self.clear_inputs()
            QMessageBox.information(self, "Deleted", "Book has been deleted successfully.")

    def clear_inputs(self):
        self.name_input.clear()
        self.quantity_input.clear()
        self.price_first_input.clear()
        self.price_second_input.clear()
        self.price_third_input.clear()

    def generate_report(self):
        if not self.book_details:
            QMessageBox.warning(self, "No Data", "No books added.")
            return

        # Load existing template
        # template_path = "Book_Report_Template.docx"
        script_dir = os.path.dirname(os.path.realpath(__file__))
        template_path = os.path.join(script_dir, "Book_Report_Template.docx")
        if not os.path.exists(template_path):
            QMessageBox.warning(self, "Template Not Found", f"The template '{template_path}' does not exist.")
            return

        doc = Document(template_path)

        # Calculate subtotals and fill tables
        total_first = self.fill_table(doc, "firsttable", "price_first")
        total_second = self.fill_table(doc, "secondtable", "price_second")
        total_third = self.fill_table(doc, "thirdtable", "price_third")

        # Replace subtotal placeholders
        self.replace_text(doc, 'asubtotal', f"{total_first:.2f}")
        self.replace_text(doc, 'bsubtotal', f"{total_second:.2f}")
        self.replace_text(doc, 'csubtotal', f"{total_third:.2f}")

        # Save the modified document with a unique name
        unique_filename = self.create_unique_filename()
        try:
            doc.save(unique_filename)
            QMessageBox.information(self, "Success", f"Document saved as '{unique_filename}'.")

            # Open the document automatically after saving
            # self.open_generated_file(unique_filename)
            # Reminder
            reminder_text = (
            "Peringatan :\n"
            "1. Baiki saiz font dalam table\n"
            "2. Baiki text supaya center\n"
            "3. Nama Cikgu perlu letak"
        )
        
            # Ask if the user wants to open the file
            reply = QMessageBox.question(
                self, 'Open Generated File',
                f"{reminder_text}\n\nDo you want to open the generated file '{unique_filename}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.open_generated_file(unique_filename)

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"An error occurred while saving the document: {e}")

    def open_generated_file(self, filename):
        """Open the generated file with the default program."""
        if sys.platform == "win32":
            os.startfile(filename)
        elif sys.platform == "darwin":
            subprocess.call(["open", filename])
        else:
            subprocess.call(["xdg-open", filename])

    def fill_table(self, doc, placeholder, price_key):
        # Locate the specific table with the given placeholder and calculate subtotal
        subtotal = 0.0
        for table in doc.tables:
            table_found = False
            for row in table.rows:
                for cell in row.cells:
                    if placeholder in cell.text:
                        table_found = True
                        break
                if table_found:
                    break

            if table_found:
                # Populate the table with book data
                for i, book in enumerate(self.book_details):
                    if i + 1 < len(table.rows):  # Check if row exists
                        row = table.rows[i + 1]
                    else:
                        row = table.add_row()

                    # Fill cells in order and calculate subtotal
                    row.cells[0].text = str(i + 1)  # Book Number
                    row.cells[1].text = book["name"]
                    row.cells[2].text = str(book["quantity"])
                    row.cells[3].text = f"RM {book[price_key]:.2f}"  # Specific price
                    row.cells[4].text = f"RM {book['quantity'] * book[price_key]:.2f}"
                    
                    # Add to subtotal
                    subtotal += book['quantity'] * book[price_key]
                break  # Stop after filling the matched table
        return subtotal

    def replace_text(self, doc, placeholder, replacement):
        """Helper function to replace text in the Word document."""
        for paragraph in doc.paragraphs:
            if placeholder in paragraph.text:
                inline = paragraph.runs
                for i in inline:
                    if placeholder in i.text:
                        i.text = i.text.replace(placeholder, replacement)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if placeholder in cell.text:
                        cell.text = cell.text.replace(placeholder, replacement)

    def create_unique_filename(self):
        """Generate a unique file name based on the current date."""
        date_today = datetime.now().strftime("%Y-%m-%d")
        base_filename = f"SebutHarga_{date_today}"
        file_number = 1
        while os.path.exists(f"{base_filename}_{file_number}.docx"):
            file_number += 1
        return f"{base_filename}_{file_number}.docx"

def main():
    app = QApplication(sys.argv)
    window = BookReportApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
