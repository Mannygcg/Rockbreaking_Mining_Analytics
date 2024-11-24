import marimo

__generated_with = "0.9.16"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        #Rockbreaking Analytics

        For many mining sites, it is sometimes necessary to have a process called 'rockbreaking'. This process is used to break material that is fed to a unit operation but deemed oversized or blocking the entry of material - this is most commonly performed prior the material being transported on a unit operations such as conveyor belts.

        Rockbreaking is necessary to prevent any blockages and damages to the equipment upstream, however performing rockbreaking  requires for the rates to stop which consequently negatively impacts production.

        On this script, we will use randomly generated data that simulates the times a processing plant uses their rockbreakers. 

        ##Data context

        The material will be sourced from different zones (Zone1, Zone2, Zone3...), each zone has a 'Rocky Ratio' (a value determined during the mining exploration), which measures how rocky the material is - thus how likely for a material to require rock breaking.

        The material will be loaded to different trucks which will then tip the material to the nearest crushing area ('A' or 'B'). The material will go through a grizzly screen and then through a crusher. Each crushing area has two rockbreakers - one at the grizzly and another at the crusher.
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
def __(os, pl, script_dir):
    #Reading files into dataframes

    data_a = pl.read_csv(os.path.join(script_dir, "A_DATA.csv")) #Reading CSV file for Primary Crushing area A

    data_b = pl.read_csv(os.path.join(script_dir, "B_DATA.csv")) #Reading CSV file for Primary Crushing area B

    data_rb = pl.read_csv(os.path.join(script_dir, "RB_DATA.csv")) #Reading CSV file for Downtime in the primary crushing areas and plant
    return data_a, data_b, data_rb


@app.cell
def __(mo):
    mo.md(
        r"""
        #Data exploration
        ## Rockbreaking data
        """
    )
    return


@app.cell
def __(data_rb):
    print('\n','Dataframe for Rockbreaking Events data','\n',
         data_rb.shape, data_rb.columns, data_rb.describe(),'\n')
    data_rb.describe()
    return


@app.cell
def __(mo):
    mo.md(r"""## Primary Crusher Area A data""")
    return


@app.cell
def __(data_a):
    data_a.describe()
    return


@app.cell
def __(mo):
    mo.md(r"""## Primary Crusher Area B data""")
    return


@app.cell
def __(data_a, data_b):
    print('\n','Dataframe for Area A data','\n',
         data_a.shape, data_a.columns, data_a.describe(),'\n')

    print('\n','Dataframe for Area B data','\n',
         data_b.shape, data_b.columns, data_b.describe(),'\n')
    data_b.describe()
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        During the initial exploration the following issues were identified.

        * Incorrect data type for date-time: data that is supposed to be represented in datetime is currently stored as a string. This currently affects: data_rb (EVENT_START and EVENT_END) and data_a + data_b (TIP_DATETIME)

        * Event's length represented in seconds: the mean length of events is 685 seconds and the median being 409 seconds, which impacts the ability to swiftly grasp the impact of the event. It is recommended to convert the data according to the appropriate analysis (sum of downtimes use hours and mean/median of downtimes use minutes).
        """
    )
    return


@app.cell
def __(data_a, data_b, data_rb, pl):
    #Splitting the downtime events into area 'A' and 'B', changing the datetime columns from string type to datetime and adjusting the Length columns from seconds to minutes
    df_rba = data_rb.filter(
        pl.col('AREA') == "Primary Crushing - A"
    ).with_columns(
        pl.col('EVENT_START').str.strptime(pl.Datetime),
        pl.col('EVENT_END').str.strptime(pl.Datetime),
        (pl.col('LENGTH')/60).round(3).alias('LENGTH')
    ).sort('EVENT_START')

    df_rbb = data_rb.filter(
        pl.col('AREA') == "Primary Crushing - B"
    ).with_columns(
        pl.col('EVENT_START').str.strptime(pl.Datetime),
        pl.col('EVENT_END').str.strptime(pl.Datetime),
        (pl.col('LENGTH')/60).alias('LENGTH')
    ).sort('EVENT_START')

    df_a = data_a.with_columns(
        pl.col('TIP_DATETIME').str.strptime(pl.Datetime)
    ).sort('TIP_DATETIME')

    df_b = data_b.with_columns(
        pl.col('TIP_DATETIME').str.strptime(pl.Datetime)
    ).sort('TIP_DATETIME')
    return df_a, df_b, df_rba, df_rbb


@app.cell
def __(df_rba, df_rbb, go, pl):
    _dfa = df_rba.group_by('LOCATION').agg(pl.col('LENGTH').sum()/60)
    _dfb = df_rbb.group_by('LOCATION').agg(pl.col('LENGTH').sum()/60)

    # Generate the bar chart, ensuring the category order is respected
    _fig = go.Figure(data=[
        go.Bar(
            x=_dfa['LOCATION'],
            y=_dfa['LENGTH'],
            name='Primary Crushing - A',
            marker=dict(color='lightblue')
        ),
        go.Bar(
            x=_dfb['LOCATION'],
            y=_dfb['LENGTH'],
            name='Primary Crushing - B',
            marker=dict(color='lightcoral')
        )
    ])

    _fig.update_layout(
        title=f'Comparison of total time (hours) rockbreaking per Location',
        xaxis=dict(
            title='Location' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (hours)' # Y-axis label
            )
    )

    _fig
    return


@app.cell
def __(df_rba, df_rbb, go, pl):
    _dfa = df_rba.group_by('LOCATION').agg(pl.col('LENGTH').mean())
    _dfb = df_rbb.group_by('LOCATION').agg(pl.col('LENGTH').mean())

    # Generate the bar chart, ensuring the category order is respected
    _fig = go.Figure(data=[
        go.Bar(
            x=_dfa['LOCATION'],
            y=_dfa['LENGTH'],
            name='Primary Crushing - A',
            marker=dict(color='lightblue')
        ),
        go.Bar(
            x=_dfb['LOCATION'],
            y=_dfb['LENGTH'],
            name='Primary Crushing - B',
            marker=dict(color='lightcoral')
        )
    ])

    _fig.update_layout(
        title=f'Comparison of mean rockbreaking time (minutes) per Location',
        xaxis=dict(
            title='Location' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (minutes)' # Y-axis label
            )
    )
    _fig
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Initial Exploration - Highlights
        * Area A has a lower downtime compared to Area B on both Grizzly and Crusher locations.
        * Area A however, seemed to have had longer rockbreaking events than Area B.
        """
    )
    return


@app.cell
def __(df_a, df_b, df_rba, df_rbb, pl):
    df_a_all = df_rba.join_asof(df_a, left_on='EVENT_START',right_on='TIP_DATETIME',strategy='backward')
    df_b_all = df_rbb.join_asof(df_b, left_on='EVENT_START',right_on='TIP_DATETIME',strategy='backward')

    _df = df_rbb.filter(pl.col('LOCATION')=='Grizzly')
    df_bg = _df.join_asof(df_b, left_on='EVENT_START',right_on='TIP_DATETIME',strategy='backward')

    _df = df_rba.filter(pl.col('LOCATION')=='Grizzly')
    df_ag = _df.join_asof(df_a, left_on='EVENT_START',right_on='TIP_DATETIME',strategy='backward')
    return df_a_all, df_ag, df_b_all, df_bg


@app.cell
def __(df_a_all, pl, px):
    _start_time = pl.datetime(2024,7,24,6,0,0)
    _end_time = pl.datetime(2024,7,31,6,0,0)

    _df = df_a_all.filter(
        (pl.col('EVENT_START')<=_end_time) & 
        (pl.col('EVENT_START')>=_start_time)
        ).group_by('LOCATION').agg(pl.col('LENGTH').sum()/60,pl.col('ROCKY_RATIO').mean()
        ).sort(
        pl.col('LOCATION'),descending=True
        )

    # Generate the bar chart, ensuring the category order is respected
    _fig = px.bar(
        _df,
        x="LOCATION", 
        y="LENGTH", 
        color='ROCKY_RATIO')

    _fig.update_layout(
        title=f'24-31/07/2024 Total RB time (hours) and mean rocky ratio per Location in Area A',
        xaxis=dict(
            title='Location' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (hours)' # Y-axis label
            )
    )

    _fig
    return


@app.cell
def __(df_b_all, pl, px):
    _start_time = pl.datetime(2024,7,24,6,0,0)
    _end_time = pl.datetime(2024,7,31,6,0,0)

    _df = df_b_all.filter(
        (pl.col('EVENT_START')<=_end_time) & 
        (pl.col('EVENT_START')>=_start_time)
        ).group_by('LOCATION').agg(pl.col('LENGTH').sum()/60,pl.col('ROCKY_RATIO').mean()
        ).sort(
        pl.col('LOCATION'),descending=True
        )

    # Generate the bar chart, ensuring the category order is respected
    _fig = px.bar(
        _df,
        x="LOCATION", 
        y="LENGTH", 
        color='ROCKY_RATIO')

    _fig.update_layout(
        title=f'Total rockbreaking time (hours) and mean rocky ratio per Location in Area B',
        xaxis=dict(
            title='Location' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (hours)' # Y-axis label
            )
    )

    _fig
    return


@app.cell
def __(df_ag, pl, px):
    _start_time = pl.datetime(2024,7,29,6,0,0)
    _end_time = pl.datetime(2024,7,30,6,0,0)

    _df = df_ag.filter(
        (pl.col('EVENT_START')<=_end_time) & 
        (pl.col('EVENT_START')>=_start_time)
    )

    _fig = px.bar(_df, x="EVENT_START", y="LENGTH", color='ROCKY_RATIO')

    _fig.update_layout(
        title=f'29/07/24 rockbreaking time (hours) and mean rocky ratio per Location in Area A',
        xaxis=dict(
            title='Location' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (hours)' # Y-axis label
            )
    )

    _fig.show()
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ##Weekly Analysis

        In this section of the report, we will be analysing the impact of rockbreaking on the different locations on a weekly basis. In this case, we will be using the data generated for the period 24/07/2024 to 31/07/2024.
        """
    )
    return


@app.cell
def __(df_ag, df_bg, pl):
    # Start and end time of the study period
    start_time = pl.datetime(2024,7,24,6,0,0)
    end_time = pl.datetime(2024,7,31,6,0,0)

    # Location A data filtered by start and time, sorted by downtime length and calculating mass/downtime ratio
    df_week_a = df_ag.filter(
        (pl.col('EVENT_START')<=end_time) & 
        (pl.col('EVENT_START')>=start_time)
    ).sort("LENGTH", descending=False).with_columns(
        (pl.col("MASS")/pl.col('LENGTH')).alias("MASS_DT_RATIO"),
        (pl.col('LENGTH')/60).alias('LENGTH')
    )

    # Location B data filtered by start and time, sorted by downtime length and calculating mass/downtime ratio
    df_week_b = df_bg.filter(
        (pl.col('EVENT_START')<=end_time) & 
        (pl.col('EVENT_START')>=start_time)
    ).sort("LENGTH", descending=False).with_columns(
        (pl.col("MASS")/pl.col('LENGTH')).alias("MASS_DT_RATIO")
    )
    return df_week_a, df_week_b, end_time, start_time


@app.cell
def __(df_week_a, make_subplots, pl, px):
    # Arrange the zones by by grouping by origin and calculating total dt length
    _total_length = df_week_a.group_by("ORIGIN").agg(pl.col("LENGTH").sum().alias("TOTAL_LENGTH"))
    _total_massdt = df_week_a.group_by("ORIGIN").agg(
        (pl.col("MASS_DT_RATIO").sum()).alias("TOTAL_MASS_DT")
    )
    # Sort by total length in descending order
    _total_length = _total_length.sort("TOTAL_LENGTH", descending=True)
    _total_massdt = _total_massdt.sort("TOTAL_MASS_DT", descending=True)

    # Convert the sorted order to a list
    _ordered_length= _total_length["ORIGIN"].to_list()
    _ordered_massdt = _total_massdt["ORIGIN"].to_list()

    # Create the first figure (Total length)
    _fig1 = px.bar(
        df_week_a,
        x="ORIGIN",
        y="LENGTH",
        color="ROCKY_RATIO",
        category_orders={"ORIGIN": _ordered_length},
        title="Rockbreaking Time (Hours) per Zone"
    )

    # Create the second figure (Total Mass/Downtime Ratio)
    _fig2 = px.bar(
        df_week_a,
        x="ORIGIN",
        y="MASS_DT_RATIO",
        color="ROCKY_RATIO",
        category_orders={"ORIGIN": _ordered_massdt},
        title="Downtime (Hours) per Zone"
    )

    # Create a subplot figure to place both figures
    _combined_fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=False, 
        vertical_spacing=0.2,
        subplot_titles=[
            "Rockbreaking Time (Hours) per Zone",
            "Mass dumped per Downtime (T/min) per Zone"
        ]
    )

    # Add the first chart to the subplot
    for _trace in _fig1.data:
        _combined_fig.add_trace(_trace, row=1, col=1)

    # Add the second chart to the subplot
    for _trace in _fig2.data:
        _combined_fig.add_trace(_trace, row=2, col=1)

    # Update layout for combined figure
    _combined_fig.update_layout(
        title="Location A - Metrics per Zone (24/07 to 31/07 2024)",
        xaxis=dict(
            title="Origin",
            categoryorder="array",
            categoryarray=_ordered_length
        ),
        xaxis2=dict(
            title="Origin",
            categoryorder="array",
            categoryarray=_ordered_massdt
        ),
        yaxis=dict(title="Rockbreaking Time (Hours)"),
        yaxis2=dict(title="Mass dumped per downtime (T/min)"),
        height=800
    )

    _combined_fig
    return


@app.cell
def __(df_week_b, make_subplots, pl, px):
    # Arrange the zones by by grouping by origin and calculating total dt length
    _total_length = df_week_b.group_by("ORIGIN").agg(pl.col("LENGTH").sum().alias("TOTAL_LENGTH"))
    _total_massdt = df_week_b.group_by("ORIGIN").agg(
        (pl.col("MASS_DT_RATIO").sum()).alias("TOTAL_MASS_DT")
    )
    # Sort by total length in descending order
    _total_length = _total_length.sort("TOTAL_LENGTH", descending=True)
    _total_massdt = _total_massdt.sort("TOTAL_MASS_DT", descending=True)

    # Convert the sorted order to a list
    _ordered_length= _total_length["ORIGIN"].to_list()
    _ordered_massdt = _total_massdt["ORIGIN"].to_list()

    # Create the first figure (Total length)
    _fig1 = px.bar(
        df_week_b,
        x="ORIGIN",
        y="LENGTH",
        color="ROCKY_RATIO",
        category_orders={"ORIGIN": _ordered_length},
        title="Rockbreaking Time (Hours) per Zone"
    )

    # Create the second figure (Total Mass/Downtime Ratio)
    _fig2 = px.bar(
        df_week_b,
        x="ORIGIN",
        y="MASS_DT_RATIO",
        color="ROCKY_RATIO",
        category_orders={"ORIGIN": _ordered_massdt},
        title="Downtime (Hours) per Zone"
    )

    # Create a subplot figure to place both figures
    _combined_fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=False, 
        vertical_spacing=0.2,
        subplot_titles=[
            "Rockbreaking Time (Hours)",
            "Mass dumped per Downtime (T/min)"
        ]
    )

    # Add the first chart to the subplot
    for _trace in _fig1.data:
        _combined_fig.add_trace(_trace, row=1, col=1)

    # Add the second chart to the subplot
    for _trace in _fig2.data:
        _combined_fig.add_trace(_trace, row=2, col=1)

    # Update layout for combined figure
    _combined_fig.update_layout(
        title="Location B - Metrics per Zone (24/07 to 31/07 2024)",
        xaxis=dict(
            title="Origin",
            categoryorder="array",
            categoryarray=_ordered_length
        ),
        xaxis2=dict(
            title="Origin",
            categoryorder="array",
            categoryarray=_ordered_massdt
        ),
        yaxis=dict(title="Rockbreaking Time (Hours)"),
        yaxis2=dict(title="Mass dumped per downtime (T/min)"),
        height=800
    )

    _combined_fig
    return


@app.cell
def __(df_week_a, pl, px):
    # Arrange the zones by by grouping by origin and calculating total dt length
    _total_length = df_week_a.group_by("ORIGIN").agg(pl.col("LENGTH").sum().alias("TOTAL_LENGTH"))
    # Sort by total length in descending order
    _total_length = _total_length.sort("TOTAL_LENGTH", descending=True)

    # Convert the sorted order to a list
    _ordered_origins = _total_length["ORIGIN"].to_list()

    # Generate the bar chart, incorporating the previously generated list
    _fig = px.bar(
        df_week_a,
        x="ORIGIN", 
        y="LENGTH", 
        color='ROCKY_RATIO',
        category_orders={"ORIGIN": _ordered_origins}
    )

    _fig.update_layout(
        title=f'Location A - Rockbreaking time (hours) per zone (24/07 to 31/07 2024)',
        xaxis=dict(
            title='Origin'
        ),
        yaxis=dict(
            title='Downtime (hours)'
            )
    )
    _fig
    return


@app.cell
def __(df_week_a, pl, px):
    # Group by ORIGIN and calculate total length per zone
    _df_total_length = df_week_a.group_by("ORIGIN").agg(
        (pl.col("MASS_DT_RATIO").sum()).alias("TOTAL_LENGTH")
    )

    # Sort ORIGIN by total length in descending order
    _df_total_lengt = _df_total_length.sort("TOTAL_LENGTH", descending=True)

    # Convert the sorted order to a list of categories
    _ordered_origins = _df_total_lengt["ORIGIN"].to_list()

    # Generate the bar chart, ensuring the category order is respected
    _fig = px.bar(
        df_week_a,
        x="ORIGIN", 
        y="MASS_DT_RATIO", 
        color='ROCKY_RATIO',
        category_orders={"ORIGIN": _ordered_origins}  # Set category order
    )

    _fig.update_layout(
        title=f'Location A - Rockbreaking time (hours) per zone (24/07 to 31/07 2024)',
        xaxis=dict(
            title='Origin' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (hours)' # Y-axis label
            )
    )
    _fig
    return


@app.cell
def __(df_bg, end_time, pl, px, start_time):
    _start_time = pl.datetime(2024,7,24,6,0,0)
    _end_time = pl.datetime(2024,7,31,6,0,0)

    _df = df_bg.filter(
        (pl.col('EVENT_START')<=end_time) & 
        (pl.col('EVENT_START')>=start_time)
    ).sort("LENGTH", descending=False)

    # Group by ORIGIN and calculate total length per zone
    _df_total_length = _df.group_by("ORIGIN").agg(pl.col("LENGTH").sum().alias("TOTAL_LENGTH"))

    # Sort ORIGIN by total length in descending order
    _df_total_length = _df_total_length.sort("TOTAL_LENGTH", descending=True)

    # Convert the sorted order to a list of categories
    _ordered_origins = _df_total_length["ORIGIN"].to_list()

    # Generate the bar chart, ensuring the category order is respected
    _fig = px.bar(
        _df,
        x="ORIGIN", 
        y="LENGTH", 
        color='ROCKY_RATIO',
        category_orders={"ORIGIN": _ordered_origins}  # Set category order
    )

    _fig.update_layout(
        title=f'Location B - Rockbreaking time (hours) per zone (24/07 to 31/07 2024)',
        xaxis=dict(
            title='Origin' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (hours)' # Y-axis label
            )
    )

    _fig
    return


@app.cell
def __(df_bg, end_time, pl, px, start_time):
    _start_time = pl.datetime(2024,7,24,6,0,0)
    _end_time = pl.datetime(2024,7,31,6,0,0)

    _df = df_bg.filter(
        (pl.col('EVENT_START')<=end_time) & 
        (pl.col('EVENT_START')>=start_time)
    ).sort("LENGTH", descending=False).with_columns(
        (pl.col("MASS")/pl.col('LENGTH')).alias("RAT")
    )

    # Group by ORIGIN and calculate total length per zone
    _df_total_length = _df.group_by("ORIGIN").agg(
        (pl.col("RAT").sum()).alias("TOTAL_LENGTH")
    )

    # Sort ORIGIN by total length in descending order
    _df_total_lengt = _df_total_length.sort("TOTAL_LENGTH", descending=True)

    # Convert the sorted order to a list of categories
    _ordered_origins = _df_total_lengt["ORIGIN"].to_list()

    # Generate the bar chart, ensuring the category order is respected
    _fig = px.bar(
        _df,
        x="ORIGIN", 
        y="RAT", 
        color='ROCKY_RATIO',
        category_orders={"ORIGIN": _ordered_origins}  # Set category order
    )

    _fig.update_layout(
        title=f'Location B - Rockbreaking time (hours) per zone (24/07 to 31/07 2024)',
        xaxis=dict(
            title='Origin' # X-axis label
        ),
        yaxis=dict(
            title='Downtime (hours)' # Y-axis label
            )
    )
    _fig
    return


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
