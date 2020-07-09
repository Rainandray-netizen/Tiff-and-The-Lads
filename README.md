TO RUN THIS CODE:
Ensure 'django-environ' and 'requests' are installed locally and create a .env file with the necessary variables

<img src="https://s3.ca-central-1.amazonaws.com/ehq-production-canada/b070f59b49e4a9161ff1f83fb03bfe8d05afbafd/original/1588346798/COVID-19-Engagement-Banner-1440-x-480-v2020.5-without-Virus.jpg_1ed9937e363c83bfa99cd19634def914?1588346798"/>

# COVID-19 Tracker and Activity Assessment 
> A data tracker and activity risk assessment in one.  

## Table of Contents
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [API](#api)
- [Resources](#resources)
- [Planning](#planning)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
- [Next Steps](#next-steps)
- [Contributors](#contributors)


## About
This app was created at the height of the COVID-19 global pandemic and inspired by [this](https://www.texmed.org/TexasMedicineDetail.aspx?id=53977) graph. In light of reopenings, restrictions being lifted and some improvements in numbers, many people are engaging in activities that may potentially be very risky but also many activities that people may think are very risky but are not. Get the latest COVID-19 stats on your country, assess, track and save how risky your daily activities are. This app aims to encourage people to disengage in highly risky activities as well as educate individuals on the safety procedures and alternative activities they may engage in. 


## Features
- As a visitor you are able to view global stats and do a general risk assessment for common activities. 
- The following features are available for logged in/signed up users...
    - Profile
        - As a user you are able to create your own personalized activities. When adding an activity, a function based on provided factors and our [resources](#resources) calculates a risk factor for you. 
        - When viewing the details for a specific activity you have added you are able to see recommendations and safety procedures based on a given risk level.
    - Dashboard
        - Based on the location you have entered in, your dashboard will be personalized to show you COVID-19 data pertaining to your country.
        - An overview of all your activities you have and the activities you have added to your current day.

## Tech Stack
- HTML + CSS
- Javascript
- Materialize
- Python
- Django
- Postgresql

## API
We used the COVID-19 API using data from John Hopkins University. This data is updated every 10 minutes. It can be found here.

## Resources
Data for risk factor calculations were sourced from CDC [here](https://www.cdc.gov/coronavirus/2019-ncov/need-extra-precautions/people-with-medical-conditions.html) and [here](https://www.cdc.gov/coronavirus/2019-ncov/daily-life-coping/going-out.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fdaily-life-coping%2Factivities.html). As well as from the Texas Medical Association [here](https://www.texmed.org/TexasMedicineDetail.aspx?id=53977). 
> Accuracy of risk factor is not guaranteed this is just an outline and estimate based on sourced data

## Planning
- [Trello](https://trello.com/b/VxQ5wmsr/team-sei)
- [ERD]()
- [Wireframes]()

## Screenshots
<img src=""/>
<img src=""/>
<img src=""/>
<img src=""/>
<img src=""/>

## Getting Started 
Click [here]() to see a demo 

## Next Steps
- 

## Contributors
<a href="https://github.com/Rainandray-netizen/Tiff-and-The-Lads/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=Rainandray-netizen/Tiff-and-The-Lads" />
</a>