--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: ips; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ips (
    ip text NOT NULL,
    hit_count integer,
    received integer,
    org text,
    region text,
    country text,
    country_name text,
    city text,
    asn text
);


ALTER TABLE public.ips OWNER TO postgres;

--
-- Data for Name: ips; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ips (ip, hit_count, received, org, region, country, country_name, city, asn) FROM stdin;
107.179.237.193	2	\N	\N	\N	\N	\N	\N	\N
73.110.89.93	3	1	Comcast Cable Communications, LLC	Michigan	US	United States	Saint Joseph	AS7922
172.248.167.44	1	1	Charter Communications Inc	California	US	United States	Murrieta	AS20001
74.12.77.46	2	1	Bell Canada	Ontario	CA	Canada	Niagara Falls	AS577
68.146.109.174	7	1	Shaw Communications Inc.	Alberta	CA	Canada	Calgary	AS6327
70.77.196.223	1	1	Shaw Communications Inc.	Alberta	CA	Canada	Calgary	AS6327
62.85.2.249	82	1	SIA Lattelecom	Riga	LV	Latvia	Riga	AS12578
104.221.69.45	6	1	Videotron Telecom Ltee	Quebec	CA	Canada	Montreal	AS5769
107.190.126.69	5	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Windsor	AS5645
142.112.142.117	1	1	Bell Canada	Ontario	CA	Canada	Windsor	AS577
72.39.48.11	1	1	Cogeco Cable	Ontario	CA	Canada	Welland	AS7992
206.189.21.107	31	1	DigitalOcean, LLC	England	GB	United Kingdom	London	AS14061
74.15.225.172	452	1	Bell Canada	Quebec	CA	Canada	Saint-Sauveur	AS577
199.83.204.50	2	1	Gosfield North Communications Co-operative Limited	Ontario	CA	Canada	Cottam	AS19465
96.49.88.74	1	1	Shaw Communications Inc.	British Columbia	CA	Canada	Coquitlam	AS6327
209.107.210.140	43	1	StackPath LLC	Texas	US	United States	Dallas	AS12989
71.212.197.147	1	1	CenturyLink Communications, LLC	Washington	US	United States	Seattle	AS209
138.34.36.46	5	1	Bell Canada	Ontario	CA	Canada	Pembroke	AS577
23.91.239.29	103	1	DISTRIBUTEL COMMUNICATIONS LTD.	Quebec	CA	Canada	Montreal	AS11814
23.233.121.8	6	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Chatham	AS5645
65.95.248.172	2	1	Bell Canada	Ontario	CA	Canada	Thorold	AS577
138.122.234.241	9	1	StackPath LLC	Rio de Janeiro	BR	Brazil	Rio de Janeiro	AS12989
107.190.60.138	4	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Windsor	AS5645
64.229.47.33	16	1	Bell Canada	Ontario	CA	Canada	Mississauga	AS577
69.172.179.228	91	1	TekSavvy Solutions, Inc.	British Columbia	CA	Canada	Vancouver	AS5645
192.235.229.58	27	1	Comwave Telecom Inc.	Ontario	CA	Canada	Leamington	AS15128
82.28.128.31	39	1	Virgin Media Limited	England	GB	United Kingdom	Dudley	AS5089
50.7.204.162	5	1	Cogent Communications	North Holland	NL	Netherlands	Halfweg	AS174
90.240.223.212	237	1	Vodafone Limited	England	GB	United Kingdom	London	AS5378
209.225.146.31	1	1	Primus Telecommunications Canada Inc.	Ontario	CA	Canada	Belleville	AS6407
209.206.117.90	1	1	Axia Connect Limited	Alberta	CA	Canada	Raymond	AS54182
142.127.238.154	1	1	Bell Canada	Ontario	CA	Canada	Burlington	AS577
64.180.18.46	22	1	TELUS Communications Inc.	British Columbia	CA	Canada	Richmond	AS852
45.248.66.157	44	1	Vortex Netsol Private Limited	Maharashtra	IN	India	Mumbai	AS136334
69.158.93.204	1	1	Bell Canada	Ontario	CA	Canada	Brampton	AS577
85.3.161.36	17	1	Bluewin	Basel-City	CH	Switzerland	Basel	AS3303
104.244.230.222	1	1	Digicel Jamaica	Kingston	JM	Jamaica	Kingston	AS33576
104.222.153.98	15	1	Micfo, LLC.	New York	US	United States	New York	AS53889
67.70.81.224	3	1	Bell Canada	Ontario	CA	Canada	Niagara Falls	AS577
70.133.223.109	3	1	AT&T Services, Inc.	Georgia	US	United States	Suwanee	AS7018
142.113.169.19	4	1	Bell Canada	Ontario	CA	Canada	Oshawa	AS577
174.95.129.230	1	1	Bell Canada	Ontario	CA	Canada	St. Catharines	AS577
69.158.127.4	13	1	Bell Canada	Ontario	CA	Canada	Pickering	AS577
201.21.221.60	54	1	CLARO S.A.	Rio Grande do Sul	BR	Brazil	Montenegro	AS28573
142.184.193.128	144	1	Bell Canada	Ontario	CA	Canada	Toronto	AS577
144.217.77.180	1	1	OVH SAS	Quebec	CA	Canada	Beauharnois	AS16276
174.88.68.229	1	1	Bell Canada	Ontario	CA	Canada	Windsor	AS577
107.179.235.116	2	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Windsor	AS5645
24.57.45.59	6	1	Cogeco Cable	Ontario	CA	Canada	Tecumseh	AS7992
172.97.156.160	1	1	DISTRIBUTEL COMMUNICATIONS LTD.	Ontario	CA	Canada	Mississauga	AS11814
71.57.149.64	19	1	Comcast Cable Communications, LLC	Florida	US	United States	Miami	AS7922
216.58.50.83	5	1	DISTRIBUTEL COMMUNICATIONS LTD.	Ontario	CA	Canada	Toronto	AS11814
72.200.152.41	1	1	Cox Communications Inc.	Rhode Island	US	United States	Pawtucket	AS22773
24.57.23.236	1	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
173.206.155.229	2	1	Primus Telecommunications Canada Inc.	Ontario	CA	Canada	Scarborough	AS6407
67.86.182.167	88	1	Cablevision Systems Corp.	New Jersey	US	United States	Neptune City	AS6128
89.240.209.176	1	1	TalkTalk	England	GB	United Kingdom	Walsall	AS13285
174.3.102.70	1	1	Shaw Communications Inc.	Alberta	CA	Canada	Edmonton	AS6327
100.33.158.110	9	1	MCI Communications Services, Inc. d/b/a Verizon Business	New York	US	United States	Ozone Park	AS701
73.77.83.81	8	1	Comcast Cable Communications, LLC	Texas	US	United States	Cypress	AS7922
99.233.11.103	11	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Mississauga	AS812
24.55.229.146	1	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
66.249.73.138	1	1	Google LLC	Virginia	US	United States	Ashburn	AS15169
144.217.75.156	62347	1	OVH SAS	Quebec	CA	Canada	Beauharnois	AS16276
198.84.155.194	10	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Chatham	AS5645
76.64.68.251	2	1	Bell Canada	Ontario	CA	Canada	Kingsville	AS577
24.47.40.12	2	1	Cablevision Systems Corp.	New Jersey	US	United States	Neptune City	AS6128
47.41.199.58	1	1	Charter Communications	California	US	United States	Cerritos	AS20115
108.173.31.122	10	1	TELUS Communications Inc.	Alberta	CA	Canada	Red Deer	AS852
24.57.201.37	1	1	Cogeco Cable	Ontario	CA	Canada	Tecumseh	AS7992
45.72.217.254	25	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Toronto	AS5645
70.48.210.153	51	1	Bell Canada	Ontario	CA	Canada	Windsor	AS577
46.244.28.68	8	1	SoftLayer Technologies Inc.	Washington	US	United States	Tukwila	AS36351
154.5.201.160	109	1	TELUS Communications Inc.	British Columbia	CA	Canada	Surrey	AS852
216.209.158.179	1	1	Bell Canada	Ontario	CA	Canada	Amhertsburg	AS577
130.156.10.3	10	1	NJEDge.Net, Inc.	New Jersey	US	United States	Jersey City	AS21976
73.144.142.243	2	1	Comcast Cable Communications, LLC	Michigan	US	United States	Royal Oak	AS7922
209.141.39.88	6	1	FranTech Solutions	Nevada	US	United States	Las Vegas	AS53667
90.206.159.231	48	1	Sky UK Limited	England	GB	United Kingdom	Birmingham	AS5607
24.146.46.60	5	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
92.237.88.118	1	1	Virgin Media Limited	England	GB	United Kingdom	Bradford	AS5089
88.108.41.185	1	1	TalkTalk	England	GB	United Kingdom	Walsall	AS9105
86.29.176.95	16	1	Virgin Media Limited	England	GB	United Kingdom	Grantham	AS5089
108.170.158.152	29	1	Start Communications	Ontario	CA	Canada	Port Colborne	AS40788
206.172.99.243	126	1	Bell Canada	Quebec	CA	Canada	Saint-Sauveur	AS577
98.194.59.78	15	\N	\N	\N	\N	\N	\N	\N
184.4.40.249	10	1	CenturyLink Communications, LLC	North Carolina	US	United States	Spring Lake	AS209
24.53.252.91	1	1	Start Communications	Ontario	CA	Canada	Hamilton	AS40788
50.100.199.15	219	1	Bell Canada	Ontario	CA	Canada	Windsor	AS577
216.144.94.126	1	1	WestTel Ltd.	\N	KY	Cayman Islands	West Bay	AS36549
73.185.183.137	14	1	Comcast Cable Communications, LLC	Minnesota	US	United States	Eden Prairie	AS7922
99.236.101.104	1	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Hamilton	AS812
89.238.128.173	6	1	M247 Ltd	England	GB	United Kingdom	Nottingham	AS9009
173.3.198.30	279	1	Cablevision Systems Corp.	New Jersey	US	United States	Cassville	AS6128
184.3.32.134	4	1	CenturyLink Communications, LLC	North Carolina	US	United States	Carthage	AS209
99.251.9.99	44	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Bowmanville	AS812
74.93.173.214	23	1	Comcast Cable Communications, LLC	Florida	US	United States	Fleming Island	AS7922
38.80.64.75	2	1	Cogent Communications	Ontario	CA	Canada	Niagara Falls	AS174
65.33.187.64	2	1	Charter Communications, Inc	Florida	US	United States	Bradenton	AS33363
24.57.240.127	247	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
47.6.23.64	354	1	Charter Communications	Michigan	US	United States	Hancock	AS20115
174.89.56.142	6	1	Bell Canada	Ontario	CA	Canada	Windsor	AS577
74.113.40.93	1	1	Intelliwave, LLC	Ohio	US	United States	Leesburg	AS25943
70.31.211.216	5	1	Bell Canada	Quebec	CA	Canada	Laval	AS577
142.114.16.182	7	1	Bell Canada	Ontario	CA	Canada	Windsor	AS577
108.162.69.51	2	1	Cogeco Cable	Ontario	CA	Canada	Chatham	AS7992
174.7.191.185	5	1	Shaw Communications Inc.	British Columbia	CA	Canada	Vancouver	AS6327
74.14.151.136	7	1	Bell Canada	Ontario	CA	Canada	Toronto	AS577
198.251.83.217	59	1	FranTech Solutions	Wyoming	US	United States	Cheyenne	AS53667
24.53.107.55	8	1	Start Communications	Ontario	CA	Canada	Windsor	AS40788
216.8.182.145	19	1	Managed Network Systems Inc.	Ontario	CA	Canada	Windsor	AS7057
75.155.132.75	13	1	TELUS Communications Inc.	British Columbia	CA	Canada	Surrey	AS852
72.141.176.204	2	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Toronto	AS812
142.183.235.87	1	1	Bell Canada	Ontario	CA	Canada	Niagara Falls	AS577
184.148.152.148	1	1	Bell Canada	Ontario	CA	Canada	Niagara Falls	AS577
24.46.154.23	5	1	Cablevision Systems Corp.	New Jersey	US	United States	Asbury Park	AS6128
216.154.47.150	10	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Mississauga	AS5645
100.36.2.189	176	1	MCI Communications Services, Inc. d/b/a Verizon Business	Virginia	US	United States	Sterling	AS701
192.99.147.142	1	1	OVH SAS	Quebec	CA	Canada	Montreal	AS16276
198.200.88.200	2	1	DISTRIBUTEL COMMUNICATIONS LTD.	Ontario	CA	Canada	Windsor	AS11814
73.184.225.56	13	1	Comcast Cable Communications, LLC	Georgia	US	United States	Loganville	AS7922
108.170.149.189	10	1	Start Communications	Ontario	CA	Canada	Stoney Creek	AS40788
73.204.92.145	2	1	Comcast Cable Communications, LLC	Florida	US	United States	Miami	AS7922
184.144.230.123	1	1	Bell Canada	Quebec	CA	Canada	Ormstown	AS577
98.143.73.156	2	1	Managed Network Systems Inc.	Ontario	CA	Canada	Windsor	AS7057
66.176.52.57	13	1	Comcast Cable Communications, LLC	Florida	US	United States	Miami	AS7922
144.217.166.92	9	1	OVH SAS	Quebec	CA	Canada	Beauharnois	AS16276
24.87.198.9	16	1	Shaw Communications Inc.	British Columbia	CA	Canada	Richmond	AS6327
96.43.189.155	1	1	FLOW	Saint James	JM	Jamaica	Montego Bay	AS30689
74.14.134.203	2	1	Bell Canada	Quebec	CA	Canada	Montreal	AS577
205.185.214.73	1	1	StackPath LLC	Texas	US	United States	Dallas	AS12989
89.238.128.171	3	1	M247 Ltd	England	GB	United Kingdom	Nottingham	AS9009
98.220.118.162	1	1	Comcast Cable Communications, LLC	Illinois	US	United States	Orland Park	AS7922
70.31.66.142	17	1	Bell Canada	Ontario	CA	Canada	Brampton	AS577
24.10.99.199	1	1	Comcast Cable Communications, LLC	California	US	United States	Sacramento	AS7922
24.57.138.198	1	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
108.206.44.187	1	1	AT&T Services, Inc.	Florida	US	United States	Fort Lauderdale	AS7018
142.59.113.55	1	1	TELUS Communications Inc.	Alberta	CA	Canada	Calgary	AS852
108.170.149.242	10	1	Start Communications	Ontario	CA	Canada	Stoney Creek	AS40788
37.228.244.82	6	1	Liberty Global B.V.	Leinster	IE	Ireland	Dublin	AS6830
74.105.158.155	3	1	MCI Communications Services, Inc. d/b/a Verizon Business	New Jersey	US	United States	Eatontown	AS701
73.93.193.114	2	1	Comcast Cable Communications, LLC	California	US	United States	Santa Maria	AS7922
96.43.179.168	1	1	FLOW	Parish of Saint Ann	JM	Jamaica	Ocho Rios	AS30689
108.162.70.147	46	1	Cogeco Cable	Ontario	CA	Canada	Chatham	AS7992
196.53.18.76	172	1	The Cable of St. Kitts	New Jersey	US	United States	Edison	AS36290
108.170.186.134	1	1	Start Communications	Ontario	CA	Canada	Leamington	AS40788
109.177.220.12	177	1	Emirates Telecommunications Corporation	Ash Shariqah	AE	United Arab Emirates	Sharjah	AS5384
99.248.150.169	46	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Oshawa	AS812
99.240.103.238	6	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Toronto	AS812
24.50.233.177	1	1	Liberty Cablevision of Puerto Rico	\N	PR	Puerto Rico	Dorado	AS14638
47.187.6.30	1	1	Frontier Communications of America, Inc.	Texas	US	United States	Grapevine	AS5650
24.80.113.198	1	1	Shaw Communications Inc.	British Columbia	CA	Canada	Vancouver	AS6327
99.232.186.206	14	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Angus	AS812
107.179.195.144	1	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Windsor	AS5645
76.117.195.18	1	1	Comcast Cable Communications, LLC	New Jersey	US	United States	Middletown	AS7922
104.158.4.100	166	1	ViaNetTV Inc	Ontario	CA	Canada	Georgetown	AS54198
24.55.242.15	35	1	Cogeco Cable	Ontario	CA	Canada	Tecumseh	AS7992
216.165.201.200	4	1	CIK Telecom INC	Quebec	CA	Canada	Montreal	AS54614
72.187.159.238	1	1	Charter Communications, Inc	Florida	US	United States	Clearwater	AS33363
72.39.126.32	5	1	Cogeco Cable	Ontario	CA	Canada	Sarnia	AS7992
90.250.36.134	1	1	Vodafone Limited	England	GB	United Kingdom	Dagenham	AS5378
37.228.243.124	4	1	Liberty Global B.V.	Leinster	IE	Ireland	Dublin	AS6830
69.172.184.119	3	1	TekSavvy Solutions, Inc.	British Columbia	CA	Canada	Vancouver	AS5645
104.152.236.210	4	1	FLOW	Kingston	JM	Jamaica	Kingston	AS30689
104.158.64.44	1	1	ViaNetTV Inc	Quebec	CA	Canada	Montreal	AS54198
99.237.115.138	19	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Toronto	AS812
67.187.3.119	2	1	Comcast Cable Communications, LLC	Virginia	US	United States	Richmond	AS7922
98.203.80.129	32	1	Comcast Cable Communications, LLC	Florida	US	United States	Hollywood	AS7922
88.111.82.22	99	1	TalkTalk	England	GB	United Kingdom	Croydon	AS9105
178.128.72.0	1	1	DigitalOcean, LLC	California	US	United States	Santa Clara	AS14061
67.193.82.17	1	1	Cogeco Cable	Ontario	CA	Canada	Brockville	AS7992
198.47.44.206	1	1	Novus Entertainment Inc.	British Columbia	CA	Canada	Vancouver	AS40029
147.147.175.14	45	1	British Telecommunications PLC	England	GB	United Kingdom	Dagenham	AS6871
99.230.128.116	1	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Toronto	AS812
75.155.241.232	2	1	TELUS Communications Inc.	British Columbia	CA	Canada	Vancouver	AS852
216.232.178.163	64	1	TELUS Communications Inc.	British Columbia	CA	Canada	Surrey	AS852
166.48.40.114	1	1	Altima Telecom	Ontario	CA	Canada	Mississauga	AS22423
162.155.156.243	1	1	Charter Communications Inc	Kentucky	US	United States	Lexington	AS10796
173.33.182.80	3	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Cambridge	AS812
24.75.170.76	2	1	Ellijay Telephone Company	Georgia	US	United States	Jasper	AS25853
24.91.236.47	5	1	Comcast Cable Communications, LLC	Massachusetts	US	United States	Brockton	AS7922
24.126.235.92	46	1	Comcast Cable Communications, LLC	Georgia	US	United States	Cumming	AS7922
109.129.162.183	435	1	Proximus NV	Brussels Capital	BE	Belgium	Brussels	AS5432
73.107.85.52	2	1	Comcast Cable Communications, LLC	Florida	US	United States	Cape Coral	AS7922
97.122.219.141	1	1	CenturyLink Communications, LLC	Colorado	US	United States	Denver	AS209
174.95.215.212	1	1	Bell Canada	Ontario	CA	Canada	Toronto	AS577
99.233.0.233	42	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Mississauga	AS812
172.72.150.67	21	1	Charter Communications Inc	North Carolina	US	United States	Charlotte	AS11426
47.20.237.181	240	1	Cablevision Systems Corp.	New Jersey	US	United States	Belmar	AS6128
108.12.255.236	1	1	MCI Communications Services, Inc. d/b/a Verizon Business	Rhode Island	US	United States	Providence	AS701
67.83.143.45	51	1	Cablevision Systems Corp.	New Jersey	US	United States	Neptune City	AS6128
173.56.211.22	1	1	MCI Communications Services, Inc. d/b/a Verizon Business	New York	US	United States	Ozone Park	AS701
24.125.177.112	9	1	Comcast Cable Communications, LLC	Georgia	US	United States	Lilburn	AS7922
162.206.138.44	1	1	AT&T Services, Inc.	Illinois	US	United States	Schaumburg	AS7018
206.48.229.138	1	1	Cable & Wireless (Cayman Islands) Ltd.	Virginia	US	United States	Herndon	AS6639
173.238.82.92	1	1	Cogeco Cable	Ontario	CA	Canada	Niagara Falls	AS7992
67.86.180.31	4	1	Cablevision Systems Corp.	New Jersey	US	United States	Neptune City	AS6128
142.117.201.184	10	1	Bell Canada	Quebec	CA	Canada	Montreal	AS577
206.248.183.88	21	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Toronto	AS5645
82.12.47.130	1	1	Virgin Media Limited	England	GB	United Kingdom	Smethwick	AS5089
12.202.64.162	1	1	AT&T Services, Inc.	Ohio	US	United States	Cleveland	AS7018
209.141.140.139	2	1	CIK Telecom INC	Ontario	CA	Canada	Mississauga	AS54614
75.110.13.94	14	1	Suddenlink Communications	North Carolina	US	United States	Greenville	AS19108
47.202.254.171	20	1	Frontier Communications of America, Inc.	Florida	US	United States	Sun City Center	AS5650
24.42.37.244	2	1	Liberty Cablevision of Puerto Rico	\N	PR	Puerto Rico	Dorado	AS14638
24.55.222.235	9	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
73.138.167.236	4	1	Comcast Cable Communications, LLC	Florida	US	United States	Fort Lauderdale	AS7922
24.57.93.213	1	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
107.191.216.68	16	1	Canal + Telecom SAS	\N	GP	Guadeloupe	Basse-Terre	AS21351
96.21.174.102	1	1	Videotron Telecom Ltee	Quebec	CA	Canada	Montreal	AS5769
76.69.137.178	30	1	Bell Canada	Ontario	CA	Canada	Toronto	AS577
50.66.82.42	16	1	Shaw Communications Inc.	Alberta	CA	Canada	Calgary	AS6327
99.237.209.156	1	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Toronto	AS812
72.39.68.30	3	1	Cogeco Cable	Ontario	CA	Canada	Milton	AS7992
73.138.28.3	32	1	Comcast Cable Communications, LLC	Florida	US	United States	Miami	AS7922
209.225.140.8	1	1	Primus Telecommunications Canada Inc.	Ontario	CA	Canada	Niagara Falls	AS6407
24.185.110.231	49	1	Cablevision Systems Corp.	New Jersey	US	United States	Neptune City	AS6128
108.168.7.53	2	1	Start Communications	Ontario	CA	Canada	Stratford	AS40788
216.8.183.138	3	1	Managed Network Systems Inc.	Ontario	CA	Canada	Windsor	AS7057
198.84.154.35	3	1	TekSavvy Solutions, Inc.	Ontario	CA	Canada	Chatham	AS5645
173.72.158.221	10	1	MCI Communications Services, Inc. d/b/a Verizon Business	Virginia	US	United States	Ashburn	AS701
65.95.237.193	21	1	Bell Canada	Ontario	CA	Canada	Mississauga	AS577
24.57.148.246	8	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
142.116.54.83	2	1	Bell Canada	Ontario	CA	Canada	Mississauga	AS577
144.172.157.171	1	1	Videotron Telecom Ltee	Quebec	CA	Canada	Gatineau	AS5769
68.174.131.167	33	1	Charter Communications Inc	New York	US	United States	New York	AS12271
82.102.30.79	1	1	M247 Ltd	Nevada	US	United States	Las Vegas	AS9009
72.137.99.2	3	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Cambridge	AS812
24.48.35.69	1	1	Videotron Telecom Ltee	Quebec	CA	Canada	Chateauguay	AS5769
142.116.159.37	4	1	Bell Canada	Ontario	CA	Canada	Mississauga	AS577
24.57.250.224	2	1	Cogeco Cable	Ontario	CA	Canada	Windsor	AS7992
24.186.48.213	6	1	Cablevision Systems Corp.	New Jersey	US	United States	Cassville	AS6128
174.48.234.196	5	1	Comcast Cable Communications, LLC	Florida	US	United States	Fort Lauderdale	AS7922
184.65.167.187	4	1	Shaw Communications Inc.	British Columbia	CA	Canada	Surrey	AS6327
70.70.156.177	1	1	Shaw Communications Inc.	British Columbia	CA	Canada	Whistler	AS6327
45.50.75.246	9	1	Charter Communications Inc	California	US	United States	Cypress	AS20001
77.99.174.193	9	1	Virgin Media Limited	England	GB	United Kingdom	Wolverhampton	AS5089
216.8.130.66	3	1	Managed Network Systems Inc.	Ontario	CA	Canada	Windsor	AS7057
73.235.226.24	1	1	Comcast Cable Communications, LLC	California	US	United States	Sacramento	AS7922
70.77.216.235	2	1	Shaw Communications Inc.	Alberta	CA	Canada	Calgary	AS6327
74.66.108.97	3	1	Charter Communications Inc	New York	US	United States	Staten Island	AS12271
172.97.148.25	117	1	DISTRIBUTEL COMMUNICATIONS LTD.	Ontario	CA	Canada	Mississauga	AS11814
138.197.170.52	11	1	DigitalOcean, LLC	Ontario	CA	Canada	Toronto	AS14061
99.237.66.186	125	1	Rogers Communications Canada Inc.	Ontario	CA	Canada	Scarborough	AS812
90.252.185.186	1	1	Vodafone Limited	England	GB	United Kingdom	Redditch	AS5378
\.


--
-- Name: ips ips_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ips
    ADD CONSTRAINT ips_pkey PRIMARY KEY (ip);


--
-- Name: TABLE ips; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.ips TO detector;


--
-- PostgreSQL database dump complete
--

