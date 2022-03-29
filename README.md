# Ukraine Tactial Map Data

## What you will find here
In this repository you will find the data we use on www.????.com. You can use this data for free, but please note the citation (see below).

## How to cite
If you want to use this data, please quote us. You have two options:
* Henry Schlottman (https://twitter.com/HN_Schlottman)
* www.????.com

## The data
All data is stored in the folder [`/data`](./data) as a csv and geojson. How they are structured:

### `units.geojson` and `units.csv`
This file contains the units and where approximately their headquarters might be. Each unit in turn consists of different battalions (more about this later). The columns/properties of the file:

| Property | Type | Description |
|----------|------|-------------|
|lat|*float*|Latitude, only in CSV|
|lon|*float*|Longitude, only in CSV|
|date|*str*|At which date a unit was there|
|icon|*str*|Nato symbol (MIL-STD-2525C).|
|type|*str*|Type of units (eg *Mechanized Infantry*)|
|strength|*str*|Strength of units (eg *Battalion*)|
|strength_in_btg|*str*|Approx. Strength in Batallion Tactical Groups|
|unit|*str*|Name of the unit|
|number|*number*|Name of the unit as a number|
|subordinate_to|*str*|Subordinates to which unit|

### `btgs.geojson` and `btgs.csv`
In this file the positions of the individual units (brigades, divisions, etc.) are stored. This file is the most accurate representation of the war.

| Property | Type | Description |
|----------|------|-------------|
|lat|*float*|Latitude, only in CSV|
|lon|*float*|Longitude, only in CSV|
|date|*str*|At which date a unit was there|
|unit|*str*|Name of the unit|
|type_of_btg|*enum*|Type of unit. One of these: `motor_rifle`, `vdv` (Russian Airborne Forces), `tank`|

## Method
The data is collected by Henry Schlottman, a former U.S. Army analyst. Using known troop positions before the war began, pictures of (destroyed) Russian war equipment, information from prisoners, and other public data, he is able to record the approximate position of each unit. Despite all the information, the data remain approximations.