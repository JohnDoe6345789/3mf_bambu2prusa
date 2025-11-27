import logging
import os
from tkinter import Button, Label, Tk, filedialog

from bambu_to_prusa.converter import BambuToPrusaConverter


class ZipProcessorGUI:
    def __init__(self, master):
        logging.debug("Initializing ZipProcessorGUI")
        self.master = master
        master.title("Bambu2Prusa 3mf Processor")

        self.label = Label(master, text="Select input and output 3mf files.")
        self.label.pack(pady=10)

        self.select_input_button = Button(master, text="Select Input Bambu 3mf", command=self.select_input)
        self.select_input_button.pack(pady=5)

        self.select_output_button = Button(master, text="Select Output Prusa 3mf", command=self.select_output)
        self.select_output_button.pack(pady=5)

        self.process_button = Button(master, text="Process", command=self.bambu3mf2prusa3mf)
        self.process_button.pack(pady=10)

        self.status_label = Label(master, text="")
        self.status_label.pack(pady=5)

        self.input_file = ""
        self.output_file = ""
        self.converter = BambuToPrusaConverter()

    def select_input(self):
        logging.debug("Selecting input file")
        self.input_file = filedialog.askopenfilename(filetypes=[("3mf files", "*.3mf")])
        self.status_label.config(text=f"Input file selected: {os.path.basename(self.input_file)}")

    def select_output(self):
        logging.debug("Selecting output file")
        self.output_file = filedialog.asksaveasfilename(defaultextension=".3mf", filetypes=[("3mf files", "*.3mf")])
        self.status_label.config(text=f"Output file selected: {os.path.basename(self.output_file)}")

    def bambu3mf2prusa3mf(self):
        logging.debug("Converting Bambu 3mf to Prusa 3mf via GUI")
        try:
            if not self.input_file or not self.output_file:
                self.status_label.config(text="Please provide both input and output files.")
                return
            self.converter.convert_archive(self.input_file, self.output_file)
            self.status_label.config(text=f"Output file created: {os.path.basename(self.output_file)}")
        except Exception as exc:  # pragma: no cover - GUI messaging
            logging.error("An error occurred during processing: %s", exc)
            self.status_label.config(text=f"Error: {exc}")


def main():
    root = Tk()
    app = ZipProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
