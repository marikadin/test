import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from other_dates import stock_symbol, date_list
import mplcursors
from extract_ddata import values
from machine import predicted_value
import sys
from test import keyword
y = stock_symbol
x = date_list
percent_change = 0

try:
    last_price = values
    if y[-1] != y[-2]:
        percent_change = (y[-1] - y[-2]) / y[-2] * 100
        percent_text = f"The percent of change is: {percent_change:.2f}%"
    else:
        percent_text = "The percent of change is: 0.00%"
except:
    try:
        if y[-1] != y[-2]:
            percent_change = (y[-1] - y[-2]) / y[-2] * 100
            percent_text = f"{percent_change:.2f}%"
    except:
        print("An error acoured, try another date")
        sys.exit()
    else:
        percent_text = "0.00%"

try:
    last_price = f"Today the open value is: ${y[-1]:,.2f}"
except:
    last_price = f"Today the open value is: ${values}"

text_color = "black"
if percent_change > 0:
    text_color = "green"
elif percent_change < 0:
    text_color = "red"

fig, ax = plt.subplots()
try:
    for i in range(1, len(y)):
        if y[-1] == y[-2]:
            line, = ax.plot([x[i - 1], x[i]], [y[i - 1], y[i]], linestyle='-', color='black', label='No Change')
        elif y[i] - y[i - 1] > 0:
            line, = ax.plot([x[i - 1], x[i]], [y[i - 1], y[i]], linestyle='-', color='green', label='Positive Change')
        elif y[i] - y[i - 1] < 0:
            line, = ax.plot([x[i - 1], x[i]], [y[i - 1], y[i]], linestyle='-', color='red', label='Negative Change')
except:
    print("An error acoured.")
    sys.exit()
if predicted_value != "Couldnt calculate the next value, try other date.":
    predicted_value = f"The predicted value for tomorrow is: ${predicted_value}"

ax.text(0.09, 1.05, last_price, transform=ax.transAxes, color="black", ha='right', fontsize=12)
ax.text(0.5, 1.05, percent_text, transform=ax.transAxes, color=text_color, ha='right', fontsize=12)
ax.text(1, 1.05, predicted_value, transform=ax.transAxes, color="green", ha='right', fontsize=12)
ax.text(0.09, 1.02, f"Stock symbole: '{keyword}'", transform=ax.transAxes, color="green", ha='right', fontsize=12)

cursor = mplcursors.cursor(hover=True)

try:
    ax.set_xticks([x[0], x[-1]])
except:
    ax.set_xticks([x[0]])

def on_hover(sel):
    y_data = sel.target[1]
    value = float(y_data)
    sel.annotation.set_position((sel.target[0], y_data))
    sel.annotation.set_text(f"Value: ${value:.2f}")

cursor.connect("add", on_hover)

fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()

def close_window(event):
    plt.close()
    print("Thank for using us.")
close_button_ax = plt.axes([0.92, 0.02, 0.06, 0.04])
button = plt.Button(close_button_ax, 'Close', color='lightcoral', hovercolor='red')
button.on_clicked(close_window)

plt.show()
print(keyword)
