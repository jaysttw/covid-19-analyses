# covid-19-analyses
Repository for analyses of publicly available COVID-19 datasets.

This repository currently covers data from the following sources:
* JHU CSSE (https://github.com/CSSEGISandData/COVID-19)
* World Bank (http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv)
* Google Mobility Data (https://www.google.com/covid19/mobility/)

### TODO:
* Build out visualisation of time series, particularly for exploring the rate at which the number of cases and the number of deaths rise.
    * To be further expanded to a proper dashboard using `dash` to visualise the key details of:
        * Total number of cases globally
        * The current rates of increase
        * Line graph showing historical rates of increase globally and for said 3 countries
        * Highlights of 3 countries.
* Build simple country-level model predicting the number of cases/deaths
* Integrate other data sources, such as:
    * University of Oxford Coronavirus Government Response Tracker (https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker)