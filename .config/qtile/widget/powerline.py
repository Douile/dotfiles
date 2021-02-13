# -*- coding:utf-8 -*-

# Copyright (c) 2020 Douile
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar
from libqtile.log_utils import logger
from libqtile.widget import base

class Powerline(base._Widget):
    """Draws a triangle"""

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('length', 10, 'Size of widget'),
        ('right', False, 'Direction of arrow (when horizontal)'),
        ('foreground', 'ffffff', 'Foreground colour'),
    ]

    def __init__(self, length=10, **config):
        base._Widget.__init__(self, length, **config)
        self.add_defaults(Powerline.defaults)

    def draw(self):
        if self.length > 0:
            self.drawer.clear(self.background or self.bar.background)

            self.drawer.set_source_rgb(self.foreground)
            if self.right:
                self.drawer.ctx.move_to(0, 0)
                self.drawer.ctx.line_to(self.length, self.bar.height/2)
                self.drawer.ctx.line_to(0, self.bar.height)
            else:
                self.drawer.ctx.move_to(self.length, 0)
                self.drawer.ctx.line_to(0, self.bar.height/2)
                self.drawer.ctx.line_to(self.length, self.bar.height)
            self.drawer.ctx.close_path()
            self.drawer.ctx.fill()

            self.drawer.draw(offsetx=self.offset, width=self.length)
