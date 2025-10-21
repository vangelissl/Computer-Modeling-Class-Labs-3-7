import pandas as pd
import matplotlib.pyplot as plt


STATES_NUM = 21
STEP = 0.25
LAM = 6
MU = 1
M = 15


def factorial(n):
    fact = 1
    for i in range(1, n + 1):
        fact *= i

    return fact


class AnalyticalModel():
    def __init__(self, c, lam, mu, m):
        self.r = lam / mu

        self.mu_general = c * mu

        self.rho = self.r / c

        self.q_0 = self.calc_q_0(c, self.r, m, self.rho)

        self.p_refusal = self.r**c / factorial(c) * self.rho**m * self.q_0

        self.p_q = self.calc_p_q(c, self.r, m, self.rho, self.q_0)

        self.Q = 1 - self.p_refusal

        self.A = lam * self.Q

        self.k_occupied = self.A / mu

        self.L_q = self.calc_L_q(c, self.r, m, self.rho, self.q_0)

        self.L_s = self.L_q + self.k_occupied

        self.W_q = self.L_q / lam

        self.W_s = self.W_q + (STEP * 60) / mu

    def calc_q_0(self, c, r, m, rho):
        q_0 = 0

        for i in range(c):
            q_0 += r**i / factorial(i)

        product = r**c / factorial(c)

        if rho != 1:
            product *= (1 - rho**(m+1)) / (1 - rho)
        else:
            product *= (m+1)
        q_0 += product

        return 1/q_0

    def calc_p_q(self, c, r, m, rho, q_0):
        p_q = r**c / factorial(c)

        if rho != 1:
            p_q *= (1 - rho**m) / (1 - rho)
        else:
            p_q *= m

        return p_q * q_0

    def calc_L_q(self, c, r, m, rho, q_0):
        L_q = r**c / factorial(c)

        if rho != 1:
            L_q *= rho
            numerator = 1 - rho**m - m * rho**m * (1 - rho)
            denominator = (1 - rho) ** 2
            L_q *= numerator / denominator
        else:
            L_q *= (m * (m+1)) / 2

        return L_q * q_0


data = {'rho': [],
        'q0': [],
        'p_refusal': [],
        'p_q': [],
        'Q': [],
        'A': [],
        'k_occupied': [],
        'L_q': [],
        'L_s': [],
        'W_q': [],
        'W_s': []
        }


def plot_scatter(df, metric):
    rho_values = df.loc[metric].values

    # Create list of workers (x-axis)
    workers = list(df.columns.astype(int))

    # Plot scatter
    plt.scatter(workers, rho_values, s=70, color='magenta', zorder=2)

    plt.title("Absolute throughput by Number of Workers")
    plt.xlabel("Number of Workers")
    plt.ylabel("A")
    plt.grid(True, zorder=1)
    plt.show()


if __name__ == '__main__':
    c = int(input('Enter max number of channels: '))

    for i in range(3, c + 1):
        model = AnalyticalModel(i, LAM, MU, M)
        data['rho'].append(model.rho)
        data['q0'].append(model.q_0)
        data['p_refusal'].append(model.p_refusal)
        data['p_q'].append(model.p_q)
        data['Q'].append(model.Q)
        data['A'].append(model.A)
        data['k_occupied'].append(model.k_occupied)
        data['L_q'].append(model.L_q)
        data['L_s'].append(model.L_s)
        data['W_q'].append(model.W_q)
        data['W_s'].append(model.W_s)

    channels = [i for i in range(3, c + 1)]
    df = pd.DataFrame(data, index=channels).T
    df.columns = channels  # optional, same as above
    df_rounded = df.round(3)
    print(df_rounded)
    plot_scatter(df, 'A')
