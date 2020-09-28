import psycopg2

try:
	conn = psycopg2.connect(
	        database='yourdb',
	        user='youruser',
	        host='localhost',
	        port=5432, #beware if your port is different
	        password='pass'
	    )

	cursor = conn.cursor()

	#value = '1; DROP TABLE S' # Why does this not delete the table S?
	#value = '1; DROP TABLE S; SELECT * FROM R' # This one will work
	value = input('Insert value of the attribute a: ')

	query = 'SELECT * FROM R WHERE a = ' + value

	cursor.execute(query)

	# position yourself over the first tuple of the result:
	row = cursor.fetchone()

	while row:
		print(row)
		# move onto the next tuple of the result
		row = cursor.fetchone()

	# if we do not commit the transactions, no data changes will be recorded -- try it
	# also, if the program crashes before this, the changes will not be commited
	# therefore to do your injection attack, you must reach this line of code correctly
	conn.commit()
	conn.close()


except Exception as e:
	print('There was an issue:')
	print(e)