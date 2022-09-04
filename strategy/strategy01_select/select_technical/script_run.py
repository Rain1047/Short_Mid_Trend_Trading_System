from script_get_daily_indicator import get_daily_indicator
import multiprocessing


if __name__ == '__main__':

    # p_1 = multiprocessing.Process(target=get_daily_indicator, args=('2019-10-01',)) 
    # p_2 = multiprocessing.Process(target=get_daily_indicator, args=('2019-07-01',))
    # p_3 = multiprocessing.Process(target=get_daily_indicator, args=('2020-04-01',))
    # p_4 = multiprocessing.Process(target=get_daily_indicator, args=('2020-07-01',))
    # p_5 = multiprocessing.Process(target=get_daily_indicator, args=('2020-10-01',))

    p_6 = multiprocessing.Process(target=get_daily_indicator, args=('2020-01-02',))
    p_7 = multiprocessing.Process(target=get_daily_indicator, args=('2021-01-04',))
    p_8 = multiprocessing.Process(target=get_daily_indicator, args=('2021-04-01',))
    p_9 = multiprocessing.Process(target=get_daily_indicator, args=('2021-07-01',))
    p_10 = multiprocessing.Process(target=get_daily_indicator, args=('2021-10-01',))
    p_11 = multiprocessing.Process(target=get_daily_indicator, args=('2022-01-03',))
    
    # p_roe.start()
    # p_pe.start()
    # p_1.start()
    # p_2.start()
    # p_3.start()
    # p_4.start()
    # p_5.start()
    p_6.start()
    p_7.start()
    p_8.start()
    p_9.start()
    p_10.start()
    p_11.start()
    print('process start')

    # p_1.join()
    # p_2.join()
    # p_3.join()
    # p_4.join()
    # p_5.join()

    p_6.join()
    p_7.join()
    p_8.join()
    p_9.join()
    p_10.join()
    p_11.join()

    # p_roe.join()
    # p_pe.join()
    # get_rev(300)

    # p_roe.join()
    # p_pe.join()
    # get_npm(6043)
    # gth('2017-01-01', '2019-04-02')

    print('Done')

# get_roe(2553) # last run: 2022/8/25 22:32
# get_pe(325)