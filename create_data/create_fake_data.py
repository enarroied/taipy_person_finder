import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    from faker import Faker

    Faker.seed(1)
    fake = Faker()

    num_rows = 50000

    return Faker, fake, num_rows, pd


@app.cell
def _(mo):
    mo.md(
        """
    # Create datasets for the application

    This notebook creates dataset files for the Taipy 🔎 Person Finder application. This application lets users look for a person in a dataset, using string similarity algorithms (Jaro-Winkler similarity, mainly; we might introduce others as well). 
    The application simulates a company with a large dataset of people coming from its information system. We code a Taipy application to let users look for people in the company dataset with two methods: by direct querying of the dataset (looking for one person in the dataset), or by uploading a file (CSV or parquet) and looking for a match.

    This notebook uses `Faker` to create the company dataset; it also generates two demonstration files (a CSV and a parquet file) to compare to the company data.

    ## Create the Application's dataset
    """
    )
    return


@app.cell
def _(fake, num_rows, pd):
    data = {
        "id": [i for i in range(num_rows)],
        "first_name": [fake.first_name() for _ in range(num_rows)],
        "family_name": [fake.last_name() for _ in range(num_rows)],
        "address": [fake.street_address() for _ in range(num_rows)],
        "city": [fake.city() for _ in range(num_rows)],
        "country": [fake.country() for _ in range(num_rows)],
        "phone": [fake.phone_number() for _ in range(num_rows)],
        "email": [fake.email() for _ in range(num_rows)],
    }

    df_fake_data = pd.DataFrame(data)
    df_fake_data.to_parquet("../src/data/fake_data.parquet", index=False)

    print(
        f"Created and saved DataFrame with {num_rows} rows to ../data/fake_data.parquet"
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Create the query data

    The following datasets can be uploaded to the application to look for matches.

    We mainly need the dataset to have first and last names in it. We also add phone numbers to simulate extra columns, because: why not?

    We use a **French locale code to make sure our names and family names are different from the ones used in the main company dataset**.
    """
    )
    return


@app.cell
def _(Faker):
    Faker.seed(2)
    fake_seed_2 = Faker('fr_FR')

    return (fake_seed_2,)


@app.cell
def _(fake_seed_2, num_rows, pd):
    trial_data  = {
        "first_name": [fake_seed_2.first_name() for _ in range(num_rows)],
        "family_name": [fake_seed_2.last_name() for _ in range(num_rows)],
        "phone": [fake_seed_2.phone_number() for _ in range(num_rows)],
    }

    trial_data = pd.DataFrame(trial_data)
    trial_data.to_parquet("../src/data/trial_dataset.parquet", index=False)
    trial_data.to_csv("../src/data/trial_dataset.csv", index=False)
    return


if __name__ == "__main__":
    app.run()
