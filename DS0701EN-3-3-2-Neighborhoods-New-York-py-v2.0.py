#%%
# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %% [markdown]
# <a href="https://cognitiveclass.ai"><img src = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs_v1/IDSNlogo.png" width = 400> </a>
#
# <h1 align=center><font size = 5>Segmenting and Clustering Neighborhoods in New York City</font></h1>
#
# %% [markdown]
# ## Introduction
#
# In this lab, you will learn how to convert addresses into their equivalent latitude and longitude values. Also, you will use the Foursquare API to explore neighborhoods in New York City. You will use the **explore** function to get the most common venue categories in each neighborhood, and then use this feature to group the neighborhoods into clusters. You will use the _k_-means clustering algorithm to complete this task. Finally, you will use the Folium library to visualize the neighborhoods in New York City and their emerging clusters.
#
# %% [markdown]
# ## Table of Contents
#
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#
# <font size = 3>
#
# 1.  <a href="#item1">Download and Explore Dataset</a>
#
# 2.  <a href="#item2">Explore Neighborhoods in New York City</a>
#
# 3.  <a href="#item3">Analyze Each Neighborhood</a>
#
# 4.  <a href="#item4">Cluster Neighborhoods</a>
#
# 5.  <a href="#item5">Examine Clusters</a>
#     </font>
#     </div>
#
# %% [markdown]
# Before we get the data and start exploring it, let's download all the dependencies that we will need.
#

# %%
from pprint import pprint
import numpy as np  # library to handle data in a vectorized manner
import pandas as pd  # library for data analsysis

pd.set_option("display.max_columns", None)

pd.set_option("display.max_rows", None)

import json  # library to handle JSON files

# !conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab
import folium  # map rendering library

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors
import requests  # library to handle requests

# !conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab
from geopy.geocoders import (
    Nominatim,  # convert an address into latitude and longitude values
)
from pandas import json_normalize  # tranform JSON file into a pandas dataframe

# import k-means from clustering stage
from sklearn.cluster import KMeans

print("Libraries imported.")

# %% [markdown]
# ## 1. Download and Explore Dataset
#
# %% [markdown]
# Neighborhood has a total of 5 boroughs and 306 neighborhoods. In order to segement the neighborhoods and explore them, we will essentially need a dataset that contains the 5 boroughs and the neighborhoods that exist in each borough as well as the the latitude and logitude coordinates of each neighborhood.
#
# %% [markdown]
# For your convenience, I downloaded the files and placed it on the server, so you can simply run a `wget` command and access the data. So let's go ahead and do that.
#

# %%
# !wget -q -O 'newyork_data.json' https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs/newyork_data.json
print("Data downloaded!")

# %% [markdown]
# #### Load and explore the data
#
# %% [markdown]
# Next, let's load the data.
#

# %%
with open("newyork_data.json") as json_data:
    newyork_data = json.load(json_data)

# %% [markdown]
# Let's take a quick look at the data.
#
# %% [markdown]
# Let's take a look at the first item in this list.
#
# %% [markdown]
# Notice how all the relevant data is in the _features_ key, which is basically a list of the neighborhoods. So, let's define a new variable that includes this data.
#

# %%
neighborhoods_data = newyork_data["features"]

# %%
neighborhoods_data[0]

# %% [markdown]
# #### Tranform the data into a _pandas_ dataframe
#
# %% [markdown]
# The next task is essentially transforming this data of nested Python dictionaries into a _pandas_ dataframe. So let's start by creating an empty dataframe.
#

# %%
# define the dataframe columns
column_names = ["Borough", "Neighborhood", "Latitude", "Longitude"]

# instantiate the dataframe
neighborhoods = pd.DataFrame(columns=column_names)

# %%
neighborhoods

# %% [markdown]
# Take a look at the empty dataframe to confirm that the columns are as intended.
#
# %% [markdown]
# Then let's loop through the data and fill the dataframe one row at a time.
#

# %%
for data in neighborhoods_data:
    borough = neighborhood_name = data["properties"]["borough"]
    neighborhood_name = data["properties"]["name"]

    neighborhood_latlon = data["geometry"]["coordinates"]
    neighborhood_lat = neighborhood_latlon[1]
    neighborhood_lon = neighborhood_latlon[0]

    neighborhoods = neighborhoods.append(
        {
            "Borough": borough,
            "Neighborhood": neighborhood_name,
            "Latitude": neighborhood_lat,
            "Longitude": neighborhood_lon,
        },
        ignore_index=True,
    )

# %% [markdown]
# Quickly examine the resulting dataframe.
#

# %%
neighborhoods.head()

# %% [markdown]
# And make sure that the dataset has all 5 boroughs and 306 neighborhoods.
#

# %%
print(
    "The dataframe has {} boroughs and {} neighborhoods.".format(
        len(neighborhoods["Borough"].unique()), neighborhoods.shape[0]
    )
)

# %% [markdown]
# #### Use geopy library to get the latitude and longitude values of New York City.
#
# %% [markdown]
# In order to define an instance of the geocoder, we need to define a user_agent. We will name our agent <em>ny_explorer</em>, as shown below.
#

# %%
address = "New York City, NY"

geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(
    "The geograpical coordinate of New York City are {}, {}.".format(
        latitude, longitude
    )
)

# %% [markdown]
# #### Create a map of New York with neighborhoods superimposed on top.
#

# %%
# create map of New York using latitude and longitude values
map_newyork = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(
    neighborhoods["Latitude"],
    neighborhoods["Longitude"],
    neighborhoods["Borough"],
    neighborhoods["Neighborhood"],
):
    label = "{}, {}".format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color="#0a81ab",
        fill=True,
        fill_color="#0a81ab",
        fill_opacity=0.7,
        parse_html=False,
    ).add_to(map_newyork)
# map_newyork.save("output/map_newyork.html")
map_newyork
# %% [markdown]
# **Folium** is a great visualization library. Feel free to zoom into the above map, and click on each circle mark to reveal the name of the neighborhood and its respective borough.
#
# %% [markdown]
# However, for illustration purposes, let's simplify the above map and segment and cluster only the neighborhoods in Manhattan. So let's slice the original dataframe and create a new dataframe of the Manhattan data.
#

# %%
manhattan_data = neighborhoods[neighborhoods["Borough"] == "Manhattan"].reset_index(
    drop=True
)
manhattan_data.head()

# %% [markdown]
# Let's get the geographical coordinates of Manhattan.
#

# %%
address = "Manhattan, NY"

geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print("The geograpical coordinate of Manhattan are {}, {}.".format(latitude, longitude))

# %% [markdown]
# As we did with all of New York City, let's visualizat Manhattan the neighborhoods in it.
#

# %%
# create map of Manhattan using latitude and longitude values
map_manhattan = folium.Map(location=[latitude, longitude], zoom_start=11)

# add markers to map
for lat, lng, label in zip(
    manhattan_data["Latitude"],
    manhattan_data["Longitude"],
    manhattan_data["Neighborhood"],
):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color="#00adb5",
        fill=True,
        fill_color="#00adb5",
        fill_opacity=0.7,
        parse_html=False,
    ).add_to(map_manhattan)

# map_manhattan.save("output/map_manhattan.html")
map_manhattan
# %% [markdown]
# Next, we are going to start utilizing the Foursquare API to explore the neighborhoods and segment them.
#
# %% [markdown]
# #### Define Foursquare Credentials and Version
#

# %%
CLIENT_ID = "U3B2T3FQDUJHBDYMRZ4555ZTFUPOCOOSUGH0NTTHPWBSF42A"  # your Foursquare ID
CLIENT_SECRET = (
    "UWWQOMEUI2E0XKHK14EWURBEXIZ4MSYHGTTGCSDRSJIXIUDL"  # your Foursquare Secret
)
ACCESS_TOKEN = "BELMADBNZPCS1LZFHO3TAEZB13MTHWKWZK3WXBQD0N4QDEKK"

VERSION = "20180605"  # Foursquare API version
LIMIT = 100  # A default Foursquare API limit value

print("Your credentails:")
print("CLIENT_ID: " + CLIENT_ID)
print("CLIENT_SECRET:" + CLIENT_SECRET)

# %% [markdown]
# #### Let's explore the first neighborhood in our dataframe.
#
# %% [markdown]
# Get the neighborhood's name.
#

# %%
manhattan_data.loc[0, "Neighborhood"]

# %% [markdown]
# Get the neighborhood's latitude and longitude values.
#

# %%
neighborhood_latitude = manhattan_data.loc[0, "Latitude"]  # neighborhood latitude value
neighborhood_longitude = manhattan_data.loc[
    0, "Longitude"
]  # neighborhood longitude value
#%%
neighborhood_name = manhattan_data.loc[0, "Neighborhood"]  # neighborhood name

print(
    "Latitude and longitude values of {} are {}, {}.".format(
        neighborhood_name, neighborhood_latitude, neighborhood_longitude
    )
)

# %% [markdown]
# #### Now, let's get the top 100 venues that are in Marble Hill within a radius of 500 meters.
#
# %% [markdown]
# First, let's create the GET request URL. Name your URL **url**.
#

# %%
# type your answer here
radius = 500
url = "https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}".format(
    CLIENT_ID,
    CLIENT_SECRET,
    VERSION,
    neighborhood_latitude,
    neighborhood_longitude,
    radius,
    LIMIT,
)
print(url)
# %% [markdown]
# Double-click **here** for the solution.
#
# <!-- The correct answer is:
# LIMIT = 100 # limit of number of venues returned by Foursquare API
# -->
#
# <!--
# radius = 500 # define radius
# -->
#
# <!--
# \\\\ # create URL
# url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
#     CLIENT_ID,
#     CLIENT_SECRET,
#     VERSION,
#     neighborhood_latitude,
#     neighborhood_longitude,
#     radius,
#     LIMIT)
# url # display URL
# -->
#
# %% [markdown]
# Send the GET request and examine the resutls
#

# %%
results = requests.get(url).json()
pprint(results)


# %% [markdown]
# From the Foursquare lab in the previous module, we know that all the information is in the _items_ key. Before we proceed, let's borrow the **get_category_type** function from the Foursquare lab.
#

# %%
# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row["categories"]
    except:
        categories_list = row["venue.categories"]

    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]["name"]


# %% [markdown]
# Now we are ready to clean the json and structure it into a _pandas_ dataframe.
#

# %%
venues = results["response"]["groups"][0]["items"]

nearby_venues = json_normalize(venues)  # flatten JSON

# filter columns
filtered_columns = [
    "venue.name",
    "venue.categories",
    "venue.location.lat",
    "venue.location.lng",
]
nearby_venues = nearby_venues.loc[:, filtered_columns]

# filter the category for each row
nearby_venues["venue.categories"] = nearby_venues.apply(get_category_type, axis=1)

# clean columns
nearby_venues.columns = [col.split(".")[-1] for col in nearby_venues.columns]

nearby_venues.head()

# %% [markdown]
# And how many venues were returned by Foursquare?
#

# %%
print("{} venues were returned by Foursquare.".format(nearby_venues.shape[0]))


# %% [markdown]
# ## 2. Explore Neighborhoods in Manhattan
#
# %% [markdown]
# #### Let's create a function to repeat the same process to all the neighborhoods in Manhattan
#

# %%
def getNearbyVenues(names, latitudes, longitudes, radius=500):
    venues_list = []
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)

        # create the API request URL
        url = "https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}".format(
            CLIENT_ID, CLIENT_SECRET, VERSION, lat, lng, radius, LIMIT
        )

        # make the GET request
        results = requests.get(url).json()["response"]["groups"][0]["items"]

        # return only relevant information for each nearby venue
        venues_list.append(
            [
                (
                    name,
                    lat,
                    lng,
                    v["venue"]["name"],
                    v["venue"]["location"]["lat"],
                    v["venue"]["location"]["lng"],
                    v["venue"]["categories"][0]["name"],
                )
                for v in results
            ]
        )

    nearby_venues = pd.DataFrame(
        [item for venue_list in venues_list for item in venue_list]
    )
    nearby_venues.columns = [
        "Neighborhood",
        "Neighborhood Latitude",
        "Neighborhood Longitude",
        "Venue",
        "Venue Latitude",
        "Venue Longitude",
        "Venue Category",
    ]

    return nearby_venues


# %% [markdown]
# #### Now write the code to run the above function on each neighborhood and create a new dataframe called _manhattan_venues_.
#

# %%
# type your answer here
manhattan_venues = getNearbyVenues(
    names=manhattan_data["Neighborhood"],
    latitudes=manhattan_data["Latitude"],
    longitudes=manhattan_data["Longitude"],
)

# %% [markdown]
# Double-click **here** for the solution.
#
# <!-- The correct answer is:
# manhattan_venues = getNearbyVenues(names=manhattan_data['Neighborhood'],
#                                    latitudes=manhattan_data['Latitude'],
#                                    longitudes=manhattan_data['Longitude']
#                                   )
# -->
#
# %% [markdown]
# #### Let's check the size of the resulting dataframe
#

# %%
print(manhattan_venues.shape)
manhattan_venues.head()

# %% [markdown]
# Let's check how many venues were returned for each neighborhood
#

# %%
manhattan_venues.groupby("Neighborhood").count()

# %% [markdown]
# #### Let's find out how many unique categories can be curated from all the returned venues
#

# %%
print(
    "There are {} uniques categories.".format(
        len(manhattan_venues["Venue Category"].unique())
    )
)

# %% [markdown]
# <a id='item3'></a>
#
# %% [markdown]
# ## 3. Analyze Each Neighborhood
#

# %%
manhattan_venues[["Venue Category"]].head()

# %%
manhattan_onehot = pd.get_dummies(
    manhattan_venues[["Venue Category"]], prefix="", prefix_sep=""
)
manhattan_onehot.head()

# %%
# one hot encoding
manhattan_onehot = pd.get_dummies(
    manhattan_venues[["Venue Category"]], prefix="", prefix_sep=""
)
manhattan_onehot
#%%
# add neighborhood column back to dataframe
manhattan_onehot["Neighborhood"] = manhattan_venues["Neighborhood"]

# move neighborhood column to the first column
fixed_columns = [manhattan_onehot.columns[-1]] + list(manhattan_onehot.columns[:-1])
manhattan_onehot = manhattan_onehot[fixed_columns]

manhattan_onehot.head()

# %% [markdown]
# And let's examine the new dataframe size.
#

# %%
manhattan_onehot.shape

# %% [markdown]
# #### Next, let's group rows by neighborhood and by taking the mean of the frequency of occurrence of each category
#

# %%
manhattan_grouped = manhattan_onehot.groupby("Neighborhood").mean().reset_index()
manhattan_grouped

# %% [markdown]
# #### Let's confirm the new size
#

# %%
manhattan_grouped.shape

# %% [markdown]
# #### Let's print each neighborhood along with the top 5 most common venues
#

# %%
num_top_venues = 5

for hood in manhattan_grouped["Neighborhood"]:
    print("----" + hood + "----")
    temp = manhattan_grouped[manhattan_grouped["Neighborhood"] == hood].T.reset_index()
    temp.columns = ["venue", "freq"]
    temp = temp.iloc[1:]
    temp["freq"] = temp["freq"].astype(float)
    temp = temp.round({"freq": 2})
    print(
        temp.sort_values("freq", ascending=False)
        .reset_index(drop=True)
        .head(num_top_venues)
    )
    print("\n")


# %% [markdown]
# #### Let's put that into a _pandas_ dataframe
#
# %% [markdown]
# First, let's write a function to sort the venues in descending order.
#

# %%
def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)

    return row_categories_sorted.index.values[0:num_top_venues]


# %% [markdown]
# Now let's create the new dataframe and display the top 10 venues for each neighborhood.
#

# %%
num_top_venues = 10

indicators = ["st", "nd", "rd"]

# create columns according to number of top venues
columns = ["Neighborhood"]
for ind in np.arange(num_top_venues):
    try:
        columns.append("{}{} Most Common Venue".format(ind + 1, indicators[ind]))
    except:
        columns.append("{}th Most Common Venue".format(ind + 1))

# create a new dataframe
neighborhoods_venues_sorted = pd.DataFrame(columns=columns)
neighborhoods_venues_sorted["Neighborhood"] = manhattan_grouped["Neighborhood"]

for ind in np.arange(manhattan_grouped.shape[0]):
    neighborhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(
        manhattan_grouped.iloc[ind, :], num_top_venues
    )

neighborhoods_venues_sorted.head()

# %% [markdown]
# <a id='item4'></a>
#
# %% [markdown]
# ## 4. Cluster Neighborhoods
#
# %% [markdown]
# Run _k_-means to cluster the neighborhood into 5 clusters.
#

# %%
# set number of clusters
kclusters = 5

manhattan_grouped_clustering = manhattan_grouped.drop("Neighborhood", 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(manhattan_grouped_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10]

# %% [markdown]
# Let's create a new dataframe that includes the cluster as well as the top 10 venues for each neighborhood.
#

# %%
# add clustering labels
neighborhoods_venues_sorted.insert(0, "Cluster Labels", kmeans.labels_)

manhattan_merged = manhattan_data

# merge manhattan_grouped with manhattan_data to add latitude/longitude for each neighborhood
manhattan_merged = manhattan_merged.join(
    neighborhoods_venues_sorted.set_index("Neighborhood"), on="Neighborhood"
)

manhattan_merged.head()  # check the last columns!

# %% [markdown]
# Finally, let's visualize the resulting clusters
#

# %%
# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i * x) ** 2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(
    manhattan_merged["Latitude"],
    manhattan_merged["Longitude"],
    manhattan_merged["Neighborhood"],
    manhattan_merged["Cluster Labels"],
):
    label = folium.Popup(str(poi) + " Cluster " + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster - 1],
        fill=True,
        fill_color=rainbow[cluster - 1],
        fill_opacity=0.7,
    ).add_to(map_clusters)

map_clusters

# %% [markdown]
# <a id='item5'></a>
#
# %% [markdown]
# ## 5. Examine Clusters
#
# %% [markdown]
# Now, you can examine each cluster and determine the discriminating venue categories that distinguish each cluster. Based on the defining categories, you can then assign a name to each cluster. I will leave this exercise to you.
#
# %% [markdown]
# #### Cluster 1
#

# %%
manhattan_merged.loc[
    manhattan_merged["Cluster Labels"] == 0,
    manhattan_merged.columns[[1] + list(range(5, manhattan_merged.shape[1]))],
]

# %% [markdown]
# #### Cluster 2
#

# %%
manhattan_merged.loc[
    manhattan_merged["Cluster Labels"] == 1,
    manhattan_merged.columns[[1] + list(range(5, manhattan_merged.shape[1]))],
]

# %% [markdown]
# #### Cluster 3
#

# %%
manhattan_merged.loc[
    manhattan_merged["Cluster Labels"] == 2,
    manhattan_merged.columns[[1] + list(range(5, manhattan_merged.shape[1]))],
]

# %% [markdown]
# #### Cluster 4
#

# %%
manhattan_merged.loc[
    manhattan_merged["Cluster Labels"] == 3,
    manhattan_merged.columns[[1] + list(range(5, manhattan_merged.shape[1]))],
]

# %% [markdown]
# #### Cluster 5
#

# %%
manhattan_merged.loc[
    manhattan_merged["Cluster Labels"] == 4,
    manhattan_merged.columns[[1] + list(range(5, manhattan_merged.shape[1]))],
]

# %% [markdown]
# ### Thank you for completing this lab!
#
# This notebook was created by [Alex Aklson](https://www.linkedin.com/in/aklson?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ) and [Polong Lin](https://www.linkedin.com/in/polonglin?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ). I hope you found this lab interesting and educational. Feel free to contact us if you have any questions!
#
# %% [markdown]
# This notebook is part of a course on **Coursera** called _Applied Data Science Capstone_. If you accessed this notebook outside the course, you can take this course online by clicking [here](http://cocl.us/DP0701EN_Coursera_Week3_LAB2).
#
# %% [markdown]
# ## Change Log
#
# | Date (YYYY-MM-DD) | Version | Changed By    | Change Description         |
# | ----------------- | ------- | ------------- | -------------------------- |
# | 2020-11-26        | 2.0     | Lakshmi Holla | Updated the markdown cells |
# |                   |         |               |                            |
# |                   |         |               |                            |
#
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
#
