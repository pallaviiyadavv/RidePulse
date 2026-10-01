import pandas as pd
from sqlalchemy import create_engine
import psycopg2 as p
df = pd.read_csv("cleaned_dataset.csv")

df.rename(columns={
    "start" : "start_location",
    "end" : "end_location"
})

engine = create_engine(
    "postgresql+psycopg2://postgres:pallavi@localhost:5432/ridepulse"
)

df.to_sql("trips" ,
          engine , 
          if_exists="replace",
          index = False
          )

print("data loaded successfullyy!" )

# postgre tk ye data phuch gaya