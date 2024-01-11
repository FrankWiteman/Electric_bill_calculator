import pandas as pd
import os


def get_state_price(excel_file, sheet_name, state_name):
    try:
        # Load Excel file
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Check if the required columns are present
        required_columns = ['State', 'Current Month']
        if all(column in df.columns for column in required_columns):
            # Convert 'Current Month' column to numeric
            df['Current Month'] = pd.to_numeric(df['Current Month'], errors='coerce')

            # Check if the state exists in the DataFrame
            if state_name in df['State'].values:
                # Retrieve the price for the specified state
                state_price = df.loc[df['State'] == state_name, 'Current Month'].iloc[0]
                return state_price
            else:
                print(f"State '{state_name}' not found in the Excel sheet.")
                return None
        else:
            print(f"Required columns {required_columns} not found in the Excel sheet.")
            return None
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None


def store_past_month_usage(value):
    with open("past_month_usage.txt", "w") as file:
        file.write(str(value))


def retrieve_past_month_usage():
    try:
        with open("past_month_usage.txt", "r") as file:
            return float(file.read())
    except FileNotFoundError:
        return None


# Example usage
excel_residential_path = r"C:\Users\frank\Documents\python excel file\Residential.xlsx"
excel_business_path = r"C:\Users\frank\Documents\python excel file\Business.xlsx"
requested_category = input("Enter the category (Residential/Business): ").title()

if requested_category == "Residential":
    excel_file_path = excel_residential_path
elif requested_category == "Business":
    excel_file_path = excel_business_path
else:
    print("Invalid category choice.")
    exit()

sheet_name = "Sheet1"  # Replace with your actual sheet name
requested_state = input("Enter the state you want the price for: ").title()

state_price = get_state_price(excel_file_path, sheet_name, requested_state)

if state_price is not None:
    stored_past_month_usage = retrieve_past_month_usage()
    use_stored_value = input(f"Use stored previous month usage ({stored_past_month_usage})? (yes/no): ").lower()

    if use_stored_value == "yes":
        prev_month_usage = float(input("Enter the previous month kilowatt usage: ") or 0)
        prev_month_unit = stored_past_month_usage
    else:
        past_month_usage = float(input("Enter the past month units: "))
        prev_month_usage = float(input("Enter the previous month kilowatt usage: ") or 0)
        # Store the newly input value for future use
        store_past_month_usage(prev_month_usage)

    current_month_usage = float(input("Enter the current month kilowatt usage: "))

    # Update stored previous month usage every time wattage is calculated
    wattage = int(current_month_usage) - int(prev_month_usage)
    store_past_month_usage(wattage)


    prev_month_cost = state_price / 100 * stored_past_month_usage
    current_month_cost = state_price / 100 * wattage

    print(f'Previous month bill: ${prev_month_cost:.2f}')
    print(f'Current month bill: ${current_month_cost:.2f}')

    if current_month_cost > prev_month_cost:
        print("Your current month bill is higher than the previous month. Consider lowering your electric usage.")
    elif current_month_cost < prev_month_cost:
        print("Good job for conserving electricity! Your current month bill is lower than the previous month.")
    else:
        print("Your current month bill is the same as the previous month.")
else:
    print("Error retrieving state information.")

