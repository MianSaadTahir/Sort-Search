import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtGui import QIcon
from sorting import bubbleSort, insertionSort, selectionSort, mergeSort, quickSort, countingSort, radixSort, bucketSort, gnomeSort, beadSort, cocktailShakerSort
from searching import filterData, multiColumnSearch


class CsvViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorting and Searching")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("background-color: #F5F5F5;")
        self.setWindowIcon(QIcon("iconS.ico"))

        font = QFont("Arial", 12, QFont.Bold)
        self.setFont(font)

        palette = QPalette()
        palette.setColor(QPalette.Button, QColor("#2C3E50")
                         )
        palette.setColor(QPalette.ButtonText, QColor(
            "#FFFFFF"))
        palette.setColor(QPalette.WindowText, QColor(
            "#2C3E50"))
        self.setPalette(palette)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.control_layout = QVBoxLayout()

        self.sorting_time_label = QLabel("Sorting time: N/A")
        self.sorting_time_label.setFont(
            QFont("Times New Roman", 14, QFont.Bold))  # Larger, bold font
        self.control_layout.addWidget(self.sorting_time_label)

        self.column_list_widget = QListWidget()
        self.column_list_widget.setSelectionMode(
            QAbstractItemView.MultiSelection)
        self.column_list_widget.setStyleSheet(
            "background-color: #FFFFFF;"  # White background for the list widget
            "border: 2px solid #34495E;"  # Dark gray border around the list widget
            "padding: 5px;"
        )
        self.column_list_widget.setFont(
            QFont("Arial", 12, QFont.Bold))  # Bold font for list widget
        self.control_layout.addWidget(
            QLabel("Select Columns to Sort:", font=QFont("Arial", 12, QFont.Bold)))
        self.control_layout.addWidget(self.column_list_widget)

        self.control_layout.addSpacing(10)

        self.algorithm_dropdown = QComboBox()
        self.algorithm_dropdown.setFont(QFont("Arial", 12, QFont.Bold))
        self.control_layout.addWidget(QLabel("Select Sorting Algorithm:"))
        self.algorithm_dropdown.addItems([
            "Bubble Sort", "Insertion Sort", "Selection Sort",
            "Merge Sort", "Quick Sort", "Counting Sort",
            "Radix Sort", "Bucket Sort", "Gnome Sort",
            "Bead Sort", "Cocktail Shaker Sort"
        ])
        self.control_layout.addWidget(self.algorithm_dropdown)

        self.load_button = QPushButton("Load Flipkart CSV")
        self.load_button.clicked.connect(self.load_csv)
        self.load_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.load_button.setStyleSheet(
            "background-color: #2980B9; color: white; padding: 5px;")
        self.control_layout.addWidget(self.load_button)

        self.control_layout.addSpacing(10)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter search term")
        self.search_bar.setFont(QFont("Arial", 12))  # Larger font for input
        self.control_layout.addWidget(self.search_bar)

        self.search_column_dropdown = QComboBox()
        self.search_column_dropdown.setFont(QFont("Arial", 12, QFont.Bold))
        self.control_layout.addWidget(QLabel("Select Search Column:"))
        self.control_layout.addWidget(self.search_column_dropdown)

        self.filter_type_dropdown = QComboBox()
        self.filter_type_dropdown.setFont(QFont("Arial", 12, QFont.Bold))
        self.control_layout.addWidget(QLabel("Select Filter Type:"))
        self.filter_type_dropdown.addItems(
            ['contains', 'starts_with', 'ends_with'])
        self.control_layout.addWidget(self.filter_type_dropdown)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        self.search_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.search_button.setStyleSheet(
            "background-color: #2C3E50; color: white; padding: 5px;")
        self.control_layout.addWidget(self.search_button)

        self.sort_button = QPushButton("Sort Selected Columns")
        self.sort_button.clicked.connect(self.sort_column)
        self.sort_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.sort_button.setStyleSheet(
            "background-color: #2C3E50; color: white; padding: 5px;")
        self.control_layout.addWidget(self.sort_button)

        self.control_layout.addSpacing(10)

        self.multi_search_column_list_widget = QListWidget()
        self.multi_search_column_list_widget.setSelectionMode(
            QAbstractItemView.MultiSelection)
        self.multi_search_column_list_widget.setStyleSheet(
            "background-color: #FFFFFF;"
            "border: 2px solid #34495E;"
            "padding: 5px;"
        )
        self.multi_search_column_list_widget.setFont(
            QFont("Arial", 12, QFont.Bold))
        self.control_layout.addWidget(
            QLabel("Select Columns for Multi-Search:"))
        self.control_layout.addWidget(self.multi_search_column_list_widget)

        self.multi_search_term_bar = QLineEdit()
        self.multi_search_term_bar.setPlaceholderText(
            "Enter search terms separated by commas")
        self.multi_search_term_bar.setFont(QFont("Arial", 12))
        self.control_layout.addWidget(self.multi_search_term_bar)

        self.multi_search_filter_type_dropdown = QComboBox()
        self.multi_search_filter_type_dropdown.setFont(
            QFont("Arial", 12, QFont.Bold))
        self.multi_search_filter_type_dropdown.addItems(['AND', 'OR'])
        self.control_layout.addWidget(
            QLabel("Select Multi-Search Filter Type:"))
        self.control_layout.addWidget(self.multi_search_filter_type_dropdown)

        self.multi_search_button = QPushButton("Multi-Search")
        self.multi_search_button.clicked.connect(self.perform_multi_search)
        self.multi_search_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.multi_search_button.setStyleSheet(
            "background-color: #2C3E50; color: white; padding: 5px;")
        self.control_layout.addWidget(self.multi_search_button)

        self.layout.addLayout(self.control_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setFont(QFont("Arial", 12))
        self.table_widget.setStyleSheet(
            "background-color: #ECF0F1;"
            "border: 2px solid #34495E;"
            "QHeaderView::section {"
            "background-color: #2F4F4F;"
            "color: #FFFFFF;"
            "font: bold 12px 'Arial';"
            "}"
        )
        self.layout.addWidget(self.table_widget)

    def load_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)", options=options)

        if file_path:
            self.df = pd.read_csv(file_path)
            self.display_data(self.df)

            self.column_list_widget.clear()
            self.column_list_widget.addItems(self.df.columns)

            self.search_column_dropdown.clear()
            self.search_column_dropdown.addItems(self.df.columns)

            self.multi_search_column_list_widget.clear()
            self.multi_search_column_list_widget.addItems(self.df.columns)

    def display_data(self, df):
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.table_widget.setItem(
                    i, j, QTableWidgetItem(str(df.iat[i, j])))

    def sort_column(self):
        selected_items = self.column_list_widget.selectedItems()
        selected_columns = [item.text() for item in selected_items]
        selected_algorithm = self.algorithm_dropdown.currentText()

        if selected_columns:
            self.sorting_time_label.setText("")
            start_time = QTime.currentTime()

            for column in reversed(selected_columns):
                column_data = self.df[column].values.tolist()

                if selected_algorithm == "Bubble Sort":
                    sorted_data = bubbleSort(column_data)
                elif selected_algorithm == "Insertion Sort":
                    sorted_data = insertionSort(column_data)
                elif selected_algorithm == "Selection Sort":
                    sorted_data = selectionSort(column_data)
                elif selected_algorithm == "Merge Sort":
                    sorted_data = mergeSort(column_data)
                elif selected_algorithm == "Quick Sort":
                    sorted_data = quickSort(column_data)
                elif selected_algorithm == "Counting Sort":
                    sorted_data = countingSort(column_data)
                elif selected_algorithm == "Radix Sort":
                    sorted_data = radixSort(column_data)
                elif selected_algorithm == "Bucket Sort":
                    sorted_data = bucketSort(column_data, num_buckets=10)
                elif selected_algorithm == "Gnome Sort":
                    sorted_data = gnomeSort(column_data)
                elif selected_algorithm == "Bead Sort":
                    sorted_data = beadSort(column_data)
                elif selected_algorithm == "Cocktail Shaker Sort":
                    sorted_data = cocktailShakerSort(column_data)

                self.df[column] = sorted_data

            self.display_data(self.df)
            elapsed_time = start_time.msecsTo(QTime.currentTime())
            self.sorting_time_label.setText(f"Sorting time: {elapsed_time} ms")

    def perform_search(self):
        selected_column = self.search_column_dropdown.currentText()
        filter_type = self.filter_type_dropdown.currentText()
        search_term = self.search_bar.text()

        if selected_column and search_term:
            filtered_df = filterData(
                self.df, selected_column, filter_type, search_term)
            self.display_data(filtered_df)

    def perform_multi_search(self):
        selected_columns = [
            item.text() for item in self.multi_search_column_list_widget.selectedItems()]
        search_terms = self.multi_search_term_bar.text().split(',')
        filter_type = self.multi_search_filter_type_dropdown.currentText()

        if selected_columns and search_terms:
            search_terms = [term.strip()
                            for term in search_terms if term.strip()]
            filtered_df = multiColumnSearch(
                self.df, selected_columns, search_terms, filter_type)
            self.display_data(filtered_df)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec_())
