# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
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

# -*- coding: utf-8 -*-

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, extension, hook
from libqtile.config import Click, Drag, Group, Key, Screen, Match, Rule
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import widget as custom_widget

from Xlib import X, display
from Xlib.ext import randr

import subprocess
import re

mod = "mod4"
border_focus = "#505050"
border_normal = "#2c2c2c"
terminal = guess_terminal()
GROUP_NAMES = "asdfuiop"

@lazy.function
def float_to_front(qtile):
    """
    Bring all floating windows of the group to front"""
    global floating_windows
    floating_windows = []
    for window in qtile.currentGroup.windows:
        if windows.floating:
            window.cmd_bring_to_front()
            floating_windows.append(window)
    floating_windows[-1].cmd_focus()

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle fullscreen
    Key([mod, "control"], "f", lazy.window.toggle_fullscreen(),
        desc="Toggle active window fullscreen"),

    # Toggle float
    Key([mod, "control"], "space", lazy.window.toggle_floating(),
        desc="Toggle active window floating"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod, "shift"], "Tab", float_to_front, desc="Move floating windows to front"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    # Manage session
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "l", lazy.spawn("dm-tool lock"), desc="Lock"),

    # Media keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),

    # Program hotkeys
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Spawn a rofi app menu"),
    Key([mod, "shift"], "r", lazy.run_extension(extension.DmenuRun(dmenu_prompt="> ")), desc="Spawn a dmenu"),

    Key([mod], "F1", lazy.spawn([terminal,"-e","htop"]), desc="Open htop"),
    Key([mod], "F2", lazy.spawn("librewolf"), desc="Open firefox"),
    Key([mod], "F3", lazy.spawn("pcmanfm"), desc="Open file manager"),
    Key([mod, "control"], "m", lazy.spawn("pavucontrol"), desc="Open volume mixer"),

    # Shutdown
    Key([mod], "0", lazy.run_extension(extension.CommandSet(dmenu_prompt="Power" , commands={
        "poweroff": "poweroff",
        "reboot": "reboot",
        "lock": "dm-tool lock",
        "logout": "qtile cmd-obj -o cmd -f shutdown",
        "reload": "qtile cmd-obj -o cmd -f restart"
    }, dmenu_command='rofi -dmenu')), desc="Open dmenu shutdown prompt"),

    # Screenshot
    Key([], "Print", lazy.spawn(["sh", "-c", "\"$HOME/.scripts/screenshot.sh\""]),desc="Take a screenshot"),
    # Key([], "Print", lazy.spawn(["sh","-c","FILE=\"$PWD/sc-$(date +%Y-%m-%d-%H-%M-%S).png\";maim -s -u | tee \"$FILE\" | xclip -selection clipboard -t image/png && notify-send -i \"$FILE\" \"Screeshotted\" \"File saved as $FILE\""]), desc="Take a screenshot"),
    Key(["shift"], "Print", lazy.spawn("peek"), desc="Take a animated screenshot"),
]

groups = [Group(i) for i in GROUP_NAMES]
groups.extend([
    Group("1", matches=[Match(wm_class="discord")], exclusive=False, layout="max", persist=True, init=True, label="Discord"),
    Group("2", matches=[Match(wm_class="spotify"),Match(wm_class="spot")], exclusive=False, layout="max", persist=True, init=True, label="Spotify"),
  ])

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Tile(border_focus=border_focus, border_normal=border_normal, border_width=0, ratio=0.55, add_after_last=True),
    layout.Max(),
    #layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    #layout.Bsp(),
    #layout.Columns(),
    #layout.Matrix(),
    #layout.MonadTall(),
    #layout.MonadWide(),
    #layout.RatioTile(),
    layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy(),
]

widget_defaults = dict(
    font='roboto mono',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

BAR_COLOR_TIME = 'd62839'
BAR_COLOR_MUSIC = 'ea9010'
BAR_COLOR_CPU = '1882b7'
BAR_COLOR_NETWORK = '6ab547'

def generic_bar(systray=False):
    widgets = [
        widget.GroupBox(disable_drag=True, hide_unused=True, this_current_screen_border=BAR_COLOR_CPU, background=BAR_COLOR_NETWORK),
        widget.CurrentLayout(background=BAR_COLOR_NETWORK),
        custom_widget.Powerline(foreground=BAR_COLOR_NETWORK, background=BAR_COLOR_MUSIC, right=True),
        # widget.Prompt(),
        widget.WindowName(show_state=True, width=bar.CALCULATED, background=BAR_COLOR_MUSIC),
        custom_widget.Powerline(foreground=BAR_COLOR_MUSIC, right=True),
        widget.Chord(
            chords_colors={
                'launch': ("#ff0000", "#ffffff"),
            },
            name_transform=lambda name: name.upper(),
        ),
        widget.Spacer(length=bar.STRETCH),
    ]

    if systray:
        widgets.extend([
          widget.Systray(),
          widget.Spacer(length=5),
        ])

    widgets.extend([
        custom_widget.Powerline(foreground=BAR_COLOR_NETWORK, right=False),
        widget.CheckUpdates(background=BAR_COLOR_NETWORK),
        # widget.DF(visible_on_warn=False, format="Disk remaining: {f}{m}/{r:.0f}%"),
        # widget.Net(interface='enp5s0', format="{down} ↓↑ {up}"),
        getattr(custom_widget,'CustomNet',widget.Net)(interface="enp5s0", format="{down} ↓↑ {up}", background=BAR_COLOR_NETWORK),
        custom_widget.Powerline(foreground=BAR_COLOR_CPU, background=BAR_COLOR_NETWORK),
        widget.Memory(format="{MemUsed}Mb", foreground="ffffff", foreground_alert="fc8f8f", background=BAR_COLOR_CPU),
        # widget.CPU(format="{freq_current}GHz {load_percent:02.01f}%", foreground="f0f000"),
        getattr(custom_widget,'CPU',widget.CPU)(format="{freq_current:04.2f}GHz {load_percent:04.1f}%", foreground="ffffff", foreground_warn="f0f000", foreground_alert="fc8f8f", background=BAR_COLOR_CPU),
        # widget.ThermalSensor(tag_sensor=None, foreground="fc8f8f", foreground_alert="ff0000"),
        custom_widget.ThermalHwmon(foreground="ffffff", foreground_alert="fc8f8f", background=BAR_COLOR_CPU),
        custom_widget.Powerline(foreground=BAR_COLOR_MUSIC, background=BAR_COLOR_CPU),
        widget.PulseVolume(volume_app="pavucontrol", background=BAR_COLOR_MUSIC),
        # widget.Volume(volume_app="pavucontrol", get_volume_command='pamixer --get-volume', mute_command='pamixer -t', volume_up_command='pamixer -i 5', volume_down_command='pamixer -d 5', background=BAR_COLOR_MUSIC),
        custom_widget.Powerline(foreground=BAR_COLOR_TIME, background=BAR_COLOR_MUSIC),
        widget.Clock(format='%Y-%m-%d %a %H:%M', background=BAR_COLOR_TIME),
    ])
    return bar.Bar(widgets, 24, background='#000000.0', opacity=1)

def get_screen_count():
    count = 0

    d = display.Display()
    s = d.screen()
    window = s.root.create_window(0, 0, 1, 1, 1, s.root_depth)
    res = randr.get_screen_resources(window)
    for id in res.outputs:
        output = randr.get_output_info(window, id, 0)
        count += output.connection ^ 1 # connection = 0 means display active
    window.destroy()
    return count

screen_count = get_screen_count()
screens = [Screen(top=generic_bar(systray=i == screen_count-1)) for i in range(0, screen_count)]

# screens = [
#     Screen(top=generic_bar(systray=True)),
# #    Screen(top=generic_bar()),
# ]

# Drag floating layouts
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
# main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    Match(role='modal'),
    Match(role='Dialog'),
    Match(role='dialog'),
    Match(wm_type='dialog'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='pavucontrol'), # pavucontrol
    # {'wmclass': 'Steam', 'wname': 'Steam Login'}, # Steam login
    # {'wname': 'Steam - News'}, # Steam news
    Match(wm_class='Steam', title=re.compile('^Install -')), # Steam install dialog
    # {'wmclass': 'Steam', 'wname': 'Settings'}, # Steam settings
    Match(wm_class='pinentry-gtk-2'), # pinentry prompt
    Match(wm_class='Browser', title=re.compile('^About [^-]*$')), # Browser about dialog
    Match(wm_class='redshift-gtk'), # Redshift info
    Match(wm_class='Conky'),
    Match(wm_class='origin.exe'),
    Match(wm_class='LethalLeague'),
], border_focus=border_focus, border_normal=border_normal)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.client_new
def client_new(window):
  # TODO: Delete and re-create groups
  class_name = window.window.get_wm_class()
  if 'discord' in class_name:
    window.togroup(group_name="1")
    return
  if 'spotify' in class_name:
    window.togroup(group_name="2")
    return
  if 'csgo_linux64' in class_name:
    subprocess.Popen(['pkill', '-USR1', '-x', 'redshift'])

@hook.subscribe.client_killed
def client_killed(window):
  class_name = window.window.get_wm_class()
  if 'csgo_linux64' in class_name:
    subprocess.Popen(['pkill', '-USR1', '-x', 'redshift'])
  

@hook.subscribe.client_name_updated
def auto_unfloat(window):
  # Auto-unfloat steam window
  if 'Steam' in window.window.get_wm_class():
    name = window.name
    if name == 'Steam':
      window.floating = False

# Auto start processes
@hook.subscribe.startup_once
def autostart():
  processes = [
    [ 'sh', '.xinitrc' ],
    [ 'nitrogen', '--restore' ],
    [ 'picom', '--experimental-backend', '-b' ],
    [ 'nm-applet' ],
    [ 'redshift-gtk' ],
    [ 'light-locker' ],
    [ 'ydotoold' ],
  ]

  for p in processes:
    subprocess.Popen(p)
