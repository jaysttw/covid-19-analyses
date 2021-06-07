# covid-19-analyses
Repository for analyses of publicly available COVID-19 datasets.

This repository currently covers data from the following sources:
* JHU CSSE (https://github.com/CSSEGISandData/COVID-19)
* World Bank (http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv)
* Google Mobility Data (https://www.google.com/covid19/mobility/)
* University of Oxford Coronavirus Government Response Tracker (https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker)

### TODO:
* [x] Build out visualisation of time series, particularly for exploring the rate at which the number of cases and the number of deaths rise.
    * [x] To be further expanded to a proper dashboard using `dash` to visualise the key details of:
        * [x] Total number of cases globally
        * [x] The current rates of increase
        * [x] Line graph showing historical rates of increase globally and for said 3 countries
        * [x] Highlights of 3 countries.
* [] Build simple country-level model predicting the number of cases/deaths
* [] Build new notebook for easy debugging of import errors.
* [] Clean and update `requirements.txt` for easy deployment.
    * Currently set to a generic environment with unused packages included. 
* [] Integrate other data sources, such as: