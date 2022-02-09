# Social-Media-Influencer-analysis

If you are interested in creating a separate environment, I added a sample requirements file.

Use the following command to create a new environment with all  required libraries:

```Python
conda create --name <environment name> --file requirements.txt
```

Please note, you need to create your own credentials for scraping.

Save the credentials in a json file 'credentials.json' with the following structure:

```json
{
    "consumer_key": "<<enter your consumer_key here>>",
    "consumer_secret": "<<enter your consumer_secret here>>",
    "bearer_token":"<<enter your bearer_token here>>",
    "access_token":"<<enter your access_token here>>",
    "access_token_secret":"<<enter your access_token_secret here>>"
}
```