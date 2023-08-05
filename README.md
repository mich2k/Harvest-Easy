<!-- PROJECT LOGO -->
<div align="center">
  <img src="res/logo_original.png" alt="Logo" width="200" height="200">

  <h1 align="center">Harvest Easy</h1>

  <p align="center">
    Una bella descrizione
  </p>
</div>

<!-- TABLE OF CONTENTS -->
  <h4><summary>Table of Contents</summary></h4>
  <ol>
    <li><a href="#abstract">Abstract</a></li>
    <li>
    <li><a href="#goals-and-why">Goals and Why</a></li>
      <a href="#demos">Demos</a>
      <ul>
          <li><a href="#image-showcase">Image showcase</a></li>
          <li><a href="#react-frontend">React Frontend</a></li>
          <li><a href="#telegram-bot">Telegram</a></li>
          <li><a href="#alerts">Alerts</a></li>
          <li><a href="#cads-showcase">Designed CADs showcase</a></li>
      </ul>
    </li>
    <li><a href="#tech-stack">Tech stack</a></li>
    <li><a href="#hw-used">Hardware used</a></li>
    <li><a href="#slides">Project slides</a></li>
    <li><a href="#licensing">License</a></li>
    <li><a href="#contact-us">Contact Us</a></li>
  </ol>


# Abstract
Harvest Easy represents a modern solution for an old and known problem: domestic waste sorting at 360 degrees. We designed this from the really ground root, starting from the 3D CADs of the prototype up to the backend AI-powered solution and the user-friendly front-end, all equipped with the needed sensors & acturators. We started 3D printing with an organic plastic polymere (PLA) the bin prototype where we added on this the RFID reader, 16x2 LCD screen, two ESP32, different ultrasonic sensors HC-SR04, DHT11 for temperature and humidity, MQ135 for CO2 & air quality sensoring, MPU-6050 as accellerometer and gryscope module, 5W photovoltaic panel, MG90s Hi-Torque servo for the automatic lid opening, 14500 Li rechargable battery and a Solar Panel Managment with BMS (Battery Managment System) module.

(during the night the bin is powered by a battery which is recharged by a solar panel during the day.
Energy management is managed by the BMS which switches between the battery and the panel based on the energy supplied by the panel itself.)

The bin is described by 4 states: empty and intact (state 1), filled and intact (state 2), empty and tampered with (state 3), and filled and tampered with (state 4). The tampered state is reached when the bin is knocked over or set on fire. Each time the bin is opened, its internal fill level and, consequently, the status is updated. If the bin is knocked over or set on fire, a notification will be sent to the telegram bot of the apartment condominiums to which the bin belongs. If the problem cannot be solved, a report is sent to the body responsible for waste collection which will resolve it.

The telegram bot will assign a pre-established score to the condominium that will solve the reported problem. The points mechanism allows you to introduce a leaderboard showing the most active condominiums (those that have solved the most problems).

In order to discourage the abandonment of waste near the bin if it is full, Harvest Easy introduces a "proximity" system: when the condominium swipes the card to authenticate, the street of the nearest free bin will be printed on the bin screen.

Harvest Easy provides a system of maps through which it is possible to see all the bins present in the city of interest. You can also check what kind of bin it is and how full it is.

To improve the waste collection system, Harvest Easy can predict the possible future fill level, based on the fill level recorded each time the bin is opened.

Harvest Easy provides a waste collection optimization system: taking into account the type of vehicle, the bins to be emptied, the prediction of bins close to being filled, and the fuel level to show the optimal route for the operator to travel.




# Goals and Why

This project has been developed for the exam *IoT & 3D Intelligent Systems* @ University of Modena and Reggio Emilia we were willing to propose a solution to a paper we read that shows the impact of waste transportation *Banias, G., Batsioula, M., Achillas, C., Patsios, S. I., Kontogiannopoulos, K. N., Bochtis, D., & Moussiopoulos, N. (2020). A Life Cycle Analysis Approach for the Evaluation of Municipal Solid Waste Management Practices: The Case Study of the Region of Central Macedonia, Greece. Sustainability, 12(19), 8221* using data provided from the italian national report from 2019 viewable [here](https://www.isprambiente.gov.it/files2019/pubblicazioni/rapporti/RapportoRifiutiUrbani_VersioneIntegralen313_2019_agg17_12_2019.pdf).

Our goals are:
- Peeking into the future basing our architecture & design on autonomous driving waste retrieval trucks
- Gamified community-based whistleblowing
- Sun powered
- Low maintenance
- Easily scalable
- Data harvesting & data filtering
- Sellable clean data
- Behaviour analysis
- Ready & pluggable into other solutions
- Pluggable into private security services
- Proprietary prototype-ready license-less design
- Powerful branding & motto




# Demos

## Image Showcase

3/4 view             |  rear view
:-------------------------:|:-------------------------:
<img width="1604" alt="pic" src="./res/bin/1.png">   |  <img width="1604" alt="pic" src="./res/bin/2.png"> 


side apartment QR             |  top view
:-------------------------:|:-------------------------:
<img width="1604" alt="pic" src="./res/bin/3.jpg">   |  <img width="1604" alt="pic" src="./res/bin/5.jpg"> 


under lid/inside view             |  front view
:-------------------------:|:-------------------------:
<img width="1604" alt="pic" src="./res/bin/7.jpg">   |  <img width="1604" alt="pic" src="./res/bin/8.jpg"> 

## React Frontend

Once the apartment manager scans the bin group QR code for initialization he will be automatically redirected to the ap. init. portal on which he will add all the apartment infos such as:
- Location infos (apartment name, street, number, city)
- Tenants infos (how many, data for each including their telegram username)
- Waste sorting infos (which sorting that apartment will follow)

<img height="600" alt="pic" src="./res/gif/apartment-init.gif"> 

<hr>


After the manager inits the apartment each user will be able to login

<img height="600" alt="pic" src="./res/gif/user-login.gif"> 

<hr>

After the user logs in the apartment dashboard will be shown, here the status of each bin, infos about the apartment and future predictions are shown

<img height="600" alt="pic" src="./res/gif/user-home.gif"> 



## Telegram Bot

Each user will be able to report for damages thus earning points, some special roles like civil servants, police etc will also be able to fix the damage and flag that; these roles won't earn points with the logic that is their duty to do this.


As we can see in this clip the bot (backend) is the first to multicast to every user in that city the damage, this is possible thank to the bin sensors which allow us to detect tampering as fire, overthrow or maximum capacity reached (this last is not flagged to users).

We introduced this bot along the city limited leaderboard for citizen too as a gamification of this problem


<img height="600" alt="pic" src="./res/gif/telegram-alert-leaderboard.gif"> 



## CADs showcase


bottom            |  bottom
:-------------------------:|:-------------------------:
<img width="1604" alt="pic" src="./res/CAD/bottom.png">   |  <img width="1604" alt="pic" src="./res/CAD/bottom2.png"> 


fem wall             |  male wall
:-------------------------:|:-------------------------:
<img width="1604" alt="pic" src="./res/CAD/fem-wall.png">   |  <img width="1604" alt="pic" src="./res/CAD/male-wall.png"> 


servo-lid hand             |  top
:-------------------------:|:-------------------------:
<img width="1604" alt="pic" src="./res/CAD/hand.png">   |  <img width="1604" alt="pic" src="./res/CAD/top2.png"> 




# Tech Stack

# Alerts

<img width="500" alt="pic" src="./res/alerts.png">


# Project Presentation

If you are curious but don't want yet to deep dive into the code you can check our presentations [here](./slides/).

**Pitch:** [click here](./slides/HE%20-%20Pitch.pdf)

**Sys Design:** [click here](./slides/HE%20-%20System%20Design.pdf)

**Technical + CAD:** [click here](./slides/HE%20-%20Technical%20and%20CAD.pdf)

# Licensing

# Contact Us

# Concept:
* Stato del bidone ("sano"/malfunzionante/manutenzione)
* Sensore di riempimento (prossimità)
* Sensore di temperatura
* Sensore di "vandalismo" : accelerometro + tilt sensor, tentativo di manomissione
* Raccolta dati per effettuare predizioni sul futuro livello di riempimento
* Motore che gestisce l'apertura/chiusura del pannello
* Dati salvati in Cloud
* Tempo raccolta pattume (Tempo di riempimento)
* Percorso ottimo basato sul livello di riempimento
* Alimentato ad energia solare + batteria
* Feedback sullo stato del bidone (lato User)