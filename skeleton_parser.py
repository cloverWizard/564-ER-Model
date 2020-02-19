
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub
import os

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

table_names = ["Item", "Category", "User", "Belong", "Sell", "Bid"]
"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def handle_string_maybe_with_quote(literal):
    # print(literal)
    literal = literal.replace('"', '""')
    return f'"{literal}"'


# ItemId, Name, Description, Currently, Buy_Price, First_Bid, Number_of_Bids
def get_item_tuple(item):
    string_key_names = ['ItemID', 'Name', 'Description']
    monetary_key_names = ['Currently', 'Buy_Price','First_Bid']
    # date_key_names = []
    int_key_names = ['Number_of_Bids']
    values = []
    for key in string_key_names:
        if not (key in item) or item[key]==None:
            values.append("NULL")
        else:
            values.append(handle_string_maybe_with_quote(item[key]))
    for key in monetary_key_names:
        if not (key in item) or item[key]==None:
            values.append(str(-1))
        else:
            values.append(transformDollar(item[key]))
    for key in int_key_names:
        if not (key in item) or item[key]==None:
            values.append(str(-1))
        else:
            values.append(str(item[key]))
    return "|".join(values)

# Format: Category
def get_category_tuples(item):
    key = 'Category'
    values = []
    if key in item and item[key] is not None:
        for category_name in item[key]:
            values.append(handle_string_maybe_with_quote(category_name))
    return "\n".join(values)

# Format: UserID, Location, Country, Rating
def get_bidder_tuple(bidder):
    string_key = ['UserID', 'Location', 'Country']
    float_key = 'Rating'
    bidder_values = []
    for key in string_key:
        if not (key in bidder) or bidder[key] == None:
            bidder_values.append("NULL")
        else:
            bidder_values.append(handle_string_maybe_with_quote(bidder[key])) 
            
    if not (float_key in bidder) or bidder[float_key] == None:
        bidder_values.append(str(-1))
    else:
        bidder_values.append(str(bidder[float_key]))
    bidder_tuple = "|".join(bidder_values)
    return bidder_tuple

# Format: UserID, Location, Country, Rating
def get_seller_tuple(item):
    seller = item["Seller"]
    seller_id = handle_string_maybe_with_quote(seller['UserID'])
    seller_location = handle_string_maybe_with_quote(item['Location'])
    seller_country = handle_string_maybe_with_quote(item['Country'])
    seller_rating = str(seller['Rating'])
    seller_tuple = f'{seller_id}|{seller_location}|{seller_country}|{seller_rating}'
    return seller_tuple

# Format: ItemId, CategoryName
def get_belong_tuples(item):
    item_ID = item['ItemID']
    key = 'Category'
    values = []
    if key in item and item[key] is not None:
        for category_name in item[key]:
            values.append(f'{item_ID}|{handle_string_maybe_with_quote(category_name)}')
    return "\n".join(values)

# Format: ItemID, SellerID, Started, Ends
def get_sell_tuple(item):
    item_ID = item['ItemID']
    sell_user_ID = item['Seller']['UserID']
    start = transformDttm(item['Started'])
    end = transformDttm(item['Ends'])
    return f'{item_ID}|{sell_user_ID}|{start}|{end}'
    
# Format: ItemID, BidderID, Time, Amount
def get_bid_tuple(item_ID, bid):
    time = transformDttm(bid['Time'])
    amount = transformDollar(bid['Amount'])
    bidder_ID = bid['Bidder']['UserID']
    return f'{item_ID}|{bidder_ID}|{time}|{amount}'

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    handlers = {}
    for name in table_names:
        path = os.path.join('dat', f'Raw{name}.dat')
        handlers[name] = open(path, "a")
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            handlers['Item'].write(get_item_tuple(item) + "\n")
            handlers['Category'].write(get_category_tuples(item) + "\n")
            handlers['User'].write(get_seller_tuple(item) + "\n")
            handlers['Belong'].write(get_belong_tuples(item) + "\n")
            handlers['Sell'].write(get_sell_tuple(item) + "\n")
            if 'Bids' in item and item['Bids'] is not None:
                for bid in item['Bids']:
                    handlers['User'].write(get_bidder_tuple(bid['Bid']['Bidder']) + "\n")
                    handlers['Bid'].write(get_bid_tuple(item['ItemID'], bid['Bid']) + "\n")
    for name in table_names:
        handlers[name].close()

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    for name in table_names:
        path = os.path.join('dat', f'Raw{name}.dat')
        if os.path.exists(path):
            os.remove(path)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
