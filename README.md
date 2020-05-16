# tsa: The Thalesians' Time Series Analysis library (TSA)

## Installation

    pip install thalesians.tsa
    
## Caveat

Please note that this is a very young library and the interfaces are in flux and may change on short notice. We hope that they will become much more rigid as time progresses.

## Please help us develop and grow thalesians.tsa!

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=H8EVMMSLPVXFN)

This library is based on the efforts of our staff, members, and volunteers. We are keen to make it serve you and your organisation, increase its scope and improve its quality user-friendliness. This takes a lot of effort. We couldn't do this without you, so we are asking for your help. Please consider making a donation. We will use this money to fund the development of this library. Thank you very much in advance on behalf of all the users and developers. To provide ongoing or organisational support, please contact us on info@thalesians.com.

## Dedication

Dedicated to the memory of some of the outstanding mathematicians, on some of whose work this library is based:
* Mark H. A. Davis (1945 - 2020)
* Leonhard Euler (1707 – 1783)
* Kiyosi Itô (1915 – 2008)
* Rudolf Emil Kálmán (1930 – 2016)
* Andrey Kolmogorov (1903 - 1987)
* Andrey Markov (1856 – 1922)
* Gisiro Maruyama (1916 – 1986)
* Norbert Wiener (1894 – 1964)

## Overview

The Thalesians time series library is a heterogeneous collection of tools for facilitating efficient

* data analysis and, more broadly,
* data science; and
* machine learning.

The originating developes' primary applications are

* quantitative finance and economics;
* electronic trading, especially,
* algorithmic trading, especially,
* algorithmic market making;
* high-frequency finance;
* financial alpha generation;
* client analysis;
* risk analysis;
* financial strategy backtesting.

However, since data science and machine learning are universal, it is hoped that this code will be useful in other areas. Therefore we are
looking for contributors with the above backgrounds as well as

* computer science,
* engineering, especially mechanical, electrical, electronic, marine, aeronautical, and aerospace,
* science, especially biochemistry and genetics, and
* medicine.

## Scope

Currently, the following functionality is implemented and is being expanded:

* stochastic filtering, including Kalman and particle filtering approaches,
* stochastic processes, including mean-reverting (Ornstein-Uhlenbeck) processes,
* Gauss-Markov processes,
* stochastic simulation, including Euler-Maruyama scheme,
* interprocess communication via "pypes",
* online statistics,
* visualisation, including interactive visualisation for Jupyter,
* pre-, post-condition, and invariant checking,
* utilities for dealing with Pandas dataframes, especially large ones,
* native Python, NumPy, and Pandas type conversions,
* interoperability with kdb+/q.

## Teaching

The library is utilised as part of the

* M5MF48/M5MR2 Data Analysis and Machine Learning course, as taught as part of the MSc in Mathematics and Finance programme in the
Department of Mathematics of Imperial College London.
