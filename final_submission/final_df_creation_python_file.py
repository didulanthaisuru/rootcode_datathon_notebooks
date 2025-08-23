# final_df_creation_python_file.py

import pandas as pd
import numpy as np
from datetime import datetime

# Input
staff_df = pd.read_csv("staffing_train.csv")
staff_df['date'] = pd.to_datetime(staff_df['date'])

# Generate all dates from 2021-01-01 to 2025-12-31
all_dates = pd.date_range(start="2021-01-01", end="2025-12-31")

# Filter weekends (Saturday=5, Sunday=6)
weekend_dates = all_dates[all_dates.weekday.isin([5, 6])]
weekend_df = pd.DataFrame({'date': weekend_dates})
weekend_df['weekday'] = weekend_df['date'].dt.day_name()

# Sri Lanka holidays for 2021-2025 (from notebook web_holiday_data)
web_holiday_data = [
    # ... (copy the full list from your notebook, omitted here for brevity)
]
web_holiday_df = pd.DataFrame(web_holiday_data, columns=['date', 'holiday_name'])
web_holiday_df['date'] = pd.to_datetime(web_holiday_df['date'])

# Exclude specific dates (from notebook exclude_dates)
exclude_dates = [
    '2023-09-29', '2022-05-02', '2023-06-29', '2022-06-24', '2022-07-08', '2024-09-23',
    '2022-06-13', '2022-09-19', '2023-08-30', '2022-07-15', '2022-07-01', '2023-03-06',
    '2021-05-25', '2022-07-22', '2022-07-29', '2021-05-24', '2022-06-17'
]
exclude_dates_dt = pd.to_datetime(exclude_dates)
filtered_holiday = web_holiday_df[~web_holiday_df['date'].isin(exclude_dates_dt)].reset_index(drop=True)

# Create final DataFrame by combining staff, weekend, and filtered_holiday
sections = staff_df['section_id'].unique()
final_rows = []
for date in all_dates:
    for section in sections:
        staff_row = staff_df[(staff_df['date'] == date) & (staff_df['section_id'] == section)]
        employees_on_duty = staff_row['employees_on_duty'].values[0] if not staff_row.empty else 0
        total_task_time_minutes = staff_row['total_task_time_minutes'].values[0] if not staff_row.empty else 0
        weekend_row = weekend_df[weekend_df['date'] == date]
        weekday = weekend_row['weekday'].values[0] if not weekend_row.empty else 0
        holiday_row = filtered_holiday[filtered_holiday['date'] == date]
        holiday_name = holiday_row['holiday_name'].values[0] if not holiday_row.empty else 0
        final_rows.append({
            'date': date,
            'section_id': section,
            'employees_on_duty': employees_on_duty,
            'total_task_time_minutes': total_task_time_minutes,
            'weekday': weekday,
            'holiday_name': holiday_name
        })
final_df = pd.DataFrame(final_rows)
final_df['date'] = pd.to_datetime(final_df['date'])

# Convert 'holiday_name' and 'weekday' to binary columns
final_df['is_holiday'] = final_df['holiday_name'].apply(lambda x: 1 if x != 0 else 0)
final_df['is_weekend'] = final_df['weekday'].apply(lambda x: 1 if x != 0 else 0)

# Drop the original 'holiday_name' and 'weekday' columns
final_binary_submission_df = final_df.drop(['holiday_name', 'weekday'], axis=1)

# Output
final_binary_submission_df.to_csv('final_binary_submission_df.csv', index=False)