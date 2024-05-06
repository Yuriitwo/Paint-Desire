import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Desire")

        self.pen_color = "black"
        self.pen_size = 3
        self.pen_type = "line"

        self.last_x, self.last_y = None, None

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.create_menu()

    def draw(self, event):
        if self.last_x and self.last_y:
            if self.pen_type == "line":
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.pen_color, width=self.pen_size, capstyle=tk.ROUND, smooth=tk.TRUE)
            elif self.pen_type == "oval":
                x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
                x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, width=0)
            elif self.pen_type == "rectangle":
                x1, y1 = self.last_x, self.last_y
                x2, y2 = event.x, event.y
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.pen_color, width=self.pen_size)
            elif self.pen_type == "star":
                points = self.calculate_star_points(event.x, event.y, 5, 30, 15)
                self.canvas.create_polygon(points, fill=self.pen_color, outline="", width=0)
            elif self.pen_type == "heart":
                self.draw_heart(event.x, event.y, 30)
            elif self.pen_type == "spiral":
                self.draw_spiral(event.x, event.y, 10, 50)
            elif self.pen_type == "yuri":
                self.draw_text("Yuri", event.x, event.y, fill=self.pen_color)
            elif self.pen_type == "eraser":  # Se o tipo de pincel for "eraser", use a cor de fundo para apagar
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="white", width=self.pen_size, capstyle=tk.ROUND, smooth=tk.TRUE)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x = None
        self.last_y = None

    def change_color(self):
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            self.pen_color = color

    def change_size(self, size):
        self.pen_size = size

    def change_pen_type(self, pen_type):
        self.pen_type = pen_type

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if file_path:
            x0 = self.root.winfo_rootx() + self.canvas.winfo_x()
            y0 = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x0 + self.canvas.winfo_width()
            y1 = y0 + self.canvas.winfo_height()
            ImageGrab.grab().crop((x0, y0, x1, y1)).save(file_path)

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        color_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Color", menu=color_menu)
        color_menu.add_command(label="Choose Color", command=self.change_color)

        size_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Size", menu=size_menu)
        size_menu.add_command(label="Small", command=lambda: self.change_size(3))
        size_menu.add_command(label="Medium", command=lambda: self.change_size(5))
        size_menu.add_command(label="Large", command=lambda: self.change_size(8))

        pen_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Pen Type", menu=pen_menu)
        pen_menu.add_command(label="Line", command=lambda: self.change_pen_type("line"))
        pen_menu.add_command(label="Oval", command=lambda: self.change_pen_type("oval"))
        pen_menu.add_command(label="Rectangle", command=lambda: self.change_pen_type("rectangle"))
        pen_menu.add_command(label="Star", command=lambda: self.change_pen_type("star"))
        pen_menu.add_command(label="Heart", command=lambda: self.change_pen_type("heart"))
        pen_menu.add_command(label="Spiral", command=lambda: self.change_pen_type("spiral"))
        pen_menu.add_command(label="Yuri", command=lambda: self.change_pen_type("yuri"))
        pen_menu.add_command(label="Eraser", command=lambda: self.change_pen_type("eraser"))  # Adicionando opção de borracha

        menu.add_command(label="Save Drawing", command=self.save_drawing)
        menu.add_command(label="Clear Canvas", command=self.clear_canvas)
        
        # Adicionar a opção "About" no menu
        menu.add_command(label="About", command=self.open_about_dialog)

    def open_about_dialog(self):
        about_text = "Paint Desire\n\nA simple paint application\n\nVersion 1.0\n\nBy Yuriitwo"
        tk.messagebox.showinfo("About", about_text)

    def calculate_star_points(self, x_center, y_center, arms, outer_radius, inner_radius):
        import math
        angle = math.pi / arms
        points = []
        for i in range(2 * arms):
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = x_center + math.cos(i * angle) * radius
            y = y_center + math.sin(i * angle) * radius
            points.append(x)
            points.append(y)
        return points

    def draw_heart(self, x_center, y_center, size):
        x0 = x_center - size
        y0 = y_center - size
        x1 = x_center + size
        y1 = y_center + size
        self.canvas.create_arc(x0, y0, x_center, y_center, start=0, extent=180, fill=self.pen_color, outline="")
        self.canvas.create_arc(x_center, y0, x1, y_center, start=0, extent=180, fill=self.pen_color, outline="")
        self.canvas.create_polygon([(x_center, y1), (x0, y_center), (x1, y_center)], fill=self.pen_color, outline="")

    def draw_spiral(self, x_center, y_center, start_radius, num_turns):
        import math
        angle_step = 0.1
        num_points = int(num_turns / angle_step)
        for i in range(num_points):
            angle = i * angle_step
            radius = start_radius + angle * 5
            x = x_center + math.cos(angle) * radius
            y = y_center + math.sin(angle) * radius
            self.canvas.create_oval(x, y, x+1, y+1, fill=self.pen_color, outline="")

    def draw_text(self, text, x, y, **kwargs):
        self.canvas.create_text(x, y, text=text, **kwargs)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
