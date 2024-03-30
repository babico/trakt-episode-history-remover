# Trakt Episode History Remover

There is an error in Jellyfin Trakt plugin ([issue](https://github.com/jellyfin/jellyfin-plugin-trakt/issues/226)). First I tried to fix with [JS](https://github.com/jellyfin/jellyfin-plugin-trakt/issues/226#issuecomment-1971455192) but its relly slow so I create a python script.

## Prerequisites

### Install Python Packages

Install pacakges via pip.

```bash
pip install python-dotenv
```

### Set `.env` file

First we need `.env` file for store Trakt App client ID and Secret. You can copy sample file for create `.env`.

```bash
cp .env.sample .env
```

### Create Trakt App

Now we need to create Trakt App to get history and remove history. [Create Trakt App](https://trakt.tv/oauth/applications/new) Enter any name to app, enter `urn:ietf:wg:oauth:2.0:oob` to Redirect uri box and click `Save App` button at bottom of page. After create the app you can see Client ID and Secret at webpage, copy these and paste to `.env` which is created earlier.

### Extract IDs

We need extract episode ID and first added episode history id

Here is an example of my problem:
![example](https://babico.s-ul.eu/7qs6G472)

#### Get Serie ID

First need to get episodes ID. Go to episode page and click to "VIEW ALL" link:
![text](https://babico.s-ul.eu/aDbFZxuu)
In my example this is the link of history of episode. So latest number is episode number: `430785`
![text](https://babico.s-ul.eu/zoJcwxks)

#### Get History ID of first added play

Now go to last page on history, scroll to bottom of page. Click `CTRL + SHIFT + C` and select last item of history. Click the exact spot.
![text](https://babico.s-ul.eu/IiMIoIzR)

Now you can see the HTML element in this element we need to store this `data-history-id` tag's value.
![text](https://babico.s-ul.eu/ltmn99Sc)

#### Edit JSON File

Go to `episodes_to_delete.json` and edit according to your information. "name", "season", "episode" is unnecessary I just added to remember which episode is which ID.

```json
{ "episodes": [
    {
        "name": "Archer",
        "season": 3,
        "episode": 8,
        "blacklist_id": 5346779973,
        "id": 430785
    },
]}
```

If you need delete more episode just add new episodes to JSON (example in the file you can look it).

## Run

Just run python file.

```bash
python main.py
```

## Notes

If you have any problem with script you can open issue or contact me via Issues tab.
