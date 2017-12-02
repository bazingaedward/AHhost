from ahhost.Interpolation import PointSourceInterpolation as PSI

psi = PSI()
psi.process(variables=['SO2','NOX'],method='linear',resolution=1)
psi.export()
