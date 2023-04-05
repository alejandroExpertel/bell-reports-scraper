import requests
import time

SLEEP_EVERY_CHECK_FINISHED = 10
MAXIMUM_RUN_TIME = 60 * 5 #300



class BellAuthorizationCode(object):

    URL = "https://portal.visualbill.com/tools/bell_code"
    code = ""
    startTime = ""

    def __init__(self):
        self.code = ""
        self.session = requests.Session()
        self.startTime = int(time.time())


    def check(self):
        timeDiff = int(time.time()) - self.startTime
        response = self.session.post(self.URL+'?offset='+str(timeDiff)).json()
        if response == None:
            return False

        self.code = response.get('code')
        return True

    def getCode(self):
        elapsed_time = 0
        maximum_time = MAXIMUM_RUN_TIME
        while not self.check():
            time.sleep(SLEEP_EVERY_CHECK_FINISHED)
            elapsed_time += SLEEP_EVERY_CHECK_FINISHED
            if elapsed_time is not None and elapsed_time > maximum_time:
                raise Exception("The execution time exceeded a maximum time of {} seconds. It takes {} seconds.".format(
                                               maximum_time, elapsed_time))

        return self.code


