import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

RAW_FILE = os.path.join(DATA_DIR, "GlobalLandTemperaturesByCountry.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "processed_temperature_country.csv")


def clean_country_name(country):
    replacements = {
        "United States": "United States of America",
        "Congo (Democratic Republic Of The)": "Democratic Republic of the Congo",
        "Côte D'Ivoire": "Cote d'Ivoire",
        "Bosnia And Herzegovina": "Bosnia and Herzegovina"
    }
    return replacements.get(country, country)


def main():
    print("Loading dataset...")
    df = pd.read_csv(RAW_FILE)

    print("Original shape:", df.shape)

    # Basic cleaning
    df = df.dropna(subset=["AverageTemperature"])
    df = df.drop_duplicates()

    # Date processing
    df["dt"] = pd.to_datetime(df["dt"], errors="coerce")
    df = df.dropna(subset=["dt"])

    df["Year"] = df["dt"].dt.year
    df["Month"] = df["dt"].dt.month

    # Keep years from 1880 onward for clearer historical analysis
    df = df[df["Year"] >= 1880]

    # Clean country names for Plotly map
    df["Country"] = df["Country"].apply(clean_country_name)

    # Aggregate monthly data into yearly country-level data
    yearly = (
        df.groupby(["Country", "Year"], as_index=False)
        .agg(
            AverageTemperature=("AverageTemperature", "mean"),
            AverageTemperatureUncertainty=("AverageTemperatureUncertainty", "mean")
        )
    )

    # Calculate baseline temperature for each country: 1951-1980
    baseline = (
        yearly[(yearly["Year"] >= 1951) & (yearly["Year"] <= 1980)]
        .groupby("Country", as_index=False)["AverageTemperature"]
        .mean()
        .rename(columns={"AverageTemperature": "BaselineTemperature"})
    )

    yearly = yearly.merge(baseline, on="Country", how="left")
    yearly["TemperatureAnomaly"] = yearly["AverageTemperature"] - yearly["BaselineTemperature"]

    # If baseline is missing for some countries, use global mean baseline
    global_baseline = yearly["BaselineTemperature"].mean()
    yearly["BaselineTemperature"] = yearly["BaselineTemperature"].fillna(global_baseline)
    yearly["TemperatureAnomaly"] = yearly["AverageTemperature"] - yearly["BaselineTemperature"]

    yearly = yearly.round({
        "AverageTemperature": 3,
        "AverageTemperatureUncertainty": 3,
        "BaselineTemperature": 3,
        "TemperatureAnomaly": 3
    })

    yearly.to_csv(OUTPUT_FILE, index=False)

    print("Processed shape:", yearly.shape)
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
