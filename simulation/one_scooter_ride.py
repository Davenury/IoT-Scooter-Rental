from database.new_scooter import ScooterFactory
from simulation.Simulation import simulate

if __name__ == "__main__":
    scooter = ScooterFactory.create(battery_model="whatever", cokolwiek="cokolwiek2")
    simulate(2020, 3, 1, 10, 12, 54, scooter, 1, mode="print")
