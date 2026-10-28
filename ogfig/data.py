# -*- coding: utf-8 -*-
"""ogfig.data — petroleum-engineering data helpers (numpy only).

    q = arps(t, qi=52.0, Di=0.0031, b=0.8)
    fit = fit_arps(t, q_obs)          # {'qi','Di','b','R2','model'}
    Sw, krw, kro = corey(Sw, ...)
    fw = fractional_flow(Sw, kro, krw, mu_o=1.8, mu_w=0.42)
    d = pressure_derivative(t, dp)
"""
import numpy as np


# --------------------------------------------------------------------- decline
def arps(t, qi, Di, b=0.0):
    """Arps decline. b=0 exponential, b=1 harmonic, 0<b<1 hyperbolic. t in days, Di in 1/d."""
    t = np.asarray(t, dtype=float)
    if abs(b) < 1e-6:
        return qi * np.exp(-Di * t)
    return qi / np.power(1.0 + b * Di * t, 1.0 / b)


def fit_arps(t, q, b_grid=None):
    """Coarse grid fit: for each b, solve (qi, Di) by least squares on the log-linear form."""
    t = np.asarray(t, dtype=float)
    q = np.asarray(q, dtype=float)
    ok = (t > 0) & (q > 0)
    t, q = t[ok], q[ok]
    b_grid = b_grid if b_grid is not None else np.round(np.arange(0.0, 1.05, 0.05), 2)

    best = None
    for b in b_grid:
        # log q = log qi - (1/b) log(1 + b*Di*t): grid over Di, linear solve for qi
        for Di in np.logspace(-5, -1.5, 160):
            f = 1.0 / np.power(1.0 + b * Di * t, 1.0 / b) if b > 1e-6 else np.exp(-Di * t)
            denom = float(np.dot(f, f))
            if denom <= 0:
                continue
            qi = float(np.dot(q, f) / denom)
            pred = qi * f
            ss_res = float(np.sum((q - pred) ** 2))
            ss_tot = float(np.sum((q - q.mean()) ** 2))
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
            if best is None or r2 > best['R2']:
                best = dict(qi=qi, Di=Di, b=b, R2=r2)
    if best is None:
        return dict(qi=np.nan, Di=np.nan, b=np.nan, R2=0.0)
    best['model'] = ('exponential' if best['b'] < 1e-6 else
                     'harmonic' if abs(best['b'] - 1) < 1e-6 else 'hyperbolic')
    return best


# -------------------------------------------------------------------- rel perm
def corey(Sw, krw_end=0.65, kro_end=1.0, nw=3.0, no=2.0, Swr=0.20, Sor=0.25):
    """Water-oil relative permeability (Corey). Sw in [Swr, 1-Sor]."""
    Sw = np.asarray(Sw, dtype=float)
    Se = np.clip((Sw - Swr) / (1.0 - Swr - Sor), 0.0, 1.0)
    krw = krw_end * np.power(Se, nw)
    kro = kro_end * np.power(1.0 - Se, no)
    return Sw, krw, kro


def fractional_flow(kro, krw, mu_o=1.8, mu_w=0.42):
    """Buckley-Leverett fractional flow of water, dimensionless 0..1 (mu in mPa·s)."""
    kro = np.asarray(kro, dtype=float)
    krw = np.asarray(krw, dtype=float)
    return (krw / mu_w) / (krw / mu_w + kro / mu_o)


# ------------------------------------------------------------------- well test
def pressure_derivative(t, dp):
    """t·dp/dt in log space (the diagnostic curve for log-log well-test plots)."""
    t = np.asarray(t, dtype=float)
    dp = np.asarray(dp, dtype=float)
    d = np.zeros_like(dp)
    with np.errstate(divide='ignore', invalid='ignore'):
        d[1:-1] = t[1:-1] * (dp[2:] - dp[:-2]) / (t[2:] - t[:-2])
    d[0] = d[1]
    d[-1] = d[-2]
    return d


# -------------------------------------------------------------------- helpers
def water_cut(qw, qo):
    qw = np.asarray(qw, dtype=float)
    qo = np.asarray(qo, dtype=float)
    return 100.0 * qw / (qw + qo)


def cumulative(q, t):
    """Trapezoidal cumulative production (same units as q x time)."""
    return np.concatenate([[0.0], np.cumsum(0.5 * (q[1:] + q[:-1]) * np.diff(t))])
