"""heartbeat"""
import time
import json

import raven

with open('./credentials.json') as f:
    credentials = json.load(f)
dsn = 'https://99da3efb421b47a5ab6d0469327d2b7d:ccbf948433cb498ebe9a451af1758974@sentry.jiukangyun.com/12'
raven_client = raven.Client(dsn)


def loop_executor(func, interval, run_event, **kwargs):
    """execute the given func in a ctrl-c interuptable loop

    :func: the function to be executed
    :interval: seconds between executions
    :run_event: the event that controls the loop to stop
    :kwargs: keyword args of func
    """
    while run_event.is_set():
        try:
            func(**kwargs)
            print('{} - {} - {} - OK'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                func.__name__,
                kwargs,
            ))
        except Exception as err:
            # report every possible exception to Sentry
            msg = '{} - {} - {} - FAIL: {}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                func.__name__,
                kwargs,
                err,
            )
            print(msg)
            raven_client.captureMessage(msg, level='error')
        finally:
            # elegantly stops the sleep function
            for i in range(interval):
                if run_event.is_set():
                    time.sleep(1)
