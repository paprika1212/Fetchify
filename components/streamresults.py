import pandas as pd
import streamlit as st
import time
import numpy as np


def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)
