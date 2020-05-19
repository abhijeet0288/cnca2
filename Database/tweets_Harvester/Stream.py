from StreamDatabase import StreamDatabase
from TwitterAPI.TwitterAPI import TwitterAPI
from TwitterAPI.TwitterError import TwitterConnectionError,TwitterRequestError
import json
import time
from textblob import TextBlob
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from common import *



streamDatabase = StreamDatabase('latestviewtest')

api = TwitterAPI(APIKey, APISecretKey, AccessToken, AccessTokenSecret)

while True:

    try:

        for tweet in api.request('statuses/filter', {'track': '', 'locations': melbourneBoundingBox}):

            if 'text' in tweet:
                print('%s -- %s' % (tweet['user']['screen_name'], tweet['text']))
                print('%s\n' % (tweet['created_at']))

                docid = tweet['id_str']
                docId = tweet['id']
                doctext = tweet['text']
                docCoordinates = tweet['coordinates']
                docUser = tweet['user']
                docTime = tweet['created_at']
                docPlace = tweet['place']
                docentities = tweet['entities']
                sentimentPolarity = TextBlob(tweet['text']).polarity
                if sentimentPolarity > 0:
                    sentiment = "positive"
                elif sentimentPolarity < 0:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"

                
                try:

                    if (docCoordinates is not None):
                        longitude = docCoordinates['coordinates'][0]
                        latitude = docCoordinates['coordinates'][1]
                        point = Point(longitude, latitude)
                        for i in geoLocations.keys():
                            if geoLocations[i]['type'] == 'polygon':
                                if geoLocations[i]['polygon'].contains(point):
                                    suburbId = i
                                    suburb = geoLocations[suburbId]['name']
                            else:
                                for polygon in geoLocations[i]['polygons']:
                                    if polygon.contains(point):
                                        suburbId = i
                                        suburb = geoLocations[suburbId]['name']
                        # return -1
                    else:
                        suburbId = None
                        suburb = None

                except Exception:
                    suburb = None

                doc = {'_id': docid, 'id_str': docid, 'id': docId, 'text': doctext, 'user': docUser,
                    'coordinates': docCoordinates, 'created_at': docTime,
                    'place': docPlace, 'entities': docentities,
                    'addressed': False, 'sentiment': sentiment, 'suburb': suburb}
                streamDatabase.saveTweet(doc)

            elif 'message' in tweet and tweet['code'] == 88:
                time.sleep(950)
                break

            elif 'disconnect' in tweet:
                break 

    except TwitterRequestError as e:
        
        if e.status_code >= 500:
            print ("Temporary Error")
            print ("Trying the request again")
            pass

        else:
            print ("Twitter Request Error")
            print ("Something wrong with the request")
            print(e.status_code)
            raise

    except TwitterConnectionError:
        print ("Twitter Connection Error")
        print ("Trying the request again")
        pass

    except Exception as e:
        print('Hello')
        print (e)
        print (Exception)
        pass

