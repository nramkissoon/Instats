from colorstats import Photoset, Photo
from .utils.feedmatch_utils import *
import requests
from io import BytesIO


class FeedMatch:
    """
    Class for handling data and methods regarding profile feed coherency.
    """

    def __init__(self, posts: [], pixel_count=20000):
        """
        Constructor

        :param pixel_count: how many pixels to use per post when processing
        """

        self.px_count = pixel_count
        self.urls = []

        for post in posts:
            self.urls.append(post.url)

        if len(self.urls) < 2:
            raise ValueError("Profile must contain at least 2 photos.")

        self.__photos = []
        for url in self.urls:
            response = requests.get(url)
            img = BytesIO(response.content)
            p = Photo.Photo(img, pixel_count=pixel_count)
            self.__photos.append(p)

        self.photo_set = Photoset.Photoset(self.__photos)
        pix_list = []
        for p in self.__photos:
            pix_list += p.pixel_data
        self.color_data = get_average_shades(sort_colors(pix_list), pix_list)

    # Photoset wrapper functions for self.photo_set -------------------------
    def avg_lightness(self):
        return self.photo_set.get_avg_lightness()

    def std_lightness(self):
        return self.photo_set.get_std_lightness()

    def avg_saturation(self):
        return self.photo_set.get_avg_saturation()

    def std_saturation(self):
        return self.photo_set.get_std_saturation()

    def color_likeness(self):
        return self.photo_set.get_color_likeness()

    def fraction_likeness(self):
        return self.photo_set.get_fraction_likeness()

    def lightness_likeness(self):
        return self.photo_set.get_lightness_likeness()

    def saturation_likeness(self):
        return self.photo_set.get_saturation_likeness()

    def overall_likeness(self, color_weight: float = .25,
                         fraction_weight: float = .25,
                         lightness_weight: float = .25,
                         saturation_weight: float = .25):
        return self.photo_set.get_overall_likeness(color_weight=color_weight,
                                                   fraction_weight=fraction_weight,
                                                   lightness_weight=lightness_weight,
                                                   saturation_weight=saturation_weight)
    # End of Photoset wrapper functions for self.photo_set -------------------------

    def color_match(self, image_src):
        """
        Calculate how similar input image is to rest of profile feed based on average color tones.

        :param image_src: filename of image
        :return float: similarity of image_src to rest of feed based on color tones
        """
        photo = Photo.Photo(image_src, pixel_count=self.px_count)
        running_sum = 0
        for color in self.color_data:
            try:
                running_sum += color_difference(photo.get_color_data([color])[color]['RGB'],
                                                self.color_data[color]['RGB'])
            except KeyError:
                running_sum += color_difference(self.color_data[color]['RGB'], (0, 0, 0))
        x = running_sum / len(self.color_data)
        return round((1 - x), 4)

    def fraction_match(self, image_src):
        """
        Calculate how similar input image is to rest of profile feed based on fractional color make up.

        :param image_src: filename of image
        :return float: similarity of image_src to rest of feed based on fractional color make up
        """
        photo = Photo.Photo(image_src, pixel_count=self.px_count)
        running_sum = 0
        for color in self.color_data:
            try:
                running_sum += abs(photo.get_color_data([color])[color]['%'] - self.color_data[color]['%'])
            except KeyError:
                running_sum += self.color_data[color]['%']
        x = running_sum / len(self.color_data)
        return round((1 - x), 4)

    def saturation_match(self, image_src):
        """
        Calculate how similar input image is to rest of profile feed based on average saturation.

        :param image_src: filename of image
        :return float: similarity of image_src to rest of feed based on average saturation.
        """
        photo = Photo.Photo(image_src, pixel_count=self.px_count)
        avg_saturation = self.photo_set.get_avg_saturation()
        return round(1 - (abs(photo.get_average_saturation() - avg_saturation)), 4)

    def lightness_match(self, image_src):
        """
        Calculate how similar input image is to rest of profile feed based on average lightness.

        :param image_src: filename of image
        :return float: similarity of image_src to rest of feed based on average lightness.
        """
        photo = Photo.Photo(image_src, pixel_count=self.px_count)
        avg_lightness = self.photo_set.get_avg_lightness()
        return round(1 - (abs(photo.get_average_lightness() - avg_lightness)), 4)

    def overall_match(self, image_src, color_weight: float = .25,
                      fraction_weight: float = .25,
                      lightness_weight: float = .25,
                      saturation_weight: float = .25):
        """
        Calculate overall similarity between input image and rest of profile feed.

        :param image_src: filename of image
        :param color_weight: weight attributed to color tones
        :param fraction_weight: weight attributed to fractional color make up
        :param lightness_weight: weight attributed to lightness
        :param saturation_weight: weight attributed to saturation
        :return float: similarity of image_src to rest of feed based on given weights.
        """
        return round(
            color_weight * self.color_match(image_src) +
            fraction_weight * self.fraction_match(image_src) +
            lightness_weight * self.lightness_match(image_src) +
            saturation_weight * self.saturation_match(image_src), 4)
