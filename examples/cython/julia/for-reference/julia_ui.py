# --- Imports ----------------------------------------------------------------
import numpy as np

from traits.api import (HasTraits, Float, Instance, Array, on_trait_change,
                        Property, Int, Enum, Callable)
from traitsui.api import View, Item, RangeEditor, Controller, HGroup, Group
from chaco import default_colormaps
from chaco.api import Plot, ArrayPlotData, hot
from enable.api import ComponentEditor
import utils

# --- Traits classes. --------------------------------------------------------

class Julia(HasTraits):

    resolution = Int(100)
    cr = Float(-0.1)
    ci = Float(0.651)
    cutoff = Int(100)
    runtime = Float()
    julia = Array()
    compute_julia = Callable()
    
    @on_trait_change('cr, ci, resolution, cutoff')
    def update_julia(self):
        self.julia = self.compute()
        
    def _julia_default(self):
        return self.compute()
    
    def compute(self):
        julia, self.runtime = self.compute_julia(self.cr, self.ci,
                                                 self.resolution,
                                                 lim=4., cutoff=self.cutoff)
        return np.log(julia)

# --- Set up the colormaps to use --------------------------------------------
def colormaps():
    cmnames = default_colormaps.color_map_name_dict.keys()
    colormaps = sorted(cmnames, key=str.lower)
    for boring in 'hot bone gray yarg gist_gray gist_yarg Greys'.split():
        colormaps.remove(boring)
    # Make 'hot' the first colormap.
    return ['hot'] + colormaps

class JuliaUI(Controller):
    
    model = Instance(Julia)
    runtime = Property(depends_on=['model.runtime'])
    plot = Instance(Plot)
    colormap = Enum(colormaps())
    
    traits_view = View(Item('controller.plot', editor=ComponentEditor(), show_label=False),
            Group(
                Item('cr', editor=RangeEditor(low=-2.0, high=2.0, low_label='-2', high_label='2'), show_label=False),
                Item('ci', editor=RangeEditor(low=-2.0, high=2.0, low_label='-2', high_label='2'), show_label=False),
                label='c_real / c_imaginary', show_border=True,
                ),
            HGroup(
                Item('resolution', editor=RangeEditor(low=50, high=1000, mode='slider')),
                Item('cutoff', editor=RangeEditor(low=100, high=300, mode='slider')),
                Item('controller.colormap'),
                ),
            Item('controller.runtime', style='readonly', show_label=False),
            width=800, height=900, resizable=True,
            title="Julia Set Explorer")
    
    @on_trait_change('model.runtime')
    def _get_runtime(self):
        return "Compute time: {:d} ms".format(int(round(self.model.runtime * 1000)))
    
    @on_trait_change('model.julia')
    def update_julia(self):
        self.plot.data.set_data('julia', self.model.julia)
    
    def _plot_default(self):
        julia = self.model.julia
        apd = ArrayPlotData(julia=julia[:-1,:-1])
        grid = np.linspace(-2, 2, self.model.resolution-1)
        X, Y = np.meshgrid(grid, grid)
        plot = Plot(apd)
        plot.aspect_ratio = 1.0
        plot.img_plot("julia", xbounds=X, ybounds=Y,
                      colormap=hot, interpolation='nearest')
        return plot
    
    def _colormap_changed(self):
        cmap = default_colormaps.color_map_name_dict[self.colormap]
        if self.plot is not None:
            value_range = self.plot.color_mapper.range
            self.plot.color_mapper = cmap(value_range)
            self.plot.request_redraw()
            

# --- main entry point -------------------------------------------------------
            
def main(args):
    suffix = args.module.rsplit('.', 1)[-1]
    if suffix in ('so', 'pyd', 'pyx'):
        utils.compiler(args.setup)
    compute_julia = utils.importer(args.module, args.function)
    julia = Julia(compute_julia=compute_julia)
    jui = JuliaUI(model=julia)
    jui.configure_traits()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('module')
    parser.add_argument('-f', '--function', default='compute_julia')
    parser.add_argument('--setup', default='setup.py')
    main(parser.parse_args())
