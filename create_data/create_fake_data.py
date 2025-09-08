import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    from faker import Faker

    Faker.seed(1)
    fake = Faker()

    num_rows = 50000

    return fake, num_rows, pd


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
def _():
    return


if __name__ == "__main__":
    app.run()
