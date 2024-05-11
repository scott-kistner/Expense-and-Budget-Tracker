 # ========== Importing Libraries ==========
import sqlite3
import datetime


# ========== Functions ==========
# ------- Connecting to Database -------
def database_connect():
    try:
        db = sqlite3.connect('./tracker_app.db') 
        cursor = db.cursor()
        return cursor, db
    except sqlite3.Error as e:
        print(f"\nError connecting to database due to: {e}\n")
        db.rollback()
        return None, None


# ------- Creating Tables -------
# Create a specific table to record expenses.
def create_expense_table():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS 
                       expense_tracker(id INTEGER PRIMARY KEY, 
                       date TEXT, 
                       description TEXT,
                       expense_category TEXT, 
                       expense_amount REAL
                       )
                       ''')
        db.commit()
    
    except sqlite3.Error as e:
        print(f"\nThe following error occurred: {e}.\n")
        db.rollback()


# Create a specific table to record income.
def create_income_table():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS 
                       income_tracker(id INTEGER PRIMARY KEY,
                       date TEXT,
                       description TEXT,
                       income_category TEXT,
                       income_amount REAL
                       )
                       ''')
        db.commit()
    
    except sqlite3.Error as e:
        print(f"\nThe following error occurred: {e}.\n")
        db.rollback()


# Create a specific table to record budgets.
def create_budget_table():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS 
                       budget_tracker(id INTEGER PRIMARY KEY,
                       expense_category TEXT UNIQUE,
                       budget REAL
                       )
                       ''')
        db.commit()
    
    except sqlite3.Error as e:
        print(f"\nThe following error occurred: {e}.\n")
        db.rollback()


# Create a specific table to record financial goals.
def create_goals_table():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS 
                       financial_goals_tracker(id INTEGER PRIMARY KEY,
                       goal,
                       target_date TEXT,
                       target_amount REAL
                       )
                       ''')
        db.commit()
    
    except sqlite3.Error as e:
        print(f"\nThe following error occurred: {e}.\n")
        db.rollback()


# ------- Pre-Populating Tables -------
# Populating expense tracker with data.
def insert_prepopulated_expenses():
    try:
        cursor, db = database_connect()


        # Prevent duplicating pre-pop data.
        cursor.execute(''' SELECT COUNT(*) FROM expense_tracker''')
        count = cursor.fetchone()[0]
        if count > 0:
            return
        

        cursor.executemany('''
                           INSERT INTO expense_tracker
                           (date, description, expense_category, expense_amount)
                           VALUES (?, ?, ?, ?)
                           ''',
                           [('2024-05-01', 'Tesco shopping', 'Food', 50.00),
                            ('2024-05-02', 'Dinner with friends', 'Entertainment', 35.00),
                            ('2024-05-03', 'Petrol refill', 'Transportation', 40.00)])
        db.commit()
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred while inserting pre-populated expenses: {e}. ~\n")
        db.rollback()


# Populating income tracker with data.
def insert_prepopulated_income():
    try:
        cursor, db = database_connect()
        

        # Prevent duplicating pre-pop data.
        cursor.execute(''' SELECT COUNT(*) FROM income_tracker''')
        count = cursor.fetchone()[0]
        if count > 0:
            return
        
        
        cursor.executemany('''
                           INSERT INTO income_tracker
                           (date, description, income_category, income_amount)
                           VALUES (?, ?, ?, ?)
                           ''',
                           [('2024-05-01', 'Salary', 'Job', 3200.00),
                            ('2024-05-15', 'Freelance work', 'Freelance', 500.00),
                            ('2024-05-20', 'Investment dividends', 'Investment', 100.00)])
        db.commit()
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred while inserting pre-populated income: {e}. ~\n")
        db.rollback()


# Populating budget tracker with data.
def insert_prepopulated_budget():
    try:
        cursor, db = database_connect()
        

        # Prevent duplicating pre-pop data.
        cursor.execute(''' SELECT COUNT(*) FROM budget_tracker''')
        count = cursor.fetchone()[0]
        if count > 0:
            return
        
        
        cursor.executemany('''
                           INSERT INTO budget_tracker
                           (expense_category, budget)
                           VALUES (?, ?)
                           ''',
                           [('Food', 300.00),
                            ('Entertainment', 100.00),
                            ('Transportation', 200.00),
                            ('Housing', 800.00)])
        db.commit()
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred while inserting pre-populated budget: {e}. ~\n")
        db.rollback()


# Populating financial goals tracker with data.
def insert_prepopulated_goals():
    try:
        cursor, db = database_connect()
        

        # Prevent duplicating pre-pop data.
        cursor.execute(''' SELECT COUNT(*) FROM financial_goals_tracker''')
        count = cursor.fetchone()[0]
        if count > 0:
            return
        
        
        cursor.executemany('''
                           INSERT INTO financial_goals_tracker
                           (goal, target_date, target_amount)
                           VALUES (?, ?, ?)
                           ''',
                           [('Emergency Fund', '2025-12-31', 10000.00),
                            ('Italy (Holiday)', '2026-06-30', 2000.00),
                            ('New Car', '2027-01-01', 20000.00)])
        db.commit()
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred while inserting pre-populated goals: {e}. ~\n")
        db.rollback()


# ------- Entering a new expense -------
def add_expense():
    try:
        cursor, db = database_connect()
        cursor.execute('''SELECT MAX(id) FROM expense_tracker
                       ''')
        max_id = cursor.fetchone()[0] or 0
        new_expense_id = max_id + 1
        
        while True:
            new_expense_date = input("\nPlease enter the date of the expense [yyyy-mm-dd]: ")
            try:
                datetime.datetime.strptime(new_expense_date, '%Y-%m-%d')
                break
            except ValueError:
                print("\n~ Invalid date format. Please try again. ~\n")

        new_expense_description = input("Please enter a short description of the expense: ").capitalize()
        new_expense_category = input("Please enter the expense category: ").title()
        new_expense_amount = float(input("Please enter the expense amount in GBP (£): "))
        
        cursor.execute('''
                       INSERT INTO expense_tracker
                       (id, date, description, expense_category, expense_amount)
                       VALUES (?, ?, ?, ?, ?)''',
                       (new_expense_id, new_expense_date, new_expense_description,
                        new_expense_category, new_expense_amount))
        db.commit()
        print(f"\nSuccess! The following has been entered into the database:")
        print(f"id:                     {new_expense_id}")
        print(f"Expense Date:           {new_expense_date}")
        print(f"Expense:                {new_expense_description}")
        print(f"Expense Category:       {new_expense_category}")
        print(f"Expense Amount:         £{new_expense_amount}")
        print("______________________________________________________________________\n")

    except sqlite3.Error as e:
        print(f"\nError: {e}")
        db.rollback()


# ------- Viewing all expenses -------
def view_expenses():
    try:
        cursor, db = database_connect()
        print("\n****** All Recorded Expenses ******\n")
        cursor.execute('''
                       SELECT * FROM expense_tracker
                       ''')
        for row in cursor:
            print(f"{row[0]}: '{row[2]}' ({row[3]}) on {row[1]} for £{row[4]}.")
            print("______________________________________________________________________\n")
        while True:
            try:
                update_expense = input("Would you like to update an expense (Y or N): ").title()
                if update_expense == "Y":
                    chosen_id = int(input("Please enter the relevant id for the expense you'd like to update: "))
                    cursor.execute('''
                                   SELECT * FROM expense_tracker WHERE id = ?
                                   ''', (chosen_id,))
                    chosen_expense = cursor.fetchone()
                    print(f"\n{chosen_expense[0]}: '{chosen_expense[2]}' ({chosen_expense[3]}) on {chosen_expense[1]} for £{chosen_expense[4]}.\n")
                    print("Options:")
                    print("1. Update expense date")
                    print("2. Update expense description")
                    print("3. Update expense category")
                    print("4. Update expense amount")
                    print("5. Delete expense")
                    print("0. Return\n")
                    update_expense_option = int(input("Which of previous options would you like to carry-out (0-5): "))
                
                
                    # ------- Update expense date -------
                    if update_expense_option == 1:
                        try:
                            while True:
                                update_expense_date = input("\nPlease enter the new date for the chosen expense [yyyy-mm-dd]: ")
                                try:
                                    datetime.datetime.strptime(update_expense_date, '%Y-%m-%d')
                                    break
                                except ValueError:
                                    print("~ Invalid date format. Please try again. ~")
                            
                            cursor.execute('''UPDATE expense_tracker SET date = ? WHERE id = ?
                                           ''', (update_expense_date, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s expense has been updated to {update_expense_date}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Update expense description -------
                    elif update_expense_option == 2:
                        try:
                            update_expense_descr = input("\nPlease enter the new description for the chosen expense: ")
                            cursor.execute('''UPDATE expense_tracker SET description = ? WHERE id = ?
                                           ''', (update_expense_descr, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s description has been updated to {update_expense_descr}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Update expense category -------
                    elif update_expense_option == 3:
                        try:
                            update_expense_cat = input("\nPlease enter the new category for the chosen expense: ")
                            cursor.execute('''UPDATE expense_tracker SET expense_category = ? WHERE id = ?
                                           ''', (update_expense_cat, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s expense category has been updated to {update_expense_cat}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Update expense amount -------
                    elif update_expense_option == 4:
                        try:
                            update_expense_amt = float(input("\nPlease enter the new amount for the chosen expense: "))
                            cursor.execute('''UPDATE expense_tracker SET expense_amount = ? WHERE id = ?
                                           ''', (update_expense_amt, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s expense amount has been updated to £{update_expense_amt}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Delete expense -------
                    elif update_expense_option == 5:
                        try:
                            delete_expense_check = input(f"\nPlease confirm you'd like to delete expense '{chosen_id}' (Y or N): ").title()
                            if delete_expense_check == "Y":
                                cursor.execute('''DELETE FROM expense_tracker where id = ?''', (chosen_id,))
                                db.commit()
                                print(f"\nSuccess! {chosen_id} has been deleted from database.\n")
                            elif delete_expense_check == "N":
                                break
                            else:
                                print("\n~ Oops - incorrect input. Please try again. ~\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()

                
                    # ----- Return to previous option menu -----
                    elif update_expense_option == 0:
                        break
                    
                    
                    else:
                        print("\n~ Oops - incorrect input. Please try again. ~\n")
                

                # ----- Return to previous option menu -----
                elif update_expense == "N":
                    break

                else:
                    print("\n~ Oops - incorrect input. Please try again. ~\n")
            
            except ValueError:
                print("\n~ Invalid input. Please enter a relevant number. ~\n")
            
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")
        db.rollback()


# ------- Viewing expenses by category -------
def view_category_expenses():
    try:
        cursor, db = database_connect()
        print("\n****** Current Expense Categories ******")
        cursor.execute('''
                       SELECT DISTINCT expense_category FROM expense_tracker
                       ''')
        category_list = cursor.fetchall()
        for category in category_list:
            print(f"- {category[0]}")
        chosen_category = input("\nPlease select which category you'd like to display: ").title()
        cursor.execute('''
                       SELECT * FROM expense_tracker WHERE expense_category = ?
                       ''', (chosen_category,))
        chosen_expenses = cursor.fetchall()
        print(f"\nSuccess! Please find expenses for '{chosen_category}' below:\n")
        for expense in chosen_expenses:
            print(f"id:                     {expense[0]}")
            print(f"Expense Date:           {expense[1]}")
            print(f"Expense:                {expense[2]}")
            print(f"Expense Category:       {expense[3]}")
            print(f"Expense Amount:         £{expense[4]}")
            print("______________________________________________________________________\n")
        
        
        # Ask the user if they want to update the chosen expense category.
        update_category = input("Would you like to update the chosen category (Y or N): ").title()
        if update_category == "Y":
            new_category = input("Please enter the new category name: ").title()
            cursor.execute('''UPDATE expense_tracker SET expense_category = ?
                           WHERE expense_category = ?
                           ''', (new_category, chosen_category))
            db.commit()
            print(f"\nSuccessfully updated the category '{chosen_category}' to '{new_category}'.\n")
        elif update_category == "N":
            print("\nCategory not updated.\n")
        else:
            print("\n~ Invalid input. Please enter either Y or N. ~\n")        
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")
        db.rollback()


# ------- Entering a new income -------
def add_income():
    try:
        cursor, db = database_connect()

        """
        Create new id for income based on the largest id value in database.
        If not id values exist, it starts at 1.
        """

        cursor.execute('''SELECT MAX(id) FROM income_tracker
                       ''')
        max_id = cursor.fetchone()[0] or 0
        new_income_id = max_id + 1


        # Ask user to input income date and validate it.
        while True:
            new_income_date = input("\nPlease enter the date of the income [yyyy-mm-dd]: ")
            try:
                datetime.datetime.strptime(new_income_date, '%Y-%m-%d')
                break
            except ValueError:
                print("\n~ Invalid date format. Please try again. ~\n")
        
        
        new_income_description = input("Please enter a short description of the income: ").title()
        new_income_category = input("Please enter the income category: ").title()
        try:
            new_income_amount = float(input("Please enter the income amount in GBP (£): "))
            cursor.execute('''
                           INSERT INTO income_tracker(
                           id, date, description, income_category, income_amount)
                           VALUES(?, ?, ?, ?, ?)''',
                           (new_income_id, new_income_date, new_income_description,
                            new_income_category, new_income_amount))
            db.commit()
            print(f"\nSuccess! The following has been entered into the database:")
            print(f"id:                     {new_income_id}")
            print(f"Income Date:            {new_income_date}")
            print(f"Income:                 {new_income_description}")
            print(f"Income Category:        {new_income_category}")
            print(f"Income Amount:          £{new_income_amount}")
            print("______________________________________________________________________\n")
        except ValueError:
            print("\n~ Error: Invalid input. Please enter a valid amount.\n ~")
            db.rollback()
    
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~")
        db.rollback()


# ------- Viewing all income -------
def view_income():
    try:
        cursor, db = database_connect()
        print("\n****** All Recorded Income ******\n")
        cursor.execute('''
                       SELECT * FROM income_tracker
                       ''')
        for row in cursor:
            print(f"{row[0]}: '{row[2]}'({row[3]}) on {row[1]} for £{row[4]}.")
            print("______________________________________________________________________\n")
        while True:
            try:
                update_income = input("Would you like to update an income (Y or N): ").title()
                if update_income == "Y":
                    chosen_id = int(input("Please enter the relevant id for the income you'd like to update: "))
                    cursor.execute('''
                                   SELECT * FROM income_tracker WHERE id = ?
                                   ''', (chosen_id,))
                    chosen_income = cursor.fetchone()
                    print(f"\n{chosen_income[0]}: '{chosen_income[2]}' ({chosen_income[3]}) on {chosen_income[1]} for £{chosen_income[4]}.\n")
                    print("\nOptions:")
                    print("1. Update income date")
                    print("2. Update income description")
                    print("3. Update income category")
                    print("4. Update income amount")
                    print("5. Delete income")
                    print("0. Return\n")
                    update_income_option = int(input("Which of previous options would you like to carry-out (0-5): "))
                
                
                    # ------- Update income date -------
                    if update_income_option == 1:
                        try:
                            while True:
                                update_income_date = input("\nPlease enter the new date for the chosen income [yyyy-mm-dd]: ")
                                try:
                                    datetime.datetime.strptime(update_income_date, '%Y-%m-%d')
                                    break
                                except ValueError:
                                    print("\n~ Invalid date format. Please try again. ~\n")
                            
                            cursor.execute('''UPDATE income_tracker SET date = ? WHERE id = ?
                                           ''', (update_income_date, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s income has been updated to {update_income_date}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Update income description -------
                    elif update_income_option == 2:
                        try:
                            update_income_descr = input("\nPlease enter the new description for the chosen income: ")
                            cursor.execute('''UPDATE income_tracker SET description = ? WHERE id = ?
                                           ''', (update_income_descr, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s description has been updated to {update_income_descr}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Update income category -------
                    elif update_income_option == 3:
                        try:
                            update_income_cat = input("\nPlease enter the new category for the chosen income: ")
                            cursor.execute('''UPDATE income_tracker SET income_category = ? WHERE id = ?
                                           ''', (update_income_cat, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s income category has been updated to {update_income_cat}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Update income amount -------
                    elif update_income_option == 4:
                        try:
                            update_income_amt = float(input("\nPlease enter the new amount for the chosen income: "))
                            cursor.execute('''UPDATE income_tracker SET income_amount = ? WHERE id = ?
                                           ''', (update_income_amt, chosen_id))
                            db.commit()
                            print(f"\nSuccess! {chosen_id}'s income amount has been updated to {update_income_amt}.\n")
                        except sqlite3.Error as e:
                            print(f"\n~ The following error occurred: {e}. ~\n")
                            db.rollback()
                

                    # ------- Delete income -------
                    elif update_income_option == 5:
                        try:
                            delete_income_check = input(f"\nPlease confirm you'd like to delete income '{chosen_id}' (Y or N): ").title()
                            if delete_income_check == "Y":
                                cursor.execute('''DELETE FROM income_tracker where id = ?''', (chosen_id,))
                                db.commit()
                                print(f"\nSuccess! {chosen_id} has been deleted from database.\n")
                            elif delete_income_check == "N":
                                break
                            else:
                                print("\n~ Oops - incorrect input. Please try again. ~\n")
                        except sqlite3.Error as e:
                            print(f"~ \nThe following error occurred: {e}. ~\n")
                            db.rollback()

                
                    # ----- Return to previous option menu -----
                    elif update_income_option == 0:
                        break
                    
                    
                    else:
                        print("\n~ Oops - incorrect input. Please try again. ~")
                

                # ----- Return to previous option menu -----
                elif update_income == "N":
                    break

                else:
                    print("\n~ Oops - incorrect input. Please try again. ~")
            
            except ValueError:
                print("\n~ Invalid input. Please enter a relevant number. ~")
            
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")
        db.rollback()


# ------- Viewing income by category -------
def view_category_income():
    try:
        cursor, db = database_connect()
        print("\n****** Current Income Categories ******")
        cursor.execute('''
                       SELECT DISTINCT income_category FROM income_tracker
                       ''')
        category_list = cursor.fetchall()
        for category in category_list:
            print(f"- {category[0]}")
        chosen_category = input("\nPlease select which category you'd like to display: ").title()
        cursor.execute('''
                       SELECT * FROM income_tracker WHERE income_category = ?
                       ''', (chosen_category,))
        chosen_income = cursor.fetchall()
        print(f"\nSuccess! Please find income for '{chosen_category}' below:\n")
        for income in chosen_income:
            print(f"id:                     {income[0]}")
            print(f"Expense Date:           {income[1]}")
            print(f"Expense:                {income[2]}")
            print(f"Expense Category:       {income[3]}")
            print(f"Expense Amount:         £{income[4]}")
            print("______________________________________________________________________\n")


        # Ask the user if they want to update the chosen income category.
        update_category = input("Would you like to update the chosen category (Y or N): ").title()
        if update_category == "Y":
            new_category = input("Please enter the new category name: ").title()
            cursor.execute('''UPDATE income_tracker SET income_category = ?
                           WHERE income_category = ?
                           ''', (new_category, chosen_category))
            db.commit()
            print(f"\nSuccessfully updated the category '{chosen_category}' to '{new_category}'.\n")
        elif update_category == "N":
            print("\nCategory not updated.\n")
        else:
            print("\n~ Invalid input. Please enter either Y or N. ~\n")        
    
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")
        db.rollback()


# ------- Calculate total expenses -------
def total_expenses():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       SELECT SUM(expense_amount) FROM expense_tracker
                       ''')
        total_expenses = cursor.fetchone()[0]
        return total_expenses
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")
        db.rollback()


# ------- Calculate total income -------
def total_income():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       SELECT SUM(income_amount) FROM income_tracker
                       ''')
        total_income = cursor.fetchone()[0]
        return total_income
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")
        db.rollback()


# ------- Calculate total net income -------
def total_net_income():
    try:
        current_total_income = total_income()
        current_total_expenses = total_expenses()
        if current_total_income is not None and current_total_expenses is not None:
            total_net_income = current_total_income - current_total_expenses
            return total_net_income
        else:
            return None
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")


# ------- Set budget for a category -------
def add_budget():
    try:
        cursor, db = database_connect()
        print("\n****** Setting a budget ******")
        cursor.execute('''
                       SELECT DISTINCT expense_category FROM budget_tracker
                       ''')
        category_list = [category[0] for category in cursor.fetchall()]
        chosen_budget_category = input(
            "\nPlease enter which category you'd like to create a budget for: ").title()
        try:
            budget_amount = float(input(
                "Please enter the budget amount in GBP (£) you'd like to spend per month: "))
            if chosen_budget_category in category_list:
                update_option = input(f"\nThe category '{chosen_budget_category}' already has a budget set. Want to replace it (Y or N): ").title()
                if update_option == "Y":
                    cursor.execute('''
                                   UPDATE budget_tracker
                                   SET budget = ?
                                   WHERE expense_category = ?''',
                                   (budget_amount, chosen_budget_category))
                    db.commit()
                    print(f"\nSuccess! Updated budget for {chosen_budget_category}.")
                else:
                    print("\nCategory not updated.")
            else:
                cursor.execute('''
                               INSERT INTO budget_tracker(
                               expense_category, budget)
                               VALUES(?, ?)''',
                               (chosen_budget_category, budget_amount))
                db.commit()
                print(f"\nSuccess! The following budget has been entered into the database:")
                print(f"Expense Category:       {chosen_budget_category}")
                print(f"Budget:                 £{budget_amount} per month")
                print("______________________________________________________________________\n")
        except ValueError:
            print("\n~ Error: Invalid input. Please enter a valid amount. ~\n")
            db.rollback()
    except sqlite3.Error as e:
        print(f"~ \nThe following error occurred: {e}. ~")
        db.rollback()


# ------- View budget for a category -------
def view_budget():
    try:
        cursor, db = database_connect()

        cursor.execute('''SELECT DISTINCT expense_category FROM expense_tracker''')
        category_list = [row[0] for row in cursor.fetchall()]
        
        print("\n****** Current Expense Categories ******")
        for category in category_list:
            print(f"- {category}")

        chosen_category = input("\nPlease select which category you'd like to display: ").title().strip()

        cursor.execute('''SELECT * FROM budget_tracker WHERE expense_category = ?''', (chosen_category,))
        budget_data = cursor.fetchone()

        if budget_data:
            budget_id, category, budget_amount = budget_data
            budget_amount = float(budget_amount)
            
            current_date = datetime.date.today()
            current_month = current_date.month
            current_year = current_date.year
            cursor.execute('''SELECT SUM(expense_amount) FROM expense_tracker
                  WHERE LOWER(expense_category) = ?
                  AND strftime('%Y-%m', date) = ?
                  ''', (chosen_category.lower(), f"{current_year}-{current_month:02}"))
            total_monthly_expenses = cursor.fetchone()[0] or 0

            if total_monthly_expenses < budget_amount:
                status = "Hooray! Under budget."
            elif total_monthly_expenses == budget_amount:
                status = "On budget."
            else:
                status = "Uh-oh! Over budget."

            print(f"\nSuccess! Please find the budget for '{chosen_category}' below:\n")
            print(f"ID:                         {budget_id}")
            print(f"Expense Category:           {category}")
            print(f"Budget:                     £{budget_amount}")
            print(f"Total Monthly Expenses:     £{total_monthly_expenses}")
            print(f"Status:                     {status}")
            print("______________________________________________________________________\n")
        else:
            print(f"\nBudget not found for '{chosen_category}'.\n")

    except sqlite3.Error as e:
        print(f"\nError: {e}")
        db.rollback()


# ------- Set financial goals -------
def add_goal():
    try:
        cursor, db = database_connect()
        goal_name = input("Please enter a name of your financial goal: ").title()
        
        
        # Ask user to input income date and validate it.
        while True:
            goal_target = input("Please enter the target date [yyyy-mm-dd] of your goal: ")
            try:
                datetime.datetime.strptime(goal_target, '%Y-%m-%d')
                break
            except ValueError:
                print("\n~ Invalid date format. Please try again. ~\n")


        try:
            goal_amount = float(input("Please enter your target amount in GBP (£): "))
            cursor.execute('''
                           INSERT INTO financial_goals_tracker(
                           goal, target_date, target_amount)
                           VALUES(?, ?, ?)''',
                           (goal_name, goal_target, goal_amount))
            db.commit()
            print(f"\nSuccess! The following goal has been entered into the database:\n")
            print(f"Goal:                 {goal_name}")
            print(f"Target Date:          {goal_target}")
            print(f"Target Amount:        £{goal_amount}")
            print("______________________________________________________________________\n")
        except ValueError:
            print("\n~ Error: Invalid input. Please enter a valid amount. ~\n")
            db.rollback()
    except sqlite3.Error as e:
        print(f"~ \nThe following error occurred: {e}. ~")
        db.rollback()


# ------- View progress of financial goals -------
def track_goals():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       SELECT * FROM financial_goals_tracker
                       ''')
        goals_list = cursor.fetchall()
        print("\n****** Current Financial Goals ******\n")
        for goal in goals_list:
            print(f"Goal:               {goal[1]}")
            print(f"Target Date:        {goal[2]}")
            print(f"Target Amount:      £{goal[3]}\n")
        print("\n****** Financial Progress ******\n")
        print("______________________________________________________________________")
        current_total_expenses = round(total_expenses(), 2)
        current_total_income = round(total_income(), 2)
        current_total_net_income = round(total_net_income(), 2)
        today = datetime.date.today()
        print(f"Today's Date:           {today}")
        print(f"Total Expenses:         £{current_total_expenses}")
        print(f"Total Income:           £{current_total_income}")
        print(f"Total Net Income:       £{current_total_net_income}")
        print("______________________________________________________________________\n")
    except sqlite3.Error as e:
        print(f"\n~ The following error occurred: {e}. ~\n")
        db.rollback()



 # ========== Main ==========
print("\n***** Welcome to your Expense and Budget Tracker App *****\n")
create_expense_table()
insert_prepopulated_expenses()
create_income_table()
insert_prepopulated_income()
create_budget_table()
insert_prepopulated_budget()
create_goals_table()
insert_prepopulated_goals()




# Menu options for the user -------
while True:
    try:
        menu = int(input('''From the following options, please choose what you'd like to do (1-11):
        1. Add expense
        2. View expenses
        3. View expenses by category
        4. Add income
        5. View income
        6. View income by category
        7. Set budget for a category
        8. View budget for a category
        9. Set financial goals
        10. View progress towards financial goals
        11. Quit
        : '''))
        if menu == 1:
            add_expense()
        
        elif menu == 2:
            view_expenses()
        
        elif menu == 3:
            view_category_expenses()
        
        elif menu == 4:
            add_income()
        
        elif menu == 5:
            view_income()

        elif menu == 6:
            view_category_income()

        elif menu == 7:
            add_budget()
        
        elif menu == 8:
            view_budget()
        
        elif menu == 9:
            add_goal()

        elif menu == 10:
            total_expenses()
            total_income()
            total_net_income()
            track_goals()
        
        elif menu == 11:
            print(f'\n***** Goodbye! Thank you for using your friendly neighbourhood, Expense and Budget Tracker App! *****\n')
            break
        
        else:
            print("\n~ Oops - incorrect input. Please try again. ~\n")

    except Exception as e:
        print(f"\n~ The following error occurred: {e}. ~\n")