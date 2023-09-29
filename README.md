## Cobblr

This tool allows you to ingest and clean api data, at the moment it's sources are limited but additional functionality will be added that allows for conversational data ingestion and endpoint building.

## Installation 
git clone https://github.com/EEXstnce/cobblr

cd cobblr

pip install -r requirements.txt

## Endpoints can easily be added!
cd source

add a new .py file for the parent source, or if the parent source already exists add the function to the parent source file

use a structure similar to other files in source to design your endpoint function

add the following to api_func_config.json-- 
  "/new_enpoint": {
    "func": "function_name",
    "url": "url.com/this_uses_keys/{0}/{1},
    "alias": "source.parent_file",
    "keys": ["key1","key2"],
    "config": ["these","are","the","keys","from", "data"]
  }

then restart the application and the data source will be available.

## Usage

If you'd like to get the data endpoint up and running very quickly it can be as simple as suggesting a commit to the cobblr repo with the new functions and the addition to api_func_config.json, if you want to run yourself a good solution is replit which will create an always online version for free or very cheaply.