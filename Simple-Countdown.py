import time
import winsound
#----------------------------------------------------
def CountDown(mins, seconds):
    while True:
        print(f'{mins}:{str(seconds).zfill(2)}')
        
        if mins == 0 and seconds == 0:
            for i in range(5):
                winsound.Beep(500, 500)
            break
        
        seconds -= 1
        if seconds < 0:
            if mins > 0:
                mins -= 1
                seconds = 59
        
        time.sleep(1)

mins = int(input('mins : '))
seconds = int(input('seconds : '))

CountDown(mins, seconds)
