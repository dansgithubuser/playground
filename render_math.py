from matplotlib import pyplot

#from matplotlib import rc
#rc('text', usetex=True)  #requires latex to be installed

formula = r'$i^2 = j^2 = k ^ 2 = i j k = -1$    (1)'

fig = pyplot.figure()
text = fig.text(0, 0, formula, color=(1, 0, 0), bbox={'facecolor': (0.5, 0.5, 0.5)})

# Saving the figure will render the text.
dpi = 300
fig.savefig('formula.png', dpi=dpi)

# Now we can work with text's bounding box.
bbox = text.get_window_extent()
width, height = bbox.size / float(dpi) + 0.005
# Adjust the figure size so it can hold the entire text.
fig.set_size_inches((width, height))

# Adjust text's vertical position.
dy = (bbox.ymin/float(dpi))/height
text.set_position((0, -dy))

# Save the adjusted text.
fig.savefig('formula.png', dpi=dpi)
