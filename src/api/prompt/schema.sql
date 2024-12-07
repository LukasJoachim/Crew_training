
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    rank INT REFERENCES ranks(rank_id),
    location INT REFERENCES locations(location_id)
);

CREATE TABLE ranks (
    rank_id SERIAL PRIMARY KEY,
    rank_name VARCHAR(100) NOT NULL
);

CREATE TABLE rank_qualifications (
    rank_id INT NOT NULL REFERENCES ranks(rank_id),
    qualification_id INT NOT NULL REFERENCES qualifications(qualification_id),
    PRIMARY KEY (rank_id, qualification_id)
);


CREATE TABLE qualifications (
    qualification_id SERIAL PRIMARY KEY,
    qualification_name VARCHAR(100) NOT NULL,
    qualification_expiry_days INT
);


CREATE TABLE trainer_licenses (
    trainer_licenses_id SERIAL PRIMARY KEY,
    trainer_licenses_name VARCHAR(100) NOT NULL
);


CREATE TABLE employee_trainer_licenses (
    trainer_licenses_id INT NOT NULL REFERENCES trainer_licenses(trainer_licenses_id),
    employee_id INT NOT NULL REFERENCES employees(employee_id),
    PRIMARY KEY (trainer_licenses_id, employee_id)
);

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    alc VARCHAR(100),
    longitude VARCHAR(100),
    latitude VARCHAR(100)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_time INT NOT NULL,
    max_course_attendees INT NOT NULL,
    trainer_license_id INT REFERENCES trainer_licenses(trainer_licenses_id),
    qualification_id INT REFERENCES qualifications(qualification_id)
);

CREATE TABLE course_locations (
    course_id INT NOT NULL REFERENCES courses(course_id),
    location_id INT NOT NULL REFERENCES locations(location_id),
    PRIMARY KEY (course_id, location_id)
);

CREATE TABLE course_events (
    course_event_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(course_id),
    course_event_start_date DATE NOT NULL,
    course_event_end_date DATE NOT NULL,
    event_location_id INT NOT NULL REFERENCES locations(location_id),
    trainer_id INT REFERENCES employees(employee_id),
    num_attenders INT
);
