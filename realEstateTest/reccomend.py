import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import locale
from pandas import DataFrame, Series

if __name__ == '__main__':
	
	df = pd.read_csv("listing_14790.csv")
	df.date = pd.to_datetime(df.date, format = "%Y%m%d")
	df.scraped_ts = pd.to_datetime(df.scraped_ts)
	##question 1: highest price? correlation between price and occupancy?

	locale.setlocale( locale.LC_ALL, '' )
	max = df.price.max()

	print "highest price at a single snapshot belong to listing: ", df[df.price == max].iloc[0]["listing_id"], " with a price of: ", locale.currency(df[df.price == max].iloc[0]["price"])

	print "the correlation between price and occupancy is: " , df.corr(method="pearson")["price"]["ultimately_booked"]

	## add some calculated columns to determine how far out the snapshot is
	## along with the month and day of the week
	df["price"] = np.where(df.price == 0, df.probable_close_price, df.price)
	df["day_of_week"] = [date.dayofweek for date in df["date"]]
	df["z_score"] = df.z_score.fillna(0)
	df["status"] = pd.Categorical.from_array(df.status).codes
	df["status"] = df["status"] - 1
	## 0=unav, 1 = av
	df["status"] = abs(df.status)


	#we are averaging status and days_out:
		#these numbers represent the the percent of time that the listing stayed open along with the average number of days the date was on the market
	df = df.groupby(["listing_id","date"]).mean().reset_index()
	df["ultimately_booked"] = np.where(df.ultimately_booked > 0, 1, 0)
	df["status"] = np.where(df.status > 0, 1, 0)

	train = df[df.listing_id != 14790]
	test = df[df.listing_id == 14790]

	print "...fitting model with formula: lm = smf.ols(formula = ""price ~  day_of_week + date"",data=train).fit()"

	lm = smf.ols(formula = "price ~ day_of_week + date",data=train).fit()

	test["predict"] = lm.predict(test)
	
	test.to_csv("14790_predictions.csv")

	print "14790_predictions.csv saved to working directory"
