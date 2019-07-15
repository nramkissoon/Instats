# Instats

A Python package for processing statistics from Instagram profiles

### Installation
install instats from command line using:
```commandline
pip3 install instats
```
### Overview

Instats is a Python package for getting and working with statistics from Instagram Profiles.
There exists modules for dealing with data about when posts were made, engagement metrics, and visual cohesiveness
of a profiles posts. It relies heavily on the [instaloader package](https://instaloader.github.io/index.html) for 
logging into Instagram and getting profile and post data. 

#### Basic Usage

From instats import instatsprofile and create and InstatsProfile object:
```python
from instats import instatsprofile

p = instatsprofile.InstatsProfile(username='some public profile')
```

Parameters for the InstatsProfile constructor:
 - *username*: username of an Instagram profile (string)
 - *password*: password of an Instagram profile (string), required for private accounts
 - *ToP_n_most_recent*: how many of a profiles most recent posts to use for time of post data (int)
 - *feedmatch*: indicate whether instance will need to process images beforehand (bool)
 - *FM_n_most_recent*: how many most recent images to consider for feedmatch (int)
 - *pixel_count_per_image*: how many pixels to use per image when processing feedmatch data (int)
 - *Eng_n_most_recent*: how many most recent posts to consider for engagement metrics (int)
 
Once an InstatsProfile is instantiated, all relevant modules and methods can be called and used.

### Limitations

Private accounts need a password to be accessed and are considerably slower to get post data from.
Furthermore, getting too many recent posts to process may cause instaloader to throw a too many requests error,
so processing several hundreds of posts from a large account is clumsy and slow.

### Possible Features to Add in the Future

1. Get a profile's most engaged followers by ranking who likes/comments on the most posts in a profile.
(this results in a too many requests error for accounts with thousands of likes per post)
2. Module for processing data on the locations of posts made.
3. Module for processing hashtag statistics and their effectiveness on engagement.
