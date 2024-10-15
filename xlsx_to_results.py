import pandas as pd

results_file = pd.ExcelFile("example_dataset.xlsx")
results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 47)
if not results_table.empty:
    print(results_table.loc[:, ["Sample Name", "Target Name", "CT"]])

results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = "35").apply(pd.to_numeric)
print(results_table.loc[:, ["Sample Name", "Target Name", "CT"]])