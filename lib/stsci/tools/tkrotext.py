""" Read-Only tkinter Text Widget.  This is a variation of the tkinter Text
widget in that the text itself is not editable (it is read-only), but it allows
selection for cut/paste to other apps.  Cut-paste may currently only work
under X11. (9/2015 enabled under OSX by adding 'c' to ALLOWED_SYMS)

A vastly simpler way of doing this is to use a tkinter.Text widget and set
it to DISABLED, but then you cannot select text.
$Id$
"""
from __future__ import division # confidence high

# System level modules
import sys
PY3K = sys.version_info[0] > 2

if PY3K:
    import tkinter as TKNTR
else:
    import Tkinter as TKNTR

ALLOWED_SYMS = ('c','Up','Down','Left','Right','Home','End','Prior','Next', \
                'Shift_L', 'Shift_R')

class ROText(TKNTR.Text):

    def __init__(self, master, **kw):
        """  defer most of __init__ to the base class """
        self._fbto = None
        if 'focusBackTo' in kw:
            self._fbto = kw['focusBackTo']
            del kw['focusBackTo']
        TKNTR.Text.__init__(self, master, **kw)
        # override some bindings to return a "break" string
        self.bind("<Key>", self.ignoreMostKeys)
        self.bind("<Button-2>", lambda e: "break")
        self.bind("<Button-3>", lambda e: "break")
        if self._fbto:
            self.bind("<Leave>", self.mouseLeft)
        self.config(insertwidth=0)

    # disallow common insert calls, but allow a backdoor when needed
    def insert(self, index, text, *tags, **kw):
        if 'force' in kw and kw['force']:
            TKNTR.Text.insert(self, index, text, *tags)

    # disallow common delete calls, but allow a backdoor when needed
    def delete(self, start, end=None, force=False):
        if force:
            TKNTR.Text.delete(self, start, end)

    # a way to disable text manip
    def ignoreMostKeys(self, event):
        if event.keysym not in ALLOWED_SYMS:
            return "break" # have to return this string to stop the event
        # To get copy/paste working on OSX we allow 'c' so that
        # they can type 'Command-c', but don't let a regular 'c' through.
        if event.keysym in ('c','C'):
            if sys.platform=='darwin' and hasattr(event,'state') and event.state != 0:
                pass # allow this through, it is Command-c
            else:
                return "break"


    def mouseLeft(self, event):
        if self._fbto:
            self._fbto.focus_set()
        return "break" # have to return this string to stop the event


# Test the above class
if __name__ == '__main__':

    import sys, time

    rot = None

    def quit():
        sys.exit()

    def clicked():
        rot.insert(TKNTR.END, "\nClicked at "+time.asctime(), force=True)
        rot.see(TKNTR.END)

    # make our test window
    top = TKNTR.Tk()
    f = TKNTR.Frame(top)

    sc = TKNTR.Scrollbar(f)
    sc.pack(side=TKNTR.RIGHT, fill=TKNTR.Y)
    rot = ROText(f, wrap=TKNTR.WORD, height=10, yscrollcommand=sc.set,
                 focusBackTo=top)
    rot.pack(side=TKNTR.TOP, fill=TKNTR.X, expand=True)
    sc.config(command=rot.yview)
    f.pack(side=TKNTR.TOP, fill=TKNTR.X)

    b = TKNTR.Button(top, text='Click Me', command=clicked)
    b.pack(side=TKNTR.TOP, fill=TKNTR.X, expand=1)

    q = TKNTR.Button(top, text='Quit', command=quit)
    q.pack(side=TKNTR.TOP)

    # start
    top.mainloop()
