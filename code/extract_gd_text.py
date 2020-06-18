import pandas as pd
import psycopg2, sys

# define a function that handles and parses psycopg2 exceptions
def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    

try:
    conn = psycopg2.connect(database="mcorrito_db",
                            host="cedar-pgsql-vm",
                            user="mcorrito")

except OperationalError as err:
    print_psycopg2_exception(err)
    conn = None

   
if conn!=None:
    cur = conn.cursor()

    try:

        copy_cmd = 'SELECT agg_pro.pro_text,agg_pro.employerid,agg_pro.year FROM agg_pro INNER JOIN firm_chars ON agg_pro.employerid = firm_chars.employerid AND agg_pro.year = firm_chars.year WHERE firm_chars.num_reviews>=25'

        outFile = open('~\projects\def-mcorrito\mcorrito\HH\temp_data\agg_pro.csv','w')
        
        cur.copy_expert(copy_cmd,outFile)

        #conn.commit()
        
    except Exception as err:
        print_psycopg2_exception(err)

    cur.close()
conn.close()



