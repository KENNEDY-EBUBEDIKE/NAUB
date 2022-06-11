# import sys
import serial
import time
import requests
from selenium import webdriver


def main():
    ip_address = "http://127.0.0.1:8000"
    number = 1
    port_open = False
    while not port_open and number <= 30:
        arduino_port = "/dev/ttyS" + str(number)
        print("\nConnecting to Arduino on port ", arduino_port, "...")
        try:
            global connect
            connect = serial.Serial(arduino_port, timeout=1)
            print("\nSUCCESSFULLY connected to Arduino on ", arduino_port)
            port_open = True

        except Exception as e:
            print(e)
            print("\nFailed to connect Micro Controller on port ", arduino_port)
            number += 1
            port_open = False

    if not port_open:
        print("\nMICRO CONTROLLER NOT CONNECTED !!!")

    if port_open:
        print("\nPREPARING THE WEB BROWSER...\n")
        browser = webdriver.Chrome(
            executable_path="C:/Users/EBUBEDIKE/Documents/PROGRAMING/CORE-PYTHON/WEBDRIVERS/chromedriver",
            keep_alive=True)
        time.sleep(1)
        print("waiting for data...")
        while port_open:

            # connect.flushInput()
            rfid_data = connect.readline().strip()

            if len(rfid_data) > 0:
                global decoded
                decoded = rfid_data.decode("utf-8")
                print("\ncard scanned!")


                global url
                url = ip_address + "/scan-profile/"
                print(decoded)

                check()
                try:
                    browser.get(url)
                except ConnectionError:
                    print("\nWEB SERVER NOT RUNNING!!!")
                    browser.quit()
                    break


def check():
    try:
        ip_address = "http://127.0.0.1:8000"
        idurl = ip_address + "/students/get-id/"
        response = requests.post(idurl, data={"rfid_code": decoded})
        student_id = response.json()['student_id']

        if student_id == '00000':
            connect.write("2".encode())
            connect.flushInput()
            print("\nACCESS DENIED")
        else:
            connect.write("1".encode())
            connect.flushInput()
            print("\nACCESS GRANTED")
    except requests.ConnectionError or requests.Timeout:
        print("\nWEB SERVER NOT RUNNING!!!")


if __name__ == '__main__':
    main()
