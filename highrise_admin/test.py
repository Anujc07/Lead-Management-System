import pandas as pd
# from io import BytesIO

# # Open the Excel file in binary mode and read its content into a BytesIO object
# with open('C:/Users/ok/Desktop/Highrise/test.xls', 'rb') as f:
#     excel_data = BytesIO(f.read())

# # Try different engines until one works
# engines = ['openpyxl', 'xlrd', 'odfpy','pyxlsb']
# for engine in engines:
#     try:
#         # Read the Excel data into a DataFrame
#         df = pd.read_excel(excel_data, engine=engine)
#         break
#     except Exception as e:
#         print(f"Failed to read with engine '{engine}': {e}")
# else:
#     print("Failed to read the Excel file with any engine.")

# # Print the DataFrame
# # print(df)

df= pd.read_excel("C:/Users/ok/Desktop/testtest.xlsx")
print(df)





# import pandas as pd
# import xlrd

# # Open the Excel file
# xls_file_path = 'C:/Users/ok/Desktop/Highrise/test.xls'
# workbook = xlrd.open_workbook(xls_file_path)

# # Read the first sheet into a DataFrame
# sheet = workbook.sheet_by_index(0)
# data = [sheet.row_values(row) for row in range(sheet.nrows)]
# df = pd.DataFrame(data[1:], columns=data[0])

# print(df)
