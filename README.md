# Old School Runescape API and Scrapers

# Tests

To run tests in this repository, follow these steps:

1. Make sure you have the necessary environment variables set up. These variables are required for the tests to run successfully.

    ```yaml
    DISCORD_WEBHOOK=...
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    AWS_DEFAULT_REGION=...
    ```

2. Run the test command in your terminal or command prompt:

   ```bash
   pytest .
   ```

   This run all the unit tests in the `tests` directory. To run all tests including the AWS tests, do

   ```bash
   pytest -m aws
   ```

   This requires all the enviroment variables to be set from step 1.

3. Check the test results in the terminal or command prompt. Any failures or errors will be displayed, allowing you to identify and fix any issues.

Note: If you encounter any issues related to environment variables, make sure they are correctly set up and accessible to the test environment.
