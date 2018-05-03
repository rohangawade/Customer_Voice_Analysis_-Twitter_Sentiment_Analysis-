import os
from subprocess import call
																																															
brands = ['#Dominos','#Pizzahut','#PapaJohns','#BurgerKing','#McDonalds','#Walmart','#Walgreens','#BestBuy','#Target','#CVSPharmacy','#Costco','#Nike', '#RalphLauren', '#Levis', '#Zara', '#TommyHilfiger','@dominos','@pizzahut','@PapaJohns','@BurgerKing','@McDonalds','@Walmart','@Walgreens','@BestBuy','@Target','@CVSPharmacy','@Costco','@Nike', '@RalphLauren', '@Levis', '@Zara', '@TommyHilfiger']
cities = ['Chicago','New_York','Florida','New_jersey','California','Boston','Seattle']

for brand in brands :	
	for city in cities :
		print(brand+" "+city)
		call_exporter = 'python Exporter_Location.py --querysearch '+brand+' --near '+city+
		# call_exporter = 'python Exporter_Location.py --querysearch '+brand+' --since 2015-01-01 --until 2016-12-31'
		call(call_exporter, shell=True)
