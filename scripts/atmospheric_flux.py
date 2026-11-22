"""Conventional atmospheric muon-neutrino flux for the ACME School.

Reference
---------
Y. Wang and O. Yasuda, "Search for sterile neutrinos by shower events at a
future neutrino telescope", Progress of Theoretical and Experimental Physics
2022, 023B04 (2022), Sec. 4.1.1, Eq. (54).
https://doi.org/10.1093/ptep/ptac010

This is an empirical approximation to the atmospheric flux at the Earth's
surface, before neutrino propagation through the Earth. It includes the
conventional pion/kaon contribution, but not prompt neutrinos, Earth
absorption, or neutrino oscillations. It is intended for teaching, not
precision flux predictions, especially above ~10 TeV.
"""

from math import sqrt


def atmospheric_numu_flux(energy, cos_theta, pdg):
    """Return the atmospheric nu_mu or anti-nu_mu differential flux.

    Parameters
    ----------
    energy : float
        Neutrino energy in GeV (strictly positive).
    cos_theta : float
        Cosine of the neutrino zenith angle, between -1 and 1.
        Only its absolute value enters the atmospheric production model;
        this function does not model propagation through the Earth.
    pdg : int
        14 for nu_mu or -14 for anti-nu_mu.

    Returns
    -------
    float
        Differential flux in GeV^-1 m^-2 s^-1 sr^-1.
    """
    if energy <= 0:
        raise ValueError("energy must be positive (GeV)")
    if not -1.0 <= cos_theta <= 1.0:
        raise ValueError("cos_theta must be between -1 and 1")
    if pdg not in (14, -14):
        raise ValueError("pdg must be 14 (nu_mu) or -14 (anti-nu_mu)")

    # Eq. (54): spectral indices fitted separately for nu_mu and anti-nu_mu.
    gamma = 2.680 if pdg == 14 else 2.696
    normalization = 0.646

    # Effective zenith cosine accounting for atmospheric curvature.
    # The published expression is for a positive local zenith cosine.
    c = abs(cos_theta)
    p1, p2, p3, p4, p5 = 0.102573, -0.068287, 0.958633, 0.0407253, 0.817285
    cos_theta_star = sqrt(
        (c * c + p1 * p1 + p2 * c**p3 + p4 * c**p5)
        / (1.0 + p1 * p1 + p2 + p4)
    )

    pion_term = 1.0 / (1.0 + 6.0 * energy * cos_theta_star / 121.0)
    kaon_term = 0.213 / (1.0 + 1.44 * energy * cos_theta_star / 897.0)

    # Eq. (54) gives cm^-2; multiply by 10^4 to obtain m^-2.
    return 1.0e4 * 2.85e-2 * normalization * energy**(-gamma) * (
        pion_term + kaon_term
    )
