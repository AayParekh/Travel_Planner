{\rtf1\ansi\ansicpg1252\cocoartf2907
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Bold;\f1\froman\fcharset0 Times-Roman;\f2\fmodern\fcharset0 Courier;
}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat0\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid1\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}
{\list\listtemplateid2\listhybrid{\listlevel\levelnfc0\levelnfcn0\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{decimal\}}{\leveltext\leveltemplateid101\'01\'00;}{\levelnumbers\'01;}\fi-360\li720\lin720 }{\listname ;}\listid2}
{\list\listtemplateid3\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat0\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid201\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid3}
{\list\listtemplateid4\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat0\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid301\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid4}
{\list\listtemplateid5\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat0\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid401\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid5}
{\list\listtemplateid6\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat0\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid501\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid6}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}{\listoverride\listid2\listoverridecount0\ls2}{\listoverride\listid3\listoverridecount0\ls3}{\listoverride\listid4\listoverridecount0\ls4}{\listoverride\listid5\listoverridecount0\ls5}{\listoverride\listid6\listoverridecount0\ls6}}
\margl1440\margr1440\vieww16080\viewh17560\viewkind0
\deftab720
\pard\pardeftab720\sa321\partightenfactor0

\f0\b\fs48 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Climate-Aware Itinerary Generator (Agentic AI class project)\
\pard\pardeftab720\sa298\partightenfactor0

\fs36 \cf0 Assignment requirements\
\pard\tx220\tx720\pardeftab720\li720\fi-720\partightenfactor0
\ls1\ilvl0
\f1\b0\fs24 \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Build an agentic system with 
\f0\b at least 3 tools
\f1\b0 \
\pard\tx220\tx720\pardeftab720\li720\fi-720\partightenfactor0
\ls1\ilvl0
\f0\b \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 At least one tool makes an external API call
\f1\b0 \
\pard\pardeftab720\sa240\partightenfactor0
\cf0 \
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs36 \cf0 Concept\
\pard\pardeftab720\sa240\partightenfactor0

\f1\b0\fs24 \cf0 Given a destination, dates, and trip length, the agent 
\f0\b generates
\f1\b0  a day-by-day itinerary constrained by:\
\pard\tx220\tx720\pardeftab720\li720\fi-720\partightenfactor0
\ls2\ilvl0\cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	1	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Historical weather for those dates\
\ls2\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	2	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 My past itineraries (pacing, activity mix, preferences)\
\ls2\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	3	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Travel time between stops (so days are geographically sensible)\
\pard\pardeftab720\sa240\partightenfactor0
\cf0 It generates an itinerary; it does not just score an existing one.\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs36 \cf0 Scope limits (keep it small)\
\pard\tx220\tx720\pardeftab720\li720\fi-720\partightenfactor0
\ls3\ilvl0
\f1\b0\fs24 \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}Stick to the basic chatbot used in index.html and app.py. Feel free to customize it, but don\'92t make a complicated UI. We are also sticking with vertex_ai/gemini-3.5-flash-lite\
{\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Any city worldwide (user types a city name, agent resolves it), one city per trip, 3-4 days max\
\ls3\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Fixed output format: day-by-day plan, outdoor activities on good-weather days, indoor on bad days\
\ls3\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 NO venue/activity search APIs, booking, or full routing UI\
\ls3\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Model suggests places from its own knowledge; 
\f0\b geocoding doubles as a check that the place exists
\f1\b0 . If Nominatim finds nothing, the agent drops or replaces the suggestion.\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs36 \cf0 Tools\

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrt\brdrnil \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth3432\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx2880
\clvertalc \clshdrawnil \clwWidth1259\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5760
\clvertalc \clshdrawnil \clwWidth5914\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0

\fs24 \cf0 Tool\cell 
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0
\cf0 Type\cell 
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0
\cf0 Source\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth3432\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx2880
\clvertalc \clshdrawnil \clwWidth1259\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5760
\clvertalc \clshdrawnil \clwWidth5914\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f2\b0\fs26 \cf0 get_historical_weather
\f1\fs24 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 External API\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Open-Meteo archive API (free, no key)\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth3432\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx2880
\clvertalc \clshdrawnil \clwWidth1259\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5760
\clvertalc \clshdrawnil \clwWidth5914\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f2\fs26 \cf0 read_my_itineraries
\f1\fs24 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Local\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Text/markdown files of my past itineraries. Located in \'91Example Itineraries\'92 folder. \cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrt\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth3432\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx2880
\clvertalc \clshdrawnil \clwWidth1259\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5760
\clvertalc \clshdrawnil \clwWidth5914\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f2\fs26 \cf0 get_travel_time
\f1\fs24 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 External API\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Nominatim (geocode) + OSRM (route), both free and keyless\cell \lastrow\row
\pard\pardeftab720\sa240\partightenfactor0
\cf0 Note: 
\f2\fs26 get_historical_weather
\f1\fs24  needs lat/long, so the agent must geocode the destination first. With any-city scope, add a dedicated fourth 
\f2\fs26 geocode_place
\f1\fs24  tool (Nominatim, or Open-Meteo's geocoding API). Ambiguous names ("Paris" vs Paris, TX) are a real risk, so the tool should accept an optional country and return several candidates plus country/region so the agent can pick.\
Any-city caveats:\
\pard\tx220\tx720\pardeftab720\li720\fi-720\partightenfactor0
\ls4\ilvl0\cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 The public OSRM demo server only reliably supports the driving profile. For walking times, either compute from straight-line distance (~5 km/h) or use a foot-routing endpoint such as routing.openstreetmap.de. Verify before relying on it.\
\ls4\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Geocoding place names in non-English cities can fail on spelling variants. The agent should retry with an alternate name or drop the place.\
\ls4\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Open-Meteo archive data is global but coarse (grid-based), so treat results as "typical conditions," not exact.\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs36 \cf0 Draft tool schemas (Anthropic-style JSON; translate to whatever Python package I use)\
\pard\pardeftab720\partightenfactor0

\f2\b0\fs26 \cf0 [\
  \{\
    "name": "get_historical_weather",\
    "description": "Daily temp and precipitation for a location over a date range in a past year. Use to estimate typical conditions for planned travel dates.",\
    "input_schema": \{\
      "type": "object",\
      "properties": \{\
        "latitude": \{"type": "number"\},\
        "longitude": \{"type": "number"\},\
        "start_date": \{"type": "string", "description": "YYYY-MM-DD, a past date"\},\
        "end_date": \{"type": "string", "description": "YYYY-MM-DD"\}\
      \},\
      "required": ["latitude", "longitude", "start_date", "end_date"]\
    \}\
  \},\
  \{\
    "name": "read_my_itineraries",\
    "description": "Returns the user's past itineraries as text. Use to infer pacing, activity mix, and preferences.",\
    "input_schema": \{\
      "type": "object",\
      "properties": \{\
        "keyword": \{"type": "string", "description": "Optional filter, e.g. 'beach' or 'city'"\}\
      \}\
    \}\
  \},\
  \{\
    "name": "get_travel_time",\
    "description": "Geocodes two place names and returns walking and driving time between them. Returns an error if a place can't be found.",\
    "input_schema": \{\
      "type": "object",\
      "properties": \{\
        "origin": \{"type": "string"\},\
        "destination": \{"type": "string"\},\
        "mode": \{"type": "string", "enum": ["walking", "driving"]\}\
      \},\
      "required": ["origin", "destination"]\
    \}\
  \}\
]\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs36 \cf0 Implementation notes for Python\
\pard\tx220\tx720\pardeftab720\li720\fi-720\partightenfactor0
\ls5\ilvl0
\f1\b0\fs24 \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Language: Python (primary), so the agent loop and tool functions will be in Python.\
\ls5\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Open-Meteo archive data lags real time by a few days, so query past years for "typical conditions," not the current week.\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs36 \cf0 Testing plan\
\pard\tx220\tx720\pardeftab720\li720\fi-720\partightenfactor0
\ls6\ilvl0
\f1\b0\fs24 \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Include at least one test case where weather clearly changes the plan (e.g., a rainy month in a destination that is normally outdoor-focused), so it's visible that the tools matter.\
\ls6\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Include a case where the model suggests a place that fails geocoding, to show the verification behavior.\
\pard\pardeftab720\sa298\partightenfactor0

\f0\b\fs36 \cf0 Next step\
\pard\pardeftab720\sa240\partightenfactor0

\f1\b0\fs24 \cf0 Write the agent loop in Python, then each tool function, then test end to end on one city.\
}