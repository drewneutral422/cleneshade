import wx
import sys

app = None
frame = None
panel = None
sizer = None

def init():
    global app, frame, panel, sizer
    # Initialize the app
    if not wx.GetApp():
        app = wx.App(False)
    
    frame = wx.Frame(None, wx.ID_ANY, "WxClene Pro", size=(800, 600))
    
    # Create the panel and sizer
    panel = wx.Panel(frame)
    sizer = wx.BoxSizer(wx.VERTICAL)
    
    # FIX: Capital 'S' in SetSizer
    panel.SetSizer(sizer)
    panel.SetAutoLayout(True)

def add(widget_type, label=None):
    global panel, sizer
    if not frame:
        print("WxClene Error: Run init() first.")
        return

    try:
        # Resolve the widget class from the wx namespace
        widget_class = getattr(wx, widget_type)
        
        # Create instance: wxWidgets requires (parent, id, label) for most items
        if label:
            # ID_ANY tells wx to generate a unique ID automatically
            new_widget = widget_class(panel, wx.ID_ANY, str(label))
        else:
            new_widget = widget_class(panel, wx.ID_ANY)
            
        # Add to sizer with padding (5px) and expansion
        sizer.Add(new_widget, 0, wx.ALL | wx.EXPAND, 5)
        
        # Refresh the layout so it appears immediately
        panel.Layout()
        return new_widget
        
    except AttributeError:
        # Use your API's error style if you prefer, or a clean print
        print(f"WxClene Error: 'wx.{widget_type}' does not exist.")
    except Exception as e:
        print(f"Runtime Error: {e}")

def show():
    if frame:
        frame.Centre() # Centers the window on screen
        frame.Show()
        app.MainLoop()