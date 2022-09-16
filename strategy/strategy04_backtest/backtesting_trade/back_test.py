import os,sys
modpath = os.path.dirname(os.path.abspath(sys.argv[-1]))
datapath = os.path.join(modpath, 'aapl_price.csv')

print(datapath)
print(os.path.abspath(sys.argv[-1]))