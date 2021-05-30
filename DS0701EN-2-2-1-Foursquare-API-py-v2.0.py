# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# <a href="https://cognitiveclass.ai"><img src = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs_v1/IDSNlogo.png" width = 400> </a>
#
# <h1 align=center><font size = 5>Learning FourSquare API with Python</font></h1>
#
# %% [markdown]
#
#
# %% [markdown]
# ## Introduction
#
# In this lab, you will learn in details how to make calls to the Foursquare API for different purposes. You will learn how to construct a URL to send a request to the API to search for a specific type of venues, to explore a particular venue, to explore a Foursquare user, to explore a geographical location, and to get trending venues around a location. Also, you will learn how to use the visualization library, Folium, to visualize the results.
#
# %% [markdown]
# ## Table of Contents
#
# 1.  <a href="#item1">Foursquare API Search Function</a>
# 2.  <a href="#item2">Explore a Given Venue</a>
# 3.  <a href="#item3">Explore a User</a>
# 4.  <a href="#item4">Foursquare API Explore Function</a>
# 5.  <a href="#item5">Get Trending Venues</a>
#
# %% [markdown]
# ### Import necessary Libraries
#

# %%
import requests  # library to handle requests
import pandas as pd  # library for data analsysis
import numpy as np  # library to handle data in a vectorized manner
import random  # library for random number generation

# get_ipython().system("pip install geopy")
from geopy.geocoders import (
    Nominatim,
)  # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image
from IPython.core.display import HTML

# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize


# get_ipython().system(" pip install folium==0.5.0")
import folium  # plotting library

print("Folium installed")
print("Libraries imported.")

# %% [markdown]
# ### Define Foursquare Credentials and Version
#
# %% [markdown]
# ##### Make sure that you have created a Foursquare developer account and have your credentials handy
#
# %% [markdown]
# ##### To obtain access token follow these steps.
#
# <br>
#
# 1.  Go to your **"App Settings"** page on the developer console of Foursquare.com
# 2.  Set the **"Redirect URL"** under **"Web Addresses"** to [https://www.google.com](https://www.google.com?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ)
#
#
# 3.  Paste and enter the following url in your web browser **(replace YOUR_CLIENT_ID with your actual client id)**:
#     [https://foursquare.com/oauth2/authenticate?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=https://www.google.com](https://foursquare.com/oauth2/authenticate?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=https://www.google.com&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ)
#
#     This should redirect you to a google page requesting permission to make the connection.
# 4.  Accept and then look at the url of your web browser **(take note at the CODE part of the url to use in step 5)**
#     It should look like [https://www.google.com/?code=CODE](https://www.google.com?code=CODE&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ)
# 5.  Copy the code value from the previous step.
#        Paste and enter the following into your web browser **(replace placeholders with actual values)**:
#     [https://foursquare.com/oauth2/access_token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&redirect_uri=https://www.google.com&code=CODE](https://foursquare.com/oauth2/access_token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&redirect_uri=https://www.google.com&code=CODE&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ).
# 6.  When you paste the link , This should lead you to a page that gives you your **access token**.
#

# %%
CLIENT_ID = "U3B2T3FQDUJHBDYMRZ4555ZTFUPOCOOSUGH0NTTHPWBSF42A"  # your Foursquare ID
CLIENT_SECRET = "UWWQOMEUI2E0XKHK14EWURBEXIZ4MSYHGTTGCSDRSJIXIUDL"  # your Foursquare Secret
ACCESS_TOKEN = "BELMADBNZPCS1LZFHO3TAEZB13MTHWKWZK3WXBQD0N4QDEKK"  # your FourSquare Access Token
VERSION = "20180604"
LIMIT = 30
print("Your credentails:")
print("CLIENT_ID: " + CLIENT_ID)
print("CLIENT_SECRET:" + CLIENT_SECRET)

# %% [markdown]
#
#
# %% [markdown]
# #### Let's again assume that you are staying at the Conrad hotel. So let's start by converting the Contrad Hotel's address to its latitude and longitude coordinates.
#
# %% [markdown]
# In order to define an instance of the geocoder, we need to define a user_agent. We will name our agent <em>foursquare_agent</em>, as shown below.
#

# %%
address = "102 North End Ave, New York, NY"

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)

# %% [markdown]
#
#
# %% [markdown]
# <a id="item1"></a>
#
# %% [markdown]
# ## 1. Search for a specific venue category
#
# > `https://api.foursquare.com/v2/venues/`**search**`?client_id=`**CLIENT_ID**`&client_secret=`**CLIENT_SECRET**`&ll=`**LATITUDE**`,`**LONGITUDE**`&v=`**VERSION**`&query=`**QUERY**`&radius=`**RADIUS**`&limit=`**LIMIT**
#
# %% [markdown]
# #### Now, let's assume that it is lunch time, and you are craving Italian food. So, let's define a query to search for Italian food that is within 500 metres from the Conrad Hotel.
#

# %%
search_query = "Italian"
radius = 500
print(search_query + " .... OK!")

# %% [markdown]
# #### Define the corresponding URL
#

# %%
url = "https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&oauth_token={}&v={}&query={}&radius={}&limit={}".format(
    CLIENT_ID,
    CLIENT_SECRET,
    latitude,
    longitude,
    ACCESS_TOKEN,
    VERSION,
    search_query,
    radius,
    LIMIT,
)
url

# %% [markdown]
# #### Send the GET Request and examine the results
#

# %%
results = requests.get(url).json()
results

# %% [markdown]
# #### Get relevant part of JSON and transform it into a _pandas_ dataframe
#

# %%
# assign relevant part of JSON to venues
venues = results["response"]["venues"]

# tranform venues into a dataframe
dataframe = json_normalize(venues)
dataframe.head()

# %% [markdown]
# #### Define information of interest and filter dataframe
#

# %%
# keep only columns that include venue name, and anything that is associated with location
filtered_columns = (
    ["name", "categories"]
    + [col for col in dataframe.columns if col.startswith("location.")]
    + ["id"]
)
dataframe_filtered = dataframe.loc[:, filtered_columns]

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


# filter the category for each row
dataframe_filtered["categories"] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [
    column.split(".")[-1] for column in dataframe_filtered.columns
]

dataframe_filtered

# %% [markdown]
# #### Let's visualize the Italian restaurants that are nearby
#

# %%
dataframe_filtered.name


# %%
venues_map = folium.Map(
    location=[latitude, longitude], zoom_start=13
)  # generate map centred around the Conrad Hotel

# add a red circle marker to represent the Conrad Hotel
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    color="red",
    popup="Conrad Hotel",
    fill=True,
    fill_color="red",
    fill_opacity=0.6,
).add_to(venues_map)

# add the Italian restaurants as blue circle markers
for lat, lng, label in zip(
    dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories
):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color="blue",
        popup=label,
        fill=True,
        fill_color="blue",
        fill_opacity=0.6,
    ).add_to(venues_map)

# display map
venues_map

# %% [markdown]
#
#
# %% [markdown]
# <a id="item2"></a>
#
# %% [markdown]
# ## 2. Explore a Given Venue
#
# > `https://api.foursquare.com/v2/venues/`**VENUE_ID**`?client_id=`**CLIENT_ID**`&client_secret=`**CLIENT_SECRET**`&v=`**VERSION**
#
# %% [markdown]
# ### A. Let's explore the closest Italian restaurant -- _Harry's Italian Pizza Bar_
#

# %%
venue_id = "4fa862b3e4b0ebff2f749f06"  # ID of Harry's Italian Pizza Bar
url = "https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&oauth_token={}&v={}".format(
    venue_id, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, VERSION
)
url

# %% [markdown]
# #### Send GET request for result
#

# %%
result = requests.get(url).json()
print(result["response"]["venue"].keys())
result["response"]["venue"]

# %% [markdown]
# ### B. Get the venue's overall rating
#

# %%
try:
    print(result["response"]["venue"]["rating"])
except:
    print("This venue has not been rated yet.")

# %% [markdown]
# That is not a very good rating. Let's check the rating of the second closest Italian restaurant.
#

# %%
venue_id = "4f3232e219836c91c7bfde94"  # ID of Conca Cucina Italian Restaurant
url = "https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&oauth_token={}&v={}".format(
    venue_id, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, VERSION
)

result = requests.get(url).json()
try:
    print(result["response"]["venue"]["rating"])
except:
    print("This venue has not been rated yet.")

# %% [markdown]
# Since this restaurant has no ratings, let's check the third restaurant.
#

# %%
venue_id = "3fd66200f964a520f4e41ee3"  # ID of Ecco
url = "https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&oauth_token={}&v={}".format(
    venue_id, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, VERSION
)

result = requests.get(url).json()
try:
    print(result["response"]["venue"]["rating"])
except:
    print("This venue has not been rated yet.")

# %% [markdown]
# Since this restaurant has a slightly better rating, let's explore it further.
#
# %% [markdown]
# ### C. Get the number of tips
#

# %%
result["response"]["venue"]["tips"]["count"]

# %% [markdown]
# ### D. Get the venue's tips
#
# > `https://api.foursquare.com/v2/venues/`**VENUE_ID**`/tips?client_id=`**CLIENT_ID**`&client_secret=`**CLIENT_SECRET**`&v=`**VERSION**`&limit=`**LIMIT**
#
# %% [markdown]
# #### Create URL and send GET request. Make sure to set limit to get all tips
#

# %%
## Ecco Tips
limit = 15  # set limit to be greater than or equal to the total number of tips
url = "https://api.foursquare.com/v2/venues/{}/tips?client_id={}&client_secret={}&oauth_token={}&v={}&limit={}".format(
    venue_id, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, VERSION, limit
)

results = requests.get(url).json()
results

# %% [markdown]
# #### Get tips and list of associated features
#

# %%
tips = results["response"]["tips"]["items"]

tip = results["response"]["tips"]["items"][0]
tip.keys()

# %% [markdown]
# #### Format column width and display all tips
#

# %%
pd.set_option("display.max_colwidth", -1)

tips_df = json_normalize(tips)  # json normalize tips

# columns to keep
filtered_columns = [
    "text",
    "agreeCount",
    "disagreeCount",
    "id",
    "user.firstName",
    "user.lastName",
    "user.id",
]
tips_filtered = tips_df.loc[:, filtered_columns]

# display tips
tips_filtered.reindex()

# %% [markdown]
# Now remember that because we are using a personal developer account, then we can access only 2 of the restaurant's tips, instead of all 15 tips.
#
# %% [markdown]
#
#
# %% [markdown]
# <a id="item3"></a>
#
# %% [markdown]
# ## 3. Search a Foursquare User
#
# > `https://api.foursquare.com/v2/users/`**USER_ID**`?client_id=`**CLIENT_ID**`&client_secret=`**CLIENT_SECRET**`&v=`**VERSION**
#
# %% [markdown]
# ### Define URL, send GET request and display features associated with user
#

# %%
idnumber = "484542633"  # user ID with most agree counts and complete profile

url = "https://api.foursquare.com/v2/users/{}/?client_id={}&client_secret={}&oauth_token={}&v={}".format(
    idnumber, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, VERSION
)  # define URL

# send GET request
results = requests.get(url).json()

user_data = results["response"]["user"]["photos"]["items"]

# results
pd.set_option("display.max_colwidth", -1)

users_df = json_normalize(user_data)
# This mainly used later to display the photo of the user
filtered_columns = ["id", "prefix", "suffix", "width", "height"]
tips_filtered = users_df.loc[:, filtered_columns]
# url
tips_filtered


# %%

g = tips_df.loc[tips_df["user.id"] == "484542633"]
print("First Name: " + tips_df["user.firstName"])
print("Last Name: " + tips_df["user.lastName"])

# %% [markdown]
# ### Retrieve the User's Profile Image
#

# %%
# 1. grab prefix of photo
# 2. grab suffix of photo
# 3. concatenate them using the image size
Image(
    url="https://fastly.4sqi.net/img/general/540x920/484542633_ELnUC1di2LwJTjPi04McysQZNqJHSCCSxS3i_GKGTEY.jpg"
)

# %% [markdown]
# Wow! So it turns out that Nick is a very active Foursquare user, with more than 250 tips.
#
# %% [markdown]
# ### Get User's tips
#

# %%
# define tips URL
user_id = "484542633"
url = "https://api.foursquare.com/v2/users/{}/tips?client_id={}&client_secret={}&oauth_token={}&v={}&limit={}".format(
    user_id, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, VERSION, limit
)

# send GET request and get user's tips
results = requests.get(url).json()
tips = results["response"]["tips"]["items"]

# format column width
pd.set_option("display.max_colwidth", -1)

tips_df = json_normalize(tips)

# filter columns
filtered_columns = ["text", "agreeCount", "disagreeCount", "id"]
tips_filtered = tips_df.loc[:, filtered_columns]

# display user's tips
tips_filtered

# %% [markdown]
# #### Let's get the venue for the tip with the greatest number of agree counts
#

# %%
tip_id = "5ab5575d73fe2516ad8f363b"  # tip id

# define URL
url = "https://api.foursquare.com/v2/users/{}/tips?client_id={}&client_secret={}&oauth_token={}&v={}".format(
    idnumber, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, VERSION
)  # define URL


# send GET Request and examine results
result = requests.get(url).json()
print(result["response"]["tips"]["items"][0]["venue"]["name"])
print(result["response"]["tips"]["items"][0]["venue"]["location"])

# %% [markdown]
# ## 4. Explore a location
#
# > `https://api.foursquare.com/v2/venues/`**explore**`?client_id=`**CLIENT_ID**`&client_secret=`**CLIENT_SECRET**`&ll=`**LATITUDE**`,`**LONGITUDE**`&v=`**VERSION**`&limit=`**LIMIT**
#
# %% [markdown]
# #### So, you just finished your gourmet dish at Ecco, and are just curious about the popular spots around the restaurant. In order to explore the area, let's start by getting the latitude and longitude values of Ecco Restaurant.
#

# %%
latitude = 40.715337
longitude = -74.008848

# %% [markdown]
# #### Define URL
#

# %%
url = "https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}".format(
    CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, radius, LIMIT
)
url

# %% [markdown]
# #### Send GET request and examine results
#

# %%
import requests


# %%
results = requests.get(url).json()
"There are {} around Ecco restaurant.".format(
    len(results["response"]["groups"][0]["items"])
)

# %% [markdown]
# #### Get relevant part of JSON
#

# %%
items = results["response"]["groups"][0]["items"]
items[0]

# %% [markdown]
# #### Process JSON and convert it to a clean dataframe
#

# %%
dataframe = json_normalize(items)  # flatten JSON

# filter columns
filtered_columns = (
    ["venue.name", "venue.categories"]
    + [col for col in dataframe.columns if col.startswith("venue.location.")]
    + ["venue.id"]
)
dataframe_filtered = dataframe.loc[:, filtered_columns]

# filter the category for each row
dataframe_filtered["venue.categories"] = dataframe_filtered.apply(
    get_category_type, axis=1
)

# clean columns
dataframe_filtered.columns = [col.split(".")[-1] for col in dataframe_filtered.columns]

dataframe_filtered.head(10)

# %% [markdown]
# #### Let's visualize these items on the map around our location
#

# %%
venues_map = folium.Map(
    location=[latitude, longitude], zoom_start=15
)  # generate map centred around Ecco


# add Ecco as a red circle mark
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    popup="Ecco",
    fill=True,
    color="red",
    fill_color="red",
    fill_opacity=0.6,
).add_to(venues_map)


# add popular spots to the map as blue circle markers
for lat, lng, label in zip(
    dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories
):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        fill=True,
        color="blue",
        fill_color="blue",
        fill_opacity=0.6,
    ).add_to(venues_map)

# display map
venues_map

# %% [markdown]
#
#
# %% [markdown]
# <a id="item5"></a>
#
# %% [markdown]
# ## 5. Explore Trending Venues
#
# > `https://api.foursquare.com/v2/venues/`**trending**`?client_id=`**CLIENT_ID**`&client_secret=`**CLIENT_SECRET**`&ll=`**LATITUDE**`,`**LONGITUDE**`&v=`**VERSION**
#
# %% [markdown]
# #### Now, instead of simply exploring the area around Ecco, you are interested in knowing the venues that are trending at the time you are done with your lunch, meaning the places with the highest foot traffic. So let's do that and get the trending venues around Ecco.
#

# %%
# define URL
url = "https://api.foursquare.com/v2/venues/trending?client_id={}&client_secret={}&ll={},{}&v={}".format(
    CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION
)

# send GET request and get trending venues
results = requests.get(url).json()
results

# %% [markdown]
# ### Check if any venues are trending at this time
#

# %%
if len(results["response"]["venues"]) == 0:
    trending_venues_df = "No trending venues are available at the moment!"

else:
    trending_venues = results["response"]["venues"]
    trending_venues_df = json_normalize(trending_venues)

    # filter columns
    columns_filtered = ["name", "categories"] + [
        "location.distance",
        "location.city",
        "location.postalCode",
        "location.state",
        "location.country",
        "location.lat",
        "location.lng",
    ]
    trending_venues_df = trending_venues_df.loc[:, columns_filtered]

    # filter the category for each row
    trending_venues_df["categories"] = trending_venues_df.apply(
        get_category_type, axis=1
    )


# %%
# display trending venues
trending_venues_df

# %% [markdown]
# Now, depending on when you run the above code, you might get different venues since the venues with the highest foot traffic are fetched live.
#
# %% [markdown]
# ### Visualize trending venues
#

# %%
if len(results["response"]["venues"]) == 0:
    venues_map = (
        "Cannot generate visual as no trending venues are available at the moment!"
    )

else:
    venues_map = folium.Map(
        location=[latitude, longitude], zoom_start=15
    )  # generate map centred around Ecco

    # add Ecco as a red circle mark
    folium.CircleMarker(
        [latitude, longitude],
        radius=10,
        popup="Ecco",
        fill=True,
        color="red",
        fill_color="red",
        fill_opacity=0.6,
    ).add_to(venues_map)

    # add the trending venues as blue circle markers
    for lat, lng, label in zip(
        trending_venues_df["location.lat"],
        trending_venues_df["location.lng"],
        trending_venues_df["name"],
    ):
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            poup=label,
            fill=True,
            color="blue",
            fill_color="blue",
            fill_opacity=0.6,
        ).add_to(venues_map)


# %%
# display map
venues_map

# %% [markdown]
# <a id="item6"></a>
#
# %% [markdown]
#
#
# %% [markdown]
# ### Thank you for completing this lab!
#
# This notebook was created by [Alex Aklson](https://www.linkedin.com/in/aklson?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ). I hope you found this lab interesting and educational. Feel free to contact me if you have any questions!
#
# This notebook modified by Nayef Abou Tayoun ([https://www.linkedin.com/in/nayefaboutayoun/](https://www.linkedin.com/in/nayefaboutayoun?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork-21253531&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ))
#
# %% [markdown]
# This notebook is part of a course on **Coursera** called _Applied Data Science Capstone_. If you accessed this notebook outside the course, you can take this course online by clicking [here](http://cocl.us/DP0701EN_Coursera_Week2_LAB1).
#
# %% [markdown]
# ## Change Log
#
# | Date (YYYY-MM-DD) | Version | Changed By    | Change Description                           |
# | ----------------- | ------- | ------------- | -------------------------------------------- |
# | 2021-03-17        | 2.1     | Lakshmi Holla | Changed the code for retreiving user profile |
# | 2020-11-26        | 2.0     | Lakshmi Holla | Updated the markdown cells                   |
# |                   |         |               |                                              |
# |                   |         |               |                                              |
#
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
#
