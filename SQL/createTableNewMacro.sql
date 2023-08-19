-- fusionner les liens ensemble dans une seule table si tout standardiser
drop table if exists t_links_inv;
--Economic Growth
drop table if exists t_us_leading_index_1968;
drop table if exists t_building_permits_25;
drop table if exists t_chicago_pmi_38;
drop table if exists t_total_vehicle_sales_85;

--Econimic Growth GrowthRate
drop table if exists t_us_leading_index_1968_gr;
drop table if exists t_building_permits_25_gr;
drop table if exists t_chicago_pmi_38_gr;
drop table if exists t_total_vehicle_sales_85_gr;

--Status scrapper
drop table if exists t_status_scraper;


CREATE TABLE t_links_inv (
	id serial PRIMARY KEY,
	links varchar(500) NOT NULL,
	show_more varchar(50) NOT NULL,
	inter integer NOT NULL,
	t_name varchar(50)
);
CREATE TABLE t_status_scraper (
	id serial PRIMARY KEY,
	scraper_name varchar(50) NOT NULL UNIQUE,
	status integer NOT NULL
);


CREATE TABLE t_us_leading_index_1968 (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);

CREATE TABLE t_building_permits_25 (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);

CREATE TABLE t_chicago_pmi_38 (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);

CREATE TABLE t_total_vehicle_sales_85 (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);


CREATE TABLE t_us_leading_index_1968_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_building_permits_25_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_chicago_pmi_38_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_total_vehicle_sales_85_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);


