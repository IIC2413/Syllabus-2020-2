import psycopg2

try:
	conn = psycopg2.connect(
	        database='yourdb',
	        user='youruser',
	        host='localhost',
	        port=5432,
	        password='pass'
	    )

	cursor = conn.cursor()

	value = input('Insert value of the attribute name: ')

	query = 'SELECT * FROM T WHERE name = %(name)s'

	cursor.execute(query,{"name":value})

    # print the results
	row = cursor.fetchone()

	while row:
		print(row)
		# move onto the next tuple of the result
		row = cursor.fetchone()

	conn.commit()
	conn.close()


except Exception as e:
	print('There was an issue:')
	print(e)
