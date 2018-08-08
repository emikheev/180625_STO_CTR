import matplotlib.pyplot as plt

plt.plot(range(10))

def onclick(event):
    print(event.key)

cid = plt.gcf().canvas.mpl_connect('key_press_event', onclick)

plt.show()