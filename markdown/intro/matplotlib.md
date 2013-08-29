Matplotlib - Plotting
---------------------

- Publication worthy plotting
- Focus on 2D with some 3D and animation support
- Can hit many different backend
- See large gallery at: [http://matplotlib.org/gallery.html](http://matplotlib.org/gallery.html)



Simple plot  
<img src="../figures/intro/simple_plot.png" style="width: 600px;"/>
```python
import pylab as pl
import numpy as np

X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)

pl.plot(X, C)
pl.plot(X, S)
pl.show()
```



Customize Everything  

```python
 # Create a figure of size 8x6 points, 80 dots per inch
pl.figure(figsize=(8, 6), dpi=80)
 # Create a new subplot from a grid of 1x1
pl.subplot(1, 1, 1)
X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)
 # Plot cosine with a blue continuous line of width 1 (pixels)
pl.plot(X, C, color="blue", linewidth=1.0, linestyle="-")
 # Plot sine with a green continuous line of width 1 (pixels)
pl.plot(X, S, color="green", linewidth=1.0, linestyle="-") # Set x limits
pl.xlim(-4.0, 4.0) # Set x ticks
pl.xticks(np.linspace(-4, 4, 9, endpoint=True)) # Set y limits
pl.ylim(-1.0, 1.0) # Set y ticks
pl.yticks(np.linspace(-1, 1, 5, endpoint=True)) # Save figure using 72 dots per inch
 # savefig("exercice_2.png", dpi=72)
 # Show result on screen
pl.show()
```



Change linestyles  
<img src="../figures/intro/simple_plot_cust.png" style="width: 600px;"/>
```python
pl.figure(figsize=(10, 6), dpi=80)
pl.plot(X, C, color="blue", linewidth=2.5, linestyle="-")
pl.plot(X, S, color="red",  linewidth=2.5, linestyle="-")
```



Adding legend  
<img src="../figures/intro/simple_plot_legend.png" style="width: 600px;"/>
```python
pl.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")
pl.plot(X, S, color="green", linewidth=2.5, linestyle="--", label="sine") # Set x limits
pl.legend(loc='upper left')
```



Moving splines  
<img src="../figures/intro/simple_plot_cust2.png" style="width: 600px;"/>
```python
ax = pl.gca() # gca stands for 'get current axis'
ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none') 
ax.xaxis.set_ticks_position('bottom') 
ax.spines['bottom'].set_position(('data',0)) 
ax.yaxis.set_ticks_position('left') 
ax.spines['left'].set_position(('data',0))
```



Histograms  
<img src="../figures/intro/hist.png" style="width: 600px;"/>

```python
import pylab as pl

pl.plot(pylab.randn(10000), 100)
pl.show()
```



Add a fit line and legend  
<img src="../figures/intro/hist_legend_fit.png" style="width: 600px;"/>
```python
n, bins, patches = pl.hist(pl.randn(1000), 40, normed=1)
l, = pl.plot(bins, pl.normpdf(bins, 0.0, 1.0), 'r--', label='fit', linewidth=3)
legend([l, patches[0]], ['fit', 'hist'])
```



Other types of plots include:

*  Scatter
*  Bar
*  Pie
*  Sankey
*  Images
*  Quivers
*  Multiplots
*  Polar 
*  3D 



Other elements to know about:

- Ticks: control how the ticks look
- Annotations: Add visual elements to your plot
- Axes: draw plots on top of themselves
- Backends: draw for different rendering engines
