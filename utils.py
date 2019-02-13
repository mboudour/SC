import networkx as nx
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict, defaultdict
import operator
import datetime
import pickle
import community
from matplotlib import rc
from matplotlib import colors as mcolors
import matplotlib as mpl
import random

def teg(G,ego):
	sn=[n for n in G.nodes() if n!=ego]

	dd={}
	for nd in G.edges(data=True):
	    if nd[0]==ego:
	        ed=nd[1]
	    else:
	        ed=nd[0]
	    j=pd.to_datetime(nd[2]['time'])
	    if ed not in dd:
	        dd[ed]=[(j,nd[2]["weight"])]  
	    else:
	        dd[ed].append((j,nd[2]["weight"]))  
	ddd={}
	for k,v in dd.items():
	    for i,u in enumerate(v):
	        ddd[k+str(i)]=u
	dds = sorted(ddd.items(), key=operator.itemgetter(1))

	cc=Counter()

	for nd in dds:
	    for kk in sn:
	        if nd[0].startswith(kk):
	            cc[(kk,nd[1][0])]+=nd[1][1]   #.strftime("%Y-%m")

	ccc={"month":[],"neighs":[],"weight":[]}
	for k,v in cc.items():
	    ccc["month"].append(k[1])
	    ccc["neighs"].append(k[0])
	    ccc["weight"].append(v)
	dfh=pd.DataFrame.from_dict(ccc)
	dfhg=dfh.groupby(["neighs",pd.Grouper(key='month',freq="M")])["weight"].sum().reset_index().sort_values('month')

	dg=dfhg.to_dict()
	bars={k:[] for k in dg["neighs"].values()}
	dates=[]
	datesd={k:[] for k in dg["month"].values()}
	neighs={k:[] for k in dg["month"].values()}
	for k,v in dg["month"].items():
	    datesd[v].append(k)
	    neighs[v].append(dg["neighs"][k])
	for k in sorted(datesd):
	    ssn=set()
	    for i,kk in enumerate(neighs[k]):
	        bars[kk].append(dg["weight"][datesd[k][i]])
	        ssn.add(kk)
	    ssn=set(sn)-ssn
	    for kk in ssn:
	        bars[kk].append(0)
	    dates.append(k.strftime("%Y-%m"))

	return bars, dates, cc, dds, dfhg

def tegd(G,ego):
	sn=[n for n in G.nodes() if n!=ego]

	dd={}
	for nd in G.edges(data=True):
	    if nd[0]==ego:
	        ed=nd[1]
	    else:
	        ed=nd[0]
	    j=pd.to_datetime(nd[2]['time'])
	    if ed not in dd:
	        dd[ed]=[(j,nd[2]["weight"])]  
	    else:
	        dd[ed].append((j,nd[2]["weight"]))  
	ddd={}
	for k,v in dd.items():
	    for i,u in enumerate(v):
	        ddd[k+str(i)]=u
	dds = sorted(ddd.items(), key=operator.itemgetter(1))

	cc=Counter()

	for nd in dds:
	    for kk in sn:
	        if nd[0].startswith(kk):
	            cc[(kk,nd[1][0])]+=nd[1][1]   #.strftime("%Y-%m")

	ccc={"day":[],"neighs":[],"weight":[]}
	for k,v in cc.items():
	    ccc["day"].append(k[1])
	    ccc["neighs"].append(k[0])
	    ccc["weight"].append(v)
	dfh=pd.DataFrame.from_dict(ccc)
	dfhg=dfh.groupby(["neighs",pd.Grouper(key='day',freq="D")])["weight"].sum().reset_index().sort_values('month')

	dg=dfhg.to_dict()
	bars={k:[] for k in dg["neighs"].values()}
	dates=[]
	datesd={k:[] for k in dg["day"].values()}
	neighs={k:[] for k in dg["day"].values()}
	for k,v in dg["day"].items():
	    datesd[v].append(k)
	    neighs[v].append(dg["neighs"][k])
	for k in sorted(datesd):
	    ssn=set()
	    for i,kk in enumerate(neighs[k]):
	        bars[kk].append(dg["weight"][datesd[k][i]])
	        ssn.add(kk)
	    ssn=set(sn)-ssn
	    for kk in ssn:
	        bars[kk].append(0)
	    dates.append(k.strftime("%Y-%m-%d"))

	return bars, dates, cc, dds, dfhg
