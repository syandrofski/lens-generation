import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings



def ea_surf(R, kappa, a_vals, msd):
    warnings.filterwarnings('ignore')
    r_vals = np.linspace(-msd, msd, round(2*msd)*100+1)
    z_vals = (r_vals**2) / (R * (1 + np.sqrt(1 - (1 + kappa)*(r_vals**2 / R**2))))
    nans = np.invert(np.isnan(z_vals))

    for i, val in enumerate(a_vals):
        z_vals += val * r_vals**(2 * i + 4)

    if not nans[0]:
        n1, n2 = np.array_split(nans, 2)
        z1, z2 = np.array_split(z_vals, 2)
        n2 = np.flip(n2)
        idx1 = np.argmax(n1)
        idx2 = np.argmax(n2)
        val1 = z_vals[idx1]
        val2 = z_vals[-1*(idx2+1)]
        z1 = np.nan_to_num(z1, nan=val1)
        z2 = np.nan_to_num(z2, nan=val2)
        z_vals = np.concatenate((z1, z2))

    return [r_vals, z_vals]


#side_1 and side_2 should include both r and z values in a list
def surfaces_to_lens(side_1, side_2, msd, thickness, multi=False):
    both_sides = pd.DataFrame(np.hstack((side_1[0].reshape(len(side_1[0]), 1), side_1[1].reshape(len(side_1[1]), 1), side_2[1].reshape(len(side_2[1]), 1))), columns=['r', 'z1', 'z2'])
    both_sides = both_sides[(both_sides['r'] <= msd) & (both_sides['r'] >= -msd)]
    np_both = both_sides.to_numpy()
    np_both[:, 2] += thickness
    front = np.flipud(np.hstack((np_both[:, 0:1], np_both[:, 1:2])))
    rear = np.hstack((np_both[:, 0:1], np_both[:, 2:3]))
    last = front[0:1, :]
    lens = np.vstack((front, rear, last))
    if multi:
        return (lens, thickness)
    return lens


def plot_single_lens(lens):
    fig, ax = plt.subplots()
    ax.plot(lens[:, 1], lens[:, 0], color='blue', linewidth=2)
    ax.set(xlim=(-5, 5), xticks=(np.arange(-5, 5)))
    ax.set(ylim=(-5, 5), yticks=(np.arange(-5, 5)))
    plt.show()


def lens_arr(lenses, spacings, save=False, check=False, display=True):
    fig, ax = plt.subplots()
    asm_len = 0
    lens = lenses[0][0]
    aggregate = lens
    check_lenses = [lens]
    thickness = lenses[0][1]
    ax.plot(lens[:, 1], lens[:, 0], color='black', linewidth=2)
    asm_len += thickness
    lenses.pop(0)
    for l_and_t, spac in zip(lenses, spacings):
        lens = l_and_t[0]
        lens[:, 1] += asm_len + spac
        aggregate = np.vstack((aggregate, lens))
        check_lenses.append(lens)
        ax.plot(lens[:, 1], lens[:, 0], color='black', linewidth=2)
        thickness = l_and_t[1]
        asm_len += thickness + spac
    aggregate = np.sort(aggregate[:, 0])
    up_bd = aggregate[0] * 1.25
    low_bd = aggregate[0] * (-1.25)
    if 1.5*asm_len > 2.5*aggregate[0]:
        up_bd = 0.75*asm_len
        low_bd = -0.75*asm_len
        x_center = asm_len/2

    ax.set(xlim=(low_bd+x_center, up_bd+x_center), xticks=(np.arange(low_bd+x_center, up_bd+x_center)))
    ax.set(ylim=(low_bd, up_bd), yticks=np.arange(low_bd, up_bd))
    plt.axis('off')
    fig = plt.gcf()
    if save:
        plt.savefig('C:/Users/spenc/PycharmProjects/SuperUROP/generated/test.png')
    if display:
        plt.show()
        plt.close()
    if check:
        return (fig, check_lenses)
    return fig


def save_plot(name, plot, addon='', custom_path='C:/Users/spenc/PycharmProjects/SuperUROP/generated/'):
    plot.savefig(custom_path + addon + '/' + name + '.png')


def main():
    multi_lens_test()


def multi_lens_test():
    msd = 2.833
    bounds_1 = ea_surf(3.336, -11.578, [-0.004987, -0.002643, 0.0003744, -0.00002296], msd)
    bounds_2 = ea_surf(4.599, 2.252, [-0.035, 0.002033, 0.0000685, -0.00003868], msd)
    lens_struct_1 = surfaces_to_lens(bounds_1, bounds_2, msd, 1.240, multi=True)
    lens_struct_2 = surfaces_to_lens(bounds_1, bounds_2, msd, 1.240, multi=True)
    larr = lens_arr([lens_struct_1, lens_struct_2], [3], save=True)
    save_plot('test2', larr)


if __name__ == '__main__':
    main()