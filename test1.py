import tkinter as tk

class TimelineApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=800, height=400)
        self.canvas.pack()

        self.start_x = 50
        self.end_x = 750
        self.y = 200
        self.arrow_width = 20
        self.arrow_length = 30
        self.weeks = 52
        self.week_width = (self.end_x - self.start_x - self.arrow_length) / self.weeks

        self.boxes = []  # Liste zum Speichern der Boxen
        self.selected_box = None  # Aktuell ausgewählte Box für Drag & Drop
        self.drag_data = None  # Daten zum Speichern der ursprünglichen Position beim Ziehen
        self.canvas.bind("<ButtonPress-1>", self.on_box_select)
        self.canvas.bind("<ButtonRelease-1>", self.on_box_release)
        self.canvas.bind("<B1-Motion>", self.on_box_drag)

        self.draw_timeline()
        self.create_box_button()

    def draw_timeline(self):
        self.canvas.create_polygon(self.start_x, self.y - self.arrow_width/2,
                                   self.end_x - self.arrow_length, self.y - self.arrow_width/2,
                                   self.end_x - self.arrow_length, self.y - self.arrow_width/2 - self.arrow_width/2,
                                   self.end_x, self.y,
                                   self.end_x - self.arrow_length, self.y + self.arrow_width/2 + self.arrow_width/2,
                                   self.end_x - self.arrow_length, self.y + self.arrow_width/2,
                                   self.start_x, self.y + self.arrow_width/2,
                                   fill='gray', outline='black')

        for week in range(self.weeks + 1):
            x = self.start_x + week * self.week_width
            self.canvas.create_line(x, self.y - 5, x, self.y + 5, width=2)
            if week % 5 == 0:
                self.canvas.create_text(x, self.y + 30, text=str(week), anchor=tk.N)

        for box in self.boxes:
            self.canvas.create_rectangle(box['x1'], box['y1'], box['x2'], box['y2'], fill='lightblue')
            text_lines = self.get_wrapped_text_lines(box['text'], box['x2'] - box['x1'] - 10)
            text_y = box['y1'] + 5
            for line in text_lines:
                self.canvas.create_text(box['x1'] + 5, text_y, text=line, anchor=tk.NW)
                text_y += 20

    def get_wrapped_text_lines(self, text, max_width):
        lines = []
        words = text.split()
        current_line = words[0]
        for word in words[1:]:
            if self.canvas.bbox(current_line + ' ' + word)[2] < max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def create_box_button(self):
        create_box_button = tk.Button(self.master, text="Box erstellen", command=self.create_box)
        create_box_button.pack()

    def create_box(self):
        box_text = self.show_text_input_dialog("Gib den Text für die Box ein:")
        if box_text:
            x1 = self.start_x + self.week_width * 2  # Initialposition der Box
            y1 = self.y - 50
            x2 = x1 + 100
            y2 = y1 + self.calculate_box_height(box_text, x2 - x1 - 10)
            box = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'text': box_text}
            self.boxes.append(box)
            self.draw_timeline()

    def calculate_box_height(self, text, max_width):
        lines = self.get_wrapped_text_lines(text, max_width)
        return len(lines) * 20 + 10

    def show_text_input_dialog(self, prompt):
        dialog = tk.Toplevel(self.master)
        dialog.title("Text eingeben")
        label = tk.Label(dialog, text=prompt)
        label.pack()
        entry = tk.Entry(dialog)
        entry.pack()
        entry.focus_set()
        ok_button = tk.Button(dialog, text="OK", command=lambda: self.on_dialog_ok(dialog, entry))
        ok_button.pack()

        self.master.wait_window(dialog)
        return self.dialog_input

    def on_dialog_ok(self, dialog, entry):
        self.dialog_input = entry.get()
        dialog.destroy()

    def on_box_select(self, event):
        x, y = event.x, event.y
        for box in self.boxes:
            if box['x1'] < x < box['x2'] and box['y1'] < y < box['y2']:
                self.selected_box = box
                self.drag_data = {'x': x, 'y': y, 'box_x1': box['x1'], 'box_x2': box['x2']}
                break

    def on_box_release(self, event):
        self.selected_box = None
        self.drag_data = None

    def on_box_drag(self, event):
        if self.selected_box and self.drag_data:
            dx = event.x - self.drag_data['x']
            dy = event.y - self.drag_data['y']
            new_x1 = self.drag_data['box_x1'] + dx
            new_x2 = self.drag_data['box_x2'] + dx
            new_y1 = self.y - 50  # Oberhalb der Zeitleiste
            new_y2 = new_y1 + self.calculate_box_height(self.selected_box['text'], new_x2 - new_x1 - 10)
            self.selected_box['x1'] = new_x1
            self.selected_box['x2'] = new_x2
            self.selected_box['y1'] = new_y1
            self.selected_box['y2'] = new_y2
            self.canvas.delete('all')
            self.draw_timeline()

    def run(self):
        self.master.mainloop()

root = tk.Tk()
app = TimelineApp(root)
app.run()
