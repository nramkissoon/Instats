from statistics import mean, stdev
from instaloader import Profile, Post


class Engagement:

    def __init__(self, prf: Profile, posts: [Post]):
        """
        Constructor

        :param prf: Instaloader.Profile object
        :param posts: list of Instaloader.Post objects

        """
        self.profile = prf
        self.posts = posts

    def avg_comment_like_ratio(self):
        """
        Returns the ratio between average comments to average likes of a profile
        """
        return self.avg_comments() / self.avg_likes()

    def avg_like_follower_ratio(self):
        """
        Returns the ratio between average likes and number of followers of a profile
        """
        return round(self.avg_likes() / self.profile.followers, 4)

    def avg_like_view_ratio(self):
        """
        Returns the ratio of average likes of video posts to the average views
        """
        return self.avg_video_likes() / self.avg_views()

    def avg_video_duration_like_ratio(self):
        """
        Returns the ratio of average video durations and video likes
        """
        return self.avg_video_duration() / self.avg_video_likes()

    def avg_video_duration(self):
        """
        Returns the average video duration of video posts
        """
        return round(mean([p.video_duration for p in self.posts if p.is_video]))

    def avg_views(self):
        """
        Returns the average views of video posts
        """
        return round(mean([p.video_view_count for p in self.posts if p.is_video]))

    def avg_video_likes(self):
        """
        Returns the average likes of video posts
        """
        return round(mean([p.likes for p in self.posts if p.is_video]))

    def avg_likes(self):
        """
        Returns average likes of a profile
        """
        return round(mean([p.likes for p in self.posts]))

    def std_likes(self):
        """
        Returns standard deviation of likes of a profile
        """
        return round(stdev([p.likes for p in self.posts]))

    def min_likes(self):
        """
        Returns the minimum likes gotten from a post
        """
        return min([p.likes for p in self.posts])

    def max_likes(self):
        """
        Returns the maximum likes gotten from a post
        """
        return max([p.likes for p in self.posts])

    def avg_comments(self):
        """
        Returns the average number of comments per post
        """
        return round(mean([p.comments for p in self.posts]), 0)

    def std_comments(self):
        """
        Returns the standard deviation of comments per post
        """
        return round(stdev([p.comments for p in self.posts]), 0)

    def min_comments(self):
        """
        Returns the minimum number of comments received by a post
        """
        return min([p.comments for p in self.posts])

    def max_comments(self):
        """
        Returns the maximum number of comments received by a post
        """
        return max([p.comments for p in self.posts])
