Searx RSS Feed Generator

Searx RSS Feed Generator is a Python script that creates an RSS feed and an OPML feed based on search results from a Searx instance. The script fetches search results periodically (every 4 hours by default) and generates an RSS feed with search results that have been published within a specified time frame.
Features

    Fetch search results from a Searx instance using a custom search query
    Generate an RSS feed with the search results
    Create an OPML feed for easy subscription to the generated RSS feed
    Validate the generated RSS feed
    Periodically update the RSS and OPML feeds based on a schedule

Installation

    Clone the repository:

bash

git clone https://github.com/yourusername/searx_rss_feed_generator.git

    Install the required dependencies:

pip install -r requirements.txt

Usage

    Edit the rss_server.py script to set your desired search query and Searx instance URL.

    Run the script:

python rss_server.py

    The script will periodically generate an RSS feed (searx_rss_feed.xml) and an OPML feed (searx_opml_feed.xml) based on the search results from the specified Searx instance.

    Access the generated RSS feed and OPML feed using a web server or a local file path, depending on your setup.

Customization

You can customize the script by modifying the following variables in the rss_server.py file:

    search_query: Set the search query for the Searx instance.
    searx_instance_url: Set the URL of the Searx instance you want to use.
    prefs_url: Set the URL for the preferences of the Searx instance.
    hours: Set the maximum age (in hours) of search results to be included in the RSS feed.
