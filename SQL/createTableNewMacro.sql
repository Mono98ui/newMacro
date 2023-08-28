-- fusionner les liens ensemble dans une seule table si tout standardiser
--Supprimer Source of data
drop table if exists t_links_inv;
drop table if exists t_indicators_fred;

--Supprimer Economic Growth Investing
drop table if exists t_us_leading_index_1968;
drop table if exists t_building_permits_25;
drop table if exists t_chicago_pmi_38;
drop table if exists t_total_vehicle_sales_85;

drop table if exists t_us_leading_index_1968_gr;
drop table if exists t_building_permits_25_gr;
drop table if exists t_chicago_pmi_38_gr;
drop table if exists t_total_vehicle_sales_85_gr;


--Supprimer Data of FRED
drop table if exists t_M1SL;
drop table if exists t_M2SL;
drop table if exists t_BOGZ1FL893169105Q;
drop table if exists t_BUSLOANS;
drop table if exists t_TOTALSL;
drop table if exists t_INDPRO;
drop table if exists t_NOCDFSA066MSFRBPHI;
drop table if exists t_PCE;
drop table if exists t_PAYEMS;
drop table if exists t_AWHMAN;
drop table if exists t_USALOLITONOSTSAM;
drop table if exists t_HOUST;
drop table if exists t_PERMIT;
drop table if exists t_IC4WSA;
drop table if exists t_HTRUCKSSA;
drop table if exists t_BOGZ1FL145020011Q;
drop table if exists t_CPIAUCSL;
drop table if exists t_PPIACO;
drop table if exists t_AHETPI;
drop table if exists t_DTWEXM;
drop table if exists t_NFORBRES;
drop table if exists t_BOGNONBR;
drop table if exists t_REQRESNS;
drop table if exists t_T10YFF;
drop table if exists t_DTB3;
drop table if exists t_FEDFUNDS;
drop table if exists t_INTDSRUSM193N;
drop table if exists t_GACDFSA066MSFRBPHI;
drop table if exists t_TB3MS;

drop table if exists t_M1SL_gr;
drop table if exists t_M2SL_gr;
drop table if exists t_BOGZ1FL893169105Q_gr;
drop table if exists t_BUSLOANS_gr;
drop table if exists t_TOTALSL_gr;
drop table if exists t_INDPRO_gr;
drop table if exists t_NOCDFSA066MSFRBPHI_gr;
drop table if exists t_PCE_gr;
drop table if exists t_PAYEMS_gr;
drop table if exists t_AWHMAN_gr;
drop table if exists t_USALOLITONOSTSAM_gr;
drop table if exists t_HOUST_gr;
drop table if exists t_PERMIT_gr;
drop table if exists t_IC4WSA_gr;
drop table if exists t_HTRUCKSSA_gr;
drop table if exists t_BOGZ1FL145020011Q_gr;
drop table if exists t_CPIAUCSL_gr;
drop table if exists t_PPIACO_gr;
drop table if exists t_AHETPI_gr;
drop table if exists t_DTWEXM_gr;
drop table if exists t_NFORBRES_gr;
drop table if exists t_BOGNONBR_gr;
drop table if exists t_REQRESNS_gr;
drop table if exists t_T10YFF_gr;
drop table if exists t_DTB3_gr;
drop table if exists t_FEDFUNDS_gr;
drop table if exists t_INTDSRUSM193N_gr;
drop table if exists t_GACDFSA066MSFRBPHI_gr;
drop table if exists t_TB3MS_gr;

--Supprimer Economic Growth GrowthRate
drop table if exists t_us_leading_index_1968_gr;
drop table if exists t_building_permits_25_gr;
drop table if exists t_chicago_pmi_38_gr;
drop table if exists t_total_vehicle_sales_85_gr;

--Supprimer Status of process
drop table if exists t_status_process;

-- Creer Source of data
CREATE TABLE t_links_inv (
	id serial PRIMARY KEY,
	links varchar(500) NOT NULL,
	show_more varchar(50) NOT NULL,
	inter integer NOT NULL,
	t_name varchar(50),
	descr varchar(500) NOT NULL
);
CREATE TABLE t_indicators_fred (
	id varchar(100) PRIMARY KEY,
	descr varchar(500) NOT NULL,
	inter integer NOT NULL,
	t_name varchar(50)
);

--Creer Status of process
CREATE TABLE t_status_process (
	id serial PRIMARY KEY,
	process_name varchar(50) NOT NULL UNIQUE,
	status integer NOT NULL
);

--Creer Economic Growth Investing Raw data
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

--Creer Economic Growth Investing growth rate
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


--Creer FRED Raw data
CREATE TABLE t_M1SL (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_M2SL (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_BOGZ1FL893169105Q (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_BUSLOANS (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_TOTALSL (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_INDPRO (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_NOCDFSA066MSFRBPHI (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_PCE (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_PAYEMS (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_AWHMAN (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_USALOLITONOSTSAM (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_HOUST (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_PERMIT (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_IC4WSA (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_HTRUCKSSA (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_BOGZ1FL145020011Q (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_CPIAUCSL (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_PPIACO (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_AHETPI (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_DTWEXM (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_NFORBRES (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_BOGNONBR (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_REQRESNS (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_T10YFF (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_DTB3 (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_FEDFUNDS (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_INTDSRUSM193N (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_GACDFSA066MSFRBPHI (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);
CREATE TABLE t_TB3MS (
	date timestamp NOT NULL UNIQUE,
	value float NOT NULL
);


--Creer FRED growth rate
CREATE TABLE t_M1SL_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_M2SL_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_BOGZ1FL893169105Q_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_BUSLOANS_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);
CREATE TABLE t_TOTALSL_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_INDPRO_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_NOCDFSA066MSFRBPHI_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_PCE_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);
CREATE TABLE t_PAYEMS_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_AWHMAN_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_USALOLITONOSTSAM_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_HOUST_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);
CREATE TABLE t_PERMIT_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_IC4WSA_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_HTRUCKSSA_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_BOGZ1FL145020011Q_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);
CREATE TABLE t_CPIAUCSL_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_PPIACO_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_AHETPI_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_DTWEXM_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);
CREATE TABLE t_NFORBRES_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_BOGNONBR_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_REQRESNS_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_T10YFF_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);
CREATE TABLE t_DTB3_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_FEDFUNDS_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_INTDSRUSM193N_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_GACDFSA066MSFRBPHI_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null,
	PRIMARY KEY(date, intervalMonth)
);

CREATE TABLE t_TB3MS_gr (
	date timestamp NOT NULL,
	value float,
	intervalMonth integer NOT null ,
	PRIMARY KEY(date, intervalMonth)
);
