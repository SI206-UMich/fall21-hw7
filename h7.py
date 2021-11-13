import unittest
import sqlite3
import json
import os

#
# Name:
# Who did you work with:
#

def readDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCategoriesTable(data, cur, conn):
    category_list = []
    for business in data['businesses']:
        business_categories = business['categories']
        for category in business_categories:
            if category['title'] not in category_list:
                category_list.append(category['title'])

    cur.execute("DROP TABLE IF EXISTS Categories")
    cur.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(category_list)):
        cur.execute("INSERT INTO Categories (id,title) VALUES (?,?)",(i,category_list[i]))
    conn.commit()

def setUpRestaurantTable(data, cur, conn):
    ## [TASK 1]: 25 points
    # Finish the function setUpRestaurantTable
    # Iterate through the JSON data to get a list of restaurants
    # Load all of the restaurants into a database table called Restaurants, with the following columns in each row:
    # restaurant_id (datatype: text; primary key)
    # name (datatype: text)
    # address (datatype: text)
    # zip_code (datatype: text)
    # category_id (datatype: integer)
    # rating (datatype: real)
    # review_count (datatype: integer)
    # price (datatype: text)
    pass


def getRestaurantsByZip(zip_code, cur, conn):
    ## [TASK 2]: 10 points
    # The function takes 3 arguments as input: a zip code
    # the database cursor, and database connection object.  
    # It selects all the restaurants of a particular zip code 
    # and returns a list of tuples. Each tuple contains 
    # the restaurant name, restaurant address, and restaurant zip code.
    pass


def getRestaurantsByZipcodeAboveRatingAndByPrice(zip_code, rating, price, cur, conn):
    ## [TASK 3]: 10 points
    # The function takes 5 arguments as input: the zip_code value,
    # the rating value, the price, the database cursor, and database connection object.
    # It selects all the restaurants at the zip_code passed to the function 
    # and at ratings bigger than or equal to the rating passed to the function 
    # and of a particular price and returns a list of tuples.
    # Each tuple in the list contains the restaurant name, restaurant address, restaurant rating, and restaurant price.
    pass



def getRestaurantsAboveRatingAboveReviewsOfCategory(rating, review_count, category, cur, conn):
    ## [TASK 4]: 15 points
    # The function takes 5 arguments as input:a rating, a review_count, a category, the database cursor,
    # and database connection object. It selects all restaurants at a category 
    # and at ratings greater than or equal to the rating passed to the function,
    # and at review_counts greater than or equal to the review_count passed to the function.
    # It returns a list of tuples, each tuple containing the
    # restaurant name, restaurant address, restaurant rating, and restaurant review_count.
    # Note: You have to use JOIN for this task.
    pass



def getRestaurantsOfType(price, rating, category, cur, conn):
    # [EXTRA CREDIT]
    # This function takes in 5 parameters: price, rating, category,
    # the database cursor, and database connection object. It returns
    # a list of all of the restaurant names that match the price, are
    # greater than or equal to that rating, and match that category.
    pass



class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'restaurants.db')
        self.cur = self.conn.cursor()
        self.data = readDataFromFile('yelp_data.txt')

    def test_businesses_table(self):
        self.cur.execute('SELECT * from Restaurants')
        resturant_list = self.cur.fetchall()
        self.assertEqual(len(resturant_list), 50)
        self.assertEqual(len(resturant_list[0]),8)
        self.assertIs(type(resturant_list[0][0]), str)
        self.assertIs(type(resturant_list[0][1]), str)
        self.assertIs(type(resturant_list[0][2]), str)
        self.assertIs(type(resturant_list[0][3]), str)
        self.assertIs(type(resturant_list[0][4]), int)
        self.assertIs(type(resturant_list[0][5]), float)
        self.assertIs(type(resturant_list[0][6]), int)
        self.assertIs(type(resturant_list[0][7]), str)

    def test_restaurants_by_zip(self):
        x = sorted(getRestaurantsByZip('48198', self.cur, self.conn))
        self.assertEqual(len(x),3)
        self.assertEqual(x[0][0],"Aubree's Pizzeria & Grill")

        y = sorted(getRestaurantsByZip('48197', self.cur, self.conn))
        self.assertEqual(len(y),3)
        self.assertEqual(y[2][0],"Mr Pizza")
        self.assertEqual(y[1][1],"1783 Washtenaw Rd, Ypsilanti")

        z = sorted(getRestaurantsByZip('48103', self.cur, self.conn))
        self.assertEqual(z[0][0],"Aamani's Smokehouse & Pizza")
        self.assertEqual(len(getRestaurantsByZip('48103', self.cur, self.conn)),7)
        self.assertEqual(z[1][2],"48103")

    def test_restaurants_by_zipcode_above_rating_by_price(self):

        z = getRestaurantsByZipcodeAboveRatingAndByPrice('48104', 4.0, '$', self.cur, self.conn)
        self.assertEqual(len(z),3)
        self.assertEqual(z[2][1],"1956 S Industrial Hwy, Ann Arbor")
        self.assertEqual(z[0][0],"NeoPapalis")

        self.assertEqual(len(getRestaurantsByZipcodeAboveRatingAndByPrice('48103', 5.0, '$', self.cur, self.conn)),0)

        a = sorted(getRestaurantsByZipcodeAboveRatingAndByPrice('48108', 3.0, '$$', self.cur, self.conn))
        self.assertEqual(len(a),2)
        self.assertEqual(a[0][3], "$$")
        self.assertEqual(a[1][2], 4.5)

        self.assertEqual(len(getRestaurantsByZipcodeAboveRatingAndByPrice('48104', 4.5, '$', self.cur, self.conn)[0]),4)


    def test_restaurants_above_rating_above_reviews_of_category(self):
 
        b = sorted(getRestaurantsAboveRatingAboveReviewsOfCategory(4.0, 100, "Salad", self.cur, self.conn))
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0][0], "NeoPapalis")

        c = sorted(getRestaurantsAboveRatingAboveReviewsOfCategory(3.0, 200, "Breweries", self.cur, self.conn))
        self.assertEqual(len(c), 3)
        self.assertEqual(c[2][1], "120 W Washington St, Ann Arbor")

        d = sorted(getRestaurantsAboveRatingAboveReviewsOfCategory(3.5, 50, "Pizza", self.cur, self.conn))
        print(d)
        self.assertEqual(len(d), 11)
        self.assertEqual(d[2][0], "Buddy's Pizza - Ann Arbor")
        self.assertEqual(d[8][3], 260)
        self.assertEqual(d[10][2], 3.5)

        e = sorted(getRestaurantsAboveRatingAboveReviewsOfCategory(5.0, 100, "Bakeries", self.cur, self.conn))
        self.assertEqual(len(e), 0)


    def test_restaurants_of_type_extra_credit(self):
        e = sorted(getRestaurantsOfType("$$", 4.0, "Pizza", self.cur, self.conn))
        self.assertEqual(len(e), 3)
        self.assertEqual(e[2][0], 'Red Rooster Pizzeria')

        f = getRestaurantsOfType("$$$$", 3.5, "Chicken Wings", self.cur, self.conn)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0][0], 'Wings N Things')

        ## Add your own stests below. Do not change anything about the above tests
        # Write at least 3 assert statements.


def main():
    json_data = readDataFromFile('yelp_data.txt')
    cur, conn = setUpDatabase('restaurants.db')
    setUpCategoriesTable(json_data, cur, conn)
    setUpRestaurantTable(json_data, cur, conn)

    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
