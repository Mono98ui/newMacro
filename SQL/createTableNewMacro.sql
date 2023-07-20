drop table if exists t_links_inv;
CREATE TABLE t_links_inv (
	id serial PRIMARY KEY,
	links varchar(500) UNIQUE NOT NULL,
	show_more varchar(50),
	inter smallint NOT NULL
);
