# Introduction into API with automation agents

Hello!

full API reference can be found [here](https://scinote-eln.github.io/scinote-api-docs/#introduction) Please note we're using V1 - version 1 for now. 

To make the API more accessible and easier to manage, we are introducing automation agents. 
Once you create yours under the "Automate with API" menu, a new team will be automatically created,
titled "[Your name]'s API testing team". This will be a sandbox for you to safely test the API, before you give 
it access to your data and even to the data of your colleagues (with their or your supervisor's permission, of course). 

You and your newly created automation agent will be the first two users in this sandbox team. 
For now, your automation agent will only be able to access and alter the data within this team. 

Have fun!

## Requirements
- Python 3 with standard libraries. 
- A computer with access to SciNote@UBT. 

## Procedure
- To get the code examples onto your computer, clone this GitHub repository, for instance, by clicking "Code => Download zip".  
- If you haven't done so yet, create an API automation agent in SciNote@UBT under the "Automate with API" menu (bottom left corner of the screen).
- Copy the automation agent credentials into the settings.json file
- Obtain the access and refresh tokens
- Run examples

### Updating the settings.json
Open the settings.json file, it should look a bit like this:
```javascript
{
    "server_url": "",
    "api_uid": "",
    "api_secret": "",
    "api_redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "authorization_code": ""
}
```
Fill in the missing values.

### Obtain access and refresh tokens
From the terminal run:
```
python3 get_auth_tokens.py
```

Hopefully you should see the response
```
Successfully acquired tokens and written them into settings file, you can start testing API using examples
```

You can now check settings.json, you should be able to see some additional values there. 
```javascript
{
  ...
  ...
  "access_token": "xxxxxx",
  "refresh_token": "xxxxx",
  "access_token_created_at": 1616778780,
  "access_token_expires_in": 7200
}
```
Congratulations you are now able to test your api access. 

### Running the example
Our example fetches the list of existing projects in the team with id 1 and outputs their names.

In terminal run following command:

```
python3 example_list_projects.py
```

You should be now able to see the project names listed as an output of the command. 


# WARNING

This code should serve as an example and should not be used in production environment. 

The settings.json file should be cleared out once you've completed the testing and secrets and tokens should be stored in safe, encrypted storage (i.e. database, secrets manager etc.) 

You should treat the tokens in confidential manner, similar as you do with your usernames and passwords. 
