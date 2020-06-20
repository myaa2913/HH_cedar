--extract gd org names (and compustat names) for merge w/HH
\copy (SELECT employerid, year, employername, conml, gvkey FROM firm_chars WHERE num_reviews >= 25 AND NULLIF(employername,'') IS NOT NULL) to '~/projects/def-mcorrito/mcorrito/HH/temp_data/gd_org_names.csv' with csv header;

--\copy (SELECT * FROM firm_chars) to '~/projects/def-mcorrito/mcorrito/HH/temp_data/gd_firm_chars.csv' with csv header;



