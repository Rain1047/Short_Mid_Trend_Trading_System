import pandas as pd
import talib as ta 

def get_score_ch(df):
    # Static
    timeperiods_close = [10, 20, 50, 150, 200]
    timeperiods_volume = [20, 50]
    # Get Close Price MA
    for i in timeperiods_close:
        df['MA {}'.format(i)] = ta.SMA(df.close, timeperiod = i)

    # Get Volume MA
    for i in timeperiods_volume:
        df['VMA {}'.format(i)] = ta.SMA(df.volume, timeperiod=i)

    # Get Volatility close and open
    df['volatility'] = abs((df.close - df.open) / df.open)
    range50 = df.volatility.describe()[5]
    range25 = df.volatility.describe()[4]
    # Get Volatility low and max
    df['volatility_max'] = abs((df.high - df.low) / df.high)
    range50_max = df.volatility_max.describe()[5]
    range25_max = df.volatility_max.describe()[4]
    # Get Volume Score
    len_ = len(df.index)
    df['vscore'] = 0
    for i in range(len_):
        if df.loc[i].volume <= df.loc[i]['VMA 50'] and df.close.loc[i] > df['MA 200'].loc[i]:
            df.vscore.loc[i] = (1 - (df.loc[i].volume / df.loc[i]['VMA 50'])) * 10
        else:
            continue

    # Get Price Score
    df['score'] = 0
    for i in range(len_):
        score = 0
        if i < 360:
            df.score.loc[i] = score
        if i >= 360:
            # 一年内最高股价
            max_value = df.loc[i-360:i]['close'].max()
            # 一年内最低股价
            min_value = df.loc[i-360:i]['close'].min()
            #---------------------------------#
            #                MA               #
            #---------------------------------#
            # ClosePrice > MA200
            # 注：MA200是一个强条件，低于MA200的不会进行购买
            if df.loc[i].close > df.loc[i]['MA 200']:
                score += 3
            else:
                score -= 5
            # ClosePrice > MA150
            if df.loc[i].close > df.loc[i]['MA 150']:
                score += 2
            else:
                score -= 3
            # ClosePrice > MA50
            if df.loc[i].close > df.loc[i]['MA 50']:
                score += 1
                if df.loc[i].close <= df.loc[i]['MA 50'] * 1.3:
                    score += 0.5
                    if df.loc[i].close <= df.loc[i]['MA 50'] * 1.2:
                        score += 0.5
                        if df.loc[i].close <= df.loc[i]['MA 50'] * 1.15:
                            score += 1.5
                            if df.loc[i].close <= df.loc[i]['MA 50'] * 1.1:
                                score += 3
                        else:
                            score -=1
                    else:
                        score -= 3
                else:
                    score -= 5
            else:
                score -= 1

            # MA150 > MA200
            if df.loc[i]['MA 150'] > df.loc[i]['MA 200']:
                score += 1
            else:
                score -= 1
            # MA50高于MA150和MA200
            if df.loc[i]['MA 50'] > max(df.loc[i]['MA 150'], df.loc[i]['MA 200']):
                score += 1
            else:
                score -= 1
            # MA200 持续走高,每个月加0.6分. 如果走低则减
            if df.loc[i]['MA 200'] > df.loc[i-30]['MA 200']:
                score += 0.6
                if df.loc[i-30]['MA 200'] > df.loc[i-60]['MA 200']:
                    score += 0.6
                    if df.loc[i-60]['MA 200'] > df.loc[i-90]['MA 200']:
                        score += 0.6
                        if df.loc[i-90]['MA 200'] > df.loc[i-120]['MA 200']:
                            score += 0.6
                            if df.loc[i-120]['MA 200'] > df.loc[i-150]['MA 200']:
                                score += 0.6
            else:
                score -= 0.6
                if df.loc[i-30]['MA 200'] < df.loc[i-60]['MA 200']:
                    score -= 0.6
                    if df.loc[i-60]['MA 200'] < df.loc[i-90]['MA 200']:
                        score -= 0.6
                        if df.loc[i-90]['MA 200'] < df.loc[i-120]['MA 200']:
                            score -= 0.6
                            if df.loc[i-120]['MA 200'] > df.loc[i-150]['MA 200']:
                                score -= 0.6


            #---------------------------------#
            #             波动率           #
            #---------------------------------#
            if df.loc[i]['volatility'] <= range50:
                score += 0.5
            else: score -=1
            if df.loc[i]['volatility'] <= range25:
                score += 1
            else: score -=1
            if df.loc[i]['volatility_max'] <= range50_max:
                score += 1
            else: score -=1
            if df.loc[i]['volatility_max'] <= range25_max:
                score += 2
            else: score -=1

            #---------------------------------#
            #          特殊价格位置        #
            #---------------------------------#
            # 当前股价比一年内最低股价高至少30%
            if df.loc[i]['close'] > min_value*1.2:
                score += 3
            else:
                score -= 1
            # 当前价格至少处于当年最高价的25%以内(越近越好,每次记0.4分)
            if df.loc[i].close > max_value*0.75:
                score += 0.4
            else:
                score -= 0.4
            if df.loc[i].close > max_value*0.8:
                score += 0.4
            else:
                score -= 0.4
            if df.loc[i].close > max_value*0.85:
                score += 0.4
            else:
                score -= 0.4
            if df.loc[i].close > max_value*0.9:
                score += 0.4
            else:
                score -= 0.4
            if df.loc[i].close > max_value*0.95:
                score += 0.4
            else:
                score -= 0.4
            if df.loc[i].close > max_value:
                score += 0.4
            else:
                score -= 0.4
        
            # 添加最后的评分
            df.score.loc[i] = score
            df['total_score'] = 0
    df.total_score = df.vscore + df.score
    df_simple = df[df['datetime']]
    return df

