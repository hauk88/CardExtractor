import numpy as np
from sklearn.linear_model import HuberRegressor

def fit_common_polynomial_normal(p_1, p_2):
    fitter = lambda points: np.polyfit([p[0] for p in points], [p[1] for p in points], 1)

    return fit_common_polynomial(p_1,p_2,fitter)

def fit_common_polynomial_outliers(p_1, p_2):
    return fit_common_polynomial(p_1,p_2,fit_polynomial_outliers_iterative)


def fit_common_polynomial(p_1, p_2, fitter):
    coef_1 = fitter(p_1)
    coef_2 = fitter(p_2)

    common_slope = (coef_1[0] + coef_2[0])/2

    coef_1[0] = common_slope
    coef_2[0] = common_slope

    return (coef_1, coef_2)


def fit_polynomial_outliers_iterative(points):
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])

    while True:
        coef, residuals, rank, singular_values, rcond = np.polyfit(x, y, 1, full=True)
        if residuals < 10:
            break
        a = coef[0]
        b = coef[1]

        point_errors = []
        for i in range(len(x)):
            x0 = x[i]
            y0 = y[i]
            d = np.abs(b+a*x0-y0)/np.sqrt(1+a**2)
            point_errors.append(d)
        idx = np.array(point_errors).argmax()
        x = np.delete(x,idx)
        y = np.delete(y,idx)

    return coef

def fit_polynomial_outliers_hubber(points):
    x = np.array([[p[0] for p in points]]).T
    y = np.array([p[1] for p in points])

    d = np.linalg.norm(y - np.ones(y.shape)*y[0])

    # fit model
    model = HuberRegressor(epsilon=1.0)
    model.fit(x, y)

    # do some predictions
    # tx = np.array([min(x), max(x)])
    # ty = model.predict(tx)

    # # compute coeffs
    # a = (ty[1] - ty[0])/(tx[1]-tx[0])
    # # y0 = ax0 + b 
    # b = ty[0] - a*tx[0]

    return np.array([model.coef_[0],model.intercept_])