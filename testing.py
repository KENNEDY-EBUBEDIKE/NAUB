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

# def multipliers():
#     return [lambda x: i * x for i in range(4)]
#
#
# final = [m(2) for m in multipliers()]
# print(final)


# def solution(A):
#     # write your code in Python 3.6
#     multiples = [num for num in A if num % 4 == 0]
#     result = sum(multiples)
#     print(result)
#
#
# solution([2,5,6,8,44,40,20])


# def solution(A):
#     # write your code in Python 3.6
#     count = 0
#     for i in range(len(A)):
#         if i != len(A) - 1:
#             if A[i] == A[i +1]:
#                 if A[i + 1] == 0:
#                     A[i + 1] = 1
#                     count += 1
#                 elif A[i + 1] == 1:
#                     A[i + 1] = 0
#                     count += 1
#     print(A, count)
#
# solution([1,1,0,1,1])


def solution(A):
    if len(A) > 0:
        count1 = 0
        count2 = 0
        for index in range(len(A)):
            if index % 2 == 0:
                if A[index] == 1:
                    count1 += 1
                if A[index] == 0:
                    count2 += 1
            else:
                if A[index] == 0:
                    count1 += 1
                if A[index] == 1:
                    count2 += 1
        print(count1, count2)
        return min(count1, count2)


print(solution([1,1,0,1,1,1]))
