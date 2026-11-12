import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# MATHEMATICS

#Goods Market
def AggExp(Y, r, a, b, G, T, Ibar, i1): #calculates the Aggregate Demand for a given interest rate 
    AE = a + b*(Y-T) + Ibar - i1*r + G
    return AE


def GoodsEquilibrium(r, a, b, G, T, Ibar, i1): #calculates the output level ar which goods market is at equilibirum for a given interest rate
    Y_eq = (a + Ibar + G - b*T - i1*r) / (1-b)
    return Y_eq

#Money Market
def MoneyDemand(Y, r, c0, c1, c2): #calculates the money demand schedule for a range of interest rate and at a given level of income
    Md = c0 + c1*Y - c2*r
    return Md

def MoneyEquilibrium(Y, c0, c1, c2, Ms): #calculates the interest rate at which money market is in equilibrium for a given income and money supply
    r_eq = (c0 + c1*Y - Ms) / c2
    return r_eq

#IS Schedule
def ISSchedule(Y, a, b, G, T, Ibar, i1): #calculates the IS schedule array
    r = (a + Ibar + G - b*T - (1-b)*Y) / i1
    return r
#LM Schedule
def LMSchedule(Y, c0, c1, c2, Ms): #calculates the LM schedule array
    r = (c0 + c1*Y - Ms) / c2
    return r

#ISLM Equilibrium
def ISLM_Equilibrium(a, b, G, T, Ibar, i1, c0, c1, c2, Ms): #calculates the simultaneous equilibrium level of income and interest rate for both money and goods market
    
    if c2 != 0:
        Y0 = (a + Ibar + G - b*T + (i1/c2)*(Ms-c0)) / ((1-b) + (i1*c1/c2))
        r0 = (c0 + c1*Y0 - Ms) / c2
    else:
        Y0 = (Ms-c0)/c1
        r0 = (a + Ibar + G - b*T - (1-b)*Y0)/i1
    return Y0, r0


# BASE EQUILIBRIUM CALCULATION
#Y0, r0 = ISLM_Equilibrium(a, b, G, T, Ibar, i1, c0, c1, c2, Ms)
#print("Base Equilibrium")
#print("Income:", Y0)
#print("Interest Rate:", r0)

#Plotting Functions
def plot_goods_market(Y0, r0, a, b, G, T, Ibar, i1, Y1, r1, a_new, b_new, G_new, T_new, Ibar_new, i1_new):

    Y_plot = np.linspace(0, 2*max(Y0,Y1), 1000) #scale of x axis
    AE_curve = AggExp(Y_plot, r0, a, b, G, T, Ibar, i1)  

    fig, ax = plt.subplots(figsize=(7, 5)) 
    ax.plot(Y_plot, AE_curve, label="AE Schedule", linewidth=2) #plots the original aggregate expenditure schedule

    if (a != a_new or b != b_new or G != G_new or T != T_new or Ibar != Ibar_new or i1 != i1_new or r0 != r1): #plot the modified graph if change occurs
        AE_curve_new = AggExp(Y_plot, r1, a_new, b_new, G_new, T_new, Ibar_new, i1_new)
        ax.plot(Y_plot, AE_curve_new, label="Modified AE", linewidth=2)
        ax.scatter(Y1, Y1, color="brown",label="New Equilibrium", zorder=5)
        
    ax.plot(Y_plot, Y_plot, label="45-degree Line", linestyle="--") #plot the 45-degree line
    ax.scatter(Y0, Y0, color="red", label="Equilibrium", zorder=5)
    ax.set_title("Goods Market Equilibrium")
    ax.set_xlabel("National Income (Y)")
    ax.set_ylabel("Aggregate Expenditure (AE)")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 2*max(Y0,Y1))
    ax.set_xlim(0, 2*max(Y0,Y1))
    #fig.tight_layout()
    return fig

def plot_money_market(Y0, r0, c0, c1, c2, Ms, Y1, r1, c0_new, c1_new, c2_new, Ms_new):

    r_plot = np.linspace(0, 2*max(r0,r1), 1000)
    MD_curve = MoneyDemand(Y0, r_plot, c0, c1, c2)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(MD_curve, r_plot, label="Money Demand", linewidth=2) #plots the original Money demand schedule

    if (c0 != c0_new or c1 != c1_new or c2 != c2_new or Y0 != Y1): #plots the modified money demand if there a change in the money market parameters or the equilibrium
        MD_curve_new = MoneyDemand(Y1, r_plot, c0_new, c1_new, c2_new)
        ax.plot(MD_curve_new, r_plot, label="Modified Money Demand", linewidth=2)
        ax.scatter(Ms_new, r1, color="brown", label="New Equilibrium", zorder=5)

    ax.axvline(Ms, color="orange", label="Money Supply") #plots the original money supply schedule
    ax.scatter(Ms, r0, color="red", label="Equilibrium", zorder=5)

    if (Ms != Ms_new): #plots the modified money supply in case there is a change 
        ax.axvline(Ms_new, color="green", linestyle="--", label="Modified Money Supply")
  
    ax.set_title("Money Market Equilibrium")
    ax.set_xlabel("Quantity of Money (M)")
    ax.set_ylabel("Interest Rate (r)")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 2*max(r0,r1))
    ax.set_xlim(0, 2*max(Ms,Ms_new))
    fig.tight_layout()
    return fig

def plot_islm(Y0, r0, a, b, G, T, Ibar, i1, c0, c1, c2, Ms, Y1, r1, a_new, b_new, G_new, T_new, Ibar_new, i1_new, c0_new, c1_new, c2_new, Ms_new):

    Y_plot = np.linspace(0, 2*max(Y0,Y1), 1000) 
    fig, ax = plt.subplots(figsize=(7, 5))

    #Plotting the IS and Modified IS schedule avoiding error when i1=0
    if (i1!=0) :
        IS_curve = ISSchedule(Y_plot, a, b, G, T, Ibar, i1)
        ax.plot(Y_plot, IS_curve, label="IS Curve", linewidth=2)
    else:
        ax.axvline(Y0, label="IS Curve", linewidth=2)

    if (a != a_new or b != b_new or G != G_new or T != T_new or Ibar != Ibar_new or i1 != i1_new):
        if(i1_new != 0):
            IS_curve_new = ISSchedule(Y_plot, a_new, b_new, G_new, T_new, Ibar_new, i1_new)
            ax.plot(Y_plot, IS_curve_new, label="Modified IS", linewidth=2, color= "green")
        else:
            ax.axvline(Y1, label="Modified IS", linewidth=2,color= "green")

    #Plotting the LM and Modified LM schedule avoiding error when c2=0
    if(c2!=0):
        LM_curve = LMSchedule(Y_plot, c0, c1, c2, Ms)
        ax.plot(Y_plot, LM_curve, label="LM Curve", linewidth=2)
    else:
        ax.axvline(Y0, label="LM Curve", linewidth=2)

    if (c0 != c0_new or c1 != c1_new or c2 != c2_new or Ms != Ms_new):
        if(c2_new !=0):
            LM_curve_new = LMSchedule(Y_plot, c0_new, c1_new, c2_new, Ms_new)
            ax.plot(Y_plot, LM_curve_new, label="Modified LM", linewidth=2, color="magenta")
        else:
            ax.axvline(Y1, label="Modified LM", linewidth=2, color="magenta")
        ax.scatter(Y1,r1, color="brown", label="New Equilibrium", zorder=5)
        
    ax.scatter(Y0, r0, color="red", label="Equilibrium", zorder=5)
    ax.axvline(Y0, color="grey", linestyle=":")
    ax.axhline(r0, color="grey", linestyle=":")
    ax.set_title("IS-LM Equilibrium")
    ax.set_xlabel("National Income (Y)")
    ax.set_ylabel("Interest Rate (r)")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 2*max(r0,r1))
    ax.set_xlim(0, 2*max(Y0,Y1))
    fig.tight_layout()
    return fig




#Streamlit Dashboard
st.title("IS-LM Interactive Simulator")
st.set_page_config(layout="wide")

# FIRST ROW
col1, col2 = st.columns(2)
with col1:
    st.subheader("Original Economic Inputs")
    st.caption("Goods Market")

    c1a, c1b = st.columns(2)

    with c1a:
        a = st.number_input("a",min_value=0.0, value=10.0)
        Ibar = st.number_input("Ī",min_value=0.0, value=400.0)
        G = st.number_input("G",min_value=0.0, value=100.0)

    with c1b:
        b = st.number_input("b",min_value=0.0, max_value=0.99, value=0.5)
        i1 = st.number_input("i₁",min_value=0.0, value=0.5)
        T = st.number_input("T",min_value=0.0, value=20.0)

    st.caption("Money Market")

    c2a, c2b = st.columns(2)

    with c2a:
        c0 = st.number_input("c₀",min_value=0.0, value=50.0)
        c2 = st.number_input("c₂",min_value=0.0, value=10.0)

    with c2b:
        c1 = st.number_input("c₁",min_value=0.01,max_value=1.0, value=0.2)
        Ms = st.number_input("Mˢ",min_value=0.0, value=150.0)

if i1 == 0 and c2 == 0:
    st.error("ERROR: i₁ and c₂ cannot both be zero.")
    st.stop()

Y0, r0 = ISLM_Equilibrium(a, b, G, T, Ibar, i1, c0, c1, c2, Ms)
print("Base Equilibrium")
print("Income:", Y0)
print("Interest Rate:", r0)


with col2:
    goods_slot = st.empty()


# SECOND ROW
col3, col4 = st.columns(2)
with col3:
    money_slot = st.empty()

with col4:
    islm_slot = st.empty()


# POLICY INTERVENTION PANEL
st.divider()
st.header("Policy Intervention")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Policy Parameters")

    st.caption("Fiscal Policy")
    G_new = st.slider("Government Spending (G)", 0.0, 500.0, float(G))
    T_new = st.slider("Taxes (T)", 0.0, 200.0, float(T))

    st.caption("Monetary Policy")
    Ms_new = st.slider("Money Supply (Ms)", 0.0, 500.0, float(Ms))

with col2:
    st.subheader("Goods Market")
    
    a_new = st.slider("Autonomous Consumption (a)", 0.0, max(500.0, 2*float(a)), float(a))
    b_new = st.slider("MPC (b)", 0.0, 0.99, float(b))
    Ibar_new = st.slider("Autonomous Investment (Ī)", 0.0, max(500.0, 2*float(Ibar)), float(Ibar))
    i1_new = st.slider("Investment Sensitivity (i₁)", 0.0, max(10.0, 2*float(i1)), float(i1))
    
with col3:
    st.subheader("Money Market")
    
    c0_new = st.slider("Autonomous Money Demand (c₀)", 0.0, max(500.0, 2*float(c0)), float(c0))
    c1_new = st.slider("Income Sensitivity (c₁)", 0.01, 1.0, float(c1))
    c2_new = st.slider("Interest Sensitivity (c₂)", 0.0, max(50.0, 2*float(c2)), float(c2))

if i1_new == 0 and c2_new == 0:
    st.error("ERROR: i₁ and c₂ cannot both be zero.")
    st.stop()   
    
Y1, r1 = ISLM_Equilibrium(a_new, b_new, G_new, T_new, Ibar_new, i1_new, c0_new, c1_new, c2_new, Ms_new)

goods_fig = plot_goods_market(Y0, r0, a, b, G, T, Ibar, i1, Y1, r1, a_new, b_new, G_new, T_new, Ibar_new, i1_new)
money_fig = plot_money_market(Y0, r0, c0, c1, c2, Ms, Y1, r1, c0_new, c1_new, c2_new, Ms_new)
islm_fig = plot_islm(Y0, r0, a, b, G, T, Ibar, i1, c0, c1, c2, Ms, Y1, r1, a_new, b_new, G_new, T_new, Ibar_new, i1_new, c0_new, c1_new, c2_new, Ms_new)

with goods_slot.container():
    st.subheader("Goods Market")
    st.pyplot(goods_fig)

with money_slot.container():
    st.subheader("Money Market")
    st.pyplot(money_fig)

with islm_slot.container():
    st.subheader("IS-LM Equilibrium")
    st.pyplot(islm_fig)