# import serial
# import time
#
# number = 0
# port_open = False
# connect = None
# while not port_open and number <= 30:
#     arduino_port = "/dev/ttyACM" + str(number)
#     print("\nConnecting to Arduino on port ", arduino_port, "...")
#     try:
#         connect = serial.Serial(arduino_port, timeout=1)
#         print("\nSUCCESSFULLY connected to Arduino on ", arduino_port)
#         port_open = True
#
#     except Exception as e:
#         print(e)
#         print("\nFailed to connect Micro Controller on port ", arduino_port)
#         number += 1
#         port_open = False
#
# if port_open:
#     # print("\nPREPARING THE WEB BROWSER...\n")
#     # browser = webdriver.Chrome(
#     #     executable_path="C:/Users/EBUBEDIKE/Documents/PROGRAMING/CORE-PYTHON/WEBDRIVERS/chromedriver",
#     #     keep_alive=True)
#     time.sleep(1)
#     print("waiting for data...")
#     while port_open:
#         # connect.flushInput()
#         rfid_data = connect.readline().strip()
#         if len(rfid_data) > 0:
#             decoded = rfid_data.decode("utf-8")
#             print(decoded, "\ncard scanned!")


# from django.core.cache import cache

def multipliers():
    return [lambda x: i * x for i in range(4)]


final = [m(2) for m in multipliers()]
print(final)
