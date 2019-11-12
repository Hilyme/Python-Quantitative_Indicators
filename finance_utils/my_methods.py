#!/usr/bin/python3
# Author : Hily
# file: my_methods
# @Time: 19-7-18 下午8:35


from funcat import *
import numpy as np
import talib


# MA(均线（SMA、KMA同）)
def get_ma(close_list, n):
    """
    """
    close_ndarray = np.array(close_list)
    close_series = MA(close_ndarray, 1)
    MA_N = MA(close_series, n)
    return MA_N


# WR
def get_wr(close_list, high_list, low_list, N=9, N1=9):
    """
    WR 威廉指标
    1.WR波动于0 - 100，100置于顶部，0置于底部。
    2.本指标以50为中轴线，高于50视为股价转强；低于50视为股价转弱
    3.本指标高于20后再度向下跌破20，卖出；低于80后再度向上突破80，买进。
    4.WR连续触底3 - 4次，股价向下反转机率大；连续触顶3 - 4次，股价向上反转机率大。
    """
    close_ndarray = np.array(close_list)
    high_ndarray = np.array(high_list)
    low_ndarray = np.array(low_list)
    close_series = MA(close_ndarray, 1)
    high_series = MA(high_ndarray, 1)
    low_series = MA(low_ndarray, 1)

    WR1 = (HHV(high_series, N) - close_series) / (HHV(high_series, N) - LLV(low_series, N)) * 100
    WR2 = (HHV(high_series, N1) - close_series) / (HHV(high_series, N1) - LLV(low_series, N1)) * 100

    return WR1


# KDJ
def get_kd(close_list, high_list, low_list, N=9, M1=3, M2=3):
    """
    KDJ 随机指标
    1.指标>80 时，回档机率大；指标<20时，反弹机率大；
    2.K在20左右向上交叉D时，视为买进信号；
    3.K在80左右向下交叉D时，视为卖出信号；
    4.J>100 时，股价易反转下跌；J<0 时，股价易反转上涨；
    5.KDJ 波动于50左右的任何信号，其作用不大。
    """
    close_ndarray = np.array(close_list)
    high_ndarray = np.array(high_list)
    low_ndarray = np.array(low_list)
    CLOSE = MA(close_ndarray, 1)
    HIGH = MA(high_ndarray, 1)
    LOW = MA(low_ndarray, 1)
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV, M1, 1)
    D = SMA(K, M2, 1)
    J = 3 * K - 2 * D
    return K, D


# SAR
def get_sar(high_list, low_list):
    """
    sar<0 down 开空 >0 up 开多
    1.任何时候都可以使用SAR 为停损点；
    2.价格涨跌的速度必须比SAR 升降的速度快，否则必会产生停损信号；
    3.SAR 由红色变成绿色时，卖出；
    4.SAR 由绿色变成红色时，买进；
    5.本指标周期参数一般设定为4天；
    6.本设定主要为寻找出现多头停损或空头停损的个股。
    """
    high_ndarray = np.array(high_list)
    low_ndarray = np.array(low_list)
    sar = talib.SAREXT(high_ndarray, low_ndarray)
    return sar.tolist()


# BOLL
def get_boll(close_list):
    """
    BOLL:MA(CLOSE,20);
    UB:BOLL+2*STD(CLOSE,20);
    LB:BOLL-2*STD(CLOSE,20);
    1.股价上升穿越布林线上限时，回档机率大；
    2.股价下跌穿越布林线下限时，反弹机率大；
    3.布林线震动波带变窄时，表示变盘在即；
    4.BOLL可配合BB、WIDTH使用；
    """
    close_ndarray = np.array(close_list)
    n = 20
    P = 20
    MID = talib.MA(close_ndarray, n)
    UPPER = MID + P / 10 * talib.STDDEV(close_ndarray, n)
    LOWER = MID - P / 10 * talib.STDDEV(close_ndarray, n)
    up = UPPER  # 上轨
    down = LOWER  # 下轨
    return up, down


# 双黄金线
def get_goldline_status(close_list):
    close_ndarray = np.array(close_list)
    close_series = MA(close_ndarray, 1)
    N = 13
    VA = 3 * WMA(close_series, N) - 2 * MA(close_series, N)
    VAR1 = REF(VA, 1)
    VAR2 = REF(VA, 2)
    if VA > VAR1 > VAR2:
        return 'r'  # 红
    elif VA < VAR1 < VAR2:
        return 'g'  # 绿
    else:
        return 'b'  # 蓝


def get_goldline_buy_point(prices):
    close_npArray = prices['close'].values.tolist()
    close_narry = np.array(close_npArray)
    close_series = MA(close_narry, 1)
    N = 13
    VA = 3 * WMA(close_series, N) - 2 * MA(close_series, N)
    VAR1 = REF(VA, 1)
    VAR2 = REF(VA, 2)
    VAR3 = REF(VA, 3)
    if VA > VAR1 > VAR2 and VAR2 < VAR3:
        return 'duo'  # 多仓买点
    elif VA < VAR1 < VAR2 and VAR2 > VAR3:
        return 'kong'  # 空仓买点


# MACD
def get_macd(close_list):
    """
    MACD 指数平滑移动平均线

    DIFF线:收盘价短期、长期指数平滑移动平均线间的差
    DEA线: DIFF线的M日指数平滑移动平均线
    MACD线:DIFF线与DEA线的差，彩色柱状线
    参数：SHORT(短期)、LONG(长期)、M 天数，一般为12、26、9
    用法：
    1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。
    2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
    3.DEA线与K线发生背离，行情反转信号。
    4.分析MACD柱状线，由红变绿(正变负)，卖出信号；由绿变红，买入信号
    """
    MACD_CLOSE = MA(np.array(close_list), 1)
    DIFF = EMA(MACD_CLOSE, 5) - EMA(MACD_CLOSE, 35)
    DEA = EMA(DIFF, 5)
    MACD = (DIFF - DEA) * 2


# ATR(波动率)
def get_atr(close_list, high_list, low_list):
    """
    算法：今日振幅、今日最高与昨收差价、今日最低与昨收差价中的最大值，为真实波幅，求真实波幅的N日移动平均
    参数：N　天数，一般取14
    """
    close_ndarray = np.array(close_list)
    high_ndarray = np.array(high_list)
    low_ndarray = np.array(low_list)
    atr = talib.ATR(high_ndarray, low_ndarray, close_ndarray)
    return atr


# adx(趋向变动的程度)
def get_adx(close_list, high_list, low_list):
    close_ndarray = np.array(close_list)
    high_ndarray = np.array(high_list)
    low_ndarray = np.array(low_list)
    adx = talib.ADX(high_ndarray, low_ndarray, close_ndarray)
    return adx


def TDX_FILTER(rec_list, n):
    res_list = []
    for i in range(len(rec_list)):
        if i < n:
            temp_n = i
        else:
            temp_n = n
        if rec_list[i] and True not in res_list[i-temp_n:i]:
            res_list.append(True)
        else:
            res_list.append(False)
    return res_list


def TDX_BACKSET(rec_list, n):
    res_list = []
    for i in range(len(rec_list)):
        if rec_list[i]:
            if len(res_list) < n:
                res_list = [True] * (len(res_list)+1)
            else:
                res_list[i-n+1:] = [True] * n
        else:
            res_list.append(False)
    return res_list


def TDX_BARSLAST(rec_list):
    for i in range(1, len(rec_list)+1):
        if rec_list[-i]:
            return i-1
