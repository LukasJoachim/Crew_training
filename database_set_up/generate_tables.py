from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Time, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

# Define the PostgreSQL connection
engine = create_engine("postgresql+psycopg2://admin:password@localhost:5432/crew_training")
Base = declarative_base()

# Define the tables
class Date_Dim(Base):
    __tablename__ = 'date_dim'
    date_id = Column(Integer, primary_key=True, autoincrement=True)
    full_date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    month_name = Column(String(50), nullable=False)
    week = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    day_name = Column(String(50), nullable=False)
    is_weekend = Column(Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint('full_date', name='uq_full_date'),  
    )

class Ranks(Base):
    __tablename__ = 'ranks'
    rank_id = Column(Integer, primary_key=True, autoincrement=True)
    rank_name = Column(String(100), nullable=False)
    __table_args__ = (
        UniqueConstraint('rank_name', name='uq_rank'),  
    )

class Locations(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    alc = Column(String(100))
    longitude = Column(String(100))
    latitude = Column(String(100))
    __table_args__ = (
        UniqueConstraint('latitude','longitude', name='uq_location'),  
    )

class Qualifications(Base):
    __tablename__ = 'qualifications'
    qualification_id = Column(Integer, primary_key=True, autoincrement=True)
    qualification_name = Column(String(100), nullable=False)
    qualification_expiry_days = Column(Integer)
    __table_args__ = (
        UniqueConstraint('qualification_name', name='uq_qualifications'),  
    )

class TrainerLicenses(Base):
    __tablename__ = 'trainer_licenses'
    trainer_licenses_id = Column(Integer, primary_key=True, autoincrement=True)
    trainer_licenses_name = Column(String(100), nullable=False)
    __table_args__ = (
        UniqueConstraint('trainer_licenses_name', name='uq_licenses'),  
    )

class Courses(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(100), nullable=False)
    course_time = Column(Integer, nullable=False)
    max_course_attendees = Column(Integer, nullable=False)
    trainer_license_id = Column(Integer, ForeignKey('trainer_licenses.trainer_licenses_id'))
    qualification_id = Column(Integer, ForeignKey('qualifications.qualification_id'))
    __table_args__ = (
        UniqueConstraint('course_name', name='uq_course'),  
    )

class Employees(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    rank = Column(Integer, ForeignKey('ranks.rank_id'))
    location = Column(Integer, ForeignKey('locations.location_id'))
    __table_args__ = (
        UniqueConstraint('name', 'surname', name='uq_employee'),  
    )

class OffTimes(Base):
    __tablename__ = 'off_times'
    off_time_id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(Integer, ForeignKey('date_dim.date_id'), nullable=False)  
    to_date = Column(Integer, ForeignKey('date_dim.date_id'), nullable=False)    
    employee_id = Column(Integer, ForeignKey('employees.employee_id'), nullable=False) 
    __table_args__ = (
        UniqueConstraint('employee_id', 'from_date', 'to_date', name='uq_off_times'),  
    )

class CourseLocations(Base):
    __tablename__ = 'course_locations'
    course_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), primary_key=True)

class RankQualifications(Base):
    __tablename__ = 'rank_qualifications'
    rank_id = Column(Integer, ForeignKey('ranks.rank_id'), primary_key=True)
    qualification_id = Column(Integer, ForeignKey('qualifications.qualification_id'), primary_key=True)

class EmployeeTrainerLicenses(Base):
    __tablename__ = 'employee_trainer_licenses'
    trainer_licenses_id = Column(Integer, ForeignKey('trainer_licenses.trainer_licenses_id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'), primary_key=True)

class CourseEvents(Base):
    __tablename__ = 'course_events'
    
    course_event_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    course_event_start_date = Column(Integer, ForeignKey('date_dim.date_id'), nullable=False)
    course_event_end_date = Column(Integer, ForeignKey('date_dim.date_id'), nullable=False)
    event_location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=False)
    trainer_id = Column(Integer, ForeignKey('employees.employee_id'), nullable=False)
    num_attenders = Column(Integer, nullable=False)
    __table_args__ = (
        UniqueConstraint(trainer_id, course_id, course_event_start_date, course_event_end_date, name='uq_course_events'),  
    )

class CourseEventsEmployees(Base):
    __tablename__ = 'course_events_employees'

    course_event_id = Column(Integer, ForeignKey('course_events.course_event_id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'), primary_key=True)

# Create a function to create each table
def create_all_tables(engine):
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_all_tables(engine)

