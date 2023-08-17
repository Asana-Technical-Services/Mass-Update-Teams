# Team Update script

This python script is used to bulk update all teams in a workspace to be private, barring any holdout teams which should be left public.

This script will also rename any teams with the prefix "ARCHIVE - "

## Requirements

This script is written using Python 3.8, though it should be compatible with most 3.x versions of python.

check your version of python locally installed with the command:

```
python -V
```

If you need to install a newer version of python, you can do so at https://www.python.org/downloads/

_Be sure to install certificates (by running the appropriate script in the python folder) if you download a new version of python_

## Operation

Be sure to install requirements from _requirements.txt_ and ideally run within a virtual environment of your choosing. We like to use _pipenv_, but _venv_ works as well

Run the script using

```
python runteamupdate.py
```

The script interactively asks for your Service Account Token, so that it is not stored anywhere in code.

Before running, you should update two parameters at the top of teamupdate.py:

- holdout teams: this is an array of GIDs of teams that should not be touched by the script. You can get the GID of a team from its URL.
- workspace: this is the GID of the workspace you're in. You can get the workspace GID by making the request: https://app.asana.com/api/1.0/workspaces with the service account token

## Rate Limits

Due to the volume of API calls this script makes, it may sometimes hit rate limits and need to set some delay between its API calls. The exact amount of delay will be printed to the console. Because the script will be running many calls in parallel, this message may print multiple times, once for each API call that was blocked due to rate limiting. These wait times will not be additive, since the calls are running in parallel. Once the wait duration is up, each API call will be retried with increasing delay until it succeeds. After ~10 tries (which would take almost 3 minutes of attempts) the individual api call will be canceled.
