# evictions

## Using Court Scraper
_`court_scraper.py`_

Once you install TamperMonkey and this script follow these steps:

1. Install [TamperMonkey](https://www.tampermonkey.net/)
1. Install [court_scraper.py](court_scraper) into TamperMonkey
1. Go to the Court Records site directly via this link: https://www.clericusmagnus.com:8443/profoundui/start?pgm=EDOCS/WDI040CL&p1=%20CH&l1=3
1. If installed successfully there should be a white box in the upper right hand corner
1. Navigate to “View Court Schedule”. Then two buttons should appear in that white box. “Next Week” and “Next Month”
1. Clicking one of those buttons will take you to the search result page for the next 7 days or 30 days, starting from the date in the From Box. Then it will navigate you back to the search parameters page.
1. If the search worked there should now be an “Export” button in that white box. You can click that to get a .csv of the results or keep clicking the Next Week/Month buttons to generate more results. The export will keep track of every search you run so you don’t need to click it after every search