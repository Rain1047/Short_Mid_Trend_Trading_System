# # import scripts
# from script_get_eps import get_eps
# from script_get_eps import get_roe
# from script_get_eps import get_pe
# from script_get_fundamentals_us import get_rev 

# # import scripts
# from script_get_fundamentals_us import get_eps
# from script_get_fundamentals_us import get_roe
# from script_get_fundamentals_us import get_pe
from script_get_fundamentals_us import get_npm
# from script_get_ticker_indicator import get_ticker_indicator_his as gth
# multiprocessing
import multiprocessing


if __name__ == '__main__':

    # p_roe = multiprocessing.Process(target=get_roe, args=(2553,)) 
    # p_pe = multiprocessing.Process(target=get_pe, args=(325,))

    # p_roe.start()
    # p_pe.start()


    # p_roe.join()
    # p_pe.join()
    # get_rev(300)

    # p_roe.join()
    # p_pe.join()
    get_npm(6043)
    # gth('2017-01-01', '2019-04-02')

    print('Done')

# get_roe(2553) # last run: 2022/8/25 22:32
# get_pe(325)