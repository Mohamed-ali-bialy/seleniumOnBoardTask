import openpyxl

class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path


    def get_column_data(self, column_name):
        """
        Extracts data from a specific column in the Excel file.
        :param column_name: The header of the column to extract data from.
        :return: List of values in the specified column.
        """
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook.active

        # Find the column index for the given column name
        headers = [cell.value for cell in sheet[1]]
        column_index = headers.index(column_name) + 1

        # Extract data from the column
        column_data = [
            row[column_index - 1]
            for row in sheet.iter_rows(min_row=2, values_only=True)
        ]

        return column_data

