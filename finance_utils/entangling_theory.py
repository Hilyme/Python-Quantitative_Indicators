# 量化工具：掘金终端
"""
缠论：
    TDX公式：
        MA30:=MA(C,30);
        MA60:=MA(C,60);

        M1:=5;
        M2:=13;
        M3:=21;
        {箱体}
        TC1S:=IF(H=HHV(H,48),H,DRAWNULL);
        TC2S:=CONST(BARSLAST(TC1S=H))+1;
        UPPERS:=CONST(IF(TC2S=1,H,REF(H,TC2S-1)));
        BC1S:=IF(L=LLV(L,48),L,DRAWNULL);
        BC2S:=CONST(BARSLAST(BC1S=L))+1;
        LOWERS:=CONST(IF(BC2S=1,L,REF(L,BC2S-1)));
        LPS:=CURRBARSCOUNT<=BC2S AND L=LOWERS;
        HPS:=CURRBARSCOUNT<=TC2S AND H=UPPERS;
        AB1S:=EMA(((2*C+H+L)/4-LLV(LOW,30))/
        (HHV(HIGH,30)-LLV(LOW,30))*100,8);
        BA1S:=EMA(AB1S,5);
        上轨:=REFDATE(REF(HHV(MAX(C,O),96),5),DATE);
        下轨:=REFDATE(REF(LLV(MIN(C,O),96),5),DATE);
        中轨:=((上轨)+(下轨))/2;
        YXHX:=DATE>=REF(DATE,BARSLAST(IF(BC2S>TC2S,LPS,HPS)));
        上沿:IF(AB1S>0 AND AB1S-BA1S<=0 AND YXHX,上轨,上轨),COLOR555555,LINETHICK2;
        中枢:IF(AB1S>0 AND AB1S-BA1S<=0 AND YXHX,中轨,中轨),COLOR555555,LINETHICK2;
        下沿:IF(AB1S>0 AND AB1S-BA1S<=0 AND YXHX,下轨,下轨),COLOR555555,LINETHICK2;
        {三K线}
        三K线:=1;
        DG:=MAX(MAX(REFX(L,1),REFX(L,2)),REFX(L,3));
        GD:=MIN(MIN(REFX(H,1),REFX(H,2)),REFX(H,3));
        AA11:=(DG+GD)/2;
        A11:=AA11>REFX(L,3) AND REFX(L,2)< AA11 AND REFX(L,1) <AA11 ;
        A21:=FILTER(A11,BARSLAST(A11)+2);
        A41:=A11 AND A21;
        A51:=IF(REF(A41,1),H,0),NODRAW;
        STICKLINE(三K线=1 && REF(A41,2),REF(GD,2),REF(DG,2),13,-1),COLORMAGENTA;
        DRAWKLINE(H,O,L,C);
        {峰谷}
        峰谷:=1;
        PA:=10;
        PB:=REF(HIGH,PA)=HHV(HIGH,2*PA+1);
        PC:=FILTER(PB,PA);
        PD:=BACKSET(PC,PA+1);
        PE:=FILTER(PD,PA);{高点}
        峰线:(REF(HIGH,BARSLAST(PE)))*峰谷,COLORRED,POINTDOT,LINETHICK2;
        AA21:=REF(LOW,PA)=LLV(LOW,2*PA+1);
        BB21:=FILTER(AA21,PA);
        CC21:=BACKSET(BB21,PA+1);
        DD21:=FILTER(CC21,PA);{低点}
        谷线:(REF(LOW,BARSLAST(DD21)))*峰谷,COLORGREEN,POINTDOT,LINETHICK2;
        {三角形中枢}
        时间:=4;
        A:=H=HHV(H,时间*5) AND HHV(H,时间*5)>REF(HHV(H,时间*5),1);
        B:=L=LLV(L,时间*5) AND LLV(L,时间*5)<REF(LLV(L,时间*5),1);
        CCA:DRAWLINE(A,H,B,L,0),COLORGREEN,LINETHICK2;
        CCB:DRAWLINE(B,L,A,H,0),COLORRED,LINETHICK2;
        N:=(0,1,1);
        {缠论高低点}
        局部低点预选A:=BACKSET(LLV(L,5)<REF(LLV(L,4),1),4);
        局部低点预选B:=BACKSET(局部低点预选A=0 AND REF(局部低点预选A,1)=1,2);
        局部低点预选C:=IF(局部低点预选B=1 AND REF(局部低点预选B,1)=0,-1,0);
        局部高点预选A:=BACKSET(HHV(H,5)>REF(HHV(H,4),1),4);
        局部高点预选B:=BACKSET(局部高点预选A=0 AND REF(局部高点预选A,1)=1,2);
        局部高点预选C:=IF(局部高点预选B=1 AND REF(局部高点预选B,1)=0,1,0);
        缺口判断:=IF(L>REF(H,1),1,IF(H<REF(L,1),-1,0));
        距前高天:=BARSLAST(局部高点预选C=1);
        距前低天:=BARSLAST(局部低点预选C=-1);
        小值周期:=LOWRANGE(L);
        大值周期:=TOPRANGE(H);
        低保留AA:=IF(局部低点预选C=-1 AND REF(距前高天,1)>REF(距前低天,1) AND LLV(L,距前高天+1)<REF(LLV(L,距前高天+1),1),-1,0);
        低保留AB:=IF(局部低点预选C=-1 AND REF(距前高天,1)<=REF(距前低天,1) AND (距前高天>=4 OR LLV(缺口判断,距前高天)=-1 OR LLV(L,距前低天+2)<REF(LLV(L,距前低天+1),1)),-1,0);
        低保留S:=IF((低保留AA=-1 OR 低保留AB=-1) AND L<REF(H,距前高天+1),-1,0);
        预判:=IF((距前低天<4 AND HHV(缺口判断,距前低天)!=1) OR REF(低保留S,距前低天)=0,1,0);
        判断:=IF(局部高点预选C=1 AND REF(距前低天,1)<=REF(距前高天,1) AND 预判=1 AND 大值周期>REF(小值周期,距前低天+1) AND 大值周期>REF(小值周期,距前低天) AND 大值周期>REF(大值周期,距前高天),1,0);
        高保留A:=IF(局部高点预选C=1 AND REF(距前低天,1)>REF(距前高天,1) AND HHV(H,距前低天+1)>REF(HHV(H,距前低天+1),1),1,0);
        高保留B:=IF(局部高点预选C=1 AND REF(距前低天,1)<=REF(距前高天,1) AND REF(低保留S,距前低天)=-1 AND (距前低天>=4 OR HHV(缺口判断,距前低天)=1),1,0);
        高保留:=IF((高保留A=1 OR 高保留B=1 OR 判断=1) AND H>REF(L,距前低天+1),1,0);
        预判A:=IF((距前高天<4 AND HHV(缺口判断,距前高天)!=1) OR REF(高保留,距前高天)=0,1,0);
        判断A:=IF(局部低点预选C=-1 AND REF(距前高天,1)<=REF(距前低天,1) AND 预判A=1 AND 小值周期>REF(大值周期,距前高天+1) AND 小值周期>REF(大值周期,距前高天) AND 小值周期>REF(小值周期,距前低天),-1,0);
        低保留A:=IF(局部低点预选C=-1 AND REF(距前高天,1)>REF(距前低天,1) AND LLV(L,距前高天+1)<REF(LLV(L,距前高天+1),1),-1,0);
        低保留B:=IF(局部低点预选C=-1 AND REF(距前高天,1)<=REF(距前低天,1) AND (距前高天>=4 OR LLV(缺口判断,距前高天)=-1 OR 判断A=-1),-1,0);
        低保留:=IF((低保留A=-1 OR 低保留B=-1) AND L<REF(H,距前高天+1),-1,0);
        距前高天A:=BARSLAST(高保留=1);
        距前低天A:=BARSLAST(低保留=-1);
        预判X:=IF((距前低天A<4 AND HHV(缺口判断,距前低天A)!=1) OR REF(低保留,距前低天A)=0,1,0);
        判断X:=IF(局部高点预选C=1 AND REF(距前低天A,1)<=REF(距前高天A,1) AND 预判X=1 AND 大值周期>REF(小值周期,距前低天A+1) AND 大值周期>REF(小值周期,距前低天A) AND 大值周期>REF(大值周期,距前高天A),1,0);
        高保留XA:=IF(局部高点预选C=1 AND REF(距前低天A,1)>REF(距前高天A,1) AND HHV(H,距前低天A+1)>REF(HHV(H,距前低天A+1),1),1,0);
        高保留XB:=IF(局部高点预选C=1 AND REF(距前低天A,1)<=REF(距前高天A,1) AND REF(低保留,距前低天A)=-1 AND (距前低天A>=4 OR HHV(缺口判断,距前低天A)=1),1,0);
        高保留X:=IF((高保留XA=1 OR 高保留XB=1 OR 判断X=1) AND H>REF(L,距前低天A+1),1,0);
        预判XA:=IF((距前高天A<4 AND HHV(缺口判断,距前高天A)!=1) OR REF(高保留XA,距前高天A)=0,1,0);
        判断XA:=IF(局部低点预选C=-1 AND REF(距前高天A,1)<=REF(距前低天A,1) AND 预判XA=1 AND 小值周期>REF(大值周期,距前高天A+1) AND 小值周期>REF(大值周期,距前高天A) AND 小值周期>REF(小值周期,距前低天A),-1,0);
        低保留XA:=IF(局部低点预选C=-1 AND REF(距前高天A,1)>REF(距前低天A,1) AND LLV(L,距前高天A+1)<REF(LLV(L,距前高天A+1),1),-1,0);
        低保留XB:=IF(局部低点预选C=-1 AND REF(距前高天A,1)<=REF(距前低天A,1) AND (距前高天A>=4 OR LLV(缺口判断,距前高天A)=-1 OR 判断XA=-1),-1,0);
        低保留X:=IF((低保留XA=-1 OR 低保留XB=-1) AND L<REF(H,距前高天A+1),-1,0);
        距前高天YA:=BARSLAST(高保留X=1);
        距前低天YA:=BARSLAST(低保留X=-1);
        预判YX:=IF((距前低天YA<4 AND HHV(缺口判断,距前低天YA)!=1) OR REF(低保留X,距前低天YA)=0,1,0);
        判断YX:=IF(局部高点预选C=1 AND REF(距前低天YA,1)<=REF(距前高天YA,1) AND 预判YX=1 AND 大值周期>REF(小值周期,距前低天YA+1) AND 大值周期>REF(小值周期,距前低天YA) AND 大值周期>REF(大值周期,距前高天YA),1,0);
        高保留YXA:=IF(局部高点预选C=1 AND REF(距前低天YA,1)>REF(距前高天YA,1) AND HHV(H,距前低天YA+1)>REF(HHV(H,距前低天YA+1),1),1,0);
        高保留YXB:=IF(局部高点预选C=1 AND REF(距前低天YA,1)<=REF(距前高天YA,1) AND REF(低保留X,距前低天YA)=-1 AND (距前低天YA>=4 OR HHV(缺口判断,距前低天YA)=1),1,0);
        高保留YX:=IF((高保留YXA=1 OR 高保留YXB=1 OR 判断YX=1) AND H>REF(L,距前低天YA+1),1,0);
        预判YXA:=IF((距前高天YA<4 AND HHV(缺口判断,距前高天YA)!=1) OR REF(高保留YXA,距前高天YA)=0,1,0);
        判断YXA:=IF(局部低点预选C=-1 AND REF(距前高天YA,1)<=REF(距前低天YA,1) AND 预判YXA=1 AND 小值周期>REF(大值周期,距前高天YA+1) AND 小值周期>REF(大值周期,距前高天YA) AND 小值周期>REF(小值周期,距前低天YA),-1,0);
        低保留YXA:=IF(局部低点预选C=-1 AND REF(距前高天YA,1)>REF(距前低天YA,1) AND LLV(L,距前高天YA+1)<REF(LLV(L,距前高天YA+1),1),-1,0);
        低保留YXB:=IF(局部低点预选C=-1 AND REF(距前高天YA,1)<=REF(距前低天YA,1) AND (距前高天YA>=4 OR LLV(缺口判断,距前高天YA)=-1 OR 判断YXA=-1),-1,0);
        低保留YX:=IF((低保留YXA=-1 OR 低保留YXB=-1) AND L<REF(H,距前高天YA+1),-1,0);
        AAAD:=IF(高保留YX=1 AND 低保留YX=-1 AND H>REF(H,REF(距前高天YA,1)+2),1,IF(高保留YX=1 AND 低保留YX=-1 AND L<REF(L,REF(距前低天YA,1)+2),-1,0));
        极点保留:=IF(AAAD=0,高保留YX+低保留YX,AAAD);
        局部极点:IF(极点保留=-1,L,IF(极点保留=1,H,DRAWNULL)),CIRCLEDOT,COLORYELLOW;
        C1:DRAWLINE(极点保留=-1,局部极点,极点保留=1,局部极点,0),COLORMAGENTA;
        C2:DRAWLINE(极点保留=1,局部极点,极点保留=-1,局部极点,0),COLORWHITE;
        {DRAWTEXT(极点保留=1,局部极点*1.002,'顶'),COLORGREEN;
        DRAWTEXT(极点保留=-1,局部极点*0.998,'底'),LINETHICK2,COLORRED;}

        HH1:=IF(H<REF(H,1)&&REF(H,1)<REF(H,2),REF(H,2),0);
        LL1:=IF(L>REF(L,1)&&REF(L,1)>REF(L,2),REF(L,2),0);
        HH2:=VALUEWHEN(HH1>0,HH1);
        LL2:=VALUEWHEN(LL1>0,LL1);
        K1:=IF(CLOSE>HH2,-3,IF(CLOSE<LL2,1,0));
        K2:VALUEWHEN(K1<>0,K1),NODRAW;

        DUO1:= K2=-3 AND REF(K2,1)>-3;
        KONG1:=K2=1  AND REF(K2,1)<1;

        STICKLINE(K2=-3,O,C,2,0),COLORRED;
        STICKLINE(K2=1,O,C,2,0),COLORLIBLUE;

        DRAWTEXT(DUO1,L*0.998,'多'),COLORYELLOW;
        DRAWTEXT(KONG1,H*1.002,'空'),COLORGREEN;
"""
"""
    单求 峰线、谷线：
        {峰谷}
        峰谷:=1;
        PA:=10;
        PB:=REF(HIGH,PA)=HHV(HIGH,2*PA+1);
        PC:=FILTER(PB,PA);
        PD:=BACKSET(PC,PA+1);
        PE:=FILTER(PD,PA);{高点}
        峰线:(REF(HIGH,BARSLAST(PE)))*峰谷,COLORRED,POINTDOT,LINETHICK2;
        AA21:=REF(LOW,PA)=LLV(LOW,2*PA+1);
        BB21:=FILTER(AA21,PA);
        CC21:=BACKSET(BB21,PA+1);
        DD21:=FILTER(CC21,PA);{低点}
        谷线:(REF(LOW,BARSLAST(DD21)))*峰谷,COLORGREEN,POINTDOT,LINETHICK2;


        峰谷赋值:1
        PA赋值:10
        PB赋值:PA日前的最高价=2*PA+1日内最高价的最高值
        PC赋值:PB的PA日过滤
        PD赋值:若PC则将最近PA+1周期置为1
        PE赋值:PD的PA日过滤
        输出峰线:(上次PE距今天数日前的最高价)*峰谷,画红色,POINTDOT,线宽为2
        AA21赋值:PA日前的最低价=2*PA+1日内最低价的最低值
        BB21赋值:AA21的PA日过滤
        CC21赋值:若BB21则将最近PA+1周期置为1
        DD21赋值:CC21的PA日过滤
        输出谷线:(上次DD21距今天数日前的最低价)*峰谷,画绿色,POINTDOT,线宽为2
        
        逻辑伪代码化：
        PB： 判断PA日前的high值是否与 2PA+1日内的high值相等 相等为True  从前依次往后推  返回的是一个由Boolean值组成的列表
        PC： 将PB的信号再进行一次过滤，  如果今天的PB==True， 那就判断前PA日到今天之间还有没有出现过True的情况， 如果有就将今天的True置为False， 从前依次往后推， 最终返回的是一个经过修改的PB
        PD:  判断当前PC的值，若PC为True 则将PA+1日内到今天的值都设为True， 从前依次往后推  返回一个Boolean值的列表
        PE:  将PD的信号进行过滤， 若今日PD==True， 则判断PA日前到今日之间还有没有出现过True的情况， 如果有就将今日置为False， 从前依次往后推， 返回修改后的PD

"""

from gm.api import *
import numpy as np
import funcat


def init(context):
    context.goods = ['SHFE.rb2001']
    context.frequency = '900s'
    context.period = 200 + 1
    subscribe(context.goods, context.frequency, context.period)


def on_bar(context, bars):
    symbol = bars[0].symbol
    frequency = bars[0].frequency
    c_eob = bars[0].eob
    # 获得历史k线
    datas = history_n(symbol=symbol, frequency=frequency, count=context.period, end_time=c_eob,
                      fields='high, low, eob', df=True)
    low_list = datas['low'].values.tolist()
    high_list = datas['high'].values.tolist()
    eob_list = datas['eob'].tolist()

    """
    PB： 判断PA日前的high值是否与 2PA+1日内的high值相等 相等为True  从前依次往后推  返回的是一个由Boolean值组成的列表
    PC： 将PB的信号再进行一次过滤，  如果今天的PB==True， 那就判断前PA日到今天之间还有没有出现过True的情况， 如果有就将今天的True置为False， 从前依次往后推， 最终返回的是一个经过修改的PB
    PD:  判断当前PC的值，若PC为True 则将PA+1日内到今天的值都设为True， 从前依次往后推  返回一个Boolean值的列表
    PE:  将PD的信号进行过滤， 若今日PD==True， 则判断PA日前到今日之间还有没有出现过True的情况， 如果有就将今日置为False， 从前依次往后推， 返回修改后的PD
    """
    pa = 10
    # --------------------------------------求峰线--------------------------------------
    # high_ndArray = np.array(high_list)
    # high_series = funcat.MA(high_ndArray, 1)
    # PB = funcat.REF(high_series, pa) == funcat.HHV(high_series, 2 * pa + 1)
    # pb_list = PB.series.tolist()
    pb_list = get_pb_list(pa, high_list)
    pc_list = TDX_FILTER(pb_list, pa)
    pd_list = TDX_BACKSET(pc_list, pa + 1)
    pe_list = TDX_FILTER(pd_list, pa)
    peak_line = high_list[-(TDX_BARSLAST(pe_list)) - 1]
    # --------------------------------------求谷线--------------------------------------
    aa21_list = get_aa21_list(pa, low_list)
    bb21_list = TDX_FILTER(aa21_list, pa)
    cc21_list = TDX_BACKSET(bb21_list, pa + 1)
    dd21_list = TDX_FILTER(cc21_list, pa)
    valley_line = low_list[-(TDX_BARSLAST(dd21_list)) - 1]

    print(eob_list[-1])
    print("峰线：", peak_line, "时间：", eob_list[-(TDX_BARSLAST(pe_list)) - 1])
    print("谷线：", valley_line, "时间：", eob_list[-(TDX_BARSLAST(dd21_list)) - 1])
    print()


def get_pb_list(pa, high_list):
    pb_list = []
    for i in range(2 * pa, len(high_list)):
        if high_list[i - pa] == max(high_list[i - 2 * pa: i]):
            pb_list.append(True)
        else:
            pb_list.append(False)
    return pb_list


def get_aa21_list(pa, low_list):
    aa21_list = []
    for i in range(2 * pa, len(low_list)):
        if low_list[i - pa] == min(low_list[i - 2 * pa: i]):
            aa21_list.append(True)
        else:
            aa21_list.append(False)
    return aa21_list


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
                res_list = [True] * (len(res_list) + 1)
            else:
                res_list[i - n + 1:] = [True] * n
        else:
            res_list.append(False)
    return res_list


def TDX_BARSLAST(rec_list):
    for i in range(1, len(rec_list) + 1):
        if rec_list[-i]:
            return i - 1


if __name__ == '__main__':
    run(strategy_id='0ee8abfc-c599-11e9-b9be-00fffdf0144e',
        filename='entangling_theory.py',
        mode=MODE_BACKTEST,
        token='6ab0252f53fda940fabc612cd1954183b24cdb72',
        backtest_start_time='2019-11-12 09:30:00',
        backtest_end_time='2019-11-12 15:30:00',
        backtest_initial_cash=5000000,
        backtest_commission_ratio=0.0001,
        )
