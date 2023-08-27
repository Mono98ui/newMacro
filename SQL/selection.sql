--Selection of tables in database
select * from t_links_inv;
select * from t_us_leading_index_1968;
select * from t_us_leading_index_1968_gr;
select * from t_building_permits_25;
select * from t_building_permits_25_gr;
select * from t_chicago_pmi_38;
select * from t_chicago_pmi_38_gr;
select * from t_total_vehicle_sales_85;
select * from t_total_vehicle_sales_85_gr;

select * from t_indicators_fred;

select * 
from t_us_leading_index_1968_gr t1
inner join t_us_leading_index_1968_gr t2
on t1.date = t2.date and t2.intervalmonth = 12
where t1.value is not NULL and t1.intervalmonth = 3 and  t2.value is not NULL
order by t1.date desc
limit 1;

select * from "t_links_inv" where length(show_more)>1
select * from t_us_leading_index_1968 offset 3;

select * from t_status_process;