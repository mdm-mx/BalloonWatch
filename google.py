import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(service_file='google.json')

# Create empty dataframe
#df = pd.DataFrame()

# Create a column
#df['name'] = ['John', 'Steve', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('MDM-6-Track')

#select the first sheet 
wks = sh[0]

data = ['1', '2', '3']
#update the first sheet with df, starting at cell B2. 
wks.insert_rows(wks.rows, values=data, inherit=True)
#wks.set_dataframe(df,(1,1))