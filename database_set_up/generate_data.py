import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

def create_date_dim(start_date:str, end_date:str) -> None:

    dates = pd.date_range(start=start_date, end=end_date)
    data = []

    for date in dates:
        data.append({
            'full_date': date,
            'year': date.year,
            'month': date.month,
            'month_name': date.strftime('%B'),
            'week': date.isocalendar()[1],
            'day': date.day,
            'day_of_week': date.dayofweek + 1,
            'day_name': date.strftime('%A'),
            'is_weekend': date.dayofweek >= 5
        })
    
    df = pd.DataFrame(data)
    df.to_sql('date_dim', engine, if_exists='append', index=False)

def create_ranks():
    ranks = ['First Officer', 'Captain', 'Cabin Service Director', 'Inflight Manager']
    df = pd.DataFrame(ranks, columns=['rank_name'])
    df.to_sql("ranks", engine, if_exists="append", index=False)

def create_locations():
    uk_cities = [
    {"country": "UK", "city": "London", "latitude": "51.5074", "longitude": "-0.1278", "alc": "LON"},
    {"country": "UK", "city": "Manchester", "latitude": "53.4808", "longitude": "-2.2426", "alc": "MAN"},
    {"country": "UK", "city": "Birmingham", "latitude": "52.4862", "longitude": "-1.8904", "alc": "BHM"},
    {"country": "UK", "city": "Liverpool", "latitude": "53.4084", "longitude": "-2.9916", "alc": "LIV"},
    {"country": "UK", "city": "Edinburgh", "latitude": "55.9533", "longitude": "-3.1883", "alc": "EDI"},
    {"country": "UK", "city": "Glasgow", "latitude": "55.8642", "longitude": "-4.2518", "alc": "GLA"},
    {"country": "UK", "city": "Leeds", "latitude": "53.7997", "longitude": "-1.5492", "alc": "LDS"},
    {"country": "UK", "city": "Bristol", "latitude": "51.4545", "longitude": "-2.5879", "alc": "BRS"},
    {"country": "UK", "city": "Sheffield", "latitude": "53.3811", "longitude": "-1.4701", "alc": "SHF"},
    {"country": "UK", "city": "Cardiff", "latitude": "51.4816", "longitude": "-3.1791", "alc": "CWL"},
    {"country": "UK", "city": "Luton", "latitude": "51.8787", "longitude": "-0.4200", "alc": "LTN"}
]
    df = pd.DataFrame(uk_cities)
    df.to_sql("locations", engine, if_exists="append", index=False)

def create_qualifications():
    aviation_qualifications = [
    {"qualification_name": "ATPL License", "qualification_expiry_days": 365},
    {"qualification_name": "Type Rating - Boeing 737", "qualification_expiry_days": 180},
    {"qualification_name": "Cabin Crew Safety Training", "qualification_expiry_days": 90},
    {"qualification_name": "Aircraft Maintenance Certification", "qualification_expiry_days": 180},
    {"qualification_name": "First Aid Certification", "qualification_expiry_days": 180},
    {"qualification_name": "Dangerous Goods Certification", "qualification_expiry_days": 365},
    ]
    df = pd.DataFrame(aviation_qualifications)
    df.to_sql("qualifications", engine, if_exists="append", index=False)

def create_trainer_licenses():
    trainer_licenses = ["Pilot Trainer License", "Cabin Crew Safety Trainer License", "Aircraft Maintenance Trainer License"]
    df = pd.DataFrame(trainer_licenses, columns=["trainer_licenses_name"])
    df.to_sql("trainer_licenses", engine, if_exists="append", index=False)

def create_courses():
    qualifications_courses = [
    {"trainer_license_id": 1, "course_name": "ATPL Training Course", "course_time": 3, "max_course_attendees": 5,"qualification_id": 1},
    {"trainer_license_id": 1, "course_name": "Boeing 737 Type Rating Course", "course_time": 2, "max_course_attendees": 10,"qualification_id": 2},
    {"trainer_license_id": 2, "course_name": "Cabin Crew Safety Course", "course_time": 1, "max_course_attendees": 20,"qualification_id": 3},
    {"trainer_license_id": 3, "course_name": "Aircraft Maintenance Course", "course_time": 4, "max_course_attendees": 5,"qualification_id": 4},
    {"trainer_license_id": 2, "course_name": "First Aid Training Course", "course_time": 1, "max_course_attendees": 20,"qualification_id": 5},
    {"trainer_license_id": 2, "course_name": "Dangerous Goods Handling Course", "course_time": 2, "max_course_attendees": 10,"qualification_id": 6}
    ]

    df = pd.DataFrame(qualifications_courses)
    df.to_sql("courses", engine, if_exists="append", index=False)

def create_employees():
    location_ids = [loc[0] for loc in session.execute(text('SELECT location_id FROM locations')).fetchall()]
    rank_distribution = {
                        "First Officer": {"count": 25, "rank_id": 1},
                        "Captain": {"count": 20, "rank_id": 2},
                        "Cabin Service Director": {"count": 20, "rank_id": 3},
                        "Inflight Manager": {"count": 35, "rank_id": 4}
                    }
    fake = Faker()
    employees = []
    surnames = set()

    while len(surnames) < 120:
        surnames.add(fake.last_name())
    for rank, details in rank_distribution.items():
        for _ in range(details["count"]):
            employee = {
                "name": fake.first_name(),
                "surname": surnames.pop(),
                "rank": details["rank_id"],
                "location": random.choice(location_ids)
            }
            employees.append(employee)
    
    df = pd.DataFrame(employees)
    df.to_sql("employees", engine, if_exists="append", index=False)

def create_off_times():
  
    employee_ids = [row[0] for row in session.execute(text("SELECT employee_id FROM employees")).fetchall()]
    year_dates = session.execute(text("SELECT DISTINCT year FROM date_dim")).fetchall()
    year_dates = [row[0] for row in year_dates]

    dates_by_year = {}
    for year in year_dates:
        dates = [row[0] for row in session.execute(
            text(f"SELECT date_id, full_date FROM date_dim WHERE year = {year} AND is_weekend = FALSE ORDER BY full_date")
        ).fetchall()]
        dates_by_year[year] = dates

    # Generate off_times for each employee
    off_time_entries = []
    for employee_id in employee_ids:
        for year, date_ids in dates_by_year.items():
            remaining_days = 25  
            used_days = set()  

            while remaining_days > 0:
                # Randomly select a chunk of off-days
                off_time_length = min(random.randint(5, 10), remaining_days)
                valid_start_date = None

                for i in range(len(date_ids) - off_time_length):
                    potential_range = date_ids[i:i + off_time_length]
                    if all(day not in used_days for day in potential_range):
                        valid_start_date = potential_range[0]
                        break

                if not valid_start_date:
                    raise ValueError(f"Cannot allocate 25 days for employee {employee_id} in year {year}.")

                start_index = date_ids.index(valid_start_date)
                off_time_range = date_ids[start_index:start_index + off_time_length]
                used_days.update(off_time_range)

                off_time_entries.append({
                    "employee_id": employee_id,
                    "from_date": off_time_range[0],
                    "to_date": off_time_range[-1]
                })

                remaining_days -= off_time_length

    df = pd.DataFrame(off_time_entries)
    df.to_sql("off_times", engine, if_exists="append", index=False)

def create_course_locations():

    course_ids = [row[0] for row in session.execute(text("SELECT course_id FROM courses")).fetchall()]
    location_ids = [row[0] for row in session.execute(text("SELECT location_id FROM locations")).fetchall()]

    course_location_entries = []
    for course_id in course_ids:
        locations_list = random.sample(location_ids, random.randint(1, 3))
        for location_id in range(len(locations_list)):  
                course_location_entries.append({
                    "course_id": course_id,
                    "location_id": locations_list[location_id]
                })
  
    df = pd.DataFrame(course_location_entries)
    df.to_sql("course_locations", engine, if_exists="append", index=False)

def create_rank_qualifications():

    rank_qualification_entries = [
        {"rank_id": 1, "qualification_id":1},
        {"rank_id": 1, "qualification_id":2},
        {"rank_id": 1, "qualification_id":4},
        {"rank_id": 1, "qualification_id":5},
        {"rank_id": 2, "qualification_id":1},
        {"rank_id": 2, "qualification_id":2},
        {"rank_id": 2, "qualification_id":4},
        {"rank_id": 2, "qualification_id":5},
        {"rank_id": 3, "qualification_id":3},
        {"rank_id": 3, "qualification_id":5},
        {"rank_id": 3, "qualification_id":6},
        {"rank_id": 4, "qualification_id":3},
        {"rank_id": 4, "qualification_id":5},
        {"rank_id": 4, "qualification_id":6}

    ]
   
    df = pd.DataFrame(rank_qualification_entries)
    df.to_sql("rank_qualifications", engine, if_exists="append", index=False)

def create_employee_trainer_licenses():
    employee_ids = [row[0] for row in session.execute(text("SELECT employee_id FROM employees")).fetchall()]
    trainer_license_ids = [row[0] for row in session.execute(text("SELECT trainer_licenses_id FROM trainer_licenses")).fetchall()]

    selected_employees = random.sample(employee_ids, 10)

    #Ensure all licenses are covered by at least one trainer
    license_coverage = {license_id: False for license_id in trainer_license_ids} 
    employee_trainer_license_entries = []

    # Assign licenses to trainers ensuring coverage
    for employee_id in selected_employees:
        num_licenses = random.sample(range(1,4), random.randint(1, 3))
        for i in range(len(num_licenses)):
            employee_trainer_license_entries.append({
                "trainer_licenses_id": num_licenses[i],
                "employee_id": employee_id
            })

    df = pd.DataFrame(employee_trainer_license_entries)
    df.to_sql("employee_trainer_licenses", engine, if_exists="append", index=False)



# create_course_events_employees
def fetch_courses():
    return session.execute(text("""
        SELECT c.course_id, c.course_time, c.max_course_attendees, c.trainer_license_id
        FROM courses c
    """)).fetchall()

def fetch_course_locations():
    course_locations = session.execute(text("""
        SELECT cl.course_id, cl.location_id
        FROM course_locations cl
    """)).fetchall()

    # Create a mapping of course_id to available locations
    course_location_map = {}
    for cl in course_locations:
        if cl.course_id not in course_location_map:
            course_location_map[cl.course_id] = []
        course_location_map[cl.course_id].append(cl.location_id)
    return course_location_map

def fetch_past_dates():
    return [row[0] for row in session.execute(
        text("SELECT date_id FROM date_dim WHERE is_weekend = FALSE AND full_date < CURRENT_DATE")
    ).fetchall()]

def fetch_trainers():
    trainers = session.execute(text("""
        SELECT etl.employee_id, etl.trainer_licenses_id
        FROM employee_trainer_licenses etl
    """)).fetchall()

    # Create a mapping of trainers to their licenses
    trainer_license_map = {}
    for trainer in trainers:
        trainer_id = trainer.employee_id
        license_id = trainer.trainer_licenses_id
        if trainer_id not in trainer_license_map:
            trainer_license_map[trainer_id] = []
        trainer_license_map[trainer_id].append(license_id)
    return trainer_license_map

def is_trainer_available(trainer_id, start_date, end_date):
    # Check if the trainer has off-times
    off_times = session.execute(text("""
        SELECT 1
        FROM off_times
        WHERE employee_id = :trainer_id
          AND (from_date <= :end_date AND to_date >= :start_date)
    """), {"trainer_id": trainer_id, "start_date": start_date, "end_date": end_date}).fetchall()

    # Check if the trainer is already assigned to another course at the same time
    overlapping_courses = session.execute(text("""
        SELECT 1
        FROM course_events
        WHERE trainer_id = :trainer_id
          AND (course_event_start_date <= :end_date AND course_event_end_date >= :start_date)
    """), {"trainer_id": trainer_id, "start_date": start_date, "end_date": end_date}).fetchall()

    return not off_times and not overlapping_courses

def is_duplicate_event(trainer_id, course_id, start_date, end_date):
    duplicate_event = session.execute(text("""
        SELECT 1
        FROM course_events
        WHERE trainer_id = :trainer_id
          AND course_id = :course_id
          AND course_event_start_date = :start_date
          AND course_event_end_date = :end_date
    """), {
        "trainer_id": trainer_id,
        "course_id": course_id,
        "start_date": start_date,
        "end_date": end_date
    }).fetchall()
    return bool(duplicate_event)

def generate_course_events(num_events, courses, course_location_map, past_date_ids, trainer_license_map):
    course_events = []

    for _ in range(num_events):
        # Randomly select a course
        course = random.choice(courses)
        course_id = course.course_id
        course_time = course.course_time
        max_attendees = course.max_course_attendees
        trainer_license_id = course.trainer_license_id

        # Select a start date
        start_date = random.choice(past_date_ids)

        # Calculate the end date
        end_date_index = min(past_date_ids.index(start_date) + course_time - 1, len(past_date_ids) - 1)
        end_date = past_date_ids[end_date_index]

        # Select a valid location
        if course_id not in course_location_map or not course_location_map[course_id]:
            print(f"Skipping course_id {course_id}: No valid locations available.")
            continue
        event_location_id = random.choice(course_location_map[course_id])

        # Select a trainer
        qualified_trainers = [
            trainer_id for trainer_id, licenses in trainer_license_map.items()
            if trainer_license_id in licenses
        ]
        available_trainers = [
            trainer_id for trainer_id in qualified_trainers
            if is_trainer_available(trainer_id, start_date, end_date)
        ]

        if not available_trainers:
            print(f"Skipping course_id {course_id}: No available trainers.")
            continue
        trainer_id = random.choice(available_trainers)

        # Check for duplicates
        if is_duplicate_event(trainer_id, course_id, start_date, end_date):
            print(f"Skipping duplicate event for trainer_id {trainer_id} and course_id {course_id}.")
            continue

        # Determine the number of attendees
        num_attendees = random.randint(5, max_attendees)

        # Add the course event
        course_events.append({
            "course_id": course_id,
            "course_event_start_date": start_date,
            "course_event_end_date": end_date,
            "event_location_id": event_location_id,
            "trainer_id": trainer_id,
            "num_attenders": num_attendees
        })

    return course_events

def create_course_events(num_events):
    courses = fetch_courses()
    course_location_map = fetch_course_locations()
    past_date_ids = fetch_past_dates()
    trainer_license_map = fetch_trainers()

    course_events = generate_course_events(num_events, courses, course_location_map, past_date_ids, trainer_license_map)

    # Insert course events into the database
    if course_events:
        df = pd.DataFrame(course_events)
        df.to_sql("course_events", engine, if_exists="append", index=False)
        print(f"Created {len(course_events)} course events successfully!")


# create_course_events_employees
def fetch_course_events():
    return session.execute(text("""
        SELECT ce.course_event_id, ce.course_id, ce.course_event_start_date, ce.course_event_end_date, ce.trainer_id, ce.num_attenders
        FROM course_events ce
    """)).fetchall()

def fetch_employees_and_qualifications():
    return session.execute(text("""
        SELECT e.employee_id, rq.qualification_id, q.qualification_expiry_days
        FROM employees e
        JOIN ranks r ON e.rank = r.rank_id
        JOIN rank_qualifications rq ON r.rank_id = rq.rank_id
        JOIN qualifications q ON rq.qualification_id = q.qualification_id
    """)).fetchall()

def fetch_employee_off_times():
    off_times = session.execute(text("""
        SELECT ot.employee_id, ot.from_date, ot.to_date
        FROM off_times ot
    """)).fetchall()

    # Create a mapping of employee off-times
    employee_off_times = {}
    for off_time in off_times:
        employee_id = off_time.employee_id
        if employee_id not in employee_off_times:
            employee_off_times[employee_id] = []
        employee_off_times[employee_id].append((off_time.from_date, off_time.to_date))
    return employee_off_times

def get_qualified_employees(course_id, employees, trainer_id, start_date, end_date, employee_off_times):
    qualified_employees = [
        emp for emp in employees
        if emp.qualification_id == session.execute(text("""
            SELECT qualification_id FROM courses WHERE course_id = :course_id
        """), {'course_id': course_id}).scalar()
        and emp.employee_id != trainer_id  # Exclude the trainer
        and not any(
            start_date <= off[1] and end_date >= off[0]  # Check overlap with off-time
            for off in employee_off_times.get(emp.employee_id, [])
        )
    ]
    return qualified_employees

def filter_eligible_employees(qualified_employees, course_id, start_date):
    eligible_employees = []
    for emp in qualified_employees:
        past_courses = session.execute(text("""
            SELECT MAX(ce.course_event_end_date) AS latest_date
            FROM course_events ce
            JOIN course_events_employees cee ON ce.course_event_id = cee.course_event_id
            WHERE cee.employee_id = :employee_id AND ce.course_id = :course_id
        """), {'employee_id': emp.employee_id, 'course_id': course_id}).fetchone()

        latest_date = past_courses.latest_date

        if latest_date is None:
            # If no past course, the employee is eligible
            eligible_employees.append(emp)
        else:
            # Check if the qualification is expired
            expiry_date = latest_date + timedelta(days=emp.qualification_expiry_days)
            if expiry_date < start_date:
                eligible_employees.append(emp)

    return eligible_employees

def assign_employees_to_course_event(course_event, employees, employee_off_times):
    course_event_id = course_event.course_event_id
    course_id = course_event.course_id
    start_date = course_event.course_event_start_date
    end_date = course_event.course_event_end_date
    trainer_id = course_event.trainer_id
    num_attendees = course_event.num_attenders

    qualified_employees = get_qualified_employees(course_id, employees, trainer_id, start_date, end_date, employee_off_times)
    eligible_employees = filter_eligible_employees(qualified_employees, course_id, start_date)

    # Shuffle employees to ensure random allocation
    random.shuffle(eligible_employees)

    # Check if there are enough employees
    if len(eligible_employees) < num_attendees:
        print(f"Insufficient qualified employees for course_event_id {course_event_id}.")
        return []

    return eligible_employees[:num_attendees]

def create_course_events_employees():
    course_events = fetch_course_events()
    employees = fetch_employees_and_qualifications()
    employee_off_times = fetch_employee_off_times()

    course_event_employee_entries = []
    for course_event in course_events:
        assigned_employees = assign_employees_to_course_event(course_event, employees, employee_off_times)
        for employee in assigned_employees:
            course_event_employee_entries.append({
                "course_event_id": course_event.course_event_id,
                "employee_id": employee.employee_id
            })

    # Insert course event employee assignments into the database
    df = pd.DataFrame(course_event_employee_entries)
    df.to_sql("course_events_employees", engine, if_exists="append", index=False)

if __name__ == "__main__":

    engine = create_engine("postgresql+psycopg2://admin:password@localhost:5432/crew_training")
    Session = sessionmaker(bind=engine)
    session = Session()

    create_date_dim('2020-01-01', '2024-12-01')
    create_ranks()
    create_locations()
    create_qualifications()
    create_trainer_licenses()
    create_courses()
    create_employees()
    create_off_times()
    create_course_locations()
    create_rank_qualifications()
    create_employee_trainer_licenses()
    create_course_events(100)
    create_course_events_employees()


