from collections import Counter
import sqlite3
import os
from math import ceil
import datetime
import time


def leap_year(year):
    """
    checks year parameter to see if the given year is a leap year.

    :param year: accepts INT between 0-9999
    :return: BOOLEAN True or False
    """
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True


def before_at(dy=0, mn=0, yr=0):
    """
    accepts day month and year parameters to output the given date

    :param dy: desired day 1-31 INT
    :param mn: desired month 1-12 INT
    :param yr: desired year 0-9999 INT
    :return: returns changed DATE object
    """
    now = datetime.date.today()
    return now.replace(year=yr, month=mn, day=dy)


def week_of_month(dt):
    """
    Accepts a date time and calculates the week of the month

    :param dt: accepts datetime or date format
    :return: returns the week of the month in INT from 1-5
    """
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))


def find_average(data):
    """
    averages total amounts from database dumps

    :param data: accepts multi-dimensional iterable data type
    :return: returns the average in a FLOAT
    """
    total = 0
    amount = len(data)
    for entry in data:
        total += entry[0]
    average = total / amount
    return round(average, 2)


def summing_it(data):
    """
    Calculates sum of database dumps

    :param data: accepts multi-dimensional iterable data type
    :return: returns total amount in a FLOAT
    """
    if data is None:
        print("Something's gone horribly wrong.")
        return 0
    total = 0
    for entry in data:
        total += entry[0]
    return round(total, 2)


def parse_by_category(category, data):
    """
    filters database content by category from dumps

    :param category: accepts string
    :param data: accepts multi-dimensional iterable data type
    :return: returns filtered multi-dimensional LIST containing TUPLES
    """
    new_dat = []
    for entry in data:
        if entry[1] == category:
            new_dat.append(entry)
    return new_dat


def parse_by_year(year, data):
    """
    filters database content by year from dumps

    :param year: accepts INT from 0-9999
    :param data: accepts multi-dimensional iterable data type
    :return: returns filtered multi-dimensional LIST containing TUPLES
    """
    new_dat = []
    for entry in data:
        date = datetime.datetime.strptime(entry[3], "%Y-%m-%d")
        if date.year == year:
            new_dat.append(entry)
    return new_dat


def parse_by_month(month, data):
    """
    filters database content by month from dumps

    :param month: accepts INT from 1-12
    :param data: accepts multi-dimensional iterable data type
    :return: returns filtered multi-dimensional LIST containing TUPLES
    """
    new_dat = []
    for entry in data:
        date = datetime.datetime.strptime(entry[3], "%Y-%m-%d")
        if date.month == month:
            new_dat.append(entry)
    return new_dat


def parse_by_week_of_month(week, data):
    """
    filters data by week of the month

    :param week: accepts INT from 1-5
    :param data: accepts multi-dimensional iterable data type
    :return: returns filtered multi-dimensional LIST containing TUPLES
    """
    new_dat = []
    for entry in data:
        date = datetime.datetime.strptime(entry[3], "%Y-%m-%d")
        if week_of_month(date) == week:
            new_dat.append(entry)
    return new_dat


def category_breakdown(data):
    """
    takes iterable data type (raw database dumps) and analyzes the categories and the amount of instances of each

    :param data: accepts multi-dimensional iterable data type
    :return: DICTIONARY of CATEGORY as STR: NUMBER OF INSTANCES in INT for all the categories in the original iterable
    """
    categories = []
    for entry in data:
        categories.append(entry[1])
    cat_set = set(categories)
    cat_amount = Counter(categories)
    cat_dict = {}
    for word in cat_set:
        new_dic = {word: cat_amount[word]}
        cat_dict.update(new_dic)
    return cat_dict


def compare_month_year_diff_averages(monthly, yearly):
    """
    Compares two sets of iterable data types which contain categories and category averages and determines which
    is greater or if they are the same and outputs a new list with the difference between the two.

    :param monthly: accepts multi-dimensional iterable data type
    :param yearly: accepts multi-dimensional iterable data type
    :return: returns a LIST containing LISTS containing 3 indexes which are category in STR format,
            the difference between the monthly and yearly average in FLOAT,
            and a STR which indicates if the monthly average is higher, lower or the same as the yearly average.
    """
    new_dat = []
    counter = 0
    for entry in monthly:
        if entry[1] > yearly[counter][1]:
            diff = round(entry[1] - yearly[counter][1], 2)
            new_dat.append([entry[0], diff, "above"])
        elif entry[1] < yearly[counter][1]:
            diff = round(yearly[counter][1] - entry[1], 2)
            new_dat.append([entry[0], diff, "below"])
        elif entry[1] == yearly[counter][1]:
            new_dat.append([entry[0], entry[1], "and it is the same as"])
        counter += 1
    return new_dat


def final_data_display(data):
    """
    function for displaying formatted database information to the user.

    :param data: accepts multi-dimensional iterable data type
    :return: returns nothing, displays data via print
    """
    for entry in data:
        print("\n Amount: ${}\n Category: {}\n Note: {}\n Date: {}".format(entry[0], entry[1], entry[2], entry[3]))
        time.sleep(.5)
    total = summing_it(data)
    print()
    print("Total amount spent: $" + str(total))
    time.sleep(.5)


def category_display_and_choice():
    """
    function that displays a menu of the available categories to the user and forces them to choose one.

    :return: returns the user's choice of category in STR format
    """
    categories = user.grab_categories()
    print("Please choose a category by number. The Categories are: ")
    counter = 1
    for entry in categories:
        print(str(counter) + ". " + entry)
        counter += 1
    while True:
        try:
            choice_category = int(input("Please choose a category by number [1, 2 etc]: "))
            if choice_category in range(1, counter):
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")
    return categories[choice_category - 1]


def user_input_year():
    """
    Function for coercing proper date value from the user

    :return: returns an INT between 0 and 9999
    """
    while True:
        try:
            year = int(input("Please choose a year [0-9999]: "))
            if year in range(0, 10000):
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")
    return year


def user_input_month():
    """
    Function for coercing proper date value from the user

    :return: returns an INT between 1 and 12
    """
    while True:
        try:
            month = int(input("Please choose a month [1-12]: "))
            if month in range(1, 13):
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")
    return month


def user_input_day(month, year):
    """
        Function for coercing proper day, date value from the user

    :param month: accepts an INT between 1 and 12
    :param year: accepts an INT between 0 and 9999
    :return: returns an INT between 1 and 31
    """
    is_leap_year = leap_year(year)
    while True:
        try:
            day = int(input("Please choose a day [1-31]: "))
            if day == 31 and (month == 4 or month == 6 or month == 9 or month == 11):
                print("Wait a second...That month doesn't have a 31st day...Let's try again")
                continue
            elif month == 2 and day > 28:
                if is_leap_year and day == 29:
                    break
                else:
                    print("Wait, how many days are in February again?")
                    continue
            if day in range(1, 31):
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")
    return day


def user_input_week():
    """
    Function for coercing proper date value from the user

    :return: returns an INT between 1-5
    """
    while True:
        try:
            week = int(input("Please choose a week [1-5]: "))
            if week in range(1, 6):
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")
    return week


def view_func(arg=""):
    """
    function mainly for displaying data to the end-user in the menu. The argument passed to the function determines
    which variables the user is prompted for and conversely the granularity of the data sorted.

    :param arg: week or month, hard-coded in the menu functions
    :return: returns nothing data is displayed via print
    """
    year = user_input_year()
    raw_data = parse_by_year(year, user.grab_data())
    if arg == "month" or arg == "week":
        month = user_input_month()
        raw_data = parse_by_month(month, raw_data)
        if arg == "week":
            week = user_input_week()
            raw_data = parse_by_week_of_month(week, raw_data)
    while True:
        try:
            choose_category = input("Would you like to see the expenses for a specific category? [y/n]: ")
            if choose_category.lower() == "y" or choose_category.lower() == "n":
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")

    if choose_category.lower() == "y":
        chosen_category = category_display_and_choice()
        display_data = parse_by_category(chosen_category, raw_data)
        if len(display_data) == 0:
            print()
            print("I'm sorry Dave, There doesn't appear to be any entries for the chosen category in the date range.")
            time.sleep(.5)
        final_data_display(display_data)

    elif choose_category.lower() == "n":
        if len(raw_data) == 0:
            print()
            print("I'm sorry Dave, There doesn't appear to be any entries for the chosen date range.")
            time.sleep(.5)
        final_data_display(raw_data)


class User:
    started = False

    def __init__(self, username):
        """
        Initializes a user object and creates a database file with username argument if one doesn't already exist.

        :param username: will be used for filename of database
        """
        if not os.path.exists(username.capitalize() + ".db"):
            try:
                # Create table
                conn = sqlite3.connect(username.capitalize() + ".db")
                c = conn.cursor()
                sql = '''CREATE TABLE EXPENSES (AMOUNT integer, CATEGORY text, NOTE text, DATE date)'''
                c.execute(sql)
                c.close()
            except sqlite3.OperationalError or ConnectionError as e:
                print(e)
                User(input("Please try again.\nPlease enter your name"))

        # creates properties for database connection and a changes the started variable which is necessary to break
        #   the while loop prompting the user for a username in the main control flow of the program
        try:
            self.user_db = sqlite3.connect(username.capitalize() + ".db")
            self.c = self.user_db.cursor()
            self.started = True
        except sqlite3.OperationalError or ConnectionError as e:
            print(e)
            print("Please try again")

    def log_current_expenses(self, amount, category, note=""):
        """
        Accepts parameters and commits them to DB file

        :param amount: Dollar amount in INT/FLOAT
        :param category: Expense category in STR
        :param note: Optional message in STR
        :return: returns nothing, commits info to database
        """

        date = datetime.date.today()
        sql = """INSERT INTO EXPENSES VALUES ({},'{}','{}','{}');""".format(amount, category.capitalize(), note, date)
        try:
            self.c.execute(sql)
            self.user_db.commit()
            print("Success!")
            time.sleep(.5)
            print()
        except sqlite3.OperationalError:
            print("ERROR, You broke something, please try again.")
            time.sleep(1.5)

    def log_previous_expenses(self, amount, category, day, month, year, note=""):
        """
        Accepts additional date parameters to backdate expenses and commits them to DB file.

        :param amount: Dollar amount in INT
        :param category: Expense category in STR
        :param day: day expense was incurred in INT
        :param month: month expense was incurred in INT
        :param year: year expense was incurred in INT
        :param note: Optional message in STR
        :return: returns nothing, commits info to database
        """
        date = before_at(day, month, year)
        sql = """INSERT INTO EXPENSES VALUES ({},'{}','{}','{}');""".format(amount, category.capitalize(), note, date)
        try:
            self.c.execute(sql)
            self.user_db.commit()
            print("Success!")
            time.sleep(.5)
            print()
        except sqlite3.OperationalError:
            print(print("ERROR, You broke something, please try again."))

    def grab_data(self, category=None):
        """
        grabs either all data from table or all data from a specific category if specified

        :param category: accepts STR
        :return: returns multi-dimensional iterable data type of LIST containing TUPLES
        """
        if category:
            sql = """SELECT * FROM EXPENSES WHERE CATEGORY = '{}'""".format(category)
        else:
            sql = """SELECT * FROM EXPENSES"""
        self.c.execute(sql)
        result = self.c.fetchall()
        return result

    def grab_categories(self):
        """
        function that takes all table entries and returns a list of categories.

        :return: returns a LIST with all the categories present in the database
        """
        data = category_breakdown(self.grab_data())
        categories = []
        for entry in data:
            categories.append(entry)
        return categories

    def yearly_avg(self, year=datetime.date.today().year):
        """
        Will calculate the yearly average transaction amount,
        if no year is specified current year will be selected

        :param year: accepts INT from 0-9999
        :return: returns average as a FLOAT
        """
        raw_dat = parse_by_year(year, self.grab_data())
        return find_average(raw_dat)

    def monthly_avg(self, month=datetime.date.today().month):
        """
        Will calculate the monthly average transaction amount,
        if no month is specified current year will be selected

        :param month: accepts INT from 1-12
        :return: returns average as a FLOAT
        """
        raw_dat = parse_by_month(month, self.grab_data())
        return find_average(raw_dat)

    def category_avg(self, category, data=None):
        """
        Will calculate the category average transaction amount,
        optional data allows for subbing in parsed iterable data.

        :param category: accepts STR
        :param data: OPTIONAL accepts multi-dimensional iterable data type
        :return: returns average as a FLOAT
        """
        if data is None:
            data = self.grab_data()

        raw_dat = parse_by_category(category, data)
        return find_average(raw_dat)

    def monthly_category_percentages(self, category, month=datetime.date.today().month):
        """
        analyzes categories for a given month (if no month is specified then the current month is used) and determines
        the percentage of spending in each category relative to the total amount spent for the month

        :param category: accepts multi-dimensional iterable data type
        :param month: Optional accepts month as INT between 1-12
        :return: returns a DICTIONARY where KEY:VALUE = Category as STR: Percentage as FLOAT
        """
        raw_dat = None
        category_list = []
        for word in category:
            category_list.append(word)
        total_amount_spent = summing_it(parse_by_month(month, self.grab_data()))
        averages = {}
        for entry in category_list:
            sql = """SELECT * FROM EXPENSES WHERE CATEGORY = '{}'""".format(entry)
            try:
                self.c.execute(sql)
                raw_dat = parse_by_month(month, self.c.fetchall())
            except sqlite3.OperationalError or ConnectionError:
                print("ERROR, You broke something, please try again.")
            cat_total = summing_it(raw_dat)
            avg = round((cat_total / total_amount_spent) * 100, 2)
            av_add = {entry: avg}
            averages.update(av_add)
        return averages

    def yearly_category_percentages(self, category, year=datetime.date.today().year):
        """
        analyzes categories for a given year (if no year is specified then the current year is used) and determines
        the percentage of spending in each category relative to the total amount spent for the year

        :param category: accepts multi-dimensional iterable data type
        :param year: Optional accepts month as INT between 0-9999
        :return: returns a DICTIONARY where KEY:VALUE = Category as STR: Percentage as FLOAT
        """
        raw_dat = None
        category_list = []
        for word in category:
            category_list.append(word)
        total_amount_spent = summing_it(parse_by_year(year, self.grab_data()))
        averages = {}
        for entry in category_list:
            sql = """SELECT * FROM EXPENSES WHERE CATEGORY = '{}'""".format(entry)
            try:
                self.c.execute(sql)
                raw_dat = parse_by_year(year, self.c.fetchall())
            except sqlite3.OperationalError or ConnectionError:
                print("ERROR, You broke something, please try again.")
            cat_total = summing_it(raw_dat)
            avg = round((cat_total / total_amount_spent) * 100, 2)
            av_add = {entry: avg}
            averages.update(av_add)
        return averages

    def monthly_report(self, month=datetime.date.today().month, year=datetime.date.today().year):
        """
        Prints out data about a month (uses current month if month is unspecified) including:

        Total amount spent

        Average monthly transaction amount
        Average yearly transaction amount
        Difference between monthly and yearly averages

        Total transactions per category
        Total spent per category
        Percentage of monthly spending by category
        Average monthly transaction amount per Category
        Average yearly transaction amount per Category

        Difference between category in averages for year and month

        :param year: accepts INT between 0-9999
        :param month: accepts INT between 1-12
        :return: returns STDOUT to console
        """
        month_data = parse_by_month(month, self.grab_data())
        year_data = parse_by_year(year, self.grab_data())
        total_spent = 0
        for entry in month_data:
            total_spent += entry[0]
        print()
        print("The total amount spent this month is: $" + str(round(total_spent, 2)))
        print()
        time.sleep(1)

        month_avg = user.monthly_avg(month)
        print("Your average transaction amount for this month is: $" + str(month_avg))
        print()
        time.sleep(1)

        year_avg = user.yearly_avg()
        print("Your average transaction amount for the year is ${}".format(year_avg))
        print()
        time.sleep(1)

        if month_avg > year_avg:
            diff = round(month_avg - year_avg, 2)
            print("Your average monthly transaction of ${} is ${} above your yearly average of ${}"
                  .format(month_avg, diff, year_avg))
            print()
        elif month_avg < year_avg:
            diff = round(year_avg - month_avg, 2)
            print("Your average monthly transaction of ${} is ${} below your yearly average of ${}"
                  .format(month_avg, diff, year_avg))
            print()
        time.sleep(1)

        cat_dict = category_breakdown(month_data)
        print("Total transactions for the month in each category:")
        for entry in cat_dict:
            print(entry + ": " + str(cat_dict[entry]))
        time.sleep(1)

        print()
        print("Total amount spent for the month by category:")
        for entry in cat_dict:
            dat1 = self.grab_data(entry)
            list_cat1 = parse_by_month(month, dat1)
            cat_sum = summing_it(list_cat1)
            print(entry + ": $" + str(cat_sum))
        time.sleep(1)

        print()
        print("Monthly spending as a percentage of each category: ")
        check = self.monthly_category_percentages(cat_dict, month)
        for entry in check:
            print(entry + ": " + str(check[entry]) + "%")
        time.sleep(1)

        print()
        print("Average monthly transaction amount per category: ")
        month_compare = []
        for entry in cat_dict:
            cat_avg = self.category_avg(entry, month_data)
            print("{}: ${}".format(entry, cat_avg))
            month_compare.append([entry, cat_avg])
        time.sleep(1)

        print()
        print("Average yearly transaction amount per category: ")
        year_compare = []
        for entry in cat_dict:
            cat_avg = self.category_avg(entry, year_data)
            print("{}: ${}".format(entry, cat_avg))
            year_compare.append([entry, cat_avg])
        time.sleep(1)

        print()
        diff_data = compare_month_year_diff_averages(month_compare, year_compare)
        for entry in diff_data:
            print("Your average monthly transaction for {} is ${} {} your yearly average"
                  .format(entry[0], entry[1], entry[2]))
            time.sleep(1)

    def fix_wrong_category(self, category_to_fix, new_category):
        """
        function which updates a category based on user choice

        :param category_to_fix:
        :param new_category:
        :return:
        """
        sql = """UPDATE EXPENSES SET CATEGORY = '{}' WHERE CATEGORY = '{}'"""\
            .format(new_category.capitalize(), category_to_fix)
        try:
            self.c.execute(sql)
            self.user_db.commit()
            print("Success!")
            time.sleep(.5)
            print()
        except sqlite3.OperationalError:
            print("ERROR, You broke something, please try again.")


def menu_function1():
    """
    main user facing function to input expenses for the current day

    :return: returns nothing, displays confirmation from called function with print via STDOUT
    """
    while True:
        try:
            amount = round(float(input("Please enter the amount: ")), 2)
            break
        except ValueError:
            print("Hey!, That's not a Number!")
    category = input("Please enter the category this expense belongs to: ")
    note = input("OPTIONAL: Enter a note for this transaction: ")
    user.log_current_expenses(amount, category, note)


def menu_function2():
    """
    main user facing function to input past expenses

    :return: returns nothing, displays confirmation from called function with print via STDOUT
    """
    while True:
        try:
            amount = round(float(input("Please enter the amount: ")), 2)
            break
        except ValueError:
            print("Hey!, That's not a Number!")
    category = input("Please enter the category this expense belongs to: ")
    note = input("OPTIONAL: Enter a note for this transaction: ")
    year = user_input_year()
    month = user_input_month()
    day = user_input_day(month, year)
    user.log_previous_expenses(amount, category, day, month, year, note)


def menu_function3():
    view_func("week")


def menu_function4():
    view_func("month")


def menu_function5():
    view_func()


def menu_function6():
    chosen_category = category_display_and_choice()
    display_data = user.grab_data(chosen_category)
    final_data_display(display_data)


def menu_function7():
    """
    I wrote the monthly_report function function before I had really conceptualized how the user would be
    interacting with the function so this function require a little bit of finesse if the user wants to display
    a monthly report for a different month or a month from a different year.

    :return: returns nothing, displays data with print to STDOUT
    """
    while True:
        try:
            current_month_check = input("Would you like to display information for the current month? [y/n]: ")
            if current_month_check == "y" or current_month_check == "n":
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")
    if current_month_check.lower() == "y":
        user.monthly_report()
    elif current_month_check.lower() == "n":
        while True:
            try:
                same_year = input("Is this month in the current calender year? [y/n]: ")
                if same_year.lower() == "y" or same_year.lower() == "n":
                    break
                else:
                    print("Please select an appropriate value.")
            except ValueError:
                print("Please select an appropriate value.")
        if same_year == "y":
            month = user_input_month()
            user.monthly_report(month=month)
        elif same_year == "n":
            year = user_input_year()
            month = user_input_month()
            user.monthly_report(month=month, year=year)


def menu_function8():
    """
    this function was added after the fact to allow users to see information about the monthly and yearly category
    percentages breakdown in a format that doesn't involve the monthly report (in which a yearly category breakdown by
    percentage isn't even a option. The function is very large as I had to finesse some data types for functions built
    to accept certain typos of iterable data.

    :return: returns nothing, displays via print to STDOUT
    """
    while True:
        try:
            user_choice = input("What you like to see a breakdown of a month or year? [y/m]: ")
            if user_choice == "y" or user_choice == "m":
                break
            else:
                print("Please select an appropriate value.")
        except ValueError:
            print("Please select an appropriate value.")
    if user_choice.lower() == "y":
        year = user_input_year()
        data1 = category_breakdown(parse_by_year(year, user.grab_data()))
        display_data = user.yearly_category_percentages(data1, year)
        print()
        for entry in display_data:
            print("{}: {}%".format(entry, display_data[entry]))
            time.sleep(.5)
    elif user_choice.lower() == "m":
        month = user_input_month()
        year = user_input_year()
        data1 = category_breakdown(parse_by_month(month, parse_by_year(year, user.grab_data())))
        display_data = user.monthly_category_percentages(data1, month)
        print()
        for entry in display_data:
            print("{}: {}%".format(entry, display_data[entry]))
            time.sleep(.5)


def menu_function9():
    """
    menu function which prints a list of all the different categories present in the database.

    :return: returns nothing, displays output with print via STDOUT
    """
    categories = user.grab_categories()
    counter = 1
    for entry in categories:
        print(str(counter) + ". {}".format(entry))
        counter += 1
    time.sleep(1)


def menu_function10():
    """
    function which replaces a mistyped category name

    :return: nothing displays confirmation from called function with print via STDOUT
    """
    print("Please choose a category to change: ")
    category_to_fix = category_display_and_choice()
    category_fix = input("Please choose what to replace " + category_to_fix + " with: ")
    user.fix_wrong_category(category_to_fix, category_fix)


def main():
    print("EXPENSE TRACKER")
    print()
    print("A Program By: Brandon Bertagnolli")
    time.sleep(1)
    print()
    print()
    print()
    print("Welcome!")
    while True:
        print()
        print("1. Enter expenses for today")
        print("2. Enter expenses for a previous date")
        print("3. View expenses by week of month")
        print("4. View expenses by month")
        print("5. View expenses by year")
        print("6. View expenses by category")
        print("7. View monthly expense report")
        print("8. View spending category percentages by month or year")
        print("9. View a list of all the categories currently in the database")
        print("10. Fix a mislabeled category")
        print("11. Quit ")
        print()
        user_input = input("Please select an option [1, 2, 3 etc]: ")

        if user_input == "1":
            menu_function1()
        elif user_input == "2":
            menu_function2()
        elif user_input == "3":
            menu_function3()
        elif user_input == "4":
            menu_function4()
        elif user_input == "5":
            menu_function5()
        elif user_input == "6":
            menu_function6()
        elif user_input == "7":
            menu_function7()
        elif user_input == "8":
            menu_function8()
        elif user_input == "9":
            menu_function9()
        elif user_input == "10":
            menu_function10()
        elif user_input == "11" or user_input == "q":
            break
        else:
            print()
            print("I didn't get that.\nPlease select an appropriate option.")
            time.sleep(1)


if __name__ == "__main__":
    while not User.started:
        user = User(input("Please enter your name: "))
        if user.started:
            break
    main()
