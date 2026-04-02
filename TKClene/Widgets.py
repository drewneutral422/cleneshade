import tkinter as tk
from tkinter import ttk # Uses 'themed' widgets for a more modern look
import sys

root = None

def init():
    global root
    root = tk.Tk()
    root.title("TKclene Window")
    root.geometry("800x600")

def add(widget_type, text=None):
    """
    Universal Factory for Tkinter.
    Usage: add("Label", "Hello") or add("Entry")
    """
    global root
    if not root:
        print("TKclene Error: Run init() first.")
        return

    try:
        # First, try to find the widget in ttk (modern) then fallback to standard tk
        if hasattr(ttk, widget_type):
            widget_class = getattr(ttk, widget_type)
        else:
            widget_class = getattr(tk, widget_type)
        
        # Create instance: Tkinter requires the parent (root) as the first arg
        if text:
            # Tkinter uses 'text' as the keyword for most display widgets
            new_widget = widget_class(root, text=str(text))
        else:
            new_widget = widget_class(root)
            
        # Add to layout (padding of 5px for consistency with your other modules)
        new_widget.pack(pady=5, padx=5, fill='x')
        
        return new_widget
        
    except AttributeError:
        print(f"TKclene Error: '{widget_type}' is not a valid Tkinter widget.")
    except Exception as e:
        print(f"Runtime Error: {e}")

def show():
    if root:
        root.mainloop()