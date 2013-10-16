# -*- coding: utf-8 -

import logging
import logging.config
import urllib2
import threading
import time
import sys

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "file": {
            "format": "%(asctime)-15s %(name)s.py <%(funcName)s> %(message)s"
        },
    },

    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "filename": "log/app.log"
        },
    },

    "root": {
        "handlers": ["file"],
        "level": "DEBUG",
    }
})

log = logging.getLogger(__name__)


class StressTest(threading.Thread):
    def __init__(self, name, url, qps):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url
        self.qps = qps
        self.sleep_time = 1.0 / qps
        log.info('sleep time is ' + str(self.sleep_time) + ' s')

    def run(self):
        global success
        global fail

        while True:
            p_time = time.time()
            content = urllib2.urlopen(self.url).read()
            #log.info("current time is " + str(time.time()))

            if content.strip():
                if mutex.acquire(1):
                    success += 1
                    mutex.release()

                    ##log.info(self.name + ' access ' + self.url + ' success')

            else:
                if mutex.acquire(1):
                    fail += 1
                    mutex.release()

                    ##log.info(self.name + ' access ' + self.url + ' fail')

                    ##if count % 100 == 0:
                    ##  log.info(
                    ## self.name + ' success accessed times is ' + str(success) + ' failed accessed times is ' + str(fail))

            last_time = time.time() - p_time
            ##log.info("request time is " + str(last_time))
            if last_time >= self.sleep_time:
                continue
            else:
                time.sleep(self.sleep_time - last_time)


## statistic thread
class Watcher(threading.Thread):
    def __init__(self, time_unit):
        threading.Thread.__init__(self)
        self.time_unit = time_unit

    def run(self):
        global success
        global fail
        global start_time

        while True:
            previous_success = success
            previous_fail = fail
            time.sleep(self.time_unit)

            total_current_req = success + fail - previous_success - previous_fail

            log.info("total send " + str(success + fail) + " , it costs " + str(time.time() - start_time))

            if success + fail > 0 and total_current_req > 0:
                log.info('average qps : ' + str((success + fail) / (time.time() - start_time)) + " ration : " + str(
                    success * 100.0 / (success + fail)) + "% current qps : " + str(
                    (success + fail - previous_success - previous_fail) / statistic_time) + " ration : " + str(
                    (success - previous_success) * 100.0 / total_current_req) + "%")


success = 0
fail = 0
mutex = threading.Lock()
statistic_time = 5  # 统计区间，
start_time = time.time()


def stress_load_work(url, qps, thread_num):
    assert (qps > 0)
    assert (thread_num > 0)

    threads = []
    for i in range(thread_num):
        work = StressTest("thread" + str(i), url, qps)
        work.start()
        threads.insert(0, work)

    #run statistic thread
    watcher_thread = Watcher(statistic_time)
    watcher_thread.start()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'parameter is not correct'
        print 'you need to input url, qps per thread, number of threads'

    else:
        print 'you are going to load stress test on ' + str(sys.argv[1])
        print 'the qps per thread is ' + sys.argv[2] + ', and the thread num is ' + sys.argv[3]
        stress_load_work(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]))









