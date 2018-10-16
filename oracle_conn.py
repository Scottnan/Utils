import pyodbc
import pandas as pd
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.101.245.77;'
                      'DATABASE=master;UID=zcglb;PWD=zcglb')
df = pd.read_sql("""SELECT * FROM WANDE.wande.dbo.AShareConsensusindex 
                    WHERE ANN_DT BETWEEN '20170101' AND '20180501'""", con=conn)
print(df)
