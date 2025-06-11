import tkinter as tk
from tkinter import ttk
import pyautogui as pag
import pygetwindow as gw
import time
import logging

class OrderSenderApp:
    def __init__(self, master):
        self.master = master
        master.title('Order Sender')
        self.create_widgets()
        self.bind_keys()
        logging.basicConfig(filename='order_sender.log', level=logging.INFO,
                            format='%(asctime)s %(message)s')

    def create_widgets(self):
        self.notional_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.account_var = tk.StringVar()
        self.volume_var = tk.StringVar(value='')
        self.status_var = tk.StringVar(value='')

        ttk.Label(self.master, text='Notional').grid(row=0, column=0, sticky='e')
        self.notional_entry = ttk.Entry(self.master, textvariable=self.notional_var)
        self.notional_entry.grid(row=0, column=1)
        self.notional_entry.focus()

        ttk.Label(self.master, text='Price').grid(row=1, column=0, sticky='e')
        self.price_entry = ttk.Entry(self.master, textvariable=self.price_var, state='disabled')
        self.price_entry.grid(row=1, column=1)

        ttk.Label(self.master, text='Stock').grid(row=2, column=0, sticky='e')
        self.stock_entry = ttk.Entry(self.master, textvariable=self.stock_var, state='disabled')
        self.stock_entry.grid(row=2, column=1)

        ttk.Label(self.master, text='Account').grid(row=3, column=0, sticky='e')
        self.account_entry = ttk.Entry(self.master, textvariable=self.account_var)
        self.account_entry.grid(row=3, column=1)

        ttk.Label(self.master, text='Volume').grid(row=4, column=0, sticky='e')
        self.volume_label = ttk.Label(self.master, textvariable=self.volume_var)
        self.volume_label.grid(row=4, column=1, sticky='w')

        self.status_label = ttk.Label(self.master, textvariable=self.status_var, foreground='blue')
        self.status_label.grid(row=5, column=0, columnspan=2, sticky='w')

    def bind_keys(self):
        self.notional_entry.bind('<Return>', self.enable_price)
        self.price_entry.bind('<Return>', self.calculate_volume)
        self.master.bind('<F1>', lambda e: self.reset_fields())
        self.master.bind('<F9>', self.send_order)

    def enable_price(self, event=None):
        self.price_entry.config(state='normal')
        self.price_entry.focus()

    def calculate_volume(self, event=None):
        try:
            n = float(self.notional_var.get())
            p = float(self.price_var.get())
            vol = 0.5 * n * 1_000_000 / p
            vol = int(round(vol / 100.0)) * 100
            self.volume_var.set(format(vol, ',d').replace(',', ' '))
        except ValueError:
            self.volume_var.set('')
            self.status_var.set('Invalid numbers')
            return
        self.stock_entry.config(state='normal')
        self.stock_entry.focus()
        self.status_var.set('')

    def reset_fields(self):
        self.notional_var.set('')
        self.price_var.set('')
        self.stock_var.set('')
        self.account_var.set('')
        self.volume_var.set('')
        self.status_var.set('')
        self.price_entry.config(state='disabled')
        self.stock_entry.config(state='disabled')
        self.notional_entry.focus()

    def send_order(self, event=None):
        stock = self.stock_var.get().strip()
        volume = self.volume_var.get().replace(' ', '')
        price = self.price_var.get().strip()
        account = self.account_var.get().strip()
        if not (stock and volume and price and account):
            self.status_var.set('Missing fields')
            return
        win = gw.getWindowsWithTitle('Test iFISe Trader vax')
        if not win:
            self.status_var.set('Trader window not found')
            return
        try:
            win[0].activate()
            time.sleep(1)
            pag.press('numlock')
            pag.press('backspace')
            time.sleep(0.1)
            pag.typewrite(stock, interval=0.05)
            pag.press('enter')
            pag.typewrite(volume, interval=0.05)
            pag.press('enter')
            pag.typewrite(f'{float(price):.2f}', interval=0.05)
            pag.press('enter')
            pag.typewrite(account, interval=0.05)
            pag.press('enter')
            pag.press('enter')
            pag.press('enter')
            pag.press('numlock')
            logging.info('Sent %s %s @ %s acc:%s', stock, volume, price, account)
            self.status_var.set(f'Sent: {stock} @ {price} Vol {self.volume_var.get()}')
        except Exception as e:
            self.status_var.set(f'Error: {e}')


def main():
    root = tk.Tk()
    app = OrderSenderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
