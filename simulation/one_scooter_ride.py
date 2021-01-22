from database.new_scooter import ScooterFactory
from simulation.Simulation import simulate_one_ride

if __name__ == "__main__":
    scooter = ScooterFactory.create(battery_model="whatever", cokolwiek="cokolwiek2")
    simulate_one_ride(2020, 3, 1, 10, 12, 54, scooter, mode="print", next_point=None)
