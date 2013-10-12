# -*- coding: utf-8 -

import logging
import logging.config
import urllib2
import threading
import time

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

        count = 0

        while True:
            count += 1
            time.sleep(self.sleep_time)
            content = urllib2.urlopen(self.url).read()

            if content.strip():
                if mutex.acquire(1):
                    success += 1
                    mutex.release()

                log.info(self.name + ' access ' + self.url + ' success')

            else:
                if mutex.acquire(1):
                    fail += 1
                    mutex.release()

                log.info(self.name + ' access ' + self.url + ' fail')

            if count % 10 == 0:
                log.info(
                    self.name + ' success accessed times is ' + str(success) + ' failed accessed times is ' + str(fail))


success = 0
fail = 0
mutex = threading.Lock()


def stress_load_work(url, qps, thread_num, lasting):
    assert (qps > 0)
    assert (thread_num > 0)

    threads = []
    for i in range(thread_num):
        work = StressTest("thread" + str(i), url, qps)
        work.start()
        threads.insert(work)

    time.sleep(lasting)


if __name__ == '__main__':
    stress_load_work('http://exp.renren.com', 100, 2, 10)









