import marimo

__generated_with = "0.9.16"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        Rockbreaking Analytics
        -

        For many mining commodities, it is sometimes necessary to have a process called 'rockbreaking'. This process is used to break material that is fed to a unit operation but deemed oversized - this is most commonly performed prior the material being transported on a conveyor belt.

        Rockbreaking is necessary to prevent any blockages and damages to the equipment downstream, however performing rockbreaking  requires for the rates to stop which consequently negatively impacts production.

        On this script, we will use randomly generated data that simulates the times a processing plant uses their rockbreakers. The assumed plant will have with two crushing areas ('A' and 'B') and two rockbreakers within each area. One at the start of the process (Grizzly) and another prior to the primary crusher (Crusher).
        """
    )
    return


@app.cell
def __():
    #Importing relevant libraries
    import os
    import marimo as mo
    import polars as pl
    import numpy as np
    import pandas as pd
    import datetime as dt
    from datetime import date
    import plotly.express as px
    import seaborn as sns
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.datasets import make_regression 
    from sklearn.svm import SVR
    return (
        GridSearchCV,
        LinearRegression,
        RandomForestRegressor,
        SVR,
        date,
        dt,
        go,
        make_regression,
        make_subplots,
        mean_squared_error,
        mo,
        np,
        os,
        pd,
        pl,
        plt,
        px,
        r2_score,
        sns,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        #Important information about the data used
        The data used in this exercise was randomly generated and does not represent any real data from any company or individual. It was created solely for illustrative and educational purposes.

        ##A_DATA and B_DATA
        Both of these datasets share the same columns but their data represents material fed from different zones and fed to different unit operations (A and B). The columns present on this data are:

        * TIP_DATETIME: time in which a truck dumped material to the grizzly.
        * ORIGIN: zone from which the material was extracted.
        * MASS: tonnes of material on the truck
        * TRUCK_ID: unique truck identifier.
        * ROCKY_RATIO: calculated likeliness for a material to be rocky - 1 being rocky and 5 being not rocky. Rockier material tends to generate more rockbreaking events.

        ##DOWNTIME_DATA 

        * AREA: indicates in which crusher (A or B) the rockbreaking event occurred.
        * LOCATION: indicates at which section of primary crusher (Grizzly or Crusher) the rockbreaking event occurred.
        * EVENT_START: time in which the event started.
        * EVENT_END: time in which the event finished.
        * LENGTH: duration of the event (seconds) that afffected performance.
        """
    )
    return


@app.cell
def __(__file__, os, pl):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    df_a = pl.read_csv(os.path.join(script_dir, "A_DATA.csv")) #Reading CSV file for Primary Crushing area A

    df_b = pl.read_csv(os.path.join(script_dir, "B_DATA.csv")) #Reading CSV file for Primary Crushing area B

    df_rb = pl.read_csv(os.path.join(script_dir, "RB_DATA.csv")) #Reading CSV file for Downtime in the primary crushing areas and plant
    return df_a, df_b, df_rb, script_dir


@app.cell
def __(df_rb):
    print('\n','Dataframe for Rockbreaking Events data','\n',
         df_rb.shape, df_rb.columns, df_rb.describe(),'\n')
    return


@app.cell
def __(df_rb):
    df_rb
    return


@app.cell
def __(df_a, df_b):
    print('\n','Dataframe for Area A data','\n',
         df_a.shape, df_a.columns, df_a.describe(),'\n')

    print('\n','Dataframe for Area B data','\n',
         df_b.shape, df_b.columns, df_b.describe(),'\n')
    return


@app.cell
def __(df_a):
    df_a
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
