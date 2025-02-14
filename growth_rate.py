from database import database
import os
from private import Private
from round_decimal import round_decimal

# Function: standardisePercentage
# Purpose: This function adjusts an index by applying a percentage change to it. 
#          It is used to calculate a new index value after accounting for a given percentage change.
# Inputs:
#   - index (float): The current index value to be adjusted.
#   - percentage (float): The percentage change to be applied to the index.
# Output:
#   - (float): The new standardized index value after applying the percentage change.
def standardisePercentage(index, percentage):
    # Calculate the adjusted index:
    # - round_decimal(1) ensures that the base is 1.
    # - percentage / 100 converts the percentage to a decimal.
    # - The multiplication applies the percentage increase to the index.
    return round_decimal(index * (round_decimal(1) + percentage / round_decimal(100)))


# Function: standardiseData
# Purpose: This function processes a dataset to calculate standardized index values 
#          by sequentially applying percentage changes to an initial base index of 1.
# Inputs:
#   - datas (list of lists): A dataset where each sublist contains:
#       1. A label (e.g., a string or identifier).
#       2. A percentage (float) to be applied to the index.
# Output:
#   - newDatas (list of lists): A new dataset where each sublist contains:
#       1. The original label.
#       2. The standardized index value after applying the percentage changes.
def standardiseData(datas):
    # Initialize the index to 1 (base index for standardization)
    index = round_decimal(1)
    # Create a list to store the new, standardized dataset
    newDatas = []
    
    # Iterate over each row in the input dataset
    for i in range(len(datas)):
        # Create a new row to store standardized data
        newData = []
        # Append the original label to the new row
        newData.append(datas[i][0])
        # Update the index by applying the percentage change using standardisePercentage
        index = standardisePercentage(index, datas[i][1])
        # Append the updated index to the new row
        newData.append(index)
        # Add the new row to the standardized dataset
        newDatas.append(newData)
    
    # Return the newly created dataset with standardized index values
    return newDatas


# Function: isDataPercent
# Purpose: This function checks whether a given table name is part of a predefined set of table names.
#          It is used to determine if the data for a specific table represents percentage values.
# Inputs:
#   - tableName (string): The name of the table to check.
# Output:
#   - (bool): True if the table name is found in the predefined set; False otherwise.
def isDataPercent(tableName):
    # Define a set of table names that represent percentage data
    setData = {"t_durable_goods_orders_86", "t_retail_sales_256", "t_us_leading_index_1968"}
    # Check if the given tableName exists in the set
    return tableName in setData


# Param:
# datas: data's form indicators
# diff: interval of days of data's update
# This function computes the three-month growth rate
# Return: the growth rate
def computethreemonth(datas, diff):

    results = []
    for i in range(len(datas)):
        try:
            current_value = round_decimal(datas[i][1])  # Apply round_decimal
            if diff == 1 and i - 90 >= 0:
                previous_value = round_decimal(datas[i - 90][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(3))) - round_decimal(1)) * round_decimal(100)
            elif diff == 7 and i - 12 >= 0:
                previous_value = round_decimal(datas[i - 12][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(3))) - round_decimal(1)) * round_decimal(100)
            elif diff == 30 and i - 3 >= 0:
                previous_value = round_decimal(datas[i - 3][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(3))) - round_decimal(1)) * round_decimal(100)
            elif diff > 30 and i - 1 >= 0:
                previous_value = round_decimal(datas[i - 1][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(3))) - round_decimal(1)) * round_decimal(100)
            else:
                growth = None
        except (ZeroDivisionError, IndexError):
            growth = round_decimal(0)
        except Exception as e:
            print(f"Something went wrong: {e}")
            growth = None

        results.append({"timestamp": datas[i][0], "value": round_decimal(growth), "intervalMonth": 3})

    return results


# Param:
# datas: data's form indicators
# diff: interval of days of data's update
# This function computes the twelve-month growth rate
# Return: the growth rate
def computetwelvemonth(datas, diff):

    results = []

    for i in range(len(datas)):
        try:
            current_value = round_decimal(datas[i][1])  # Apply round_decimal
            if diff == 1 and i - 261 >= 0:
                previous_value = round_decimal(datas[i - 261][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(12))) - round_decimal(1)) * round_decimal(100)
            elif diff == 7 and i - 52 >= 0:
                previous_value = round_decimal(datas[i - 52][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(12))) - round_decimal(1)) * round_decimal(100)
            elif diff == 30 and i - 12 >= 0:
                previous_value = round_decimal(datas[i - 12][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(12))) - round_decimal(1)) * round_decimal(100)
            elif diff > 30 and i - 4 >= 0:
                previous_value = round_decimal(datas[i - 4][1])
                growth = (((current_value / previous_value) ** (round_decimal(12) / round_decimal(12))) - round_decimal(1)) * round_decimal(100)
            else:
                growth = None
        except (ZeroDivisionError, IndexError):
            growth = round_decimal(0)
        except Exception as e:
            print(f"Something went wrong: {e}")
            growth = None

        results.append({"timestamp": datas[i][0], "value": round_decimal(growth), "intervalMonth": 12})

    return results

def computetwelvemonthPhily(datas, diff):
    results = []

    for i in range(len(datas)):
        try:
            current_value = round_decimal(datas[i][1])  # Apply round_decimal
            if diff == 30 and i - 12 >= 0:
                previous_value = round_decimal(datas[i - 12][1])
                growth = ((current_value - previous_value) / abs(previous_value))
            else:
                growth = None
        except (ZeroDivisionError, IndexError):
            growth = round_decimal(0)
        except Exception as e:
            print(f"Something went wrong: {e}")
            growth = None

        results.append({"timestamp": datas[i][0], "value": round_decimal(growth), "intervalMonth": 12})

    return results

pr = Private()
db = database(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

list_links = db.fetch_links("length(show_more)", ">", "2")
indicators = db.fetch_indicators()
db.update_status("process_investing", 3)

# Calculate growth rate data from investing.com
for link in list_links:
    datas = db.fetch_table_Main(link[4], "", "", "")
    if isDataPercent(link[4]):
        datas=standardiseData(datas)
    results = computethreemonth(datas, link[3])
    db.insert_value_component_gr(link[4] + "_gr", results)
    results = computetwelvemonth(datas, link[3])
    db.insert_value_component_gr(link[4] + "_gr", results)

db.update_status("process_investing", 4)

db.update_status("process_fred", 3)

# Calculate growth rate data from Fred
for indicator in indicators:

    datas = db.fetch_table_Main(indicator[3].lower(), "", "", "")
    results = computethreemonth(datas, indicator[2])
    db.insert_value_component_gr(indicator[3].lower() + "_gr", results)
    if(indicator[3] == "t_GACDFSA066MSFRBPHI"):
        results = computetwelvemonthPhily(datas, indicator[2])
    else:
        results = computetwelvemonth(datas, indicator[2])
    db.insert_value_component_gr(indicator[3].lower() + "_gr", results)

db.update_status("process_fred", 4)

pr.clean()
