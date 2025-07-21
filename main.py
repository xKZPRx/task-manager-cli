""" Task Manager by Kacper Wawrzonkiewicz (xKZPRx) """
import os
from data.database import (create_database, add_list_todb, add_task_todb,
                          get_lists_names_fromdb, get_tasks_titles_fromdb, remove_list_fromdb, remove_task_fromdb)
import sqlite3


class TaskManager:
    def __init__(self):
        self.running = True

        self.tasks_lists = {}
        self.update_tasks_lists()

    
    def update_tasks_lists(self):
        self.tasks_lists.clear()
        lists_names = get_lists_names_fromdb()
        for n, list_name in enumerate(lists_names):
            n += 1
            self.tasks_lists[n] = list_name


    def clear_terminal(self):
        os.system('cls')


    def build_menu(self):
        print("*-------------------- Task Manager Menu --------------------*")
        print("Choose one of the commands below:")
        print("  (1) Show tasks lists/tasks")
        print("  (2) Add new tasks list/task")
        print("  (3) Remove task list/task")
        print("  Type 'exit' in order to leave the task manager")


    def get_user_input(self):
        user_input = input("> ")
        return user_input
    

    def display_add_options(self):
        print("*-------------------- Add Options Menu ---------------------*")
        print("Choose one of the commands below:")
        print("  (1) Create a new tasks list")
        print("  (2) Add a new task")
        print()
        print("Type anything in order to go back")


    def build_list_creation_menu(self):
        print("*----------------------------------- Create Tasks List -----------------------------------*")
        print("Please provide tasks list details below")

    
    def build_task_creation_menu(self):
        print("*----------------------------------- Add Task -----------------------------------*")
        print("Please provide task details below")


    def validate_list_details(self, name):
        error_message = None

        name = name.strip()
        if len(name) == 0:
            error_message = "List name cannot be empty!"
            return False, error_message
        
        if len(name) > 30:
            error_message = "List name cannot be more than 30 characters long."
            return False, error_message

        return True, error_message
    
    
    def validate_task_details(self, title):
        error_message = None

        title = title.strip()
        if len(title) == 0:
            error_message = "Task title cannot be empty!"
            return False, error_message
        
        if len(title) > 50:
            error_message = "Task title cannot be more than 50 characters long."
            return False, error_message

        return True, error_message
    

    def extract_and_display_lists(self):
        print("*-------------------- Lists Display ---------------------*")
        print("Choose one of the lists below:")
        if self.tasks_lists:
            for n, list_name in self.tasks_lists.items():
                print(f"  ({n}) {list_name}")
        else:
            print("> No data")
            print()
            return False
        
        print()
        print("Type anything in order to go back")

        return n
    

    def extract_and_display_tasks(self, list_index):
        list_name = self.tasks_lists[list_index]
        tasks = get_tasks_titles_fromdb(list_name)

        print("*-------------------- Tasks Display ---------------------*")
        if tasks:
            for task in tasks:
                print(f"> {task}")
        else:
            print("> No data")
            print()
            return False
        
        print()
        print("Type anything in order to return to the menu")


    def display_remove_options(self):
        print("*-------------------- Remove Options ---------------------*")
        print("Choose what you want to delete")
        print("  (1) Tasks Lists")
        print("  (2) Task")
        print()
        print("Type anything in order to go back")


    def display_lists_to_remove(self):
        print("*-------------------- Lists to Remove ---------------------*")
        print("Choose the list you want to remove")
        if self.tasks_lists:
            for n, list_name in self.tasks_lists.items():
                print(f"  ({n}) {list_name}")
        else:
            print("> No data")
            print()
            return
        
        print()
        print("Type anything in order to return to the menu")

        return n
    

    def display_tasks_lists(self):
        print("*---------------------- Tasks Lists -----------------------*")
        print("Choose the list to delete task from")
        if self.tasks_lists:
            for n, list_name in self.tasks_lists.items():
                print(f"  ({n}) {list_name}")
        else:
            print("> No data")
            print()
            return False
        
        print()
        print("Type anything in order to return to the menu")

        return n
    

    def display_tasks_to_remove(self, list_name):
        tasks_list = {}

        print("*-------------------- Tasks to Remove ---------------------*")
        print("Choose the task you want to delete")
        tasks = get_tasks_titles_fromdb(list_name)
        if tasks:
            for n, task in enumerate(tasks):
                n += 1
                print(f"  ({n}) {task}")
                tasks_list[n] = task
        else:   
            print("> No data")
            print()
            return False
        
        print()
        print("Type anything in order to return to the menu")

        return n, tasks_list


    def leave_task_manager(self):
        self.running = False
        quit(0)


    def draw_error(self, error_message):
        print("*-------------------------- Error --------------------------*")
        print(f"> {error_message}")
        print()

    def draw_success(self, success_message):
        print("*------------------------- Success -------------------------*")
        print(f"> {success_message}")
        print()


    def run(self):
        self.clear_terminal()

        while self.running:
            self.update_tasks_lists()

            self.build_menu()
            user_input = self.get_user_input()

            # (1) Show tasks lists/tasks
            if user_input == "1":
                self.clear_terminal()
                
                if not self.extract_and_display_lists():
                    continue

                self.clear_terminal()    
                lists_amount = self.extract_and_display_lists()
                user_input = self.get_user_input()

                try:
                    user_input = int(user_input)
                    if user_input <= 0 or user_input > lists_amount:
                        self.clear_terminal()
                        self.draw_error("Please enter a valid list id")

                    else:
                        self.clear_terminal()
                        
                        if not self.extract_and_display_tasks(user_input):
                            continue

                        user_input = self.get_user_input()
                        self.clear_terminal()
                        continue

                except ValueError:
                        self.clear_terminal()
                        continue

            # (2) Add new tasks list/task
            elif user_input == "2":
                self.clear_terminal()
                self.display_add_options()
                user_input = self.get_user_input()

                if user_input == "1":
                    self.clear_terminal()
                    self.build_list_creation_menu()
                    list_name = input("> List name: ")
                    
                    valid, error_message = self.validate_list_details(list_name)
                    if valid and not error_message:
                        try:
                            add_list_todb(list_name)
                            self.clear_terminal()
                            self.draw_success(f"List: '{list_name}' has been added successfully!")

                        except sqlite3.IntegrityError:
                            self.clear_terminal()
                            self.draw_error("This tasks list already exists.")

                    else:
                        self.clear_terminal()
                        self.draw_error(error_message)

                elif user_input == "2":
                    self.clear_terminal()
                    self.build_task_creation_menu()
                    list_name = input("> List name: ")
                    task_title = input("> Task title: ")

                    valid, error_message = self.validate_task_details(task_title)
                    if valid and not error_message:
                        try:
                            add_task_todb(list_name, task_title)
                            self.clear_terminal()
                            self.draw_success(f"Task: '{task_title}' has been added successfully!")

                        except TypeError:
                            self.clear_terminal()
                            self.draw_error("This tasks list doesn't exist.")

                    else:
                        self.clear_terminal()
                        self.draw_error(error_message)

                else:
                    self.clear_terminal()
                    continue

            # (3) Remove tasks list/task
            elif user_input == "3":
                self.clear_terminal()
                self.display_remove_options()
                user_input = self.get_user_input()

                if user_input == "1":
                    self.clear_terminal()

                    if not self.display_lists_to_remove():
                        continue

                    self.clear_terminal()
                    lists_amount = self.display_lists_to_remove()
                    user_input = self.get_user_input()

                    try:
                        user_input = int(user_input)
                        if user_input <= 0 or user_input > lists_amount:
                            self.clear_terminal()
                            self.draw_error("Please enter a valid list id")

                        else:
                            self.clear_terminal()
                            list_name = self.tasks_lists[user_input]

                            remove_list_fromdb(list_name)
                            self.draw_success(f"List: '{list_name}' has been deleted successfully.")
                            continue

                    except ValueError:
                            self.clear_terminal()
                            continue

                elif user_input == "2":
                    self.clear_terminal()

                    if not self.display_tasks_lists():
                       continue
                    
                    self.clear_terminal()
                    lists_amount = self.display_tasks_lists()
                    user_input = self.get_user_input()

                    try:
                        user_input = int(user_input)
                        if user_input <= 0 or user_input > lists_amount:
                            self.clear_terminal()
                            self.draw_error("Please enter a valid list id")

                        else:
                            self.clear_terminal()
                            list_name = self.tasks_lists[user_input]

                            if not self.display_tasks_to_remove(list_name):
                                continue

                            self.clear_terminal()
                            tasks_amount, tasks_list = self.display_tasks_to_remove(list_name)
                            user_input = self.get_user_input()

                            try:
                                user_input = int(user_input)
                                if user_input <= 0 or user_input > tasks_amount:
                                    self.clear_terminal()
                                    self.draw_error("Please enter a valid task id")

                                else:
                                    self.clear_terminal()
                                    task_title = tasks_list[user_input]

                                    remove_task_fromdb(list_name, task_title)
                                    self.draw_success(f"Task '{task_title}' has been removed successfully.")
                                    continue

                            except ValueError:
                                self.clear_terminal()
                                continue

                    except ValueError:
                            self.clear_terminal()
                            continue            

                else:
                    self.clear_terminal()
                    continue

            # Leave task manager
            elif user_input == "exit":
                self.clear_terminal()
                self.leave_task_manager()

            # Handle invalid input
            else:
                self.clear_terminal()
                self.draw_error("Invalid input! Please try again.")


if __name__ == "__main__":
    create_database()
    task_manager = TaskManager()
    task_manager.run()
