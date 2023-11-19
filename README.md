# IBMDataScience-Capstone
**Capstone Assignment:** In this capstone, you will take the role of a data scientist working for a new rocket company, SpaceY, that would like to compete with SpaceX founded by Billionaire industrialist Allon Musk. Your job is to determine the price of each launch. You will do this by gathering information about SpaceX and creating dashboards for your team. You will also determine if SpaceX will reuse the first stage. Instead of using rocket science to determine if the first stage will land successfully, you will train a machine learning model and use public information to predict if SpaceX will reuse the first stage.

## Collecting the Data
Data will be collected using the SpaceX REST API. Specfically, https://api.spacexdata.com/v4/ and will reference the specific end points _/capsules_, _/cores_, _/launch/past_, _/rockets_, _/launches_, _/payloads_.

### Data Collection Processes
**Calling API**
url = "https://api.spacexdata.com/v4/launch/past"
response = requests.get(url)
response.json()
data = pd.json_normalize(response.json())

**Webscraping**
We will be using BeautifulSoup for scraping data from popular wiki pages. Once collected, the data will need to be parsed and put into a Panda's dataframe for further analysis.

### Data Wrangling
The data will need to be cleaned and entries will need to be prep'd for analysis. We will need to deal with null values and search using further API endpoints, via the rocket identification number.
