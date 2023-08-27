
--Autorisation of user into the database
REVOKE ALL ON DATABASE "MacroDB" FROM public;  
GRANT CONNECT ON DATABASE "MacroDB" TO "Test_autorization_group";

GRANT USAGE ON SCHEMA public TO "Test_autorization_group";

GRANT ALL ON ALL TABLES IN SCHEMA public TO "Test_autorization_group";
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO "Test_autorization_group"; -- don't forget those
GRANT "Test_autorization_group" TO "Test_user";




