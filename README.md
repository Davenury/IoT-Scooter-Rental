# IoT-Scooter-Rental
![Language](https://img.shields.io/badge/Language-Python-blue) ![Type](https://img.shields.io/badge/Type-Backend-gray)

### Table of contents
* [Documentation](#documentation)
* [Code structure](#code-structure)
* [How to get this to work?](#how-to-get-this-to-work)
  * [How to run full simulation?](#how-to-run-full-simulation)
  * [How to run one simulation for one scooter?](#how-to-run-one-simulation-for-one-scooter)
* [Create your own scooter!](#make-your-own-scooter)

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
* devices - directory with all IoT devices classes and things that are necessary for them to work.
  * battery_dict_file.py - file with python dictionary that storage the maximum distance that this battery model can run without charging.
  * Telemetry.py - file that consists Telemetry class. It's used to wrap all necessary informations about the scooter's state.
  * Scooter.py - file that consists Scooter class implentation. Scooter class consists methods that are required to communicate with AWS IoT broker.
  * new_scooter.py - file that consists ScooterFactory class. ScooterFactory makes new scooter out of kwargs that are passed as an argument (more about this in Make your own scooter section).
* others/exceptions.py - file that consists our custom StopSimulationException.
* python - directory with compiled library psycopg2 that we needed to upload to AWS lambda functions, so they could connect to Postgres database.
* simulation - directory with files that are responsible for running different types of simulations.
  * one_scooter_ride.py - file that permits the user to create his own parametrized scooter and runs one ride for it.
  * run.py - file that creates ten scooters and then runs parallel simulation on them all.
  * Simulation.py - file that contains implementations of different types of simulations and all helper functions that we thought could be useful for us (also they made the code cleaner).
* We have also certificates directory, that consists AWS certificates and file credentials.json. This file consists a key to OpenRouteService that we used to simulate rides.
  
---

### How to get this to work?
To prepare this project for work, create virtual enviroment (`python -m venv ./<name_of_your_venv>`) and then type `pip install -r requirements.txt`, so all necessary modules can be installed.
To run this simulation you'll also need a certificates directory with file "credentials.json". In there, you'll need to make
```
{
 "key": "<YOUR_API_KEY>" 
}
```
You can get API_KEY from [this site](https://openrouteservice.org/plans/) (of course you need to sign up for this). Otherwise, the simulation won't work! After signing up and confirming your e-mail, you'll be redirected to site, where you can copy your API_KEY.

#### How to run full simulation?
To run parallel simulation on ten scooters, you have two possibilities:
* if you're using PyCharm, just click on the green arrow.
* if you're not using PyCharm, go to your cmd, cd to simulation directory and then type `python run.py`
Please note, that this simulation runs in parallel and it's running in print mode, so things you're going to see in your terminal can be quite messy. We used this type of simulation with send mode, so we could just send data to AWS broker but for this you'd need to have a certificates that (from obvoius reasons) aren't in Github.


#### How to run one simulation on one scooter?
To run one simulation on one scooter you also have two possibilities:
* if you're using PyCharm, go to one_scooter_ride.py file and click green arrow.
* if you're not using PyCharm, go to your cmd, cd to simulation directory and type `python one_scooter_ride.py`

---

### Make your own scooter!
We've also included a way to make a brand new scooter that will be personalized to you. To make yourself one scooter, go to one_scooter_ride.py file. In line 8, you'll find line: "scooter = ScooterFactory.create(". Then, there's a list of parameters that you can modify to your needs. You don't have to include them all but then, they'll be defalut. Table with parameters that you can change:
|Parameter|Type of parameter|Mean of parameter|
|---|---|---|
|battery_model|String|Model of battery of your scooter|
|battery_level|float|Start battery level|
|battery_temp|float|Start battery temperature|
|vehicle_type|int|Type of your scooter|
|mac|String|MAC address of your scooter|
|set_custom_battery_functions|boolean|For details look below|
|x|float|x coordination of started position of your scooter|
|y|float|x coordination of started position of your scooter|

If you set custom battery model (one that isn't "Dualthron Thunder" or "AGDA Electric"), you'll have to also include additional position in max_battery_distance_dict, that will look like `"<YOUR_BATTERY_MODEL_TYPE>": n,`, where n is maximal number of kilometers that your battery could ride before charging.

If you want to set custom methods that will calculate battery level drop and battery temperature rise between two points, set parameter "set_custom_battery_functions" to True and then go to new_scooter file and in ScooterFactory class implement your custom methods (new_scooter_battery_drop_function and new_scooter_battery_temp_raise_function).
