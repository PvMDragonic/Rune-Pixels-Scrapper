# Rune-Pixels-Scrapper
A tool made using Selenium for scrapping the records of daily total XP for a given list of clan names from RunePixels.

## Usage
Feed a list of clan names into the `scrap()` function. The names must have hyphens as word separators (`Drunken-Dwarf`; `Rom-Rom-Purr`; etc), otherwise it wont load the correct RunePixels clan page.

## Limitations
* If the clan has days where it didn't gain any XP randomly scattered throughout the month, the scrapper will just bundle the days that have XP together, as it can't handle empty gaps. Screw `<canvas>`, honestly.

* Very very small XP columns may also go unnoticed, as the scrapper tries to hover over them so the XP for that day gets loaded in.

* Sometimes it takes a while for a given page to load, as RunePixels seems to be a bit slow. The scrapper waits for five seconds before searching for the desired HTML elements, and if the page doesn't load properly by then, it'll crash (as it wont find the canvas). 