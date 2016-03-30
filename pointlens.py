#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants as const
from astropy import units as u

def rad2mas (rad):
	"""
	Convertitore da radianti a milliarcosecondi.
	"""
	mas = rad*(180./np.pi)*3600.*1000.
	return (mas)


def einstein_rad (M, D_l, D_s):
	"""
	Calcola il raggio di Einstein in radianti
	Si assume che D_s = D_l + D_ls
	M va in masse solari, le distanze in parsec.
	"""
	G = const.G.value
	c = const.c.value
	mass = M*const.M_sun.value
	D_ls = D_s - D_l
	dist = D_ls/(D_s*D_l*const.pc.value)

	theta = np.sqrt(4.*G*mass*dist/c**2)

	return (theta)


def image_pos (y):
	"""
	Dà la distanza dell'immagine (x_i) e 
	della controimmagine (x_c) rispetto alla
	lente, disposte lungo una retta che collega
	lente e sorgente. L'output è la lista x
	che contiene x_i e x_c.
	"""
	x_i = 0.5*(y + np.sqrt(y**2 + 4.))
	x_c = 0.5*(y - np.sqrt(y**2 + 4.))
	x = [x_i, x_c]
	return (x)


def magnification (y):
	"""
	Calcola l'amplificazione di immagine (m_i)
	e controimmagine (m_c) che si formano
	con un evento di microlensing. L'output
	è la lista mu che contiene m_i e m_c.
	"""
	m_i = 0.5*(1. + (y**2 + 2.)/(y*np.sqrt(y**2+4.)))
	m_c = 0.5*(1. - (y**2 + 2.)/(y*np.sqrt(y**2+4.)))
	mu = [m_i, m_c]
	return (mu)

M = 1.
D_l = 4.e3
D_s = 8.e3
beta = 1.e-1*u.mas

theta_E = einstein_rad(M, D_l, D_s)*u.rad
y = beta.to(u.rad)/theta_E

x = image_pos(y)
mu = magnification(y)
theta = x*theta_E.to(u.mas)

print
print "The Einstein radius is %s" %theta_E.to(u.mas)
print
print "The image is at %s from the lens" %theta[0]
print "The counterimage is at %s from the lens" %theta[1]
print
print "The image is amplificated of %s" %mu[0]
print "The counterimage is amplificated of %s" %mu[1]
print "The total amplification is %s" %sum(np.absolute(mu))
print
