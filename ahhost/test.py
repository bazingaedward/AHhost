from ahhost.Interpolation import PointSourceInterpolation as PSI

psi = PSI()
psi.process(variables=['SO2','NOX'])
psi.export()
