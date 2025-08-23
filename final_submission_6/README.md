
# Comprehensive Workforce Planning and Prediction Pipeline

This project provides a robust, modular pipeline for workforce planning and prediction for 2025. It integrates advanced data preprocessing, holiday adjustments, time series forecasting, and regression modeling. The solution is designed for organizations seeking data-driven employee allocation and planning.

## Flow of Code (Detailed)

### 1. Data Loading & Preprocessing
- **Staffing Data Import:** Loads historical staffing data (2021-2024) from CSV, parses dates, and ensures correct data types.
- **Feature Engineering:** Creates new columns for year, month, day of week, quarter, and binary flags for holidays and weekends. Calculates 'is_working_day' by combining holiday and weekend flags.
- **Holiday Data Integration:** Scrapes/generates a comprehensive holiday DataFrame for 2021-2025, merges with main dataset, and excludes special dates to ensure only valid holidays are flagged.
- **Dataset Assembly:** Combines staffing, weekend, and holiday data into a unified DataFrame, ensuring every date-section combination is represented, even if no staff were present.

### 2. Training Data Analysis
- **Statistical Summary:** Aggregates statistics (mean, std, min, max) for employee count and task time per section.
- **Correlation Analysis:** Calculates Pearson correlation between employee count and task time for each section, identifying sections with strong/weak relationships.

### 3. Prophet Forecasting for Task Time
- **Model Training:** Trains a Prophet time series model for each section using historical task time data. Custom seasonalities (monthly, quarterly) and regressors (holiday, weekend) are added for improved accuracy.
- **Hyperparameter Tuning:** Uses Optuna or manual tuning to optimize Prophet parameters per section. Fallback defaults are used for new/unseen sections.
- **Prediction:** Forecasts daily task times for 2025 for each section, including confidence intervals (upper/lower bounds).

### 4. Weighted Regression for Employee Prediction
- **Huber Regression Model:** Trains a robust Huber regression model for each section to predict employee count from task time. Parameters are tuned per section for best fit.
- **Efficiency Calculation:** Calculates median task time per employee for each section, used as a secondary prediction method.
- **Weighted Combination:** Combines regression and efficiency-based predictions using a weighted average, where the weight is determined by the regression model's R² score (higher R² → more trust in regression).
- **Constraints:** Applies minimum/maximum employee limits based on historical data, and allows for a buffer above historical max for future predictions.

### 5. Task-to-Employee Conversion
- **Prediction Assembly:** Converts forecasted task times to employee requirements for each date-section using the weighted model. Calculates confidence intervals for employee predictions.
- **Output Mapping:** Maps predictions back to the main DataFrame for 2025, ensuring all relevant columns (predicted employee count, bounds, task time) are filled.

### 6. Analysis & Visualization
- **Section-wise Analysis:** Summarizes predictions by section, including average, min, max employees, peak/low months, and quarterly averages.
- **Monthly Planning:** Aggregates predictions by month for workforce planning, showing total employee-days, average daily workforce, and peak days.
- **Visualizations:** Generates bar charts, pie charts, scatter plots, and time series for trends, section-wise distributions, and confidence intervals. Plots are saved for reporting and dashboard use.

### 7. Model Export & Output
- **Pickle Export:** Saves all trained models and parameters to a single pickle file (`predictions_full.pkl`) for easy deployment and reuse.
- **CSV Outputs:** Exports all key results (full predictions, section analysis, monthly planning, etc.) to CSV for further analysis and integration.

## Model Architecture Diagram

```
+-------------------+
|   Data Sources    |
| (CSV: staffing,   |
|  holidays, etc.)  |
+-------------------+
         |
         v
+-------------------+
| Data Preprocessing|
| - Feature Eng.    |
| - Holiday Merge   |
| - Working Day Calc|
+-------------------+
         |
         v
+-------------------+
| Prophet Forecast  |
| (Section-wise)    |
| - Task Time Pred. |
| - Hyperparam Tune |
+-------------------+
         |
         v
+-------------------+
| Huber Regression  |
| (Section-wise)    |
| - Employee Pred.  |
| - Weighted Output |
+-------------------+
         |
         v
+-------------------+
| Analysis & Export |
| - Visualizations  |
| - CSV/PKL Output  |
+-------------------+
```

## Preprocessing Pipelines
- **Feature Engineering:** Date parsing, binary flags for holidays/weekends, working day calculation.
- **Holiday Integration:** Merge web-scraped holiday data, exclude special dates, create binary flags.
- **Train-Test Split:** Use 2021-2024 for training, 2025 for prediction.

## Models Used
- **Prophet:** Time series forecasting for daily task time per section, with custom seasonalities and regressors. Each section gets its own tuned model for best accuracy.
- **Huber Regression:** Robust regression for employee count prediction, tuned per section. Combines with efficiency-based prediction for reliability.

## Prediction Logic (Pickle Inference)
- **Model Loading:** Loads all trained models and parameters from `predictions_full.pkl`.
- **Feature Engineering:** Applies same preprocessing steps to new/evaluation data (date parsing, holiday/weekend flags).
- **Task Time Prediction:** Uses Prophet model for each section to forecast task time for new dates. If unavailable, falls back to average or default value.
- **Employee Prediction:** Uses Huber regression and efficiency ratio, weighted by R², to predict required employees. Applies minimum constraints and outputs final predictions.
- **Output Formatting:** Results are mapped to requested output format (row_id, true_required_employees) for submission or further use.

## Deployment Ideas
- **Batch Prediction:** Use exported pickle file (`predictions_full.pkl`) for batch inference on new data.
- **API Service:** Wrap pipeline in a REST API (e.g., Flask/FastAPI) for real-time workforce planning.
- **Dashboard:** Integrate outputs with BI tools (Power BI, Tableau) for interactive planning and visualization.
- **Cloud Deployment:** Deploy models and pipeline on Azure ML, AWS SageMaker, or GCP AI Platform for scalability.

## Output Files
- `complete_final_full_2025_dataset.csv`: Main output with 2025 predictions and confidence intervals.
- `2025_workforce_analysis_by_section.csv`: Section-wise workforce analysis.
- `2025_working_days_predictions.csv`: Working day predictions for 2025.
- `2025_monthly_workforce_planning.csv`: Monthly workforce planning summary.
- `predictions_full.pkl`: All trained models and parameters for deployment.

## References
- [Facebook Prophet Documentation](https://facebook.github.io/prophet/)
- [Scikit-learn HuberRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html)

---
For further details, see the notebook `combine_fcode_2.ipynb` and `pickel_code.ipynb` for inference logic.
