from .feedmatch import FeedMatch
from .timeofpost import TimeOfPost
from .engagement import *
from instaloader import Instaloader, Profile, TwoFactorAuthRequiredException, LoginRequiredException
from pandas import DataFrame


class InstatsProfile(object):
    """
    Class for a single Instagram account.
    """

    def __init__(self,
                 username: str,
                 password: str = None,
                 ToP_n_most_recent: int = 9,
                 feedmatch: bool = True,
                 FM_n_most_recent: int = 9,
                 pixel_count_perimage: int = 20000,
                 Eng_n_most_recent: int = 9):
        """
        Constructor

        :param username: Instagram username
        :param password: Instagram password (required for private accounts)
        :param ToP_n_most_recent: how many recent posts to consider for time of post data
        :param feedmatch: whether or not to include feedmatch processing in this instance
        :param FM_n_most_recent: n most recent photos to consider for feed matching
        :param pixel_count_perimage: how many pixels to process per image
        """
        self.username = username
        self.__IL_instance = Instaloader()
        self.logged_in = False

        if password is not None:
            try:
                self.__IL_instance.login(self.username, password)
                self.logged_in = True
            except TwoFactorAuthRequiredException:
                print("Suggested solution: turn off Two-Factor Authentication before using this package.")
        self.profile = Profile.from_username(self.__IL_instance.context, self.username)
        if self.profile.is_private and password is None:
            raise LoginRequiredException("Password field required for private profiles.")

        num_posts = max([ToP_n_most_recent, FM_n_most_recent, Eng_n_most_recent])
        self.__posts = []
        try:
            p = self.profile.get_posts()
            for post in p:
                if num_posts == 0:
                    break
                else:
                    self.__posts.append(post)
                    if not post.is_video:
                        num_posts -= 1
        except IndexError:
            raise IndexError("Profile must contain posts.")
        if len(self.__posts) == 0:
            raise ValueError("Profile contains no posts")

        self.__photo_posts = []
        for post in self.__posts:
            if not post.is_video:
                self.__photo_posts.append(post)

        self.top = TimeOfPost(self.__posts[:ToP_n_most_recent])

        if feedmatch:
            self.feedmatch = FeedMatch(posts=self.__photo_posts[:FM_n_most_recent],
                                       pixel_count=pixel_count_perimage)

        self.engagement = Engagement(self.profile, posts=self.__posts[:Eng_n_most_recent])

    def follower_following_ratio(self):
        """
        Get follower to following ratio of profile.
        """
        return self.profile.followers / self.profile.followees

    def post_data(self):
        """
        Creates a pandas DataFrame of data from a profiles posts that can be used for other processing.
        """
        d = {'post url': [], 'date of post': [], 'post time of day': [], 'likes': [],
             'comments': [], 'is video': [], 'video views': [], 'location': []}
        for post in self.__posts:
            d['post url'].append(post.url)
            d['date of post'].append(post.date_local.timetuple())

            h = post.date_local.hour * 60 * 60
            m = post.date_local.minute * 60
            s = post.date_local.second

            d['post time of day'].append(h + m + s)
            d['likes'].append(post.likes)
            d['comments'].append(post.comments)
            d['is video'].append(post.is_video)
            d['video views'].append(post.video_view_count)
            d['location'].append(post.location)
        df = DataFrame(data=d)
        return df
