SmartClip
=========

[Website](http://www.smartclip.me/)

[Chrome Extension](https://chrome.google.com/webstore/detail/smartclip/dfinnoojjhjeehmahanjjbcdjpdmepge)


The smart way to capture the web. Clip now, read later. With the SmartClip Google Chrome extension, you can capture text, links, and images seamlessly to your SmartClip account. 
Gather anything from the web when inspiration hits, whether it's for business or pleasure. 

Powered by SmartFile
====================
SmartFile provides powerful integration to give you control over your data. All your clippings are saved automatically to your SmartFile account and available for download as PDF.

Installation
============
Requires Python 2.7 and MySQL

1. Clone this repo.
2. Set up a virtual environment with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
2. Install requirements by running `pip install -r requirements.txt`
3. You will need to create a `secrets.py` module in the smartclip directory. In there you will need to include your own generated keys through [SmartFile](https://www.smartfile.com/dev/): `SMARTFILE_API_KEY`, `SMARTFILE_API_PASSWORD`, `OAUTH_TOKEN`, `OAUTH_SECRET`
4. Change the database setting to a database of your choice.

License
========
Copyright 2013 (c), Stephanie Chan and Manpreet Singh. This project is protected under the GNU General Public License.
