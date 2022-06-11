# import sys
import serial
import requests


def main():
    ip_address = "http://127.0.0.1:8000"
    number = 1
    port_open = False
    while not port_open and number <= 30:
        arduino_port = "COM" + str(number)
        print("\nConnecting to Arduino on port ", arduino_port, "...")
        try:
            global connect
            connect = serial.Serial(arduino_port, timeout=1)
            print("\nSUCCESSFULLY connected to Arduino on ", arduino_port)
            port_open = True

        except WindowsError:
            print("\nFailed to connect Arduino on port ", arduino_port)
            number += 1
            port_open = False

    if not port_open:
        print("\nMICRO CONTROLLER NOT CONNECTED !!!")

    if port_open:
        print("waiting for data...")
        while port_open:

            # connect.flushInput()
            rfid_data = connect.readline().strip()

            if len(rfid_data) > 0:
                global decoded
                decoded = rfid_data.decode("utf-8")
                print("\ncard scanned!")

                try:
                    url = ip_address + "/staff-attendance"
                    response = requests.post(url, data={"rfid_code": decoded})
                    status = response.json()['status']
                    print(status)
                except requests.ConnectionError or requests.Timeout:
                    print("\nWEB SERVER NOT RUNNING!!!")
                    break


if __name__ == '__main__':
    main()
