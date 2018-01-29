import time
from threading import Thread, Event

from heartbeat import loop_executor
from heartbeat import analysis, application, infrastructure


def main():
    run_event = Event()
    run_event.set()
    threads = []
    threads.append(Thread(target=loop_executor,
                          args=(analysis.pc_jrisk_service, 30, run_event),
                          kwargs={'env': 'prod'}))
    threads.append(Thread(target=loop_executor,
                          args=(analysis.ocr_server, 30, run_event),
                          kwargs={'env': 'prod'}))
    threads.append(Thread(target=loop_executor,
                          args=(analysis.pdata, 30, run_event),
                          kwargs={'env': 'prod'}))
    threads.append(Thread(target=loop_executor,
                          args=(application.precise_application_interface, 30, run_event),
                          kwargs={'env': 'prod'}))
    threads.append(Thread(target=loop_executor,
                          args=(application.log_worker, 30, run_event),
                          kwargs={'env': 'prod'}))
    threads.append(Thread(target=loop_executor,
                          args=(infrastructure.rabbit, 30, run_event),
                          kwargs={'env': 'prod'}))
    threads.append(Thread(target=loop_executor,
                          args=(infrastructure.redis, 30, run_event),
                          kwargs={'env': 'prod'}))
    for thread in threads:
        thread.start()
    try:
        while True:
            time.sleep(.5)
    except KeyboardInterrupt:
        print('attempting to close threads')
        run_event.clear()
        for thread in threads:
            thread.join()
        print('threads successfully closed')


if __name__ == '__main__':
    main()
