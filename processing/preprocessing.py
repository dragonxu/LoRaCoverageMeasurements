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

           File: preprocessing.py
        Created: 2018-10-30
         Author: Gilles Callebaut
    Description: Preprocessing raw data coming from Arduino Receiver
                 - concatenates different raw csv files
                 - filters data (e.g., values withouth GPS)
                 - removes unneeded data
                 - sorts by time
                 - distance to transmitters (CENTER)
                 - PL
                Stores a pickle file in ../result
"""

import glob
import os

import numpy as np
import pandas as pd

import util as util
import json

HEADER_LONG = ["time", "sat", "satValid", "hdopVal", "hdopValid", "vdopVal", "pdopVal", "lat", "lon", "locValid", "age",
               "ageValid", "alt", "altValid", "course", "courseValid", "speed", "speedValid", "rssi", "snr", "freqError",  "sf", "isPacket"]
HEADER_SHORT = ["time", "sat", "satValid", "hdopVal", "hdopValid", "vdopVal", "pdopVal", "lat", "lon", "locValid", "age",
          "ageValid", "alt", "altValid", "rssi", "snr",  "sf", "isPacket"]

currentDir = os.path.dirname(os.path.abspath(__file__))
path_to_measurements = os.path.abspath(os.path.join(
    currentDir, '..', 'data'))
output_path=os.path.abspath(os.path.join(
                currentDir, '..', 'result'))

with open(os.path.join(path_to_measurements, "measurements.json")) as f:
    config = json.load(f)
    measurements = config["measurements"]
    for measurement in measurements:
        path_to_measurement = os.path.join(path_to_measurements, measurement, 'all')
        all_files=glob.glob(os.path.join(path_to_measurement, "*.csv"))

        print("--------------------- PREPROCESSING {} ---------------------".format(measurement))
        size=0
        df_from_each_file = []
        for file in all_files:
            size += os.path.getsize(file)
        
            df = pd.read_csv(file, sep=',', header=None,names=None)
            df.columns = HEADER_LONG if(df.shape[1] == len(HEADER_LONG)) else HEADER_SHORT
            df_from_each_file.append(df)

        df = pd.concat(df_from_each_file, ignore_index=True, sort=False)
        print(" Reading {0} files {1:.2f} kB".format(len(all_files), size/(1024)))
        total_rows=df.shape[0]

        df=util.filter(df)

        conf_file=os.path.join(path_to_measurement, 'conf.json')

        CENTER = config[measurement]["center"]


        util.addDistanceTo(df, CENTER)
        df=df[df['distance'] < 100*1000]
        util.addPathLossTo(df)
        current_rows=df.shape[0]
        current_rows_data=df[df.isPacket > 0].shape[0]
        print(" Processed {0}/{1} {2:.1f}% rows".format(current_rows,
              total_rows, (current_rows/total_rows)*100))
        print(" Processed {0}/{1} {2:.1f}% and {3:.1f}% of total".format(current_rows_data,
              current_rows, (current_rows_data/current_rows)*100, (current_rows_data/total_rows)*100))
        
        df['noise'] = df['rss'] - df['snr']
        # efective signal power according to Understanding collisions in a LoRaWAN
        df['esp'] = df['rss'] + df['snr'] - 10*np.log10(1+10**(0.1*df['snr']))

        output_file="preprocessed_data.pkl"
        output_file_path=os.path.join(output_path, measurement, output_file)
        df.to_pickle(output_file_path)

        print(" Saving to {}".format(output_file_path))
        print("--------------------- DONE preprocessing.py ---------------------")
