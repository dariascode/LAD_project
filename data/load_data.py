import pandas as pd

def load_data():
    url = "https://raw.githubusercontent.com/dariascode/LAD_project/refs/heads/main/cars_cleaned_dataset.csv"

    df = pd.read_csv(url)

    print("Dataset loaded successfully")
    print("Shape:", df.shape)

    return df



if __name__ == "__main__":
    df = load_data()
    print(df.head())