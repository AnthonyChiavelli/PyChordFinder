#!/usr/bin/python2.7

import wx
import chordfinder

class main_frame(wx.Frame):
    """ Subclass wx.Frame to provide a window for app """
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, title="Chord Finder",
                          style = wx.MINIMIZE_BOX, size = (200,200))
        self.init_gui()
        self.Center()
        self.Show(True)

    def init_gui(self):
        #Set up the main panel
        main_panel = wx.Panel(self)
        main_panel.SetBackgroundColour('#4f5049')

        #Title text
        title_text = wx.StaticText(main_panel,label= 'Chord Finder')
        title_text.SetForegroundColour((255,255,255))

        #Chord input TextCtrl
        self.chord_input = wx.TextCtrl(main_panel,id=100)
        self.chord_input.SetBackgroundColour((140,140,140))
        self.chord_input.SetFocus()

        #Chord output ListBox
        self.chord_output = wx.ListBox(main_panel, -1, size = (130,80))
        self.chord_output.SetBackgroundColour((140,140,140))


        #Vertical Sizer
        vert_sizer = wx.BoxSizer(wx.VERTICAL)


        #Add widgets to the vertical sizer
        vert_sizer.Add(title_text, 0, wx.CENTER | wx.TOP, 20)
        vert_sizer.Add(self.chord_output, 1, wx.CENTER | wx.ALL, 20)
        vert_sizer.Add(self.chord_input, 0, wx.CENTER | wx.ALL, 20)


        #Event bindings
        self.Bind(wx.EVT_TEXT, self.update_chords)
        self.Bind(wx.EVT_KEY_UP, self.on_key)


        #Set the sizer for the panel
        main_panel.SetSizer(vert_sizer)

    def on_key(self, event):
        """ Called when a key is released """
        #If the input box has focus and the user presses enter
        if (event.GetKeyCode() == wx.WXK_RETURN and
                self.FindFocus() == self.chord_input):
            self.chord_input.Clear()
        if event.GetKeyCode() == wx.WXK_ESCAPE: #Exit when escape is pressed
            self.Close()

    def update_chords(self, event):
        """ Uses chordfinder.find_chords to populate the listbox with chord names """
        self.chord_output.Clear()
        chords = chordfinder.find_chords(self.chord_input.GetValue())
        self.chord_output.Set(chords)

app = wx.App(False)
main_frame_instance = main_frame(None)
app.MainLoop()
