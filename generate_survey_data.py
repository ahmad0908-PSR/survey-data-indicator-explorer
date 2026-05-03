import pandas as pd
import random
from datetime import datetime, timedelta

NUM_RECORDS = 1000

REGION = "Central Highlands"
PROVINCES = ["North Valley", "East Plains", "South Ridge"]
DISTRICTS = ["District A", "District B", "District C"]
GENDERS = ["Male", "Female"]
AGE_GROUPS = ["18-24", "25-34", "35-49", "50+"]
MONTHS = ["Jan", "Feb", "Mar", "Apr"]

START_DATE = datetime(2024, 1, 1)

data = []

for i in range(1, NUM_RECORDS + 1):
    survey_date = START_DATE + timedelta(days=random.randint(0, 120))
    missing_count = random.choice([0, 0, 1, 2, 3])

    row = {
        "respondent_id": f"R{str(i).zfill(4)}",
        "gender": random.choice(GENDERS),
        "age_group": random.choice(AGE_GROUPS),
        "household_size": random.randint(1, 10),
        "region": REGION,
        "province": random.choice(PROVINCES),
        "district": random.choice(DISTRICTS),
        "survey_date": survey_date.date(),
        "year": survey_date.year,
        "month": MONTHS[min(survey_date.month - 1, 3)],
        "school_attendance": random.choice(["Yes", "No"]),
        "health_service_access": random.choice(["Yes", "No"]),
        "clean_water_access": random.choice(["Yes", "No"]),
        "food_security_status": random.choice(["Secure", "Insecure"]),
        "response_complete": missing_count == 0,
        "missing_fields_count": missing_count
    }

    data.append(row)

df = pd.DataFrame(data)
df.to_csv("survey_data_anonymized.csv", index=False)

print("✅ survey_data_anonymized.csv generated successfully")