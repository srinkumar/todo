# Write your code here

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# new_row = Table(string_field = 'This is string field',
#                 date_field = datetime.strptime('01-24-2020', '%m-%d-%Y').date())
# session.add(new_row)
# session.commit()
#
# rows = session.query(Table).all()
# first_row = rows[0] # In case rows list is not empty
#
# print(first_row.string_field) # Will print value of the string_field
# print(first_row.id) # Will print the id of the row.
# print(first_row) # Will print the string that was returned by __repr__ method


def get_command():
    print()
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    comm = int(input())
    if comm < 0 or comm > 6:
        print("Invalid command. Exiting the program")
        comm = 0
    return comm


def add_task():
    global session
    print("Enter task")
    task_str = input()
    print("Enter deadline")
    date_str = input()
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    row = Table(task=task_str, deadline=date)
    session.add(row)
    session.commit()
    print("The task has been added!")


def print_rows_with_deadline(rows):
    if not rows:
        print("Nothing to do!")
    else:
        for idx, row in enumerate(rows):
            print(f"{idx + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")


def print_days_tasks(date):
    global session
    rows = session.query(Table).filter(Table.deadline == date).all()
    if not rows:
        print("Nothing to do!")
    else:
        for idx, row in enumerate(rows):
            print(f"{idx + 1}. {row.task}")


def print_todays_tasks():
    global session
    date = datetime.today().date()
    print()
    print(f"Today {date.day} {date.strftime('%b')}:")
    print_days_tasks(date)


def print_all_tasks():
    global session
    rows = session.query(Table).order_by(Table.deadline).all()
    print_rows_with_deadline(rows)


def print_weeks_tasks():
    global session
    weekday_str = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(7):
        date = datetime.today() + timedelta(days=i)
        print()
        print(f"{weekday_str[date.weekday()]} {date.day} {date.strftime('%b')}:")
        print_days_tasks(date.date())


def print_missed_tasks():
    global session
    date = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline < date).order_by(Table.deadline).all()
    print()
    print("Missed tasks:")
    print_rows_with_deadline(rows)


def delete_task():
    global session
    rows = session.query(Table).order_by(Table.deadline).all()
    print_rows_with_deadline(rows)
    task = int(input("Chose the number of the task you want to delete: "))
    session.delete(rows[task-1])
    session.commit()
    print("The task has been deleted!")

while True:
    command = get_command()
    if command == 0:
        break
    elif command == 1:
        print_todays_tasks()
    elif command == 2:
        print_weeks_tasks()
    elif command == 3:
        print_all_tasks()
    elif command == 4:
        print_missed_tasks()
    elif command == 5:
        add_task()
    elif command == 6:
        delete_task()
print("Bye!")
