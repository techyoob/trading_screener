

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
import os
import tensorflow as tf



import os
from dotenv import load_dotenv
load_dotenv()







class Handler:



    def __init__(self):
        print(" init lstm handler")




    def train(self):
        print(" training ")