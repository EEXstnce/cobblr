# Inverse Finance Data Analysis

This code performs various calculations and data processing tasks related to the Inverse Finance platform. It retrieves data from different API endpoints, performs calculations, and prints the results.

## Prerequisites

Before running the code, make sure you have the following dependencies installed:

- `getters.inv_api` module
- `util.printer` module
- `util.asset` module
- `util.firm` module
- `policy.pces` module
- `policy.dbr_issue` module

## Usage

To use this code, you can follow the steps below:

1. Import the necessary modules from the appropriate package.
2. Define the API endpoints in the `api_endpoints` dictionary.
3. Execute the code to fetch data from the API endpoints and perform calculations.
4. Review the printed outputs to see the results of the calculations.

Note: Make sure you have the required dependencies installed as mentioned in the "Prerequisites" section.

## API Endpoints

The following API endpoints are used in this code:

- `markets`: Retrieves data related to market information.
- `fed`: Retrieves data related to the Fed overview.
- `fixed`: Retrieves data related to fixed markets.
- `positions`: Retrieves data related to firm positions.
- `price`: Retrieves data related to DBR price.
- `dbr`: Retrieves data related to DBR emissions transparency.

## Output

The code produces various printed outputs, including:

- DBR FX rate.
- DBR issuance per year.
- DBR value per year.
- Total INV stake.
- DBR per INV.
- DBR value per INV.

## Note

Please ensure that you have the necessary access rights and permissions to fetch data from the provided API endpoints.
