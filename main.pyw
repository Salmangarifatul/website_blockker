from tkinter import *
import blocker_GUI
from blocker_GUI import GUI

# main function untuk menjalankan program
def main():
    # membuat GUI
    root = Tk()
    # GUI judul, ukuran, dll
    root.title("Website blocker")
    root.geometry(f"{blocker_GUI.width}x{blocker_GUI.height}")
    root.resizable(0, 0)
    root.iconbitmap("blocker.ico")
    root.protocol("WM_DELETE_WINDOW", lambda: GUI.main_closing(root))

    # membuat 3 frame, frame judul, frame block, dan list blocking frame
    # bagian atas frame
    top_frame = Frame(root, bg="red", width=blocker_GUI.width, height=blocker_GUI.prct(20, blocker_GUI.height))
    top_frame.place(x=0, y=0)

    # bagian tengah frame
    middle_frame = Frame(root, bg="#D3D3D3", width=blocker_GUI.width, height=blocker_GUI.prct(30, blocker_GUI.height))
    middle_frame.place(x=0, y=blocker_GUI.prct(20, blocker_GUI.height))

    # bagian bawah frame
    bottom_frame = Frame(root, bg="white", width=blocker_GUI.width, height=blocker_GUI.prct(50, blocker_GUI.height))
    bottom_frame.place(x=0, y=blocker_GUI.prct(50, blocker_GUI.height))

    # title label
    title_lbl = Label(top_frame, text="Website Blocker", fg="Black", font=("Poppins Bold", 30), bg="red").place(
        x=blocker_GUI.prct(22, blocker_GUI.width), y=blocker_GUI.prct(5, blocker_GUI.height))

    # membuat label, tombol dan entry untuk frame bagian tengah
    GUI.create_middle_frame(middle_frame, bottom_frame)

    # membuat label dan tombol untuk frame bagian bawah
    GUI.create_bottom_frame(bottom_frame)

    # running GUI
    mainloop()

if __name__ == '__main__':
    main()

