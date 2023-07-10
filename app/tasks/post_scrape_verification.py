import pandas as pd
from akiya_mart_tasks.database import get_daily_listing_counts


# Current by day
# new by day
# gone by day


def verify_scrape(run_date):
    pivot_df = get_daily_listing_counts(run_date)
    for source in pivot_df.columns:
        daily_record_counts = pivot_df[source].dropna().tolist()
        if daily_record_counts:
            current_day_count = daily_record_counts[-1]
            past_week_data = daily_record_counts[-8:-1]
            data_series = pd.Series(past_week_data)
            mean = data_series.mean()
            std_dev = data_series.std()
            is_alert = (current_day_count < mean - 2 * std_dev) or (
                current_day_count > mean + 2 * std_dev
            )
            print(
                f"AKIYA-MART-TASKS POST-SCRAPE-VERIFICATION: source: {source}, current day count: {current_day_count}, mean: {mean}, std dev: {std_dev}, alert: {is_alert}"
            )
