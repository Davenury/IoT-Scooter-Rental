# IoT-Scooter-Rental
![Language](https://img.shields.io/badge/Language-Python-blue) ![Type](https://img.shields.io/badge/Type-Backend-gray)

### Table of contents
* [Documentation](#documentation)
* [Code structure](#code-structure)

### Documentation
Documentation (in Polish Language) can be read at https://docs.google.com/document/d/1zEjy7z5E_UMGPCno7TT_twpnFpKNj3joK38SD58azTg/edit?usp=sharing.

### Database structure
![Database structure](https://imgur.com/PoW3ih9.png)

---

### Code structure
* aws_lambda_functions - directory with all lambda functions that we used in AWS cloud:
  * begin_ride_lambda.py - file with lambda function that triggers, when we begin new ride. Then we insert new ride into rides table.
  * end_ride_lambda.py - file with lambda function that triggers, when we end ride. Then we update ride in rides table.
  * scooter_insert_data_lambda.py - file with lambda functions that triggers every time, when we send a scooter_info. Here we insert data into scooter_info. In case of emergency we also update here scooter state.
* database - dirctory with files that are supposed to prepare scooter before running of simulation:
  * begin_ride.py - file that sets client_id and ride_id to scooter.
  * scooter_prepare.py - file that sets initial values to scooter.
  
  
---

### How to get this work?

#### How to run full simulation?

#### How to run one simulation on one scooter?

---

### Make your own scooter!
