from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def __get_meters__(m):
    return str(float(m)*1609.344)

def __get_miles__(m):
    return str(round(float(m)/1609.344))

def __build_query__(location, term, radius, offset=False):  # Builds queries to fetch restaurant data
    if not offset:
        query = '{search (location: "' + location + '", term: "' + term \
                + '", radius: ' + radius + ', sort_by: "rating", limit: 30) {'
    else:
        query = '{search (location: "' + location + '", term: "' + term + '", offset:' \
                + str(offset) + ', sort_by: "rating" open_now: true, limit: 30) {'

    query += ' total business{id name rating price distance}}}'

    return gql(query)

# iterates through data and collects restaurants with 4.5 stars or greater
def __select_tasty_spots__(data, collection=[]):
    for restaurant in data['business']:
        if len(collection) >= 7:
            break
        if restaurant['rating'] >= 4.5:
            m = __get_miles__(restaurant['distance'])
            collection.append([restaurant['id'], restaurant['name'], restaurant['rating'], restaurant['price'], m])

    return collection, data['total']


class API:
    def __init__(self):  # Initialize object by connecting to API
        apiKey = 'Yelp Token Here'

        _transport = RequestsHTTPTransport(url='https://api.yelp.com/v3/graphql', use_json=True, )
        _transport.headers = {"User-Agent": "Mozilla/5.0 (X11; buntu; "
                                            + "Linux x86_64; rv:58.0) Gecko/0100101 Firefox/58.0",
                              "Authorization": "Bearer {}".format(apiKey), "content-type": "application/json", }

        self.client = Client(transport=_transport, fetch_schema_from_transport=True, )

    # request information from Yelps API and parses it to return a list of restaurants
    def getRestaurants(self, location, term, radius):
        meters = __get_meters__(radius[0])
        query = __build_query__(location, term, meters)

        try:
            restaurants, total = __select_tasty_spots__(self.client.execute(query)['search'])
            offset = 0
        except Exception:
            return 0, 0

        while len(restaurants) < 7 and (offset + 30) < total:
            offset += 30
            try:
                query = __build_query__(location, term, meters, offset)
                restaurants, total = __select_tasty_spots__(self.client.execute(query)['search'], restaurants)
            except Exception:
                return restaurants, 1

        return restaurants, 1

    #retrieves information for 1 restaurant from the API
    def getFinerDetails(self, id):
        query = gql('{business (id: "' + id + '"){name price rating location{address1 city state postal_code} '
                    + 'reviews{text} review_count hours{open{start end day}} categories{title alias}}}')

        return self.client.execute(query)['business']
