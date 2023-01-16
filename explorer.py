import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import lens_gen as lg
import random
from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing

class Surface_Parameters():
    def __init__(self):
        self.radius = smart_gen('r', paired=False)[0]
        self.kappa = smart_gen('k', paired=False)[0]
        self.all_a = smart_gen('a', paired=False)
        self.msd = smart_gen('msd', paired=False)
        self.thickness = smart_gen('t', paired=False)

    def set_radius(self, rad):
        self.radius = rad

    def set_kappa(self, k):
        self.kappa = k

    def set_given_a(self, power, val):
        self.all_a[int((power/2)-2)] = val

    def set_msd(self, m):
        self.msd = m

    def set_thickness(self, t):
        self.thickness = t

    def get_radius(self):
        return self.radius

    def get_kappa(self):
        return self.kappa

    def get_given_a(self, power):
        return self.all_a[int((power / 2) - 2)]

    def get_msd(self):
        return self.msd

    def get_thickness(self):
        return self.thickness


def gen_surfaces(n_surfs):
    surfs = []
    for i in range(n_surfs):
        surfs.append(Surface_Parameters())
    return surfs


def gen_simple_vals():
    radius = (random.random() - 0.5) * 12
    msd = random.random() * 2 + 1.2
    kappa = (random.random() - 0.5) * 25
    a4 = (random.random() - 0.5) * 2 * 10**-1
    a6 = (random.random() - 0.5) * 2 * 10**-2
    a8 = (random.random() - 0.5) * 2 * 10**-3
    a10 = (random.random() - 0.5) * 2 * 10**-4
    a12 = (random.random() - 0.5) * 2 * 10**-5
    all_a = [a4, a6, a8, a10, a12]
    thickness = random.random() * 4 + 2
    return (radius, kappa, all_a, msd, thickness)


def smart_gen(param, paired=True):
    out = []
    if paired:
        paired = 2
    else:
        paired = 1
    if param == 'r':
        for i in range(paired):
            radius = (random.random() - 0.5) * 12
            out.append(radius)
    elif param == 'k':
        for i in range(paired):
            kappa = (random.random() - 0.5) * 25
            out.append(kappa)
    elif param == 'msd':
        msd = random.random() * 4 + 0.75
        out = msd
    elif param == 't':
        thickness = random.random() * 2 + 0.5
        out = thickness
    elif param == 's':
        spacing = random.random() * 0.75
        out = spacing
    elif param[0] == 'a':
        for i in range(paired):
            all_a = []
            for power in range(4, 14, 2):
                a = (random.random() - 0.5) * 2 * 10**(-1*((power/2)))#-1))
                all_a.append(a)
            out.extend(all_a)
    else:
        print('Invalid parameter choice.')
        exit(0)
    return out


def validate(lenses):
    bad = False
    for i in range(len(lenses)):
        '''
        idx = np.random.choice(lenses[i].shape[0], round(lenses[i].shape[0]/100), replace=False)
        if not LinearRing(np.unique(lenses[i][idx], axis=0)).is_simple:
            return True
        '''
        try:
            lenses[i] = Polygon(lenses[i])
        except:
            return True
    for i in range(len(lenses)):
        for j in range(len(lenses)):
            if not i == j:
                if lenses[i].intersects(lenses[j]):
                    return True
    return False


def raytrace(lenses):
    pass


def main():
    total = 0
    success = 0
    while success < 1000:
        lenses = []
        spacings = []
        for i in range(3):
            r1, r2 = smart_gen('r')
            k1, k2 = smart_gen('k')
            msd = smart_gen('msd', paired=False)
            thickness = smart_gen('t', paired=False)
            spacing = smart_gen('s', paired=False)
            as_1, as_2 = smart_gen('a')
            s1 = lg.ea_surf(r1, k1, as_1, msd)
            s2 = lg.ea_surf(r2, k2, as_2, msd)
            lenses.append(lg.surfaces_to_lens(s1, s2, msd, thickness, multi=True))
            spacings.append(thickness)
        f, val = lg.lens_arr(lenses, spacings, check=True, display=False)
        if not validate(val):
            success += 1
            lg.save_plot('R1_plot_' + str(success), f, 'second_set')
        total += 1
        print('Total: ' + str(total))
        print('Successful ' + str(success))


if __name__ == '__main__':
    main()