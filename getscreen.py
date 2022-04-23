from win32api import GetSystemMetrics
from win32con import SM_CMONITORS


monitornumber = GetSystemMetrics(SM_CMONITORS)
print(monitornumber)
