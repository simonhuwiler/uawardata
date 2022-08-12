# Ukraine War Data

## What you will find here
In this repository you will find the data we use on [www.uawardata.com](https://www.uawardata.com). You can use this data for free, but please note the citation (see below).

## How to cite
If you want to use this data, please quote us. You have two options:
* Henry Schlottman (https://twitter.com/HN_Schlottman)
* uawardata.com (https://www.uawardata.com)

## The data
*If you already use the data, have a look at the chapter `Data Structure Changes` for any recent changes*  

All data is stored in the folder [`/data`](./data) as [csv](./data/csv) and [geojson](./data/geojson). The structure:

### Units
Files:
* `units_all.geojson` and `units_all.csv`: All data points
* `units_current.geojson` and `units_current.csv`: Only the most current day

The **Unit**-files contains the units and where approximately their headquarters might be. Each unit in turn consists of different battalions (more about this later). The columns/properties of the files:

| Property | Type | Description |
|----------|------|-------------|
|date|*str*|At which date a unit was there (`%Y-%m-%d`)|
|lat|*float*|Latitude, only in CSV|
|lng|*float*|Longitude, only in CSV|
|icon|*str*|Nato symbol (MIL-STD-2525C).|
|icon15|*str*|Nato symbol (MIL-STD-2525C) but with a length of 15 chars. Missing chars are filled with `-`. Handy for ArcGIS-Users|
|type|*str*|Type of units (eg *Mechanized Infantry*)|
|strength|*str*|Strength of units (eg *Battalion*)|
|strength_in_btg_number|*number*|Approx. Strength in Batallion Tactical Groups|
|strength_in_btg_text|*text*|Approx. Strength in Batallion Tactical Groups (could be `< 1`)|
|unit|*str*|Name of the unit|
|unitnumber|*str*|Name of the unit|
|subordinate_to|*str*|Subordinates to which unit|
|sources_url|*str*|Comma separated list with URL to Sources|
|sources_date|*str*|Comma separated list with date of source. Corresponds with `sources_url`|
|country|*enum*|Country where the unit is from. One of these: `ru`, `ua`, `na`|
|stacked|*bool*|`True` if more than one feature/unit is at this exact location|

### BTGs
Files:
* `btgs_all.geojson` and `btgs_all.csv`: All data points
* `btgs_current.geojson` and `btgs_current.csv`: Only the most current day

The **BTGs**-files contains the position of each individual unit (brigades, divisions, etc.). This file is the most accurate representation of the military presence.

| Property | Type | Description |
|----------|------|-------------|
|date|*str*|At which date a unit was there (`%Y-%m-%d`)|
|lat|*float*|Latitude, only in CSV|
|lng|*float*|Longitude, only in CSV|
|unit|*str*|Name of the unit|
|type_of_btg|*enum*|Type of unit. One of these: `motor_rifle`, `vdv` (Russian Airborne Forces), `tank`|
|country|*enum*|Country where the unit is from. One of these: `ru` (Russia), `ua` (Ukraine), `na` (unknow)|

## Data Structure Changes
**`2022-08-12` Added Sources**  
Added the columns `sources_url` and `sources_date`

**`2022-05-17` Added icon15 für ArcGIS-Users**  
Added column `icon15`. The MIL-STD-2525C-Symbol will have a length of 15 chars. Filled from the right with `-`.

**`2022-04-24` Added country code**  
Added country code to field `country`. One of these:
* `ru` = Russia
* `ua` = Ukraine
* `na` = unknown

**`2022-04-22` Multiple icons at same location**  
Now several icons can have the same coordinates. On uawardata.com they are displayed stacked, one above the other. In the data, they are still added separately.  
These Units are marked with `stacked = true`

## Accuracy Ukrainian troops
We reduce accuracy of Ukrainian troops and show:
* Only data from official government sources
* We do no other OSINT analysis (equipment, .etc.)
* Coordinates will be only 3 significant figures

## Methodology
The data is collected by Henry Schlottman, a former U.S. Army analyst. Using known troop positions before the war began, pictures of (destroyed) Russian war equipment, information from prisoners, and other public data, he is able to record the approximate position of each unit. Despite all the information, the data remain approximations.

## Thanks to
This project is only possible because of these people and companies:
* [maptiler.com](https://www.maptiler.com/), our technology sponsor. Check them out!
* [Volodymyr Agafonkin](https://agafonkin.com/), an Ukrainian Software developer and founder of the framework that powers the map
* The OSINT-Community

## Credits
Made by [Henry Schlottman](https://twitter.com/HN_Schlottman) and [Simon Huwiler](https://twitter.com/simon_huwiler)