import numpy as np
import pandas as pd
from scipy.stats import norm
from tqdm import tqdm

class InvtSim:
    def __init__(self, j, fcst, truth, alpha:float, L=3, period=28, h = 1, b = 19):
        self.h         = h
        self.b         = b 
        self.alpha     = alpha            # service level
        self.period    = period           # forecats horizon
        self.fcst      = np.array(fcst)   # forecasts
        self.truth     = np.array(truth)  # actual demand
        self.L         = L                # lead-time
        # store these information
        self.sst_l     = []  # safety stock
        self.ot_l      = []  # order
        self.ipt_l     = []  # inventory position
        self.DtL_l     = []  # forecasted demands over the lead time
        self.net_l     = []  # net inventory
        self.wip_l     = []  # work in progress
        self.backlog_l = []  # backlog
        self.ch_l      = []  # holding costs
        self.cb_l      = []  # backlog costs
    def ob_ss_t(self, t, window=3):
        start = max(0, t+1 - window)  # ensure the index available
        if t == 0:
            return 0
        std_err = np.std( self.truth[start:t] - self.fcst[start:t])
        return norm.ppf(self.alpha) * std_err * np.sqrt(self.L)
    def ob_all_t(self):
        # initial inventory
        ip_t = sum(self.fcst[:self.L])
        net_t = sum(self.fcst[:self.L]) # assumption that the initial net inventory is equal to the actual demand for the first period
        wip_t = 0
        backlog = 0
        for t in range(self.period):
            # ss
            ss_t = self.ob_ss_t(t = t)
            self.sst_l.append(ss_t)
            # DtL
            DtL = np.sum(self.fcst[t:t + self.L])
            self.DtL_l.append(DtL)
            # o_t_L, o_t_1, wip_t, net_t
            o_t_L = self.ot_l[-self.L] if t >= self.L else 0
            wip_t = wip_t + (self.ot_l[-1] if t >= 1 else 0) - o_t_L
            net_t = net_t + o_t_L - self.truth[t]
            if net_t < 0:
                backlog = abs(net_t)  # record backlog
            '''
            else:
                backlog = max(0, - net_t)  # backlog '''
            # ip and order
            ip_t = wip_t + net_t # do not involve the backlog
            o_t = max(0, DtL + ss_t - ip_t) # consider the backlog
            # holding and backlogging cost
            ch_t = self.h * max(0, net_t)
            cb_t = self.b * max(0, -net_t)
            # store all data
            self.ot_l.append(o_t)
            self.ipt_l.append(ip_t)
            self.net_l.append(net_t)
            self.wip_l.append(wip_t)
            self.backlog_l.append(backlog)
            self.ch_l.append(ch_t)
            self.cb_l.append(cb_t)
            backlog = 0
        return pd.DataFrame({
            'DtL': self.DtL_l, 'ot': self.ot_l, 'sst': self.sst_l,
            'ip': self.ipt_l,
            'true_demand': self.truth, 'forecasts':self.fcst, 
            'wip': self.wip_l, 'net': self.net_l,
            'backlog': self.backlog_l, 'ch': self.ch_l, 'cb': self.cb_l})