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

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
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
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)

migrate = Migrate(app, db)

Base = declarative_base()

# done in config.py and statement above

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

    # setup one to many relation of Venue to Shows
    shows = relationship("Show")

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String)

    # one to many relation of Artist to Shows, shows only have a single artist
    show = relationship("Show")

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.String, nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def my_datetime(value):
    date = dateutil.parser.parse(value)
    return format_datetime(date, locale='en')

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
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
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    # match either case, use lower() on search term
    search_term = request.form.get('search_term', '').lower()
    search_string = "%{}%".format(search_term)

    # find matches for search_term in venues, use lower on db
    venue_matches = Venue.query.filter(func.lower(Venue.name).contains(search_string)).all()

    num_matches = len(venue_matches)

    # create response dict and set number of matches
    response = {}
    response['count'] = num_matches

    # now build up the data part of response, it needs a list of dicts with name
    response['data'] = []

    for venue in venue_matches:
        response['data'].append({'name': venue.name, 'id': venue.id})

    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    # find venue by given ID in the URL
    venue = Venue.query.filter(Venue.id == venue_id).first()

    # venue = venue[0]

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

    shows_list = Show.query.filter_by(venue_id=venue_id).all()
    data['past_shows'] = []
    data['upcoming_shows'] = []
    past_shows_count = 0
    upcoming_shows_count = 0

    for show in shows_list:
        # get the artist record from this show's artist ID
        artist_record = Artist.query.filter(Artist.id == show.artist_id).first()

        # build dict for artist info
        artist_dict = {
                'start_time': show.start_time,
                'artist_id': show.artist_id,
                'artist_name': artist_record.name,
                'artist_image_link': artist_record.image_link
            }

        # need to convert show time format to TZ naive for comparison
        show_start = dateutil.parser.parse(show.start_time)
        show_start = show_start.replace(tzinfo=None)

        if show_start < datetime.now():
            # put the show info into data['past_shows']
            data['past_shows'].append(artist_dict)
            past_shows_count += 1
        else:
            # put the show info into data['upcoming_shows']
            data['upcoming_shows'].append(artist_dict)
            upcoming_shows_count += 1

    # now add the counts to data
    data['past_shows_count'] = past_shows_count
    data['upcoming_shows_count'] = upcoming_shows_count

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
        db.rollback()
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

    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        flash('Venue id=' + venue_id + ' was successfully deleted!')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('/venues'))

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

    venue.name=form.name.data,
    venue.city=form.city.data,
    venue.state=form.state.data,
    venue.address=form.address.data,
    venue.phone=form.phone.data,
    venue.genres=genres,
    venue.facebook_link=form.facebook_link.data,
    venue.image_link=form.image_link.data,
    venue.website=form.website_link.data,
    venue.seeking_talent=form.seeking_talent.data,
    venue.seeking_description=form.seeking_description.data

    db.session.commit()
    
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()

    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

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
