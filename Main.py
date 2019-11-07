import tkinter as tk
import GUI, GUIsupport

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    GUIsupport.set_Tk_var()
    top = GUI.GUI(root)
    GUIsupport.init(root, top)
    root.mainloop()
w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    GUIsupport.set_Tk_var()
    top = GUI.GUI(w)
    GUIsupport.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


def __main__():
    vp_start_gui()

if __name__ == __main__():
    __main__()