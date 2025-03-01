import numpy as np
import pandas as pd
from scipy.stats import norm
np.random.seed(42)

####################################################### Function of Forecasted Demand over Lead Time:
def ob_D_tL(
    t,                # current period
    fcst_1,           # forecasted demand from models
    L:int = 3         # lead_time
):
    return sum(fcst_1[t:t+L])

####################################################### Function for Safety Stock:
def ob_ss_t(
    fcst_1_errors,         # forecast errors
    alpha,                 # service_level
    L:int = 3              # lead_time
):
    import numpy as np
    from scipy.stats import norm
    return norm.ppf(alpha)*np.std(fcst_1_errors)*np.sqrt(L)

####################################################### Function for Invt. Position:
def ob_ip_t(
    ip_t,                    # invnt. at t
    net_t,                   # net invt. at t
    w_t,                     # work-in-progress at t
    o_t,                     # amount of orders at time stamp t
    truth_1,                 # true values for a single time series
    fcst_1,                  # forecats for a single time series
    t ,                      # time stamp
    o_t_L = np.nan, 
    L:int=3
):
    if t < 3:
        net_t += np.mean(fcst_1[:L]) - truth_1[t]     # at time stemp t+1
        w_t   += o_t - np.mean(fcst_1[:L])            # at time stemp t+1
    else:
        net_t += o_t_L - truth_1[t]                   # at time stemp t+1
        w_t   += o_t - o_t_L                          # at time stemp t+1
    ip_t  += o_t - truth_1[t]                         # at time stemp t+1
    return ip_t, net_t, w_t

####################################################### Function for Cost:
def cost(
    h = 1,          # holding costs
    b = 19,         # backlog costs
    net_invt = 0    # initial net_invt, will be changed as time t goes.
):
    ch = h*max(0, net_invt)    # costs for Holding products
    cb = b*max(0,-net_invt)    # costs for Backlogging products
    return ch, cb

####################################################### Function for O_t and simulation:
def single_tsis(
    j:int, # the jth time series
    fcst, # the forecasted demand
    truth,# the true values
    lead_time = 3, # lead time
    h = 1,
    b = 19,
    a:float = 0.90,
    # initial position
    ip_t = 0 ,# initial inventory
    wig  = 0 ,# work-in-progress
    net = 0 ,# initial net inventory
    period:int = 28, 
):
    #
    DtL_l, ot_l, sst_l, ch_l, cb_l, ipt_l, net_l, wig_l = [], [], [], [], [], [], [], []
    #
    fcst_1 = np.array(fcst)[j:(j+1)*period]
    truth_1= np.array(truth)[j:(j+1)*period]
    errors = np.array(fcst_1 - truth_1)
    # ot
    for i in range(period):
        if i < 3: # t0
            DtL = ob_D_tL(t = i, fcst_1 = fcst_1, L=lead_time)
            DtL_l.append(DtL)
            
            ss_t = ob_ss_t(fcst_1_errors = errors, alpha = a, L=lead_time)
            
            o_t =  DtL + ss_t - ip_t # order simulation
            ot_l.append(o_t)
            
            ch,cb = cost(h=1,b=19, net_invt = net)
            ch_l.append(ch)
            cb_l.append(cb)
            
            ip_t, net, wig = ob_ip_t(ip_t = ip_t, net_t = net, w_t = wig, o_t = o_t, truth_1=truth_1, fcst_1= fcst_1, t = i , o_t_L = 0) ################
            ipt_l.append(ip_t)
            net_l.append(net)
            wig_l.append(wig)
            
        else:
            DtL = ob_D_tL(t = i, fcst_1 = fcst_1, L=lead_time)
            DtL_l.append(DtL)
            
            ss_t = ob_ss_t(fcst_1_errors = errors, alpha = a, L=lead_time)
            
            o_t = max(0, DtL + ss_t - ip_t) # order simulation
            ot_l.append(o_t)
            
            ch,cb = cost(h=1,b=19, net_invt = net)
            ch_l.append(ch)
            cb_l.append(cb)
            
            ip_t, net, wig = ob_ip_t(ip_t = ip_t, net_t = net, w_t = wig, o_t = o_t, truth_1=truth_1, fcst_1= fcst_1, t = i, o_t_L = ot_l[i-lead_time])
            ipt_l.append(ip_t)
            net_l.append(net)
            wig_l.append(wig)
    return pd.DataFrame({"DtL":DtL_l, "ot":ot_l,"ipt":ipt_l,"net":net_l, "wig": wig_l, "ch": ch_l, "cb":cb_l})
