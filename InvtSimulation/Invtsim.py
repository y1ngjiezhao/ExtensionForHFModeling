#from Invtsim import *
import numpy as np
import pandas as pd
from scipy.stats import norm
import warnings
warnings.simplefilter("ignore")

class InvtSim:
    def __init__(self, 
                 fcst, 
                 truth, 
                 name: str, 
                 residual = None, 
                 L=1, period=28, 
                 h=1, 
                 b=(9,19,99)):
        self.name      = name # models' name
        self.h         = h
        self.b90,self.b95,self.b99 = b
        
        self.period    = period 
        self.fcst      = np.array(fcst)   
        self.truth     = np.array(truth)  
        self.residual  = np.array(residual)
        self.L         = L 
        self.name_l    = []
        
        self.a_90,    self.a_95 ,   self.a_99      = 0.9,0.95,0.99
        self.sst_90l, self.sst_95l, self.sst_99l   = [], [], []
        self.wip_90l, self.wip_95l, self.wip_99l   = [], [], []
        self.ot_90l,  self.ot_95l,  self.ot_99l    = [], [], []
        self.ipt_90l, self.ipt_95l, self.ipt_99l   = [], [], []
        self.net_90l, self.net_95l, self.net_99l   = [], [], []
        self.ch_90l,  self.ch_95l,  self.ch_99l    = [], [], []
        self.cb_90l,  self.cb_95l,  self.cb_99l    = [], [], [] 
        self.bkl_90l, self.bkl_95l, self.bkl_99l   = [], [], []
    def ob_ss_t(self):
        se = np.std(self.residual, ddof=1)
        ss_90 = norm.ppf(self.a_90) * se * np.sqrt(self.L)
        ss_95 = norm.ppf(self.a_95) * se * np.sqrt(self.L)
        ss_99 = norm.ppf(self.a_99) * se * np.sqrt(self.L)
        return (ss_90,ss_95,ss_99)
        
    
    def ob_all_t(self): 
        self.ss90, self.ss95, self.ss99 = self.ob_ss_t()
        dtl_init   = np.sum(self.truth[:self.L])
        self.ip_90t, self.ip_95t, self.ip_99t    =  dtl_init , dtl_init, dtl_init
        self.net_90t, self.net_95t, self.net_99t =  self.ip_90t, self.ip_95t, self.ip_99t
        self.wip_90t, self.wip_95t, self.wip_99t =  0, 0, 0
        self.bkl_90t, self.bkl_95t, self.bkl_99t =  0, 0, 0
        for t in range(self.period):
            # name
            #self.sst_90l.append(self.ss90)
            #self.sst_95l.append(self.ss95)
            #self.sst_99l.append(self.ss99)
            self.name_l.append(f"{self.name}")
            # calculate the Demand over lead time
            DtL = np.sum(self.fcst[t:t + self.L])
            
            # calculate orders
            self.o_90t = max(0, DtL + self.ss90 - self.ip_90t) 
            self.o_95t = max(0, DtL + self.ss95 - self.ip_95t) 
            self.o_99t = max(0, DtL + self.ss99 - self.ip_99t) 
            #print(self.o_90t,self.o_95t, self.o_99t)
            # work-in-progress and updation
            if self.L == 1:
                self.o_t_90L = self.o_90t
                self.o_t_95L = self.o_95t
                self.o_t_99L = self.o_99t
            elif self.L>1:
                self.o_t_90L = self.ot_90l[-self.L] if len(self.ot_90l) >= self.L else 0 #(self.ot_90l[-1] if len(self.ot_90l) > 0 else 0)
                self.o_t_95L = self.ot_95l[-self.L] if len(self.ot_95l) >= self.L else 0 #(self.ot_95l[-1] if len(self.ot_95l) > 0 else 0)
                self.o_t_99L = self.ot_99l[-self.L] if len(self.ot_99l) >= self.L else 0 #(self.ot_99l[-1] if len(self.ot_99l) > 0 else 0)
            # update the work-in-progress
            #self.wip_90t = self.wip_90t + (self.ot_90l[-1] if len(self.ot_90l) > 0 else 0) - self.o_t_90L
            #self.wip_95t = self.wip_95t + (self.ot_95l[-1] if len(self.ot_95l) > 0 else 0) - self.o_t_95L
            #self.wip_99t = self.wip_99t + (self.ot_99l[-1] if len(self.ot_99l) > 0 else 0) - self.o_t_99L
            # update the net inventory
            self.net_90t = self.net_90t + self.o_t_90L - self.truth[t]
            self.net_95t = self.net_95t + self.o_t_95L - self.truth[t]
            self.net_99t = self.net_99t + self.o_t_99L - self.truth[t]
            # update the backlog
            self.bkl_90t = max(0, -self.net_90t) if self.net_90t < 0 else 0
            self.bkl_95t = max(0, -self.net_95t) if self.net_95t < 0 else 0
            self.bkl_99t = max(0, -self.net_99t) if self.net_99t < 0 else 0
            # save the backlogs
            self.bkl_90l.append(self.bkl_90t)
            self.bkl_95l.append(self.bkl_95t)
            self.bkl_99l.append(self.bkl_99t)
            # inventory position updataion
            self.ip_90t = self.ip_90t + self.o_90t - self.truth[t]
            self.ip_95t = self.ip_95t + self.o_95t - self.truth[t]
            self.ip_99t = self.ip_99t + self.o_99t - self.truth[t]
            # save ipt for each service level 
            self.ipt_90l.append(self.ip_90t)
            self.ipt_95l.append(self.ip_95t)
            self.ipt_99l.append(self.ip_99t)
            # save it  for each service level
            self.net_90l.append(self.net_90t)
            self.net_95l.append(self.net_95t)
            self.net_99l.append(self.net_99t)
            
            #self.wip_90l.append(self.wip_90t)
            #self.wip_95l.append(self.wip_95t)
            #self.wip_99l.append(self.wip_99t)
            
            # calcutate holding costs
            self.ch_90t = self.h * max(0, self.net_90t)
            self.ch_95t = self.h * max(0, self.net_95t)
            self.ch_99t = self.h * max(0, self.net_99t)
            # calcutate backlogging costs
            self.cb_90t = self.b90 * self.bkl_90t
            self.cb_95t = self.b95 * self.bkl_95t
            self.cb_99t = self.b99 * self.bkl_99t
            # save holding costs
            self.ch_90l.append(self.ch_90t)
            self.ch_95l.append(self.ch_95t)
            self.ch_99l.append(self.ch_99t)
            # save backlogging costs
            self.cb_90l.append(self.cb_90t)
            self.cb_95l.append(self.cb_95t)
            self.cb_99l.append(self.cb_99t)
            # save the order here
            self.ot_90l.append(self.o_90t)
            self.ot_95l.append(self.o_95t)
            self.ot_99l.append(self.o_99t)
        return pd.DataFrame({
            'name': self.name_l,
            'true_demand': self.truth, 
            'forecasts': self.fcst,
            'ot_90': self.ot_90l, 
            #'sst_90': self.sst_90l,
            'ip_90': self.ipt_90l,
            #'wip_90': self.wip_90l,
            'net_90': self.net_90l,
            'backlog_90': self.bkl_90l, 
            'ch_90': self.ch_90l, 
            'cb_90': self.cb_90l,
            
            'ot_95': self.ot_95l, 
            #'sst_95': self.sst_95l,
            'ip_95': self.ipt_95l,
            #'wip_95': self.wip_95l,
            'net_95': self.net_95l,
            'backlog_95': self.bkl_95l, 
            'ch_95': self.ch_95l, 
            'cb_95': self.cb_95l,
            
            'ot_99': self.ot_99l, 
            #'sst_99': self.sst_99l,
            'ip_99': self.ipt_99l,
            #'wip_99': self.wip_99l,
            'net_99': self.net_99l,
            'backlog_99': self.bkl_99l, 
            'ch_99': self.ch_99l, 
            'cb_99': self.cb_99l})
    
    def ob_all_t_fixedcase(self,fixed_order:pd.DataFrame): 
        #self.ss90, self.ss95, self.ss99 = self.ob_ss_t()
        dtl_init   = np.sum(self.truth[:self.L])
        self.ip_90t, self.ip_95t, self.ip_99t    =  dtl_init , dtl_init, dtl_init
        self.net_90t, self.net_95t, self.net_99t =  self.ip_90t, self.ip_95t, self.ip_99t
        self.wip_90t, self.wip_95t, self.wip_99t =  0, 0, 0
        self.bkl_90t, self.bkl_95t, self.bkl_99t =  0, 0, 0
        a,b,c = np.array(fixed_order.iloc[:,0]), np.array(fixed_order.iloc[:,1]),np.array(fixed_order.iloc[:,2])
        
        for t in range(self.period):
            # name
            #self.sst_90l.append(self.ss90)
            #self.sst_95l.append(self.ss95)
            #self.sst_99l.append(self.ss99)
            self.name_l.append(f"{self.name}")
            # calculate the Demand over lead time
            #DtL = np.sum(self.fcst[t:t + self.L])
            
            # calculate orders
            self.o_90t =  a[t]
            self.o_95t =  b[t]
            self.o_99t =  c[t]
            
            #print(self.o_90t,self.o_95t, self.o_99t)
            # work-in-progress and updation
            if self.L == 1:
                self.o_t_90L = self.o_90t
                self.o_t_95L = self.o_95t
                self.o_t_99L = self.o_99t
            elif self.L>1:
                self.o_t_90L = self.ot_90l[-self.L] if len(self.ot_90l) >= self.L else 0 #(self.ot_90l[-1] if len(self.ot_90l) > 0 else 0)
                self.o_t_95L = self.ot_95l[-self.L] if len(self.ot_95l) >= self.L else 0 #(self.ot_95l[-1] if len(self.ot_95l) > 0 else 0)
                self.o_t_99L = self.ot_99l[-self.L] if len(self.ot_99l) >= self.L else 0 #(self.ot_99l[-1] if len(self.ot_99l) > 0 else 0)
            # update the work-in-progress
            #self.wip_90t = self.wip_90t + (self.ot_90l[-1] if len(self.ot_90l) > 0 else 0) - self.o_t_90L
            #self.wip_95t = self.wip_95t + (self.ot_95l[-1] if len(self.ot_95l) > 0 else 0) - self.o_t_95L
            #self.wip_99t = self.wip_99t + (self.ot_99l[-1] if len(self.ot_99l) > 0 else 0) - self.o_t_99L
            # update the net inventory
            self.net_90t = self.net_90t + self.o_t_90L - self.truth[t]
            self.net_95t = self.net_95t + self.o_t_95L - self.truth[t]
            self.net_99t = self.net_99t + self.o_t_99L - self.truth[t]
            # update the backlog
            self.bkl_90t = max(0, -self.net_90t) if self.net_90t < 0 else 0
            self.bkl_95t = max(0, -self.net_95t) if self.net_95t < 0 else 0
            self.bkl_99t = max(0, -self.net_99t) if self.net_99t < 0 else 0
            # save the backlogs
            self.bkl_90l.append(self.bkl_90t)
            self.bkl_95l.append(self.bkl_95t)
            self.bkl_99l.append(self.bkl_99t)
            # inventory position updataion
            self.ip_90t = self.ip_90t + self.o_90t - self.truth[t]
            self.ip_95t = self.ip_95t + self.o_95t - self.truth[t]
            self.ip_99t = self.ip_99t + self.o_99t - self.truth[t]
            # save ipt for each service level 
            self.ipt_90l.append(self.ip_90t)
            self.ipt_95l.append(self.ip_95t)
            self.ipt_99l.append(self.ip_99t)
            # save it  for each service level
            self.net_90l.append(self.net_90t)
            self.net_95l.append(self.net_95t)
            self.net_99l.append(self.net_99t)
            
            #self.wip_90l.append(self.wip_90t)
            #self.wip_95l.append(self.wip_95t)
            #self.wip_99l.append(self.wip_99t)
            
            # calcutate holding costs
            self.ch_90t = self.h * max(0, self.net_90t)
            self.ch_95t = self.h * max(0, self.net_95t)
            self.ch_99t = self.h * max(0, self.net_99t)
            # calcutate backlogging costs
            self.cb_90t = self.b90 * self.bkl_90t
            self.cb_95t = self.b95 * self.bkl_95t
            self.cb_99t = self.b99 * self.bkl_99t
            # save holding costs
            self.ch_90l.append(self.ch_90t)
            self.ch_95l.append(self.ch_95t)
            self.ch_99l.append(self.ch_99t)
            # save backlogging costs
            self.cb_90l.append(self.cb_90t)
            self.cb_95l.append(self.cb_95t)
            self.cb_99l.append(self.cb_99t)
            self.ot_90l.append(self.o_90t) 
            self.ot_95l.append(self.o_95t) 
            self.ot_99l.append(self.o_99t) 
            # save the order here
            #self.ot_90l.append(self.o_90t)
            #self.ot_95l.append(self.o_95t)
            #self.ot_99l.append(self.o_99t)
        return pd.DataFrame({
            'name': self.name_l,
            'true_demand': self.truth, 
            'forecasts': self.fcst,
            'ot_90': self.ot_90l, 
            #'sst_90': self.sst_90l,
            'ip_90': self.ipt_90l,
            #'wip_90': self.wip_90l,
            'net_90': self.net_90l,
            'backlog_90': self.bkl_90l, 
            'ch_90': self.ch_90l, 
            'cb_90': self.cb_90l,
            
            'ot_95': self.ot_95l, 
            #'sst_95': self.sst_95l,
            'ip_95': self.ipt_95l,
            #'wip_95': self.wip_95l,
            'net_95': self.net_95l,
            'backlog_95': self.bkl_95l, 
            'ch_95': self.ch_95l, 
            'cb_95': self.cb_95l,
            
            'ot_99': self.ot_99l, 
            #'sst_99': self.sst_99l,
            'ip_99': self.ipt_99l,
            #'wip_99': self.wip_99l,
            'net_99': self.net_99l,
            'backlog_99': self.bkl_99l, 
            'ch_99': self.ch_99l, 
            'cb_99': self.cb_99l})
