from tkinter import *
from tkinter import filedialog, simpledialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

bg_img = ""
logo = ""
mark_text = ""

def open_img():
    global bg_img
    bg_img = filedialog.askopenfilename(title="Select A File")
    try:
        print(f"{bg_img.split('/')[-1]} selected")
        if bg_img != "":
            img = Image.open(bg_img)
            rImg = resize(img)
            rImg = ImageTk.PhotoImage(rImg)
            canvas.itemconfig(i_img, image=rImg)
            print(canvas)
            print(canvas.image)
            canvas.image = rImg  # keep reference to the image
            print(canvas.image)
    except AttributeError:
        print("Image didn't open.")

##testing image change
def back():
    global bg_img, logo, mark_text
    bg_img = ""
    logo = ""
    mark_text = ""
    canvas.itemconfig(i_img, image=r_initial)

def input_text():
    global mark_text
    mark_text = simpledialog.askstring(title="Text", prompt="Enter your text here:")
    print(f"text:\n{mark_text}")

def open_logo():
    global logo
    logo = filedialog.askopenfilename()
    try:
        print(f"{logo.split('/')[-1]} selected")
    except AttributeError:
        print("Logo didn't open.")

def resize(image):
    o_size = image.size
    f_size = (400, 400)
    factor = min(float(f_size[1])/o_size[1], float(f_size[0])/o_size[0])
    width = int(o_size[0] * factor)
    height = int(o_size[1] * factor)
    image = image.resize((width, height), Image.ANTIALIAS)
    return image

def merge():
    global bg_img, logo, mark_text
    with Image.open(bg_img) as im:
        image_copy = im.copy().convert("RGBA")
        if logo != "":
            mark = Image.open(logo)
            mark_copy = mark.copy().resize((round(image_copy.size[0]*0.4), round(image_copy.size[1]*0.4)))
            position = (image_copy.size[0] - mark_copy.size[0], image_copy.size[1] - mark_copy.size[1])
            image_copy.paste(mark_copy, position, mark_copy.convert("RGBA"))
            print("logo marked.")
        if mark_text != "":
            draw = ImageDraw.Draw(image_copy)
            font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", 100)
            position = (round(image_copy.size[0] / 2), round(image_copy.size[1] / 2))
            draw.text(position, mark_text, (255, 255, 255), font=font)
            print("text printed.")
        # save processed image
        finish_img = image_copy.convert("RGB")
        finish_img_name = f"{bg_img.split('/')[-1].split('.')[0]}" + "wm.jpg"
        finish_img.save(fr'C:\Users\laure\Desktop\New folder (3)\{finish_img_name}')
        finish_img.show()

window = Tk()
window.title("Melody Watermark")
window.config(padx=100, pady=100)

canvas = Canvas(width=500, height=300, highlightthickness=0)

initial_image = Image.open("initial.jpg")
resize_img = resize(initial_image)
r_initial = ImageTk.PhotoImage(resize_img)
i_img = canvas.create_image(250, 150, image=r_initial)
canvas.image = r_initial
canvas.grid(column=2, row=0, columnspan=4)

img_btn = Button(text="Select Image", command=open_img)
img_btn.grid(column=3, row=1, padx=50, pady=50, columnspan=2)

text_btn = Button(text="Add Text", command=input_text)
text_btn.grid(column=3, row=3, sticky="E", padx=10)

logo_btn = Button(text="Add Logo", command=open_logo)
logo_btn.grid(column=4, row=3, sticky="W", padx=10)

back_btn = Button(text="Change", command=back)
back_btn.grid(column=0, row=3)

watermark_btn = Button(text="Watermark Image", command=merge)
watermark_btn.grid(column=5, row=3, columnspan=2)

window.mainloop()