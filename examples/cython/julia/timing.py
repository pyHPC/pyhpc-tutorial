import utils
# import pylab as pl
import numpy as np

def main(args):
    suffix = args.module.rsplit('.', 1)[-1]
    if suffix in ('so', 'pyd', 'pyx'):
        utils.compiler(args.setup)
    compute_julia = utils.importer(args.module, args.function)
    jla, time = compute_julia(args.cr, args.ci, args.N, 2.0, 4., args.cutoff)
    print "Compute time: %fs" % time
    # pl.imshow(np.log(jla), cmap=pl.cm.hot)
    # pl.show()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('module', help="""The module to use -- either a pure
            python module or a Cython .pyx file.  If given a .pyx file, it will
            be compiled automatically.""")
    parser.add_argument('-f', '--function', default='compute_julia', help="The function from the module to call, default `compute_julia`")
    parser.add_argument('--setup', default='setup.py')
    parser.add_argument('-cr', default=-0.1, help='The real component of the C parameter.')
    parser.add_argument('-ci', default=0.651, help='The imaginary component of the C parameter.')
    parser.add_argument('-N', default=200, help='The number of grid points to use.')
    parser.add_argument('--cutoff', default=10**3, help='The cutoff value, controls the image detail.')
    main(parser.parse_args())
