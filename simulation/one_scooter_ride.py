from database.new_scooter import ScooterFactory
from simulation.Simulation import simulate_one_ride

if __name__ == "__main__":
    scooter = ScooterFactory.create(
        battery_model="Dualthron Thunder",
        cokolwiek="cokolwiek2",
        y=19.913833776717745,
        x=50.067602018072364,
        battery_level=1.5
    )
    simulate_one_ride(2020, 3, 1, 10, 12, 54, scooter, mode="print", next_point=[19.936798813465444, 50.06204171628422])
