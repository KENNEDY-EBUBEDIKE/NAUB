import requests
import serial
import time
import sys
from selenium import webdriver


def main(current_exam):
    ip_address = "http://127.0.0.1:8000"

    """ CHECKING THE EXISTENCE OF THE ENTERED COURSE """
    try:
        ex_url = ip_address + "/exams/check-course/"
        response = requests.post(ex_url, data={"current_exam": current_exam})
        if response.json()["response"] == "EXAM APPROVED":
            pass
        else:
            print(response.json())
            sys.exit()
    except requests.ConnectionError or requests.Timeout:
        print("\nWEB SERVER NOT RUNNING!!!")
        sys.exit()

    """
    ESTABLISHING MICRO CONTROLLER CONNECTIONS
    """

    number = 1
    port_open = False
    while not port_open and number <= 30:
        arduino_port = "COM" + str(number)
        print(number)
        print("Connecting to MICRO CONTROLLER on port ", arduino_port)
        try:
            global connect
            connect = serial.Serial(arduino_port, timeout=1)
            print("Successfully connected to MICRO CONTROLLER on ", arduino_port)
            port_open = True

        except WindowsError:
            print("Failed to connect MICRO CONTROLLER on port ", arduino_port)
            number += 1
            print(arduino_port)
            port_open = False

    if not port_open:
        print("\nMICRO CONTROLLER NOT CONNECTED !!!")
        sys.exit()

    if port_open:
        print("PREPARING THE BROWSER....")
        browser = webdriver.Chrome(
            executable_path="C:/Users/EBUBEDIKE/Documents/PROGRAMING/CORE-PYTHON/WEBDRIVERS/chromedriver",
            keep_alive=True)
        time.sleep(1)
        print("waiting for data")

        while True:
            rfid_data = connect.readline().strip()

            if len(rfid_data) > 0:
                decoded = rfid_data.decode("utf-8")
                print(decoded)

                try:
                    idurl = ip_address + "/students/get-id/"
                    response = requests.post(idurl, data={"rfid_code": decoded})
                    student_id = response.json()['student_id']
                except requests.ConnectionError or requests.Timeout:
                    print("\nWEB SERVER NOT RUNNING!!!")
                    browser.quit()
                    break

                if not student_id == "00000":

                    url = ip_address + "/exams/exam-profile/" + str(student_id) + "/" + current_exam

                    try:
                        browser.get(url)
                    except Exception as e:
                        print(e)
                        print("INTERNET_DISCONNECTED "
                              " 404 URL Not Found")
                        browser.quit()
                        sys.exit()
                else:
                    browser.get(ip_address + '/students/error/')


if __name__ == '__main__':
    main("MTH121")
