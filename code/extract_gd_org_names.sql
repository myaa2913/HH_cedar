--extract gd org names (and compustat names) for merge w/HH
\copy (SELECT employerid, year, employername, conml FROM firm_chars WHERE nr_500_f_annual_new >= 25 AND NULLIF(employername,'') IS NOT NULL) to '~/projects/def-mcorrito/mcorrito/HH/temp_data/gd_org_names.csv' with csv header;
