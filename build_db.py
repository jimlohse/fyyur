import psycopg2

from psycopg2.extensions import AsIs

conn = psycopg2.connect(
    host="localhost",
    database="fyyurdb",
    user="postgres",
    password="letmein")

# data

musicalhop = {
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"} 

musicalhop_shows = [{
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }]

dueling = {
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "seeking_description": "",
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    }

parksquare ={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "seeking_description": "",
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80" }
    
    
parksquare_shows = [{
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    },{
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]


gunsnpetals = {
    "id": 1,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"}

quevedo ={
    "id": 2,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "website": "",
    "seeking_venue": False,
    "seeking_description": "",
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"}

wildband = {
    "id": 3,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "seeking_description": "",
    "facebook_link": "",
    "website": "",
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"}

gunsnpetals_shows = [{
    "id": 1,
    "venue_id": 1,
    "artist_id" : 1,
    "start_time": "2019-05-21T21:30:00.000Z"}]
    
quevedo_shows = [{
    "id": 2,
    "venue_id": 3,
    "artist_id" : 2,
    "start_time": "2019-06-15T23:00:00.000Z"
    }]

wildband_shows = [{
    "id": 3,
    "venue_id": 3,
    "artist_id" : 3,
    "start_time": "2035-04-01T20:00:00.000Z"
    }, {
    "id": 4,
    "venue_id": 3,
    "artist_id" : 3,
    "start_time": "2035-04-08T20:00:00.000Z"
    }, {
    "id": 5,
    "venue_id": 3,
    "artist_id" : 3,
    "start_time": "2035-04-15T20:00:00.000Z"
    }]

# processing data

try:
    cur = conn.cursor()

    # cur.execute("SELECT * FROM artist")
    # print("Number of rows is ", cur.rowcount)
    # row = cur.fetchone()
    # print("Number of rows in artist is: ", row) 

    # for the_venue in [musicalhop, dueling, parksquare]:

    #     columns = list(the_venue.keys())

    #     the_venue['genres'] = ', '.join(the_venue['genres'])

    #     values = [the_venue[column] for column in columns]

    #     insert_statement = 'insert into venue (%s) values %s'

    #     cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    #     # print(cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))

    # for the_artist in [gunsnpetals, quevedo, wildband]:
    #     columns = list(the_artist.keys())

    #     the_artist['genres'] = ', '.join(the_artist['genres'])

    #     values = [the_artist[column] for column in columns]

    #     insert_statement = 'insert into artist (%s) values %s'

    #     cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    #     # print(cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))

    for the_shows in [gunsnpetals_shows, quevedo_shows, wildband_shows]:

        for the_show in the_shows:
            columns = list(the_show.keys())

            values = [the_show[column] for column in columns]

            insert_statement = 'insert into show (%s) values %s'

            # cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            print(cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))

    # commit everything
    # conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()