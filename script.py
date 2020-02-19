string_key = {'User': ['Location','Country'], 'Item':['Name','Description']}
number_key = {'User': ['Rating'], 'Item': ['Currently','Buy_Price','FirstBid']}

for table in string_key:
	for column in string_key[table]:
		print (f'UPDATE {table} SET {column} = NULL WHERE {column} == "NULL";')

for table in number_key:
	for column in number_key[table]:
		print (f'UPDATE {table} SET {column} = NULL WHERE {column} == -1;')
