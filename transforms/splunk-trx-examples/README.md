# Install the Splunk Enterprise SDK for Python

Using pip

```
pip install splunk-sdk 
```

# Connect to Splunk Enterprise using the Splunk Enterprise SDK for Python

To start a Splunk Enterprise session, the first thing your program must do is connect to Splunk Enterprise by sending login credentials to the splunkd server. 
Splunk Enterprise returns an authentication token, which is then automatically included in subsequent calls for the rest of your session. By default, the token is valid for one hour, but is refreshed every time you make a call to splunkd.


https://dev.splunk.com/enterprise/docs/devtools/python/sdk-python/howtousesplunkpython/howtoconnectpython

The basic steps to connect to Splunk Enterprise are as follows:

1. Import the splunklib.client module. This module contains the Service class, which is the primary entry point to the Splunk client library and provides access to most Splunk Enterprise resources.
2. Create a Service instance by using the connect function, which logs in and returns the new object.


Here are the different ways to connect to Splunk Enterprise.

## Log in using a bearer token

Refer to [bearer token login](/transforms/splunk-trx-examples/splunk_api_auth/bearer_token.py)

## Log in using a session key

Refer to [session key login](\splunk_api_auth\session_key.py)

## Log in using your username and password

Refer to [username and password login](\splunk_api_auth\username_password.py)


# Splunk Auth Example Transforms

## Bearer Token
Refer to [bearer token auth transform](\transforms\BearerTokenAuth.py)

## Session Key
Refer to [session key auth transform](\transforms\SessionKeyAuth.py)

## Username and Password
Refer to [username and password transform](\transforms\UsernamePasswordAuth.py)

# Splunk Search Example Transforms

## Authentication
The splunk example transforms use bearer API authentication.
Other authentication methods can be found in the `splunk_api_auth` folder

## Search Mode
The examples use the Splunklib `one-shot` search mode to retrieve results.

One-shot: A one-shot search is a blocking search that is scheduled to run immediately. Instead of returning a search job, this mode returns the results of the search once completed. Because this is a blocking search, the results are not available until the search has finished.

## To create a basic one-shot search and display results
The simplest way to get data out of Splunk Enterprise is with a one-shot search, which creates a synchronous search. Unlike normal or blocking searches, the one-shot search does not create and return a search job, but rather it blocks until the search finishes and then returns a stream containing the events. To set properties for the search (for example, to specify a time range to search), create a dictionary with the property key-value pairs. Some common properties are:

- _output_mode_: Specifies the output format of the results (XML, JSON, JSON_COLS, JSON_ROWS, CSV, ATOM, or RAW).
- _earliest_time_: Specifies the earliest time in the time range to search. The time string can be a UTC time (with fractional seconds), a relative time specifier (to now), or a formatted time string.
- _latest_time_: Specifies the latest time in the time range to search. The time string can be a UTC time (with fractional seconds), a relative time specifier (to now), or a formatted time string.
- _rf_: Specifies one or more fields to add to the search.

https://dev.splunk.com/enterprise/docs/devtools/python/sdk-python/howtousesplunkpython/howtorunsearchespython/

## Base search

The code example runs a Splunk search query to retrieve the results from the main index from the last 2 years

Refer to [base search](\transforms\BaseSearch.py)

https://docs.splunk.com/Documentation/SCS/current/Search/Timevariables


## Date time range search

The sample transform contains a date time range filter that searches the main index for the given date time range

Refer to [date time range search](\transforms\DateTimeSearch.py)


## Index search

The sample transform contains a setting to input a Splunk index name to allow filtering of search results based on index

Refer to [index search](\transforms\IndexSearch.py)


## Where condition search


Refer to [where search](\transforms\WhereSearch.py)

https://docs.splunk.com/Documentation/SCS/current/SearchReference/WhereCommandOverview


## Sort search

Refer to [sort search](\transforms\SortSearch.py)

https://docs.splunk.com/Documentation/SCS/current/SearchReference/SortCommandOverview
