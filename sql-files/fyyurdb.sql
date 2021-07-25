--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7 (Ubuntu 12.7-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.7 (Ubuntu 12.7-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: artist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist (
    id integer NOT NULL,
    name character varying NOT NULL,
    city character varying(120) NOT NULL,
    state character varying(120) NOT NULL,
    phone character varying(120) NOT NULL,
    genres character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    seeking_venue boolean NOT NULL,
    seeking_description character varying(500),
    website character varying
);


ALTER TABLE public.artist OWNER TO postgres;

--
-- Name: artist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artist_id_seq OWNER TO postgres;

--
-- Name: artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.artist_id_seq OWNED BY public.artist.id;


--
-- Name: show; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.show (
    id integer NOT NULL,
    venue_id integer NOT NULL,
    artist_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL
);


ALTER TABLE public.show OWNER TO postgres;

--
-- Name: show_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.show_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.show_id_seq OWNER TO postgres;

--
-- Name: show_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.show_id_seq OWNED BY public.show.id;


--
-- Name: venue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.venue (
    id integer NOT NULL,
    name character varying NOT NULL,
    city character varying(120) NOT NULL,
    state character varying(120) NOT NULL,
    address character varying(120) NOT NULL,
    phone character varying(120) NOT NULL,
    image_link character varying(500),
    facebook_link character varying(120),
    genres character varying(120),
    website character varying(500),
    seeking_talent boolean NOT NULL,
    seeking_description character varying(500)
);


ALTER TABLE public.venue OWNER TO postgres;

--
-- Name: venue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venue_id_seq OWNER TO postgres;

--
-- Name: venue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.venue_id_seq OWNED BY public.venue.id;


--
-- Name: artist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist ALTER COLUMN id SET DEFAULT nextval('public.artist_id_seq'::regclass);


--
-- Name: show id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show ALTER COLUMN id SET DEFAULT nextval('public.show_id_seq'::regclass);


--
-- Name: venue id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venue ALTER COLUMN id SET DEFAULT nextval('public.venue_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
0624392c1c9e
\.


--
-- Data for Name: artist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artist (id, name, city, state, phone, genres, image_link, facebook_link, seeking_venue, seeking_description, website) FROM stdin;
2	Matt Quevedo	New York	NY	300-400-5000	Jazz	https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80	https://www.facebook.com/mattquevedo923251523	f		
3	The Wild Sax Band	San Francisco	CA	432-325-5432	Jazz, Classical	https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80		f		
4	Tugging People	Santa Fe	NM	857-555-1212	Alternative, Blues, Classical		https://facebook.com/TuggingRopes	t	we'll play anywhere!	https://tuggingropes.com
1	Guns N Petals Edited	San Francisco	CA	326-123-5000	Blues, Classical, Country	https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80	https://www.facebook.com/GunsNPetals	t	Looking for shows to perform at in the San Francisco Bay Area!	https://www.gunsnpetalsband.com
\.


--
-- Data for Name: show; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.show (id, venue_id, artist_id, start_time) FROM stdin;
1	1	1	2019-05-21T21:30:00.000Z
2	3	2	2019-06-15T23:00:00.000Z
3	3	3	2035-04-01T20:00:00.000Z
4	3	3	2035-04-08T20:00:00.000Z
5	3	3	2035-04-15T20:00:00.000Z
6	3	2	2021-07-23T15:14:05Z
7	1	3	2021-07-23T15:24:10Z
\.


--
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.venue (id, name, city, state, address, phone, image_link, facebook_link, genres, website, seeking_talent, seeking_description) FROM stdin;
1	The Musical Hop	San Francisco	CA	1015 Folsom Street	123-123-1234	https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60	https://www.facebook.com/TheMusicalHop	Jazz, Reggae, Swing, Classical, Folk	https://www.themusicalhop.com	t	We are on the lookout for a local artist to play every two weeks. Please call us.
2	The Dueling Pianos Bar	New York	NY	335 Delancey Street	914-003-1132	https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80	https://www.facebook.com/theduelingpianos	Classical, R&B, Hip-Hop	https://www.theduelingpianos.com	f	
6	Venue Test 3 edited	San Jose	CA	123 Main Street	408 555-1212		https://facebook.com/TestingVenue3	Alternative, Classical, Country	https://testingvenue3.com	t	anyone, really
3	Park Square Live Music & Coffee edited	San Francisco	CA	34 Whiskey Moore Ave	415-000-1234	https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80	https://www.facebook.com/ParkSquareLiveMusicAndCoffee	Classical, Folk, Jazz	https://www.parksquarelivemusicandcoffee.com	f	
\.


--
-- Name: artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.artist_id_seq', 4, true);


--
-- Name: show_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.show_id_seq', 7, true);


--
-- Name: venue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.venue_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- Name: show show_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_pkey PRIMARY KEY (id);


--
-- Name: venue venue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (id);


--
-- Name: show show_artist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artist(id);


--
-- Name: show show_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venue(id);


--
-- PostgreSQL database dump complete
--

