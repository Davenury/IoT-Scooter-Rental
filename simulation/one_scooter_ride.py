from devices.new_scooter import ScooterFactory
from simulation.Simulation import simulate_one_ride

if __name__ == "__main__":
    scooter = ScooterFactory.create(
        battery_model="Dualthron Thunder",
        cokolwiek="cokolwiek2",
        y=19.913833776717745,
        x=50.067602018072364,
        battery_level=80,
        set_custom_battery_functions=False
    )
    simulate_one_ride(scooter, mode="print", next_point=[19.936798813465444, 50.06204171628422])
