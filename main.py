"""Shutdown timer"""

import os
import customtkinter as ctk
from modules.service import ctk_init, mk_frm, mk_lbl, mk_btn


class App(ctk.CTk):
    """Main app"""

    def __init__(self) -> None:
        super().__init__()
        ctk_init(self, "Shutdown timer", 500, 420)
        self.total_min: int = 0
        self.timer_id: str = ""
        self.timer_label_id: str = ""
        self.remaining_seconds: int = 0

        self.columnconfigure(0, weight=1, uniform="a")

        self.top_frm = mk_frm(
            self,
            {
                "fg_color": "transparent",
                "border_width": 1,
            },
            {"row": 0, "column": 0, "pady": 10, "padx": 10},
        )

        self.top_frm.columnconfigure(0, weight=1, uniform="a")
        self.header = mk_lbl(
            self.top_frm,
            {"text": "Shutdown timer", "fg_color": "transparent"},
            {"row": 0, "column": 0, "pady": 10, "padx": 10},
        )

        self.midd_frm = mk_frm(
            self,
            {
                "fg_color": "transparent",
                "border_width": 1,
            },
            {"row": 1, "column": 0, "pady": 10, "padx": 10},
        )
        self.midd_frm.columnconfigure((0, 1, 2), weight=1, uniform="a")

        self.min_01 = mk_btn(
            self.midd_frm,
            {"text": " 1 min", "command": lambda: self.add_min(1)},
            {"row": 0, "column": 0, "pady": 10, "padx": 10},
        )
        self.min_05 = mk_btn(
            self.midd_frm,
            {"text": " 5 min", "command": lambda: self.add_min(5)},
            {"row": 0, "column": 1, "pady": 10, "padx": 10},
        )
        self.min_15 = mk_btn(
            self.midd_frm,
            {"text": "15 min", "command": lambda: self.add_min(15)},
            {"row": 0, "column": 2, "pady": 10, "padx": 10},
        )
        self.min_30 = mk_btn(
            self.midd_frm,
            {"text": "30 min", "command": lambda: self.add_min(30)},
            {"row": 1, "column": 0, "pady": 10, "padx": 10},
        )
        self.min_60 = mk_btn(
            self.midd_frm,
            {"text": "1 hour", "command": lambda: self.add_min(60)},
            {"row": 1, "column": 1, "pady": 10, "padx": 10},
        )
        self.reset = mk_btn(
            self.midd_frm,
            {"text": "reset", "fg_color": "#8d5700", "command": self.reset_total},
            {"row": 1, "column": 2, "pady": 10, "padx": 10},
        )
        self.setmin = mk_btn(
            self.midd_frm,
            {"text": "- set -", "fg_color": "#008d49", "command": self.set_and_run},
            {"row": 2, "column": 2, "pady": 10, "padx": 10},
        )

        self.totallbl = mk_lbl(
            self.midd_frm,
            {"text": "cas: 00:00", "anchor": "w", "fg_color": "#1c1c1c"},
            {"row": 2, "column": 0, "columnspan": 2, "pady": 10, "padx": 10},
        )
        self.midfrm_list: list = [
            self.min_01,
            self.min_05,
            self.min_15,
            self.min_30,
            self.min_60,
            self.reset,
            self.setmin,
        ]

        self.btm_frm = mk_frm(
            self,
            {
                "fg_color": "transparent",
                "border_width": 1,
            },
            {"row": 2, "column": 0, "pady": 10, "padx": 10},
        )

        self.infolbl = mk_lbl(
            self.btm_frm, {"text": ""}, {"row": 0, "column": 0, "pady": 10, "padx": 10}
        )

        self.ext_btn = mk_btn(
            self,
            {"text": "exit", "command": self.destroy},
            {"row": 4, "column": 0, "pady": 10, "padx": 10},
            "e",
        )
        self.cancel_btn = mk_btn(
            self,
            {"text": "cancel", "state": "disabled", "command": self.cancel_timer},
            {"row": 4, "column": 0, "pady": 10, "padx": 10},
            "w",
        )
        self.countdownlbl = mk_lbl(
            self,
            {"text": "", "fg_color": "black", "anchor": "w"},
            {"row": 3, "column": 0, "pady": 10, "padx": 10, "ipady": 10, "ipadx": 10},
        )

    def reset_total(self) -> None:
        """reset total time"""
        self.total_min = 0
        self.totallbl.configure(text="cas: 00:00")

    def add_min(self, amount: int):
        """pripocitej mnozstvi"""
        self.total_min += amount
        hour, mins = divmod(self.total_min, 60)
        self.totallbl.configure(text=f"cas: {str(hour).zfill(2)}:{str(mins).zfill(2)}")

    def shutdown(self) -> None:
        """Shutdown computer"""
        self.countdownlbl.configure(text="pocitac se vypne za 10 sekund!!!")
        os.system("shutdown /s /t 10")

    def start_countdown(self) -> None:
        """Spustí odpočítávání na labelu."""
        if self.remaining_seconds > 0:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.countdownlbl.configure(text=f"Zbývá: {mins} min {secs} sec")
            self.remaining_seconds -= 1
            self.timer_label_id = self.after(1000, self.start_countdown)

    def set_and_run(self) -> None:
        """Spustí funkci na odpočet"""
        if self.total_min > 0:
            for item in self.midfrm_list:
                item.configure(state="disabled")
            self.cancel_btn.configure(state="enabled")
            self.remaining_seconds = self.total_min * 60
            self.timer_id = self.after((self.total_min * 60 * 1000), self.shutdown)
            self.start_countdown()
            hour, mins = divmod(self.total_min, 60)
            self.infolbl.configure(
                text=f"Odpočet nastaven na {str(hour).zfill(2)}:{str(mins).zfill(2)} hod."
            )
        else:
            self.infolbl.configure(text="cas neni nastaven")

    def cancel_timer(self) -> None:
        """Zruší odpočet"""
        self.after_cancel(self.timer_id)
        self.after_cancel(self.timer_label_id)
        self.infolbl.configure(text="Odpocet zrusen")
        self.timer_id = ""
        self.timer_label_id = ""
        self.cancel_btn.configure(state="disabled")
        for item in self.midfrm_list:
            item.configure(state="enabled")


if __name__ == "__main__":
    app: App = App()
    app.mainloop()
