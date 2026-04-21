"""
NEXAH Universality Detector
===========================

Searches for period-doubling transitions and
estimates Feigenbaum scaling ratios.

Output
------
Console report + scaling plot
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# NEXAH dynamics
# --------------------------------------------------

def step(theta,n,drift):

    return (theta + (2*np.pi)/n + np.deg2rad(drift))%(2*np.pi)


# --------------------------------------------------
# estimate orbit period
# --------------------------------------------------

def detect_period(n,drift,steps=4000):

    theta=0.1
    traj=[]

    for _ in range(steps):

        theta=step(theta,n,drift)
        traj.append(theta)

    traj=np.array(traj[-500:])

    for p in range(1,50):

        if np.allclose(traj[:-p],traj[p:],atol=1e-4):
            return p

    return None


# --------------------------------------------------
# scan drift parameter
# --------------------------------------------------

def find_transitions(n):

    drifts=np.linspace(0,6,500)

    periods=[]

    for d in drifts:

        p=detect_period(n,d)

        periods.append(p if p is not None else 0)

    return drifts,np.array(periods)


# --------------------------------------------------
# find doubling points
# --------------------------------------------------

def detect_doublings(drifts,periods):

    transitions=[]

    prev=periods[0]

    for i in range(1,len(periods)):

        if periods[i] == 2*prev and prev>0:

            transitions.append(drifts[i])

        prev=periods[i]

    return transitions


# --------------------------------------------------
# compute Feigenbaum ratios
# --------------------------------------------------

def feigenbaum_ratios(transitions):

    ratios=[]

    for i in range(len(transitions)-2):

        num=transitions[i+1]-transitions[i]
        den=transitions[i+2]-transitions[i+1]

        if den!=0:
            ratios.append(num/den)

    return ratios


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot(periods):

    plt.figure(figsize=(10,5))

    plt.plot(periods)

    plt.title("Period Structure")

    plt.xlabel("Drift index")
    plt.ylabel("Detected period")

    plt.tight_layout()

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

def main():

    print("\nRunning universality detector...\n")

    n=7

    drifts,periods=find_transitions(n)

    plot(periods)

    transitions=detect_doublings(drifts,periods)

    print("\nPeriod-doubling points:")
    print(transitions)

    ratios=feigenbaum_ratios(transitions)

    print("\nFeigenbaum ratios:")
    print(ratios)

    if ratios:
        print("\nMean ratio:",np.mean(ratios))


if __name__=="__main__":
    main()
