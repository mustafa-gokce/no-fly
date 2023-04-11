"""
Generate binary no-fly zone data from airport data.
"""

import pandas as pd


def main():
    """Main function."""

    # load databases
    runways = pd.read_csv("ourairports-data/runways.csv")
    airports = pd.read_csv("ourairports-data/airports.csv")

    # drop all columns except latitude and longitude
    runways = runways.drop(columns=["airport_ref", "surface", "lighted", "closed",
                                    "le_ident", "le_elevation_ft", "le_displaced_threshold_ft",
                                    "he_ident", "he_elevation_ft", "he_displaced_threshold_ft"])

    # rename columns
    runways = runways.rename(columns={"id": "runway", "airport_ident": "airport", "length_ft": "runway_length", "width_ft": "runway_width",
                                      "le_latitude_deg": "runway_latitude_low", "le_longitude_deg": "runway_longitude_low",
                                      "he_latitude_deg": "runway_latitude_high", "he_longitude_deg": "runway_longitude_high",
                                      "le_heading_degT": "runway_heading_low", "he_heading_degT": "runway_heading_high"})

    # add columns from airports dataframe
    runways["airport_type"] = runways["airport"].map(airports.set_index("ident")["airport_type"])
    runways["airport_name"] = runways["airport"].map(airports.set_index("ident")["airport_name"])
    runways["airport_latitude"] = runways["airport"].map(airports.set_index("ident")["latitude_deg"])
    runways["airport_longitude"] = runways["airport"].map(airports.set_index("ident")["longitude_deg"])
    runways["continent"] = runways["airport"].map(airports.set_index("ident")["continent"])
    runways["country"] = runways["airport"].map(airports.set_index("ident")["iso_country"])

    # order rows by runway
    runways = runways.sort_values(by=["runway"])

    # check for duplicates in runway column
    if runways["runway"].duplicated().any():
        print("Duplicate runways found!")
        print(runways[runways["runway"].duplicated()])
        return

    # re-order columns
    runways = runways[["runway", "airport", "airport_type", "airport_name", "runway_length", "runway_width",
                       "continent", "country", "airport_latitude", "airport_longitude",
                       "runway_latitude_low", "runway_longitude_low", "runway_heading_low",
                       "runway_latitude_high", "runway_longitude_high", "runway_heading_high"]]

    # drop all runways with NaN values on latitude and longitude
    runways = runways.dropna(subset=["airport_latitude", "airport_longitude"])

    # drop closed runways
    runways = runways[runways["airport_type"] != "closed"]

    # save runways dataframe to csv file
    runways.to_csv("runways.csv", index=False)


if __name__ == "__main__":
    main()
