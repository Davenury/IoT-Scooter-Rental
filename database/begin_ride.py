from time import sleep

import psycopg2


def begin_ride(scooter, conn):
    cur = conn.cursor()

    cur.execute(
        'select actual_time from scooter_info where scooter_id = %s order by actual_time desc limit 1',
        (scooter.id,)
    )
    start_time = cur.fetchone()[0]

    cur.execute(
        'select id, client_id from rides where scooter_id = %s and start_time = %s',
        (scooter.id, start_time)
    )
    result = cur.fetchone()
    if result is not None:
        ride_id, client_id = result
        print(ride_id, client_id)
        return ride_id, client_id
    return -1, -1


def set_begin_attributes(scooter):
    print("before while")
    try:
        conn = psycopg2.connect(host="scooter-database.cciikk1f6cy6.us-east-1.rds.amazonaws.com", port=5432,
                                dbname="postgres", user="scooter",
                                password="scooter1"
                                )

        while scooter.ride == -1:
            print(f"{scooter.id} set_begin_attributes")
            scooter.ride, scooter.user_id = begin_ride(scooter, conn)
            sleep(0.2)
        print("ok")
    finally:
        try:
            conn.close()
        except:
            pass
        if scooter.ride == -1 and scooter.user_id == -1:
            set_begin_attributes(scooter)
