
-- ********************************************************************

-- ***** BYOD UNCOMMENT *****
-- UNCOMMENT if running the script on your own device
-- 
-- DROP SCHEMA IF EXISTS hr;
-- CREATE SCHEMA IF NOT EXISTS  hr;
-- USE  hr ;
-- 
-- ***** END UNCOMMENT *****


SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 ;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 ;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO';
SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 ;

--
-- Table structure for table  countries 
--

DROP TABLE IF EXISTS  countries ;

CREATE TABLE  countries  (
   country_id  char(2) NOT NULL,
   country_name  varchar(40) DEFAULT NULL,
   region_id  int(11) NOT NULL,
  PRIMARY KEY ( country_id ),
  KEY  countr_reg_fk  ( region_id ),
  CONSTRAINT  countr_reg_fk  FOREIGN KEY ( region_id ) REFERENCES  regions  ( region_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Inserting data for table  countries 
--

LOCK TABLES  countries  WRITE;
ALTER TABLE  countries  DISABLE KEYS;
INSERT INTO  countries  VALUES ('AR','Argentina',2),('AU','Australia',3),('BE','Belgium',1),('BR','Brazil',2),('CA','Canada',2),('CH','Switzerland',1),('CN','China',3),('DE','Germany',1),('DK','Denmark',1),('EG','Egypt',4),('FR','France',1),('IL','Israel',4),('IN','India',3),('IT','Italy',1),('JP','Japan',3),('KW','Kuwait',4),('ML','Malaysia',3),('MX','Mexico',2),('NG','Nigeria',4),('NL','Netherlands',1),('SG','Singapore',3),('UK','United Kingdom',1),('US','United States of America',2),('ZM','Zambia',4),('ZW','Zimbabwe',4);
ALTER TABLE  countries  ENABLE KEYS;
UNLOCK TABLES;

--
-- Table structure for table  departments 
--

DROP TABLE IF EXISTS  departments ;

CREATE TABLE  departments  (
   department_id  int(4) NOT NULL,
   department_name  varchar(30) NOT NULL,
   manager_id  int(6) DEFAULT NULL,
   location_id  int(4) NOT NULL,
  PRIMARY KEY ( department_id ),
  UNIQUE KEY  dept_id_pk  ( department_id ),
  KEY  dept_loc_fk  ( location_id ),
  KEY  dept_mgr_fk  ( manager_id ),
  CONSTRAINT  dept_loc_fk  FOREIGN KEY ( location_id ) REFERENCES  locations  ( location_id ),
  CONSTRAINT  dept_mgr_fk  FOREIGN KEY ( manager_id ) REFERENCES  staff  ( staff_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Inserting data for table  departments 
--

LOCK TABLES  departments  WRITE;
ALTER TABLE  departments  DISABLE KEYS;
INSERT INTO  departments  VALUES (10,'Administration',200,1700),(20,'Marketing',201,1800),(30,'Purchasing',114,1700),(40,'Human Resources',203,2400),(50,'Shipping',121,1500),(60,'IT',103,1400),(70,'Public Relations',204,2700),(80,'Sales',145,2500),(90,'Executive',100,1700),(100,'Finance',108,1700),(110,'Accounting',205,1700),(120,'Treasury',NULL,1700),(130,'Corporate Tax',NULL,1700),(140,'Control And Credit',NULL,1700),(150,'Shareholder Services',NULL,1700),(160,'Benefits',NULL,1700),(170,'Manufacturing',NULL,1700),(180,'Construction',NULL,1700),(190,'Contracting',NULL,1700),(200,'Operations',NULL,1700),(210,'IT Support',NULL,1700),(220,'NOC',NULL,1700),(230,'IT Helpdesk',NULL,1700),(240,'Government Sales',NULL,1700),(250,'Retail Sales',NULL,1700),(260,'Recruiting',NULL,1700),(270,'Payroll',NULL,1700);
ALTER TABLE  departments  ENABLE KEYS;
UNLOCK TABLES;

-- Table structure for table  staff 
--

DROP TABLE IF EXISTS  staff ;

CREATE TABLE  staff  (
   staff_id  int(6) NOT NULL,
   first_name  varchar(20) DEFAULT NULL,
   last_name  varchar(25) NOT NULL,
   email  varchar(25) NOT NULL,
   phone_number  varchar(20) DEFAULT NULL,
   hire_date  date NOT NULL,
   job_id  varchar(10) NOT NULL,
   salary  decimal(8,2) DEFAULT NULL,
   commission_pct  decimal(2,2) DEFAULT NULL,
   supervisor_id  int(6) DEFAULT NULL,
   department_id  int(4) DEFAULT NULL,
  PRIMARY KEY ( staff_id ),
  UNIQUE KEY  emp_emp_id_pk  ( staff_id ),
  KEY  emp_dept_fk  ( department_id ),
  KEY  emp_job_fk  ( job_id ),
  KEY  emp_manager_fk  ( supervisor_id ),
  CONSTRAINT  emp_dept_fk  FOREIGN KEY ( department_id ) REFERENCES  departments  ( department_id ),
  CONSTRAINT  emp_job_fk  FOREIGN KEY ( job_id ) REFERENCES  jobs  ( job_id ),
  CONSTRAINT  emp_manager_fk  FOREIGN KEY ( supervisor_id ) REFERENCES  staff  ( staff_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Inserting data for table  staff 
--

LOCK TABLES  staff  WRITE;
/*!40000 ALTER TABLE  staff  DISABLE KEYS */;
INSERT INTO  staff  VALUES (100,'Steven','King','SKING','515.123.4567','2003-06-17','AD_PRES',240000.00,NULL,NULL,90),(101,'Neena','Kochhar','NKOCHHAR','515.123.4568','2005-09-21','AD_VP',170000.00,NULL,100,90),(102,'Lex','De Haan','LDEHAAN','515.123.4569','2001-01-13','AD_VP',170000.00,NULL,100,90),(103,'Alexander','Hunold','AHUNOLD','590.423.4567','2006-01-03','IT_PROG',90000.00,NULL,102,60),(104,'Bruce','Ernst','BERNST','590.423.4568','2007-05-21','IT_PROG',60000.00,NULL,103,60),(105,'David','Austin','DAUSTIN','590.423.4569','2005-06-25','IT_PROG',48000.00,NULL,103,60),(106,'Valli','Pataballa','VPATABAL','590.423.4560','2006-02-05','IT_PROG',48000.00,NULL,103,60),(107,'Diana','Lorentz','DLORENTZ','590.423.5567','2007-02-07','IT_PROG',42000.00,NULL,103,60),(108,'Nancy','Greenberg','NGREENBE','515.124.4569','2002-08-17','FI_MGR',120080.00,NULL,101,100),(109,'Daniel','Faviet','DFAVIET','515.124.4169','2002-08-16','FI_ACCOUNT',90000.00,NULL,108,100),(110,'John','Chen','JCHEN','515.124.4269','2005-09-28','FI_ACCOUNT',82000.00,NULL,108,100),(111,'Ismael','Sciarra','ISCIARRA','515.124.4369','2005-09-30','FI_ACCOUNT',77000.00,NULL,108,100),(112,'Jose Manuel','Urman','JMURMAN','515.124.4469','2006-03-07','FI_ACCOUNT',78000.00,NULL,108,100),(113,'Luis','Popp','LPOPP','515.124.4567','2007-12-07','FI_ACCOUNT',69000.00,NULL,108,100),(114,'Den','Raphaely','DRAPHEAL','515.127.4561','2002-12-07','PU_MAN',110000.00,NULL,100,30),(115,'Alexander','Khoo','AKHOO','515.127.4562','2003-05-18','PU_CLERK',31000.00,NULL,114,30),(116,'Shelli','Baida','SBAIDA','515.127.4563','2005-12-24','PU_CLERK',29000.00,NULL,114,30),(117,'Sigal','Tobias','STOBIAS','515.127.4564','2005-07-24','PU_CLERK',28000.00,NULL,114,30),(118,'Guy','Himuro','GHIMURO','515.127.4565','2006-11-15','PU_CLERK',26000.00,NULL,114,30),(119,'Karen','Colmenares','KCOLMENA','515.127.4566','2007-08-10','PU_CLERK',35000.00,NULL,114,30),(120,'Matthew','Weiss','MWEISS','650.123.1234','2004-07-18','ST_MAN',80000.00,NULL,100,50),(121,'Adam','Fripp','AFRIPP','650.123.2234','2005-04-10','ST_MAN',82000.00,NULL,100,50),(122,'Payam','Kaufling','PKAUFLIN','650.123.3234','2003-05-01','ST_MAN',79000.00,NULL,100,50),(123,'Shanta','Vollman','SVOLLMAN','650.123.4234','2005-10-10','ST_MAN',65000.00,NULL,100,50),(124,'Kevin','Mourgos','KMOURGOS','650.123.5234','2007-11-16','ST_MAN',58000.00,NULL,100,50),(125,'Julia','Nayer','JNAYER','650.124.1214','2005-07-16','ST_CLERK',32000.00,NULL,120,50),(126,'Irene','Mikkilineni','IMIKKILI','650.124.1224','2006-09-28','ST_CLERK',27000.00,NULL,120,50),(127,'James','Landry','JLANDRY','650.124.1334','2007-01-14','ST_CLERK',24000.00,NULL,120,50),(128,'Steven','Markle','SMARKLE','650.124.1434','2008-03-08','ST_CLERK',22000.00,NULL,120,50),(129,'Laura','Bissot','LBISSOT','650.124.5234','2005-08-20','ST_CLERK',33000.00,NULL,121,50),(130,'Mozhe','Atkinson','MATKINSO','650.124.6234','2005-10-30','ST_CLERK',28000.00,NULL,121,50),(131,'James','Marlow','JAMRLOW','650.124.7234','2005-02-16','ST_CLERK',35000.00,NULL,121,50),(132,'TJ','Olson','TJOLSON','650.124.8234','2007-04-10','ST_CLERK',21000.00,NULL,121,50),(133,'Jason','Mallin','JMALLIN','650.127.1934','2004-06-14','ST_CLERK',33000.00,NULL,122,50),(134,'Michael','Rogers','MROGERS','650.127.1834','2006-08-26','ST_CLERK',29000.00,NULL,122,50),(135,'Ki','Gee','KGEE','650.127.1734','2007-12-12','ST_CLERK',24000.00,NULL,122,50),(136,'Hazel','Philtanker','HPHILTAN','650.127.1634','2008-02-06','ST_CLERK',22000.00,NULL,122,50),(137,'Renske','Ladwig','RLADWIG','650.121.1234','2003-07-14','ST_CLERK',36000.00,NULL,123,50),(138,'Stephen','Stiles','SSTILES','650.121.2034','2005-10-26','ST_CLERK',32000.00,NULL,123,50),(139,'John','Seo','JSEO','650.121.2019','2006-02-12','ST_CLERK',27000.00,NULL,123,50),(140,'Joshua','Patel','JPATEL','650.121.1834','2006-04-06','ST_CLERK',35000.00,NULL,123,50),(141,'Trenna','Rajs','TRAJS','650.121.8009','2003-10-17','ST_CLERK',35000.00,NULL,124,50),(142,'Curtis','Davies','CDAVIES','650.121.2994','2005-01-29','ST_CLERK',31000.00,NULL,124,50),(143,'Randall','Matos','RMATOS','650.121.2874','2006-03-15','ST_CLERK',26000.00,NULL,124,50),(144,'Peter','Vargas','PVARGAS','650.121.2004','2006-07-09','ST_CLERK',35000.00,NULL,124,50),(145,'John','Russell','JRUSSEL','011.44.1344.429268','2004-10-01','SA_MAN',140000.00,0.40,100,80),(146,'Karen','Partners','KPARTNER','011.44.1344.467268','2005-01-05','SA_MAN',135000.00,0.30,100,80),(147,'Alberto','Errazuriz','AERRAZUR','011.44.1344.429278','2005-03-10','SA_MAN',120000.00,0.30,100,80),(148,'Gerald','Cambrault','GCAMBRAU','011.44.1344.619268','2007-10-15','SA_MAN',110000.00,0.30,100,80),(149,'Eleni','Zlotkey','EZLOTKEY','011.44.1344.429018','2008-01-29','SA_MAN',105000.00,0.20,100,80),(150,'Peter','Tucker','PTUCKER','011.44.1344.129268','2005-01-30','SA_REP',100000.00,0.30,145,80),(151,'David','Bernstein','DBERNSTE','011.44.1344.345268','2005-03-24','SA_REP',95000.00,0.25,145,80),(152,'Peter','Hall','PHALL','011.44.1344.478968','2005-08-20','SA_REP',90000.00,0.25,145,80),(153,'Christopher','Olsen','COLSEN','011.44.1344.498718','2006-03-30','SA_REP',80000.00,0.20,145,80),(154,'Nanette','Cambrault','NCAMBRAU','011.44.1344.987668','2006-12-09','SA_REP',75000.00,0.20,145,80),(155,'Oliver','Tuvault','OTUVAULT','011.44.1344.486508','2007-11-23','SA_REP',70000.00,0.15,145,80),(156,'Janette','King','JKING','011.44.1345.429268','2004-01-30','SA_REP',100000.00,0.35,146,80),(157,'Patrick','Sully','PSULLY','011.44.1345.929268','2004-03-04','SA_REP',95000.00,0.35,146,80),(158,'Allan','McEwen','AMCEWEN','011.44.1345.829268','2004-08-01','SA_REP',90000.00,0.35,146,80),(159,'Lindsey','Smith','LSMITH','011.44.1345.729268','2005-03-10','SA_REP',80000.00,0.30,146,80),(160,'Louise','Doran','LDORAN','011.44.1345.629268','2005-12-15','SA_REP',75000.00,0.30,146,80),(161,'Sarath','Sewall','SSEWALL','011.44.1345.529268','2006-11-03','SA_REP',70000.00,0.25,146,80),(162,'Clara','Vishney','CVISHNEY','011.44.1346.129268','2005-11-11','SA_REP',105000.00,0.25,147,80),(163,'Danielle','Greene','DGREENE','011.44.1346.229268','2007-03-19','SA_REP',95000.00,0.15,147,80),(164,'Mattea','Marvins','MMARVINS','011.44.1346.329268','2008-01-24','SA_REP',72000.00,0.10,147,80),(165,'David','Lee','DLEE','011.44.1346.529268','2008-02-23','SA_REP',68000.00,0.10,147,80),(166,'Sundar','Ande','SANDE','011.44.1346.629268','2008-03-24','SA_REP',64000.00,0.10,147,80),(167,'Amit','Banda','ABANDA','011.44.1346.729268','2008-04-21','SA_REP',62000.00,0.10,147,80),(168,'Lisa','Ozer','LOZER','011.44.1343.929268','2005-03-11','SA_REP',115000.00,0.25,148,80),(169,'Harrison','Bloom','HBLOOM','011.44.1343.829268','2006-03-23','SA_REP',100000.00,0.20,148,80),(170,'Tayler','Fox','TFOX','011.44.1343.729268','2006-01-24','SA_REP',96000.00,0.20,148,80),(171,'William','Smith','WSMITH','011.44.1343.629268','2007-02-23','SA_REP',74000.00,0.15,148,80),(172,'Elizabeth','Bates','EBATES','011.44.1343.529268','2007-03-24','SA_REP',73000.00,0.15,148,80),(173,'Sundita','Kumar','SKUMAR','011.44.1343.329268','2008-04-21','SA_REP',61000.00,0.10,148,80),(174,'Ellen','Abel','EABEL','011.44.1644.429267','2004-05-11','SA_REP',110000.00,0.30,149,80),(175,'Alyssa','Hutton','AHUTTON','011.44.1644.429266','2005-03-19','SA_REP',88000.00,0.25,149,80),(176,'Jonathon','Taylor','JTAYLOR','011.44.1644.429265','2006-03-24','SA_REP',86000.00,0.20,149,80),(177,'Jack','Livingston','JLIVINGS','011.44.1644.429264','2006-04-23','SA_REP',84000.00,0.20,149,80),(178,'Kimberely','Grant','KGRANT','011.44.1644.429263','2007-05-24','SA_REP',70000.00,0.15,149,NULL),(179,'Charles','Johnson','CJOHNSON','011.44.1644.429262','2008-01-04','SA_REP',62000.00,0.10,149,80),(180,'Winston','Taylor','WTAYLOR','650.507.9876','2006-01-24','SH_CLERK',32000.00,NULL,120,50),(181,'Jean','Fleaur','JFLEAUR','650.507.9877','2006-02-23','SH_CLERK',31000.00,NULL,120,50),(182,'Martha','Sullivan','MSULLIVA','650.507.9878','2007-06-21','SH_CLERK',35000.00,NULL,120,50),(183,'Girard','Geoni','GGEONI','650.507.9879','2008-02-03','SH_CLERK',28000.00,NULL,120,50),(184,'Nandita','Sarchand','NSARCHAN','650.509.1876','2004-01-27','SH_CLERK',42000.00,NULL,121,50),(185,'Alexis','Bull','ABULL','650.509.2876','2005-02-20','SH_CLERK',41000.00,NULL,121,50),(186,'Julia','Dellinger','JDELLING','650.509.3876','2006-06-24','SH_CLERK',34000.00,NULL,121,50),(187,'Anthony','Cabrio','ACABRIO','650.509.4876','2007-02-07','SH_CLERK',30000.00,NULL,121,50),(188,'Kelly','Chung','KCHUNG','650.505.1876','2005-06-14','SH_CLERK',38000.00,NULL,122,50),(189,'Jennifer','Dilly','JDILLY','650.505.2876','2005-08-13','SH_CLERK',36000.00,NULL,122,50),(190,'Timothy','Gates','TGATES','650.505.3876','2006-07-11','SH_CLERK',29000.00,NULL,122,50),(191,'Randall','Perkins','RPERKINS','650.505.4876','2007-12-19','SH_CLERK',35000.00,NULL,122,50),(192,'Sarah','Bell','SBELL','650.501.1876','2004-02-04','SH_CLERK',40000.00,NULL,123,50),(193,'Britney','Everett','BEVERETT','650.501.2876','2005-03-03','SH_CLERK',39000.00,NULL,123,50),(194,'Samuel','McCain','SMCCAIN','650.501.3876','2006-07-01','SH_CLERK',32000.00,NULL,123,50),(195,'Vance','Jones','VJONES','650.501.4876','2007-03-17','SH_CLERK',28000.00,NULL,123,50),(196,'Alana','Walsh','AWALSH','650.507.9811','2006-04-24','SH_CLERK',31000.00,NULL,124,50),(197,'Kevin','Feeney','KFEENEY','650.507.9822','2006-05-23','SH_CLERK',30000.00,NULL,124,50),(198,'Donald','OConnell','DOCONNEL','650.507.9833','2007-06-21','SH_CLERK',26000.00,NULL,124,50),(199,'Douglas','Grant','DGRANT','650.507.9844','2008-01-13','SH_CLERK',26000.00,NULL,124,50),(200,'Jennifer','Whalen','JWHALEN','515.123.4444','2003-09-17','AD_ASST',44000.00,NULL,101,10),(201,'Michael','Hartstein','MHARTSTE','515.123.5555','2004-02-17','MK_MAN',130000.00,NULL,100,20),(202,'Pat','Fay','PFAY','603.123.6666','2005-08-17','MK_REP',60000.00,NULL,201,20),(203,'Susan','Mavris','SMAVRIS','515.123.7777','2002-06-07','HR_REP',65000.00,NULL,101,40),(204,'Hermann','Baer','HBAER','515.123.8888','2002-06-07','PR_REP',100000.00,NULL,101,70),(205,'Shelley','Higgins','SHIGGINS','515.123.8080','2002-06-07','AC_MGR',120080.00,NULL,101,110),(206,'William','Gietz','WGIETZ','515.123.8181','2002-06-07','AC_ACCOUNT',83000.00,NULL,205,110);
/*!40000 ALTER TABLE  staff  ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table  job_history 
--

DROP TABLE IF EXISTS  job_history ;

CREATE TABLE  job_history  (
   staff_id  int(6) NOT NULL,
   start_date  date NOT NULL,
   end_date  date NOT NULL,
   job_id  varchar(10) NOT NULL,
   department_id  int(4) NOT NULL,
  PRIMARY KEY ( staff_id , start_date ),
  UNIQUE KEY  jhist_emp_id_st_date_pk  ( staff_id , start_date ),
  KEY  jhist_job_fk  ( job_id ),
  KEY  jhist_dept_fk  ( department_id ),
  CONSTRAINT  jhist_dept_fk  FOREIGN KEY ( department_id ) REFERENCES  departments  ( department_id ),
  CONSTRAINT  jhist_emp_fk  FOREIGN KEY ( staff_id ) REFERENCES  staff  ( staff_id ),
  CONSTRAINT  jhist_job_fk  FOREIGN KEY ( job_id ) REFERENCES  jobs  ( job_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Inserting data for table  job_history 
--

LOCK TABLES  job_history  WRITE;
/*!40000 ALTER TABLE  job_history  DISABLE KEYS */;
INSERT INTO  job_history  VALUES (101,'1997-09-21','2001-10-27','AC_ACCOUNT',110),(101,'2001-10-28','2005-03-15','AC_MGR',110),(102,'2001-01-13','2006-07-24','IT_PROG',60),(114,'2006-03-24','2007-12-31','ST_CLERK',50),(122,'2007-01-01','2007-12-31','ST_CLERK',50),(176,'2006-03-24','2006-12-31','SA_REP',80),(176,'2007-01-01','2007-12-31','SA_MAN',80),(200,'1995-09-17','2001-06-17','AD_ASST',90),(200,'2002-07-01','2006-12-31','AC_ACCOUNT',90),(201,'2004-02-17','2007-12-19','MK_REP',20);
/*!40000 ALTER TABLE  job_history  ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table  jobs 
--

DROP TABLE IF EXISTS  jobs ;

CREATE TABLE  jobs  (
   job_id  varchar(10) NOT NULL,
   job_title  varchar(35) NOT NULL,
   min_salary  int(6) DEFAULT NULL,
   max_salary  int(6) DEFAULT NULL,
  PRIMARY KEY ( job_id ),
  UNIQUE KEY  job_id_pk  ( job_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Inserting data for table  jobs 
--

LOCK TABLES  jobs  WRITE;
/*!40000 ALTER TABLE  jobs  DISABLE KEYS */;
INSERT INTO  jobs  VALUES ('AC_ACCOUNT','Public Accountant',0,90000),('AC_MGR','Accounting Manager',0,160000),('AD_ASST','Administration Assistant',0,60000),('AD_PRES','President',0,400000),('AD_VP','Administration Vice President',0,300000),('FI_ACCOUNT','Accountant',0,90000),('FI_MGR','Finance Manager',0,160000),('HR_REP','Human Resources Representative',0,90000),('IT_PROG','Programmer',0,100000),('MK_MAN','Marketing Manager',0,150000),('MK_REP','Marketing Representative',0,90000),('PR_REP','Public Relations Representative',0,105000),('PU_CLERK','Purchasing Clerk',0,55000),('PU_MAN','Purchasing Manager',0,150000),('SA_MAN','Sales Manager',0,200800),('SA_REP','Sales Representative',0,120080),('SH_CLERK','Shipping Clerk',0,55000),('ST_CLERK','Stock Clerk',0,50000),('ST_MAN','Stock Manager',0,85000);
/*!40000 ALTER TABLE  jobs  ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table  locations 
--

DROP TABLE IF EXISTS  locations ;

CREATE TABLE  locations  (
   location_id  int(4) NOT NULL,
   street_address  varchar(40) DEFAULT NULL,
   postal_code  varchar(12) DEFAULT NULL,
   city  varchar(30) NOT NULL,
   state_province  varchar(25) DEFAULT NULL,
   country_id  char(2) NOT NULL,
  PRIMARY KEY ( location_id ),
  UNIQUE KEY  loc_id_pk  ( location_id ),
  KEY  loc_c_id_fk  ( country_id ),
  CONSTRAINT  loc_c_id_fk  FOREIGN KEY ( country_id ) REFERENCES  countries  ( country_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Inserting data for table  locations 
--

LOCK TABLES  locations  WRITE;
/*!40000 ALTER TABLE  locations  DISABLE KEYS */;
INSERT INTO  locations  VALUES (1000,'1297 Via Cola di Rie','00989','Roma',NULL,'IT'),(1100,'93091 Calle della Testa','10934','Venice',NULL,'IT'),(1200,'2017 Shinjuku-ku','1689','Tokyo','Tokyo Prefecture','JP'),(1300,'9450 Kamiya-cho','6823','Hiroshima',NULL,'JP'),(1400,'2014 Jabberwocky Rd','26192','Southlake','Texas','US'),(1500,'2011 Interiors Blvd','99236','South San Francisco','California','US'),(1600,'2007 Zagora St','50090','South Brunswick','New Jersey','US'),(1700,'2004 Charade Rd','98199','Seattle','Washington','US'),(1800,'147 Spadina Ave','M5V 2L7','Toronto','Ontario','CA'),(1900,'6092 Boxwood St','YSW 9T2','Whitehorse','Yukon','CA'),(2000,'40-5-12 Laogianggen','190518','Beijing',NULL,'CN'),(2100,'1298 Vileparle (E)','490231','Bombay','Maharashtra','IN'),(2200,'12-98 Victoria Street','2901','Sydney','New South Wales','AU'),(2300,'198 Clementi North','540198','Singapore',NULL,'SG'),(2400,'8204 Arthur St',NULL,'London',NULL,'UK'),(2500,'Magdalen Centre, The Oxford Science Park','OX9 9ZB','Oxford','Oxfordshire','UK'),(2600,'9702 Chester Road','09629850293','Stretford','Manchester','UK'),(2700,'Schwanthalerstr. 7031','80925','Munich','Bavaria','DE'),(2800,'Rua Frei Caneca 1360 ','01307-002','Sao Paulo','Sao Paulo','BR'),(2900,'20 Rue des Corps-Saints','1730','Geneva','Geneve','CH'),(3000,'Murtenstrasse 921','3095','Bern','BE','CH'),(3100,'Pieter Breughelstraat 837','3029SK','Utrecht','Utrecht','NL'),(3200,'Mariano Escobedo 9991','11932','Mexico City','Distrito Federal,','MX');
/*!40000 ALTER TABLE  locations  ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table  regions 
--

DROP TABLE IF EXISTS  regions ;

CREATE TABLE  regions  (
   region_id  int(11) NOT NULL,
   region_name  varchar(25) DEFAULT NULL,
  PRIMARY KEY ( region_id ),
  UNIQUE KEY  reg_id_pk  ( region_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Inserting data for table  regions 
--

LOCK TABLES  regions  WRITE;
ALTER TABLE  regions  DISABLE KEYS ;
INSERT INTO  regions  VALUES (1,'Europe'),(2,'Americas'),(3,'Asia'),(4,'Middle East and Africa');
ALTER TABLE  regions  ENABLE KEYS;
UNLOCK TABLES;


SET SQL_MODE=@OLD_SQL_MODE ;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

COMMIT;