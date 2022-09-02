<<<<<<< HEAD
# # import scripts
# from script_get_eps import get_eps
# from script_get_eps import get_roe
# from script_get_eps import get_pe
from script_get_fundamentals_us import get_rev 
||||||| 20daee0
# import scripts
from script_get_eps import get_eps
from script_get_eps import get_roe
from script_get_eps import get_pe
=======
# import scripts
from script_get_fundmentals_us import get_eps
from script_get_fundmentals_us import get_roe
from script_get_fundmentals_us import get_pe
from script_get_fundmentals_us import get_npm
>>>>>>> ea7a3e9bdf4a2937be7f0a7ca8a8ce413b379ca1
# multiprocessing
import multiprocessing


if __name__ == '__main__':

    # p_roe = multiprocessing.Process(target=get_roe, args=(2553,)) 
    # p_pe = multiprocessing.Process(target=get_pe, args=(325,))

    # p_roe.start()
    # p_pe.start()

<<<<<<< HEAD
    # p_roe.join()
    # p_pe.join()
    get_rev(300)
||||||| 20daee0
=======
    # p_roe.join()
    # p_pe.join()
    get_npm()
>>>>>>> ea7a3e9bdf4a2937be7f0a7ca8a8ce413b379ca1
    print('Done')

# get_roe(2553) # last run: 2022/8/25 22:32
# get_pe(325)