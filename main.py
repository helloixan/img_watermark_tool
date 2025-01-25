from tkinter import *
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
from tkinter import messagebox, END
from PIL import ImageTk
from img_processing import *
import os

PRIMARY_COLOR = "#2d8eff"
NEGATIVE_COLOR = "#ff4949"
POSITIVE_COLOR = "#13ce66"

WTM_PREVIEW_SIZE = (400, 400)
IMG_PREVIEW_SIZE = (800, 800)
PARAGPRAH_FONT = ("Arial", 12)
RESIZE_FACTOR = 1/6
window = Tk()
# ------------------ UX SETUP ----------------------- #
# setup wtm
wtm_path = ""
wtm_pil_img = Image.Image()
wtm_pil_prev = Image.Image()
wtm_tk_img = PhotoImage()
wtm_canvas_id = 0
wtm_options = {
    'resize_factor': RESIZE_FACTOR,
    'opacity': 1.0,
    'position': 'center'
}
# setup img
list_img_paths = []
img_path = ""
selected_img_pil = Image.Image()
selected_img_pil_prev = Image.Image()
selected_img_tk = PhotoImage()
img_canvas_id = 0
modif_img_pil = Image.Image()

def select_watermark():
    global wtm_path
    global wtm_pil_img
    global wtm_pil_prev
    global wtm_tk_img
    global img_canvas_id

    wtm_path = askopenfilename()
    wtm_pil_img = Image.open(wtm_path)
    wtm_pil_prev = wtm_pil_img.copy()
    
    wtm_pil_prev.thumbnail(WTM_PREVIEW_SIZE)
    width, height = wtm_pil_prev.size
    wtm_tk_img = ImageTk.PhotoImage(wtm_pil_prev)
    canvas.delete("all")
    canvas.config(width=width, height=height)
    img_canvas_id = canvas.create_image(int(width/2), int(height/2), image=wtm_tk_img)

def select_images():
    global list_img_paths
    if not wtm_path :
        messagebox.showinfo(message="Please select a watermark first!", title="Select Images")
    else :
        new_img_paths = askopenfilenames()
        for path in new_img_paths :
            if path not in list_img_paths:
                list_img_paths.append(path)
                img_name = os.path.basename(path)
                listbox_files.insert(END, img_name)

def preview_img(event):
    global img_path
    global selec_img_pil
    img_name = listbox_files.get(listbox_files.curselection())
    for path in list_img_paths:
        if img_name in path:
            img_path = path
    selec_img_pil = Image.open(img_path)
    update_img()

def update_img():
    global img_path
    global selec_img_pil_prev
    global selec_img_tk
    global img_canvas_id
    global modif_img_pil

    modif_img_pil = add_wtm(wtm_pil_img, selec_img_pil, wtm_options)

    selec_img_pil_prev = modif_img_pil.copy()
    selec_img_pil_prev.thumbnail(IMG_PREVIEW_SIZE)
    selec_img_tk = ImageTk.PhotoImage(selec_img_pil_prev)
    width, height = selec_img_pil_prev.size
    canvas.delete("all")
    canvas.config(width=width, height=height)
    img_canvas_id = canvas.create_image(int(width / 2), int(height / 2), image=selec_img_tk)


def change_position():
    wtm_options['position'] = position_state.get()
    if wtm_path and img_path:
        update_img()


def change_size(expand_coef):
    wtm_options['resize_factor'] = RESIZE_FACTOR * float(expand_coef)
    if wtm_path and img_path:
        update_img()


def change_opacity(opac_value):
    wtm_options['opacity'] = float(opac_value)
    if wtm_path and img_path:
        update_img()

def save_all():
    if wtm_path and list_img_paths:
        save_dir = askdirectory(title="Select the Save Folder")
        for path in list_img_paths:
            img_pil = Image.open(path)
            new_img_pil = add_wtm(wtm_pil_img, img_pil, wtm_options)
            save_path = save_dir + '/' + os.path.basename(path)
            new_img_pil.save(save_path)
        messagebox.showinfo(message="All Images have been saved!",
                            title="Saving Successful")
    else:
        messagebox.showinfo(message="You haven't uploaded a watermark and/or an image.",
                            title="Can't Save")

def clear():
    global wtm_path, wtm_canvas_id, wtm_options, list_img_paths, img_path, img_canvas_id
    canvas.config(width=0, height=0)

    wtm_path = ""
    wtm_canvas_id = 0
    wtm_options = {
        'resize_factor': RESIZE_FACTOR,
        'opacity': 1.0,
        'position': 'bottom right'
    }

    listbox_files.delete(0, END)
    list_img_paths = []
    img_path = ""
    img_canvas_id = 0
    
    position_state.set(value="center")
    opacity_bar.set(1)
    size_bar.set(1)

# ---------------------- UI SETUP ------------------------ #
window.title("Image Watermark Tool")
window.config(padx=15, pady=15)

# setup font
h1_font = ('Arial', 24, 'bold')
lg_font = ('Arial', 12)
std_font = ('Arial', 10, 'bold')
bold_font = ('Arial', 12, 'bold')

# creating widgets
title_label = Label(window, text="Image Watermark Tool", font=h1_font)
select_wtm_button = Button(window, text="Select Watermark", font=std_font, width=20, command=select_watermark, bg=PRIMARY_COLOR, fg="WHITE")
select_img_button = Button(window, text="Select Images", font=std_font, width=20, command=select_images, bg=PRIMARY_COLOR, fg="WHITE")

scrollbar_files = Scrollbar(window)
listbox_files = Listbox(window, height=6, yscrollcommand=scrollbar_files.set, font=std_font)
listbox_files.bind("<<ListboxSelect>>", preview_img)
scrollbar_files.config(command=listbox_files.yview)

size_label = Label(text="Size", font=bold_font, justify=LEFT)
size_bar = Scale(from_=1, to=5, orient=HORIZONTAL, command=change_size, resolution=0.5)
opacity_label = Label(text="Opacity", font=bold_font)
opacity_bar = Scale(from_=0, to=1, orient=HORIZONTAL, command=change_opacity, resolution=0.1)
opacity_bar.set(1)

position_label = Label(text="Position", font=bold_font)
position_state = StringVar(value="center")
center_btn = Radiobutton(text="Center", value="center", variable=position_state, font=std_font,
                         command=change_position)
top_l_btn = Radiobutton(text="Top Left", value="top left", variable=position_state, font=std_font,
                        command=change_position)
top_r_btn = Radiobutton(text="Top Right", value="top right", variable=position_state, font=std_font,
                        command=change_position)
bottom_l_btn = Radiobutton(text="Bottom Left", value="bottom Left", variable=position_state, font=std_font,
                           command=change_position)
bottom_r_btn = Radiobutton(text="Bottom Right", value="bottom right", variable=position_state, font=std_font,
                           command=change_position)

save_btn = Button(text="Save All", font=std_font, width=20, command=save_all, bg=POSITIVE_COLOR)
clear_btn = Button(text="Clear workspace", font=std_font, width=20, command=clear, bg=NEGATIVE_COLOR)
copyright_label = Label(text="© Iksan Risandy", font=std_font)
canvas = Canvas(width=0, height=0)


# Placing widgets
title_label.grid(row=0, column=1, columnspan=3, sticky=W)
select_wtm_button.grid(row=2, column=0, columnspan=2)
select_img_button.grid(row=2, column=2)
scrollbar_files.grid(row=3, column=0, sticky=N+S, pady=10)
listbox_files.grid(row=3, column=1, columnspan=3, sticky=E+W, pady=10)
size_label.grid(row=4, column=1)
size_bar.grid(row=4, column=2, columnspan=2, sticky=E+W)
opacity_label.grid(row=5, column=1)
opacity_bar.grid(row=5, column=2, columnspan=2, sticky=E+W)
position_label.grid(row=7, column=1)
center_btn.grid(row=7, column=2, sticky=W)
top_l_btn.grid(row=8, column=2, sticky=W)
top_r_btn.grid(row=9, column=2, sticky=W)
bottom_l_btn.grid(row=7, column=3, sticky=W)
bottom_r_btn.grid(row=8, column=3, sticky=W)
save_btn.grid(row=10, column=2, pady=20, padx=20)
clear_btn.grid(row=10, column=1, pady=20, padx=20)
copyright_label.grid(row=11, column=1, sticky=S+W)
canvas.grid(row=0, column=4, rowspan=12)

window.mainloop()