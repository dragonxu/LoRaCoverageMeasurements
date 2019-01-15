
"""
    ____  ____      _    __  __  ____ ___
   |  _ \|  _ \    / \  |  \/  |/ ___/ _ \
   | | | | |_) |  / _ \ | |\/| | |  | | | |
   | |_| |  _ <  / ___ \| |  | | |__| |_| |
   |____/|_| \_\/_/   \_\_|  |_|\____\___/
                             research group
                               dramco.be/

    KU Leuven - Technology Campus Gent,
    Gebroeders De Smetstraat 1,
    B-9000 Gent, Belgium

           File: plt_heatmap.py
        Created: 2018-10-30
         Author: Gilles Callebaut
    Description:
"""

import json
import os
from math import sqrt

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy import stats

import util as util

SPINE_COLOR = 'gray'
FORMAT = "pdf"
MARKER = "+"




currentDir = os.path.dirname(os.path.abspath(__file__))
path_to_measurements = os.path.abspath(os.path.join(
    currentDir, '..', 'data'))
input_path = os.path.abspath(os.path.join(
    currentDir, '..', 'result'))
input_file_name = "preprocessed_averaged_data.pkl"


with open(os.path.join(path_to_measurements, "measurements.json")) as f:
    config = json.load(f)
    measurements = config["measurements"]
    for measurement in measurements:
        print("--------------------- RSS MODEL {} ---------------------".format(measurement))
        
        CENTER = config[measurement]["center"]

        input_file_path = os.path.join(
            input_path, measurement, input_file_name)

        df = pd.read_pickle(input_file_path)
        util.addDistanceTo(df, CENTER)
        
        fig = plt.figure(figsize=(4, 3))
        ax = fig.add_subplot(1, 1, 1)
        
        sns.scatterplot(x='distance', y='rss_mean', 
                        data=df, ci=None, color=".1", marker=MARKER, alpha=0.3)
        
        plt.show()

    