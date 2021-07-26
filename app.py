#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json
from re import search
import dateutil.parser
import datetime
import babel
# from babel.dates import format_datetime
from flask import Flask, json, jsonify, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment

# moved to models.py
from flask_sqlalchemy import SQLAlchemy

# added once models.py was created
from models import db, Venue, Artist, Show

from sqlalchemy import func
#moved to models.py
#from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import logging
from logging import Formatter, FileHandler

from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate

from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)

# set a couple env vars
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_DEBUG'] = True

app.config.from_object('config')

# moved to models.py
# db = SQLAlchemy(app)

# instead use
db.init_app(app)

toolbar = DebugToolbarExtension(app)

migrate = Migrate(app, db)

Base = declarative_base()

# done in config.py and statement above

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def my_datetime(value):
    date = dateutil.parser.parse(value)
    return format_datetime(date, locale='en')

def format_datetime(value, format='medium'):
    # per https://knowledge.udacity.com/questions/649442
    # modified the way the database stores time, changed column from 
    # text to a datetime, so I modified the next line, the parser is not needed
    date = value # dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en_US')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

    venues = Venue.query.all()

    venue_locations = db.session.query(Venue.city, Venue.state).distinct().all()

    data = []

    # setup outer shell of data to return
    for location in venue_locations:
        venues_dict = {'city': location[0], 'state': location[1], 'venues': []}

        # find venues at this location and make venues_dict
        venue_list_by_location = db.session.query(Venue.city, Venue.name, Venue.id).all()

        for venue in venue_list_by_location:
            if venue[0] == venues_dict['city']:
                venues_dict['venues'].append({'name': venue[1], 'id': venue[2]})

        # append the venues info to the data list
        data.append(venues_dict)

    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venue with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    # match either case, use lower() on search term
    search_string = case_insensitive_search_term(request.form.get('search_term', ''))

    # find matches for search_term in venues, use lower on db
    venue_matches = Venue.query.filter(Venue.name.ilike(search_string)).all()

    num_matches = len(venue_matches)

    # create response dict and set number of matches
    response = {}
    response['count'] = num_matches

    # now build up the data part of response, it needs a list of dicts with name
    response['data'] = []

    for venue in venue_matches:
        num_past_shows, num_upcoming_shows = get_num_shows(Venue, venue.id)

        response['data'].append({'name': venue.name, 'id': venue.id,
        'num_upcoming_shows': num_upcoming_shows})


    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term'))

@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    # find venue by given ID in the URL
    venue = Venue.query.get(venue_id)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link }

    # convert genres to a list from a string
    data['genres'] = data['genres'].replace(" ","")
    data['genres'] = data['genres'].split(",")

    data['past_shows'] = []
    data['upcoming_shows'] = []

    # THESE 2 comments are the way the reviewer said to collect the records, looks ugly but more efficient at scale.
    # past_shows = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<compare_now_time).all()
    # upcoming_shows = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>compare_now_time).all()

    # so I hope you like this line, it's adapted from the reviewer feedback. Once I added the right relationships in the models.py file, 
    # the ability to use past_show.artist.name and the like started working
    past_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
    upcoming_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()

    # past_ and upcoming_shows are lists, so take the len
    # and add the counts to data dict
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    # now go through the past and upcoming shows and create sub-dicts to add to the data dict, need one for each show, and add the sub-dicts

    for past_show in past_shows:
        # build dict for artist info
        artist_dict = {
                'start_time': past_show.start_time,
                'artist_id': past_show.artist_id,
                'artist_name': past_show.artist.name,
                'artist_image_link': past_show.artist.image_link
            }

        data['past_shows'].append(artist_dict)
    
    for upcoming_show in upcoming_shows:
        # build dict for artist info
        artist_dict = {
                'start_time': upcoming_show.start_time,
                'artist_id': upcoming_show.artist_id,
                'artist_name': upcoming_show.artist.name,
                'artist_image_link': upcoming_show.artist.image_link
            }
    
        data['upcoming_shows'].append(artist_dict)

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()

    # nothing to see here

    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

    error = False
    form = VenueForm()

    try:
        genres_string = ", ".join(form.genres.data)

        new_venue = Venue(
            name = form.name.data,
            city = form.city.data,
            state = form.state.data,
            address = form.address.data,
            phone = form.phone.data,
            genres = genres_string, # note the var from above, not the direct form data
            image_link = form.image_link.data,
            facebook_link = form.facebook_link.data,
            website = form.website_link.data,
            seeking_talent = form.seeking_talent.data,
            seeking_description = form.seeking_description.data
        )

        db.session.add(new_venue)
        db.session.commit()
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        if not error:
            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
            return render_template('pages/home.html')
        else:
            # TODO: on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    error = False

    try:

        # I never did figure out which / how to get SQL Alchemy to automatically delete children shows of the parent venue to be deleted
        # for now I am just finding shows by venue_id and deleting them first, it's faster than a join
        Show.query.filter_by(venue_id=venue_id).delete()

        # now delete the "parent" show
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        if not error:
            flash('Venue id=' + venue_id + ' was successfully deleted!')
            return redirect(url_for('/venues'))
        else:
            flash('Venue id=' + venue_id + ' was NOT deleted! See the console for error message.')

# Edit Venues

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    db_venue = Venue.query.filter_by(id=venue_id).first()

    venue = {
        'id': db_venue.id,
        'name': db_venue.name
    }

    genres = db_venue.genres.replace(" ","").split(",")

    form.name.data = db_venue.name
    form.city.data = db_venue.city
    form.state.data = db_venue.state
    form.address.data = db_venue.address
    form.phone.data = db_venue.phone
    form.genres.data = genres #note the exception, this is set above, it's a list
    form.facebook_link.data = db_venue.facebook_link
    form.image_link.data = db_venue.image_link
    form.website_link.data = db_venue.website
    form.seeking_talent.data = db_venue.seeking_talent
    form.seeking_description.data = db_venue.seeking_description

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    form = VenueForm()

    venue = db.session.query(Venue).get(venue_id)

    # make a string out of the genres list for the db
    genres = ", ".join(form.genres.data)
    if form.seeking_talent.data == True:
        seeking_talent_bool = True
    else:
        seeking_talent_bool = False

    venue.name=form.name.data
    venue.city=form.city.data
    venue.state=form.state.data
    venue.address=form.address.data
    venue.phone=form.phone.data
    venue.genres=genres
    venue.facebook_link=form.facebook_link.data
    venue.image_link=form.image_link.data
    venue.website=form.website_link.data
    venue.seeking_talent=seeking_talent_bool
    venue.seeking_description=form.seeking_description.data

    db.session.commit()
    
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

    artists = db.session.query(Artist).all()

    data = []

    for artist in artists:
        artist_dict = {
            'id': artist.id,
            'name': artist.name
        }
        data.append(artist_dict)

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

    # match either case, use lower() on search term
    search_string = case_insensitive_search_term(request.form.get('search_term', ''))

    artist_matches = Artist.query.filter(Artist.name.ilike(search_string)).all()

    num_matches = len(artist_matches)

    # create response dict and set number of matches
    response = {}
    response['count'] = num_matches

    # now build up the data part of response, it needs a list of dicts with name
    response['data'] = []

    for artist in artist_matches:
        num_past_shows, num_upcoming_shows = get_num_shows(Artist, artist.id)

        response['data'].append({'name': artist.name, 
                'id': artist.id,
                'num_upcoming_shows': num_upcoming_shows})

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>', methods=['GET'])
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    # find artist by given ID in the URL
    artist = Artist.query.get(artist_id)

    data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "seeking_venue": artist.seeking_venue,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link }

    # convert genres to a list from a string
    data['genres'] = data['genres'].replace(" ","")
    data['genres'] = data['genres'].split(",")

    # TODO: the rest of this is just screaming to be made into a function
    # along with the very similar code from '/venues/<int:venue_id>', methods=['GET']

    data['past_shows'] = []
    data['upcoming_shows'] = []

    # implementing joins here too, like in /venues/venue_id GET method
    past_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
    upcoming_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()

    # past_ and upcoming_shows are lists, so take the len
    # and add the counts to data dict
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
    
    # now go through the past and upcoming shows and create sub-dicts to add to the data dict, need one for each show, and add the sub-dicts

    for past_show in past_shows:

        # build dict for venue info
        venue_dict = {
                'start_time': past_show.start_time,
                'venue_id': past_show.venue_id,
                'venue_name': past_show.venue.name,
                'venue_image_link': past_show.venue.image_link
            }

        data['past_shows'].append(venue_dict)

    for upcoming_show in upcoming_shows:

        # build dict for venue info
        venue_dict = {
                'start_time': upcoming_show.start_time,
                'venue_id': upcoming_show.venue_id,
                'venue_name': upcoming_show.venue.name,
                'venue_image_link': upcoming_show.venue.image_link
            }

        data['upcoming_shows'].append(venue_dict)


    return render_template('pages/show_artist.html', artist=data)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()

    # nothing to see here
    
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    error = False
    form = ArtistForm()

    try:
        genres_string = ", ".join(form.genres.data)

        new_artist = Artist(
            name = form.name.data,
            city = form.city.data,
            state = form.state.data,
            phone = form.phone.data,
            genres = genres_string, # note the var from above, not the direct form data
            image_link = form.image_link.data,
            facebook_link = form.facebook_link.data,
            website = form.website_link.data,
            seeking_venue = form.seeking_venue.data,
            seeking_description = form.seeking_description.data
        )

        db.session.add(new_artist)
        db.session.commit()
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        if not error:
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
            return render_template('pages/home.html')
        else:
            # TODO: on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):

    # screams to be made into a function, very similar code to 
    # '/venues/<venue_id>', methods=['DELETE']

    # BONUS CHALLENGE: Implement a button to delete a Artist on a Artist Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    error = False

    try:

        # I never did figure out which / how to get SQL Alchemy to automatically delete children shows of the parent venue to be deleted
        # for now I am just finding shows by artist_id and deleting them first, it's faster than a join
        Show.query.filter_by(artist_id=artist_id).delete()

        # now delete the "parent" show
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        if not error:
            flash('Artist id=' + artist_id + ' was successfully deleted!')
            return redirect(url_for('/artists'))
        else:
            flash('Artist id=' + artist_id + ' was NOT deleted! See the console for error message.')

#  Update Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # TODO: populate form with fields from artist with ID <artist_id>

    form = ArtistForm()

    db_artist = Artist.query.filter_by(id=artist_id).first()

    artist = {
        'id': db_artist.id,
        'name': db_artist.name
    }

    genres = db_artist.genres.replace(" ","").split(",")

    form.name.data = db_artist.name
    form.city.data = db_artist.city
    form.state.data = db_artist.state
    form.phone.data = db_artist.phone
    form.genres.data = genres #note the exception, this is set above, it's a list
    form.facebook_link.data = db_artist.facebook_link
    form.image_link.data = db_artist.image_link
    form.website_link.data = db_artist.website
    form.seeking_venue.data = db_artist.seeking_venue
    form.seeking_description.data = db_artist.seeking_description

    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    form = ArtistForm()

    artist = db.session.query(Artist).get(artist_id)

    # make a string out of the genres list for the db
    genres = ", ".join(form.genres.data)

    artist.name=form.name.data
    artist.city=form.city.data
    artist.state=form.state.data
    artist.phone=form.phone.data
    artist.genres=genres
    artist.facebook_link=form.facebook_link.data
    artist.image_link=form.image_link.data
    artist.website=form.website_link.data
    artist.seeking_venue=form.seeking_venue.data
    artist.seeking_description=form.seeking_description.data

    db.session.commit()

    return redirect(url_for('show_artist', artist_id=artist_id))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    data = []

    shows = Show.query.all()

    for show in shows:

        artist = db.session.query(Artist).get(show.artist_id)

        show_dict = {
            'venue_id': show.venue_id,
            'artist_id': show.artist_id,
            'venue_name': db.session.query(Venue).get(show.venue_id).name,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        }

        data.append(show_dict)

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create', methods=['GET'])
def create_shows():
    # renders form. do not touch.
    form = ShowForm()

    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    form = ShowForm()

    error = False

    # fix the time format, assume format like 2021-07-23 14:55:31,
    # need format like 2019-05-21T21:30:00.000Z

    start_time_list = str(form.start_time.data).split(" ")
    start_time = 'T'.join(start_time_list)
    start_time = start_time + 'Z'

    new_show = Show(
        venue_id=form.venue_id.data,
        artist_id=form.artist_id.data,
        start_time=start_time
    )

    try:
        db.session.add(new_show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    if not error:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
        return render_template('pages/home.html')
    else:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


# ************** HELPERS *************

# match either case, use lower() on search term
def case_insensitive_search_term(initial_term):
    search_term = initial_term.lower()
    search_string = "%{}%".format(search_term)

    return search_string

def get_num_shows(table, id):
    if table == Artist:
        shows_list = Show.query.filter_by(artist_id=id).all()
    elif table == Venue:
        shows_list = Show.query.filter_by(venue_id=id).all()

    past_shows_count = 0
    upcoming_shows_count = 0

    for show in shows_list:

        if show.start_time >= datetime.now():
            upcoming_shows_count += 1
        else:
            past_shows_count += 1

    return past_shows_count, upcoming_shows_count

    

# ************** ERROR HANDLERS ******

@app.errorhandler(404)
def not_found_error(error):

    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):

    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
