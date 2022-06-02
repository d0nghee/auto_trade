import pyupbit
import time
import datetime

def cal_target(ticker) :
    dataf = pyupbit.get_ohlcv(ticker, 'day')
    today = dataf.iloc[-1]
    yday = dataf.iloc[-2]
    y_range = yday['high'] - yday['low']
    target = today['open'] + y_range * 0.5
    return target

access_key = "input"
secret_key = "input"
upbit = pyupbit.Upbit(access_key, secret_key)


target = cal_target('KRW-BTC')
oper = False
coin = False


while True :
    now_t = datetime.datetime.now()

    # 매도
    if now_t.hour == 8 and now_t.minute == 59 and 50 <= now_t.second <= 59 :
        if oper is True and coin is True :
            btc = upbit.get_balance('KRW-BTC')
            upbit.sell_market_order('KRW-BTC', btc)
            coin = False
            print('^^^^^^^^^^^^^^매도^^^^^^^^^^^^^^')
        oper = False
        time.sleep(10)

    # 목표 갱신
    if now_t.hour == 9 and now_t.minute == 0 and 20 <= now_t.second <= 30 :
        target = cal_target('KRW-BTC')
        oper = True
    now_price = pyupbit.get_current_price('KRW-BTC')

    # 매수
    if oper is True and coin is False and now_price >= target :
        krw = upbit.get_balance('KRW')
        upbit.buy_market_order('KRW-BTC', krw) # 비율 설정 ex)krw * n
        coin = True
        print('******************매수*******************')
    
    print()
    print(f'현재시간 : {now_t}')
    print(f'목표 : {target} 현재가 : {now_price}')
    print()
    print(f'보유 상태 : {coin} 동작 상태 : {oper}')
    print()
    time.sleep(1)
