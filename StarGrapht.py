# Kendall Park FIRST PYTHON GUI FROM SCRATCH BABY.
# This code is gross. The bastard child of Python and Java.
# It is also disgustingly self-referential.

# NEXT TIME: 
# NEXT GOAL: 

# BIG GOALS: 
# X. Get all three plotting algorithms implemented, with GUI features
# 2. Need to be able to save graph images as PNGs
# 3. Get axes and labels, key, and other graph data displaying and editable
# 4. Display info on what coordinates on the mouse is pointed at bottom
# 5. Fancy color, appearance, tweaking stuff

# LIST OF STUFFS
# 1. When the program loads, it is not automatically the right size
# 3. Need to be able to manipulate multiple graphs (remember naming issues)
# 4. Better way to encapsulate graph drawing capabilities (HRD, LUM, etc)

import wx # GUI program
import os # Necessary for I/O with files

# The recommended way to use wx with mpl is with the WXAgg backend. 
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
  FigureCanvasWxAgg as FigCanvas, \
  NavigationToolbar2WxAgg as NavigationToolbar

import plotdata as pl
import numpy as n
  
class MainWindow(wx.Frame):
  # This class forms the main frame of the application, extends wx.Frame
  
  title = 'StarGrapht'
  
  def __init__(self):
    wx.Frame.__init__(self, None, -1, self.title)
    
    # important variables 
    # TODO: encapsulate these
    self.spaceDown = False # Boolean for holding the space bar down
    self.buttonDown = False
    self.altDown = False
    self.shiftDown = False
    oldX = 0
    oldY = 0
        
    self.dirname = ""
    self.filename = ""
    self.plots = []
    
    # call some methods to set up contents
    self.menubar = self.create_menu_bar()
    self.graphpanel = self.create_graph_panel() # redundant... some other way to convey
                                              # the creation of self.graphpanel?
    self.statusbar = self.create_status_bar()
    
    # creates top options bar
    self.topleftpanel = wx.Panel(self.graphpanel)
    graphalgs = ["HRD", "LUM", "RCPLOT"]
    self.combobox = wx.ComboBox(self.topleftpanel, -1, choices=graphalgs, style=wx.CB_READONLY)
    self.combobox.Bind(wx.EVT_COMBOBOX, self.enter_combo)
    self.combobox.SetValue("HRD")
    
    self.tabpane = wx.Notebook(self.graphpanel, 1, style=wx.NB_TOP)
    
    refreshbutton = wx.Button(self.topleftpanel, -1, "Refresh")
    xtitlebutton = wx.Button(self.topleftpanel, -1, "x-title")
    ytitlebutton = wx.Button(self.topleftpanel, -1, "y-title")
    
    refreshbutton.Bind(wx.EVT_BUTTON, self.refresh_graph)
    
    # Layout with BoxSizers
    self.hboxtopleft = wx.BoxSizer(wx.HORIZONTAL)
    self.hboxtopleft.Add(refreshbutton, 1, wx.GROW)
    self.hboxtopleft.Add(xtitlebutton, 1, wx.GROW)
    self.hboxtopleft.Add(ytitlebutton, 1, wx.GROW)
    
    self.vboxtopleft = wx.BoxSizer(wx.VERTICAL)
    self.vboxtopleft.Add(self.combobox, 1, wx.GROW)
    self.vboxtopleft.Add(self.hboxtopleft, 1, wx.GROW)
    self.topleftpanel.SetSizer(self.vboxtopleft)
    
    self.hboxtop = wx.BoxSizer(wx.HORIZONTAL)
    self.hboxtop.Add(self.topleftpanel, 0, wx.GROW)
    self.hboxtop.Add(self.tabpane, 1, wx.GROW)
    
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.hboxtop, 0, wx.LEFT | wx.TOP)
    self.vbox.Add(self.canvas, 1, wx.LEFT | wx.BOTTOM | wx.GROW)# note: figure this out 
    self.graphpanel.SetSizer(self.vbox)
    self.vbox.Fit(self)
    
    #Load a graph!
    self.open_sequence()
    
    self.Show()
    
  def refresh_graph(self, event): # should find a way to do this w/o resetting axes
    for plot in self.plots:
      plot.plotdata.reload_data()
    self.refresh_plot()
    
  def enter_combo(self, event):
    self.plot_algorithm(event.GetString())
  
  def refresh_plot(self):
    self.plot_algorithm(self.combobox.GetValue())
      
  def plot_algorithm(self, string):
    if string == "HRD":
      self.draw_HRD()
    elif string == "LUM":
      self.draw_LUM()
    elif string == "RCPLOT":
      self.draw_RCPLOT()
    
  def create_status_bar(self):
    return self.CreateStatusBar()
    
  def create_menu_bar(self):
    filemenu = wx.Menu()
    menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a plot")
    menuSave = filemenu.Append(wx.ID_SAVE, "&Save", "Save a graph as a png")
    menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
    menubar = wx.MenuBar()
    menubar.Append(filemenu, "&File") # Add filemenu to menubar
    self.SetMenuBar(menubar) #Adding the MenuBar to the Frame content.
    
    # Bind events
    self.Bind(wx.EVT_MENU, self.on_open, menuOpen)
    self.Bind(wx.EVT_MENU, self.on_save, menuSave)
    self.Bind(wx.EVT_MENU, self.on_exit, menuExit)
    return menubar
    
  def on_exit(self, e):
    self.Close(True) # close the frame
    
  def on_open(self, e):
    self.open_sequence()
    
  def open_sequence(self):
    dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.plot1", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      self.filename = dlg.GetFilename()
      self.dirname = dlg.GetDirectory()
      nametaken = False
      for plot in self.plots: # we check to make sure we aren't loading duplicate data
        if plot.filename == self.filename and plot.dirname == self.dirname:
          nametaken = True
      if (not nametaken):
        self.plots += [pl.Plot(self.dirname, self.filename)]
        self.refresh_plot()
        self.create_plot_tabs()
    dlg.Destroy()
    
  def on_save(self, e):
    dlg = wx.FileDialog(self, "Save your file", self.dirname, "", ".png", wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      dirname = dlg.GetDirectory()
      path = dlg.GetPath()
      self.fig.savefig(filename+".png", format='png')
    dlg.Destroy()
    
  def create_plot_tabs(self):
    self.tabpane.DeleteAllPages()
  
    for i in range(len(self.plots)):
      panel = wx.Panel(self.tabpane)
      button = wx.Button(panel, i, "Close", (-1,-1))
      text = wx.StaticText(panel, -1, "Custom options for "+self.plots[i].nickname+" ...will be implemented later...") # dummy text
      hbox = wx.BoxSizer(wx.HORIZONTAL)
      hbox.Add(button, 0, wx.GROW)
      hbox.Add(text, 1, wx.GROW)
      panel.SetSizer(hbox)
      button.Bind(wx.EVT_BUTTON, self.close_plot, id=i)
      self.tabpane.AddPage(panel, self.plots[i].nickname)
      
  def close_plot(self, event):
    self.plots.pop(event.GetId())
    self.create_plot_tabs()
    self.refresh_plot()
    
  def draw_HRD(self):
    self.subplot.clear()
    for plot in self.plots:
      self.subplot.plot(n.log10(n.array(plot.plotdata.Teff)), plot.plotdata.L)
      x1, x2 = self.subplot.get_xlim()
      if x1 < x2: # We like reverse axes on HRD
        self.subplot.set_xlim(self.subplot.get_xlim()[::-1])
      self.subplot.set_xlabel('logT')
      self.subplot.set_ylabel('logL')
    self.canvas.draw()
    self.graphpanel.SetFocus()
    
  def draw_LUM(self):
    # TODO: create this function, add button for it
    self.subplot.clear()
    for plot in self.plots:
      self.subplot.plot(plot.plotdata.time, plot.plotdata.L, 'k-', plot.plotdata.time, plot.plotdata.LH, 'r--', plot.plotdata.time, plot.plotdata.LHe, 'y-', plot.plotdata.time, plot.plotdata.LC, 'c--', plot.plotdata.time, plot.plotdata.Lnu, 'b-')
      self.subplot.legend( ('total lum', 'H lum', 'He lum', 'C lum', 'Nu lum') )
      self.subplot.set_xlabel('Time (10^7 years)')
      self.subplot.set_ylabel('logL')
      
      x1, x2 = self.subplot.get_xlim() # check for reverse axes... kinda a hack
      if x1 > x2: # We like reverse axes on HRD
        self.subplot.set_xlim(self.subplot.get_xlim()[::-1])
    self.canvas.draw()
    self.graphpanel.SetFocus()
    
  def draw_RCPLOT(self):
    # TODO: create this function, add button for it
    self.subplot.clear()
    for plot in self.plots:
      self.subplot.plot(plot.plotdata.rhoc, plot.plotdata.Tmax, 'b-', plot.plotdata.rhoc, plot.plotdata.Tc, 'r--')
      
      x1, x2 = self.subplot.get_xlim() # check for reverse axes... kinda a hack
      if x1 > x2: # We like reverse axes on HRD
        self.subplot.set_xlim(self.subplot.get_xlim()[::-1])
        
    self.subplot.set_xlabel('K')
    self.subplot.set_ylabel('K')
    self.subplot.legend( ('max T', 'central T') )
    self.canvas.draw()
    self.graphpanel.SetFocus()
  
    
  def create_graph_panel(self):
    # TODO: graphpanel is technically a global, encapsulate this later
    self.graphpanel = wx.Panel(self)
    # TODO: fig is technically a global, encapsulate this later
    self.fig = Figure((8.0, 6.0), dpi=100)
    # TODO: same with canvas and subplot, there's a better way to do this
    self.canvas = FigCanvas(self.graphpanel, -1, self.fig)
    self.subplot = self.fig.add_subplot(111) # note: figure out what numbers mean
    
    # Set Events
    cid = self.canvas.mpl_connect('scroll_event', self.on_scroll) #cid is for id
    cid2 = self.canvas.mpl_connect('button_press_event', self.on_button_press)
    cid3 = self.canvas.mpl_connect('key_press_event', self.on_key_press)
    cid4 = self.canvas.mpl_connect('key_release_event', self.on_key_release)
    cid5 = self.canvas.mpl_connect('button_release_event', self.on_button_release)
    cid6 = self.canvas.mpl_connect('motion_notify_event', self.on_motion)
    
    return self.graphpanel


  def on_scroll(self, event):
    #print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
    x, y = event.xdata, event.ydata
    x1, x2 = self.subplot.get_xlim()
    y1, y2 = self.subplot.get_ylim()
    if x is not None and y is not None: # make sure we're in graph bounds
      xscl = 0.1 # scaling factors
      yscl = 0.1
      if self.altDown:
        yscl = 0 # set this to 0 because alt doesn't change the yscale, only the xscale
      if self.shiftDown:
        xscl = 0 # set this to 0 because shift doesn't change the xscale
      xlen = (x2-x1) # abs size of x axis
      ylen = (y2-y1) # abs size of y axis
      xc = x1 + (x2-x1)/2
      yc = y1 + (y2-y1)/2
      
      if event.step < 0: # Zoom out
        # the x-shift allows the zoom to center around the mouse, same for ysh
        xsh = -((((xlen/2)-xlen*xscl)*(xc-x))/(xlen/2) - (xc-x))
        ysh = -((((ylen/2)-ylen*yscl)*(yc-y))/(ylen/2) - (yc-y))
        # First we zoom out according to scaling factor, then we shift
        self.subplot.set_xlim(x1-xlen*xscl + xsh, x2+xlen*xscl + xsh)
        self.subplot.set_ylim(y1-ylen*yscl + ysh, y2+ylen*yscl + ysh)
      elif event.step > 0: # Zoom in
        xsh = -((((xlen/2)+xlen*xscl)*(xc-x))/(xlen/2) - (xc-x))
        ysh = -((((ylen/2)+ylen*yscl)*(yc-y))/(ylen/2) - (yc-y))
        self.subplot.set_xlim(x1+xlen*xscl + xsh, x2-xlen*xscl + xsh)
        self.subplot.set_ylim(y1+ylen*yscl + ysh, y2-ylen*yscl + ysh)
      self.canvas.draw()
    
  def on_button_press(self, event):
    self.oldX = event.xdata
    self.oldY = event.ydata
    self.buttonDown = True
    #print 'button down'

    
  def on_button_release(self, event):
    self.buttonDown = False
  
  def on_key_press(self, event):
    if event.key == ' ':
      self.spaceDown = True
    elif event.key == 'alt':
      self.altDown = True
    elif event.key == 'shift':
      self.shiftDown = True
    
  def on_key_release(self, event):
    if event.key == ' ':
      self.spaceDown = False
    elif event.key == 'alt':
      self.altDown = False
    elif event.key == 'shift':
      self.shiftDown = False
    
  def on_motion(self, event):
    x, y = event.xdata, event.ydata
    self.statusbar.SetStatusText("("+str(x)+", "+str(y)+")")
    # self.spaceDown and
    if self.buttonDown and x is not None and y is not None:
      xch = self.oldX - x
      ych = self.oldY - y
      x1, x2 = self.subplot.get_xlim()
      y1, y2 = self.subplot.get_ylim()
      self.subplot.set_xlim(x1+xch, x2+xch)
      self.subplot.set_ylim(y1+ych, y2+ych)
      self.canvas.draw()
  
app = wx.App(False)
frame = MainWindow()
app.MainLoop()
    
    
