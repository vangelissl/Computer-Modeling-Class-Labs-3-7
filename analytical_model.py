STATES_NUM = 21


def r(lam, mu):
    return lam / mu


def mu_general(c, mu):
    return c * mu


def rho(gen_mu, lam):
    return lam / gen_mu


def q_0(c, r, rho, m):
    q0 = 0

    for i in range(c):
        q0 += r**i / factorial(i)

    q0 += (r**c / factorial(c)) * (1 - rho**(m+1)) / (1 - rho)

    return 1 / q0


def p_q(c, r, rho, m, q0):
    return (r**c / factorial(c)) * (1 - rho**m * q0) / (1 - rho)


def p_refusal(c, r, m, rho, q_0):
    return (r**c * rho**m * q_0) / factorial(c)


def Q(p_refusal):
    return 1 - p_refusal


def A(lam, p_refusal):
    return lam * (1 - p_refusal)


def k_occupied(A, mu):
    return A / mu


def factorial(n):
    fact = 1
    for i in range(1, n + 1):
        fact *= i

    return fact


def L_q(c, r, rho, m, q_0):
    return (r**c / factorial(c)) * rho * ((1 - rho**m - m*rho**m*(1 - rho))/(1 - rho)**2) * q_0


def L_s(L_q, k_occupied):
    return L_q + k_occupied


def W_q(L_q, lam):
    return L_q / lam


def W_s(W_q, mu):
    return W_q + 1 / mu


if __name__ == '__main__':
    number = 3
    print(factorial(3))
