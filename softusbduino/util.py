from uncertainties import ufloat


def u_analog(an):
    return ufloat((an, 1))


def an2v(an, vcc):
    if an is None:
        return
    return an / 1023.0 * vcc


def u_an2v(an, vcc):
    return an2v(u_analog(an), vcc)


def pwm2v(an, vcc):
    if an is None:
        return
    return an / 255.0 * vcc


def v2pwm(v, vcc):
    if v is None:
        return
    return int(v / vcc * 255 + 0.5)


def an2pwm(an):
    if an is None:
        return
    return int(an / 1023 * 255 + 0.5)
