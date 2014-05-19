import os
import pkg_resources
import json

from flask import Blueprint, url_for, Markup


class Gemoji(object):

    @classmethod
    def init_app(self, app):
        app.config.setdefault('GEMOJI_CLASS', 'gemoji')
        gemoji_images_path = (pkg_resources
            .resource_filename(__package__, 'static/images/emoji'))
        names = map(lambda s: os.path.splitext(s)[0],
                    filter(lambda s: s.endswith('.png'),
                           os.listdir(gemoji_images_path)))
        gemoji_files_path =  (pkg_resources
            .resource_filename(__package__, 'static/files'))
        gemoji_map = "%s/%s" % tuple([gemoji_files_path, "emojimap.json"])
        f = open(gemoji_map, "r")
        json_data = json.load(f, encoding="UTF8")
        self.char_map = {}
        for mapping in json_data["map"]:
            self.char_map[mapping["key"]] = mapping["value"]
        gemoji = Blueprint('gemoji', __name__, static_folder='static')
        app.register_blueprint(gemoji, url_prefix='/gemoji')

        @app.template_filter('gemoji')
        def gemoji_filter(s, height='auto'):
            s = self.replace_unicode(s)
            splits = s.split(':')
            splits_len = len(splits)
            out = ''
            for i, w in enumerate(splits):
                if w in names:
                    out = out[:-1]
                    out += Markup('<img src="%s" alt="%s" class="%s" height="%s">' % (
                        url_for('gemoji.static',
                                filename='images/emoji/%s.png' % w),
                        w,
                        app.config['GEMOJI_CLASS'],
                        height,
                    ))
                elif i + 1 < splits_len:
                    out += w + ':'
                else:
                    out += w

            return out


    # This feature translates unicode characters into emoji strings
    @classmethod
    def name_for(self, character):
        if character in self.char_map:
            return self.char_map[character]
        else:
            return character

    @classmethod
    def replace_unicode(self, s):
        for key in self.char_map.keys():
            s = s.replace(key, self.char_map[key])
        return s
