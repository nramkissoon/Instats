from datetime import timedelta
import time
from statistics import mean, stdev, median


class TimeOfPost:
    """
    Class for handling profile data regarding the time posts are made.
    """

    def __init__(self, posts: []):
        """
        Constructor

        :param posts: list of Instaloader.Post objects

        """
        self.post_times = self.__post_times(posts)

        if len(self.post_times) <= 2:
            raise ValueError("Profile must have at least 3 posts.")

        self.__times_between_posts = []
        prev = self.post_times[0]

        i = 1
        while i < len(self.post_times):
            self.__times_between_posts.append(
                time.mktime(prev.timetuple()) - time.mktime(self.post_times[i].timetuple()))
            prev = self.post_times[i]
            i += 1

    @staticmethod
    def __post_times(posts):
        post_times = []
        for post in posts:
            post_times.append(post.date_local)
        return post_times

    def avg_post_frequency(self, as_string=False):
        """
        Calculate the average post frequency of a set of posts.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: average post frequency of a set of posts
        """
        avg = mean(self.__times_between_posts)
        if as_string:
            return str(timedelta(seconds=round(avg, 2)))
        return avg

    def get_post_frequency_stdev(self, as_string=False):
        """
        Calculate the standard deviation of post frequency of a set of posts.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: standard deviation of post frequency of a set of posts
        """
        if as_string:
            return str(timedelta(seconds=round(stdev(self.__times_between_posts), 2)))
        return stdev(self.__times_between_posts)

    def get_post_frequency_med(self, as_string=False):
        """
        Calculate the median of time between posts.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: median of time between posts
        """
        if as_string:
            return str(timedelta(seconds=round(median(self.__times_between_posts), 2)))
        return median(self.__times_between_posts)

    def longest_time_no_post(self, as_string=False):
        """
        Get the longest period of time between two posts.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: longest period of time between two posts
        """
        from_last_post = time.time() - time.mktime(self.post_times[0].timetuple())
        if as_string:
            return str(timedelta(seconds=round(max(self.__times_between_posts + [from_last_post]), 2)))
        return max(self.__times_between_posts + [from_last_post])

    def time_since_last_post(self, as_string=False):
        """
        Get the current amount of time since last post.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: current amount of time since last post
        """
        from_last_post = time.time() - time.mktime(self.post_times[0].timetuple())
        if as_string:
            return str(timedelta(seconds=round(from_last_post)))
        return from_last_post

    def shortest_time_between_posts(self, as_string=False):
        """
        Get the shortest period of time between two posts.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: shortest period of time between two posts
        """
        if as_string:
            return str(timedelta(seconds=round(min(self.__times_between_posts), 2)))
        return min(self.__times_between_posts)

    def avg_post_time(self, as_string=True):
        """
        Get the average time of day of when posts are made.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: average time of day of when posts are made
        """
        vals = []
        for posttime in self.post_times:
            m = posttime.minute * 60
            hr = posttime.hour * 60 * 60
            sec = posttime.second
            vals.append(m + hr + sec)
        avg = mean(vals)
        if as_string:
            return str(timedelta(seconds=avg, microseconds=0))
        return avg

    def stdev_post_time(self, as_string=True):
        """
        Get the standard deviation of the time of day of when posts are made.

        :param as_string: indicates whether or not to return a string in standard time formatting or in seconds (int)
        :return: standard deviation of the time of day of when posts are made
        """
        vals = []
        for posttime in self.post_times:
            m = posttime.minute * 60
            hr = posttime.hour * 60 * 60
            sec = posttime.second
            vals.append(m + hr + sec)
        st = stdev(vals)
        if as_string:
            return str(timedelta(seconds=st, microseconds=0))
        return st
