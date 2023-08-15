drop table if exists t_links_inv;
--Economic Growth
drop table if exists t_us_leading_index_1968;
drop table if exists t_building_permits_25;
drop table if exists t_chicago_pmi_38;
drop table if exists t_total_vehicle_sales_85;

CREATE TABLE t_links_inv (
	id serial PRIMARY KEY,
	links varchar(500) NOT NULL,
	show_more varchar(50) NOT NULL,
	inter integer NOT NULL,
	t_name varchar(50)
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


