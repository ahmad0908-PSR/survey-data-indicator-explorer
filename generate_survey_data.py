import pandas as pd
import random
from datetime import datetime, timedelta

# ---------------------------------------
# SETTINGS
# ---------------------------------------
NUM_RECORDS = 1500

REGION_MAP = {
    "Central Highlands": ["North Valley", "East Plains", "South Ridge"],
    "Coastal Belt": ["Bay District", "Harbor Plains", "Delta Zone"],
    "Northern Corridor": ["Highland North", "River Bend", "Border Plains"]
}

DISTRICTS = ["District A", "District B", "District C"]
GENDERS = ["Male", "Female"]
AGE_GROUPS = ["18-24", "25-34", "35-49", "50+"]
YEARS = [2022, 2023, 2024, 2025]

data = []

for i in range(1, NUM_RECORDS + 1):
    year = random.choice(YEARS)
    start_date = datetime(year, 1, 1)
    survey_date = start_date + timedelta(days=random.randint(0, 364))

    region = random.choice(list(REGION_MAP.keys()))
    province = random.choice(REGION_MAP[region])
    district = random.choice(DISTRICTS)

    missing_count = random.choice([0, 0, 0, 1, 2, 3])

    row = {
        "respondent_id": f"R{str(i).zfill(5)}",
        "gender": random.choice(GENDERS),
        "age_group": random.choice(AGE_GROUPS),
        "household_size": random.randint(1, 10),
        "region": region,
        "province": province,
        "district": district,
        "survey_date": survey_date.date(),
        "year": year,
        "month": survey_date.strftime("%b"),
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

print("✅ survey_data_anonymized.csv generated with multiple regions and years")