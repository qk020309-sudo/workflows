from threading import Thread

from browser_pool import BrowserPool
from task_manager import TaskManager
from link_collector import collect_links
from worker import worker
from monitor import monitor_timeout


def main():
    while True:
        print('请输入线程数(1-10)')
        try:
            num = int(input())
            if num >= 1 and num <= 10:
                break
        except:
            print('请输入一个整数')
            continue
    task_manager = TaskManager()

    pool = BrowserPool(num)

    pool.start()

    # 启动10个worker
    for browser in pool.browsers:

        t = Thread(
            target=worker,
            args=(browser, task_manager, pool)
        )

        t.daemon = True
        t.start()

    # 启动采集
    collector = Thread(
        target=collect_links,
        args=(task_manager,)
    )

    collector.daemon = True
    collector.start()

    # 启动监控
    monitor = Thread(
        target=monitor_timeout,
        args=(pool,)
    )

    monitor.daemon = True
    monitor.start()

    print("系统启动完成")

    while True:
        pass


if __name__ == "__main__":
    main()
