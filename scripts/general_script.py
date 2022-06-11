from selenium import webdriver
import time
import os
import requests
import sys
import serial
from serial.serialutil import SerialException
# from ast import literal_eval


def connect_hardware():
    number = 0
    port_open = False
    connection = None
    while not port_open and number <= 30:
        device_port = "/dev/ttyUSB" + str(number)  # for Linux
        # device_port = "COM" + str(number)  # for windows
        print("\nConnecting to Device on port ", device_port, "...")
        try:
            connection = serial.Serial(device_port, timeout=1)

            print("\nSUCCESSFULLY connected to Device on ", device_port)
            port_open = True
            return port_open, connection

        except Exception as e:
            print(e)
            print("\nFailed to connect Micro Controller on port ", device_port)
            number += 1
            port_open = False
    return port_open, connection


def browser_setup():
    print("\nPREPARING THE WEB BROWSER...\n")
    browser = webdriver.Firefox(
        # executable_path='C:/Users/EBUBEDIKE/Documents/WEB-DEVELOPMENT/NAUB-RFID/RFID_MGT/scripts/geckodriver',
        executable_path='geckodriver',
        keep_alive=True)
    time.sleep(1)
    browser.implicitly_wait(2)
    browser.set_page_load_timeout(10)
    return browser


def post_selenium(url: str, data: dict):
    input_template = '<input type="hidden" name="{k}" id="{k}" value="{v}"><BR>\n'
    inputs = ""
    print(data)
    if data:
        for k, v in data.items():
            if v != '':
                inputs += input_template.format(k=k, v=v)
        html = f'<html><body>\n<form action="{url}" method="post" id="form-id">\n' \
               f'{inputs}<input type="submit" id="input-box">\n</form></body></html>'

        html_file = os.path.join(os.getcwd(), 'temp.html')
        with open(html_file, "w") as text_file:
            text_file.write(html)

        return html_file


def main(server_address, button):
    ip_address = "http://" + str(server_address)

    if button == "access":
        port_open, connection = connect_hardware()
        if port_open:
            browser = browser_setup()
            time.sleep(1)
            print("waiting for data...")
            while port_open:
                try:
                    rfid_data = connection.readline().strip()
                    if len(rfid_data) > 1:
                        rfid_code = rfid_data.decode("utf-8")
                        # dec_code  = re.sub(r'[\x00-\x1F]+', '', rfid_code)
                        # print(dec_code)
                        url = ip_address + "/scan-profile/"
                        html_file = post_selenium(url=url, data={"rfid_code": rfid_code})
                        try:
                            browser.get(f"file://{html_file}")
                            browser.find_element_by_id('input-box').click()
                        except Exception as e:
                            print("\nWEB SERVER NOT RUNNING!!!\n", e)
                            # browser.close()
                            # break
                except SerialException:
                    print("Device Disconnected")
                    port_open = False

    elif button == "exam":
        current_exam = input("Enter Current Exam: ")
        try:
            ex_url = ip_address + "/exams/check-course/"
            response = requests.post(ex_url, data={"current_exam": current_exam})
            if response.json()["response"] == "EXAM APPROVED":
                port_open, connection = connect_hardware()
                if port_open:
                    browser = browser_setup()
                    time.sleep(1)
                    print("Browser Ready")
                    while port_open:
                        try:
                            rfid_data = connection.readline().strip()
                            if len(rfid_data) > 1:
                                rfid_code = rfid_data.decode("utf-8")
                                print(rfid_code, "  card scanned!")
                                url = ip_address + "/exams/exam-profile/"
                                html_file = post_selenium(url=url, data={
                                    "rfid_code": rfid_code,
                                    "current_exam": current_exam
                                                                         })
                                try:
                                    browser.get(f"file://{html_file}")
                                    browser.find_element_by_id('input-box').click()
                                except Exception as e:
                                    print("\nWEB SERVER NOT RUNNING!!!\n", e)
                                    # browser.close()
                                    # break
                        except SerialException:
                            print("Device Disconnected")
                            port_open = False
            else:
                print(response.json()["response"])
                sys.exit()
        except requests.ConnectionError or requests.Timeout:
            print("\nWEB SERVER NOT RUNNING!!!")
            sys.exit()

    if button == "staff_attendance":
        port_open, connection = connect_hardware()
        if port_open:
            print("Ready For Scan....")
            try:
                while port_open:
                    try:
                        rfid_data = connection.readline().strip()
                        if len(rfid_data) > 1:
                            rfid_code = rfid_data.decode("utf-8")
                            print(rfid_code, "  card scanned!")
                            url = ip_address + "/staff/staff-attendance/"
                            response = requests.post(url, data={"rfid_code": rfid_code})
                            print(response.json()['status'])
                            print("Ready For Scan....")
                    except SerialException:
                        print("Device Disconnected")
                        port_open = False
            except Exception as e:
                print("\nWEB SERVER NOT RUNNING!!!", e)


if __name__ == '__main__':
    try:
        main('127.0.0.1:8000', button='access')
    except KeyboardInterrupt:
        sys.exit()
