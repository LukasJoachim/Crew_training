
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    rank INT REFERENCES ranks(rank_id),
    location INT REFERENCES locations(location_id)
);
COMMENT ON COLUMN employees.employee_id IS 'Unique ID for the employee';
COMMENT ON COLUMN employees.name IS 'First Name of the employee';
COMMENT ON COLUMN employees.surname IS 'Last name of the employee';
COMMENT ON COLUMN employees.rank IS 'Reference ID to the rank table';
COMMENT ON COLUMN employees.location IS 'Reference ID to the location table';

CREATE TABLE ranks (
    rank_id SERIAL PRIMARY KEY,
    rank_name VARCHAR(100) NOT NULL
);
COMMENT ON COLUMN ranks.rank_id IS 'Unique ID for the Rank';
COMMENT ON COLUMN ranks.rank_name IS 'Name of the Rank (First Officer, Captain, etc.)';


CREATE TABLE rank_qualifications (
    rank_id INT NOT NULL REFERENCES ranks(rank_id),
    qualification_id INT NOT NULL REFERENCES qualifications(qualification_id),
    PRIMARY KEY (rank_id, qualification_id)
);
COMMENT ON COLUMN rank_qualifications.rank_id IS 'References to the rank table';
COMMENT ON COLUMN rank_qualifications.qualification_id IS 'References to the Qualification table';


CREATE TABLE qualifications (
    qualification_id SERIAL PRIMARY KEY,
    qualification_name VARCHAR(100) NOT NULL,
    qualification_expiry_days INT
);
COMMENT ON COLUMN qualifications.qualification_id IS 'Unique ID for the Qualification';
COMMENT ON COLUMN qualifications.qualification_name IS 'Name of the Qualification';
COMMENT ON COLUMN qualifications.qualification_expiry_days IS 'Number of days before the qualification expires';


CREATE TABLE trainer_licenses (
    trainer_licenses_id SERIAL PRIMARY KEY,
    trainer_licenses_name VARCHAR(100) NOT NULL
);
COMMENT ON COLUMN trainer_licenses.trainer_licenses_id IS 'Unique ID for the trainer License';
COMMENT ON COLUMN trainer_licenses.trainer_licenses_name IS 'Name of the trainer license';


CREATE TABLE employee_trainer_licenses (
    trainer_licenses_id INT NOT NULL REFERENCES trainer_licenses(trainer_licenses_id),
    employee_id INT NOT NULL REFERENCES employees(employee_id),
    PRIMARY KEY (trainer_licenses_id, employee_id)
);
COMMENT ON COLUMN employee_trainer_licenses.trainer_licenses_id IS 'References to the trainer_licenses table';
COMMENT ON COLUMN employee_trainer_licenses.employee_id IS 'References to the employee table';

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    alc VARCHAR(100),
    longitude VARCHAR(100),
    latitude VARCHAR(100)
);
COMMENT ON COLUMN locations.location_id IS 'Unique ID for the location';
COMMENT ON COLUMN locations.country IS 'Country of the location';
COMMENT ON COLUMN locations.city IS 'City of the location';
COMMENT ON COLUMN locations.alc IS 'Airline Code of the location';
COMMENT ON COLUMN locations.longitude IS 'Longitude of the location';
COMMENT ON COLUMN locations.latitude IS 'Latitude of the location';


CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_time INT NOT NULL,
    max_course_attendees INT NOT NULL,
    trainer_license_id INT REFERENCES trainer_licenses(trainer_licenses_id),
    qualification_id INT REFERENCES qualifications(qualification_id)
);
COMMENT ON COLUMN courses.course_id IS 'Unique ID for the course';
COMMENT ON COLUMN courses.course_name IS 'Name of the course';
COMMENT ON COLUMN courses.course_time IS 'Duration of the course in days';
COMMENT ON COLUMN courses.max_course_attendees IS 'Maximum number of attendees for the course';
COMMENT ON COLUMN courses.trainer_license_id IS 'References to the trainer_licenses table';
COMMENT ON COLUMN courses.qualification_id IS 'References to the qualifications table';

CREATE TABLE course_locations (
    course_id INT NOT NULL REFERENCES courses(course_id),
    location_id INT NOT NULL REFERENCES locations(location_id),
    PRIMARY KEY (course_id, location_id)
);
COMMENT ON COLUMN course_locations.course_id IS 'References to the courses table';
COMMENT ON COLUMN course_locations.location_id IS 'References to the location table';

CREATE TABLE course_events (
    course_event_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(course_id),
    course_event_start_date DATE NOT NULL,
    course_event_end_date DATE NOT NULL,
    event_location_id INT NOT NULL REFERENCES locations(location_id),
    trainer_id INT REFERENCES employees(employee_id),
    num_attenders INT
);
COMMENT ON COLUMN course_events.course_event_id IS 'Unique ID for the course event';
COMMENT ON COLUMN course_events.course_id IS 'References to the courses table';
COMMENT ON COLUMN course_events.course_event_start_date IS 'Start date of the course event';
COMMENT ON COLUMN course_events.course_event_end_date IS 'End date of the course event';
COMMENT ON COLUMN course_events.event_location_id IS 'References to the location table';
COMMENT ON COLUMN course_events.trainer_id IS 'References to the employee table';
COMMENT ON COLUMN course_events.num_attenders IS 'Number of attenders for the course event';
