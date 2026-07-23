import base64
import math
import datetime
import pandas as pd
import streamlit as st

# Seiten-Konfiguration
st.set_page_config(
    page_title="Sport-Tagebuch", page_icon="🏃‍♀️", layout="centered"
)

# --- Eigenes Icon für "Beweglichkeit" (Original-Bild des Nutzers) ---
BEWEGLICHKEIT_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAFAAAABOCAAAAACSps6aAAAHNklEQVRYw6WYf4xUVxXHv99z3/zYnVnIUooJBLWV"
    "GIpQKOVXg4gN/qLRWjHgH1bRSmtVSmVpAKXVglIIpSQtNgSsP0o0QqKm2gZrUCiy29YlaYmJrQUrrW2T0loXurM/"
    "37vn+Mfsws6bNzOPdTbZZO677zPfc8+595x7aDDQzND4o5m3n7lsAZXVj0gaaDQEAOijNEAt/OmLb+HG/XmfRHQB"
    "rfxnjEKADXnm3p13RiS6Z0spSHgKydJooRh9SDbmwWf3ngnU0A5JMIfUEEDoBYiAxgab5l/fDQ9gEjRxBr2negpV"
    "2dhgowa7zzqDxyok2mOAwgOSQh0AaPPpPfBw+MLiHkkUCBgMkFQ4o8qubgf4zPo6s4C0QPriyZ/Bw2Hl7JKrOzUV"
    "0MywY8ABvrhOxfh/A6nFjl/Bw+G2qb0N3kgDNAO2Q0A//s6ogcBUQGrhj09QIbjjvf0CmPfeakVHkAJoottAo5/8"
    "jVCAKNNkHAgdErWmAWrh98dEQWu7vBSoFM+fPDduaktfsntSAM1wAgT1qlsGnAbRD/e9BlyxerX5JGIKIIGJAMRf"
    "OaaHQe+yowTtlXVPHXBJmzqVUzAXHorn/pPR7J1Hs4CBmcc35JKAND/Y6Ggw6b/mDA1oX4inF8owJnvi6oqgNMkN"
    "eqYK7GjsLAgcOoEnLpxMbvBJaHXspNt6uA4A8AxwasTwS0lz0209zIeH4vnzGHkyBKMFUsKp7wENL5/G9BHjVyel"
    "onTH1+CEGSCcPY/P5IZyHv3YG3zC2+lMNlwHAujEzLVwjqBz2HhF32iBRsyHQvGXLm6+JVKDabR2Q6+zUQJJP32M"
    "0Xhq3q+DRw4sas1dtuTxXf2JySpNYMNgTYuPlyP6U9tnhm/2jp3APrJyK19CYAPu/FkYAJEnF9z17uQPtPb1xHmX"
    "YLLR53afcgZA1Q0+MPsXDMwl89LtZcufmXPuolq16++/tsfFgalNNqpsPXdxi3jK0bkPFSImJoE0Cn3h+OLKl53a"
    "oaWlYHROMaPea5XzPHH7G3nlaOLQ6JsPHJHYWaru398KEqvUFAoz57dU50zvfrczcRkbAY1R7uGXYnuMBDy+29GS"
    "QGzkFLPcq3O6Yu8RMIhe1V4cWUikcopR3X1dlQIdvr3cHNS92JbVS1boCx2LYvLs8hcGr32TBud/vKo7c0FiGoVm"
    "tM2xkBGsHz9xT7kEbvtbi48tR12g0TcfPFwZMvTTvt7bddO9EJh039obi+4GXrZMdzxkiI0tmdbSh/IKaNB5X86n"
    "V2j0uYdfrPSI6Ce+1Pf0munL+wHA47d9sdxXzylmudfmvBMPtT3nf/4PoDwaRDNO2LDNZafUKZaM3m17x/nK0aCt"
    "DxQ1gGKKm3Oxi1pthUZfeHZhQj3kTIf/T1qzNkJl2NRXuEmlmugBofcYv3TFR8b0xXN9UBsXtvzoiPMAyAqq0CsK"
    "S1Z8fIKFpapMUNtkzb88v7yJacKKlcwuWP7p9yMcgKMhtpdrKTSYrO9yHqDNLHSMUJmftXTZNPE9Jg4JxU0Nhcao"
    "uH9leQEzHXN/8+BxlL/Qxh2eHYYq1Vm07l6m5t/4DgyAw4a5pc8fPbJIXfmX/rvkUMY7SWwCSC2Fxqj4lUedB0Rn"
    "tTtVaQ5X73NaXtFgz6oeVt8AzGVtwBIVGqPiY4+KB2DYWYgkYCnau9VDABj11rsL4pMyFDPJCs2C0vx/0gDn73io"
    "FBiNaoVffm1AFADF3/yIDMYzvbms0ScBjVFxze6yh6c82xKRgNGilmMr3irvxCD66MFxgzHrzGUtcQ2NUfHIkvIi"
    "62OfHcrnRoQtp5b9PYjKxHmHc1qtEIlraEHPOggApyuHeaBZpjTl2MeiAACiTOf+nE94V6qBxii//aRTgH7i1kiG"
    "w4O0oLfl0FcjAoDiuYTuDHFaqnm+pXMHPABi26T+EV0fWhBGP908NJCkD+FTCQolXDdYNvimL1cWbTRn3d+7HbXb"
    "GMzEgcao6cH2ssGt92usiUUTYDxwCUD64gtb4AEINk/pibe5aEQ4vF5J7vxcPJYMvKvbARC/5JtVORLgBVLioWdN"
    "lUCjL+z7g/MAtGmnS66i6/W2aLEMo02v3A0F4PymWSPKjHRAY29lW8fM3Ma3nQHi563rC+q2aBKPlf5DFVdy+sLB"
    "g+IBqHsgrzVwtRVSx1V4mZo/u2HoVG37cMnV7yElP1xYodCCe14tGzxt00BNXh2n0CbLiF/Swl9/gqFTdWzY6LLB"
    "pBFCQBnuYxk61AFwdlvVJaRaIatGBQDEGFx82AQC4t/3g1Bq92VbIQDRGrdWBAAF5oYvHKKfbI2CANgxYaBmmSe4"
    "IRcGQcQbK5u7xgyNgBCWydDMzNh75d7myOv3V5Sc1fqwdM3uIIq4a2GPjBx3ObFyqoCBNlTNa/b1w32LZgzWL5Qz"
    "//qzXv/BCq+RUi5KjAbY8CIalTRYjbv10OJTSVh8kqGs73+z/aglbdXMJwAAAABJRU5ErkJggg=="
)


def beweglichkeit_icon_html(size_px):
  """Gibt das eigene Beweglichkeit-Icon (Originalbild) als img-Tag zurück."""
  return (
      f"<img src='data:image/png;base64,{BEWEGLICHKEIT_ICON_B64}' "
      f"style='height:{size_px}px; width:{size_px}px; object-fit:contain; "
      f"vertical-align:middle;' />"
  )

# --- Eigenes Icon für "Balance" (vom Nutzer bereitgestelltes Bild) ---
BALANCE_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAAAOusbgAAAAYFBMVEX///////7//v7+///+/v79/v7+/f7+/f3+"
    "/fz9/f79/f39/fz8/fz8/Pz8/Pv7+/v49/Xv7unj4dbSzrvcwZjbwJfKwabUuo+nsqGhrpmhrZifq5ilpId4iXRm"
    "emNdcVkQ+o+2AAAQDElEQVR42qVbi7arqLJl74WpEw0qYKLGR/7/L09VAQqKWfvca4/uTmLipF6zHrBESVdRptf+"
    "/r69uqXfoLeAXwT8hy6ZPgHcb8H/UB4fLEV4cyvPF2TXsq0DIPoapL+ie+AAIfxWhv/hi5so8xf9TqI0UPB/IfMV"
    "GT5M7/p3+MN00TK+D2WQGE7AQYdF5q7cPynco2S5SyWT1dwj8Eg3FxLjk0HmNJ79SB4+lOFdcfzy/lJc4GZElwdT"
    "0so2EQBy69vunj++AobI1llhnDgS8hK5B4S7AMcvQAR8z2lTHtV1y6k8VkMSXTLorEh9HzZgqNJ4KfwvIVL6Pa+z"
    "k2p9OEEUhHCK81jV+UiOguImY2i4cA0IS4dj9EMKnN4/OM+v4l0Q3ol94GhPca0+yLzOayUPD3F4HCgIQFxoTt52"
    "sktXgK5aKbrobaWqqtq0XETWAe/PUuZiOfJqeYQuzg6Bl2oaVQq+/uJ3+IUs67qKpXMLcWtJcD2Df2GuhEW2WFWN"
    "YqRWG2N0i4CtxqtldFRBHFxFzgv5SYUHLjIMn41URm3NMC3LNFgEBgI2tnv2ndWNED8kdwl5py+8KMFnU2C4XfwE"
    "YVHB2s7rugxGew2X9x9WgLF933cGJXeWzy2+2JMeu7e4jo6Y5+pSSDOtn+XFoCVa2jlXVasS0aW2/dxbvKkq+Eou"
    "nl82G0MRsvaRQPBTpYS082edDII+PCaw5/Pya1yXaAxCdwhdX0bmHngQFQJIclBkgxTNZxB20CSqCtqvhbGi2by9"
    "lqgTkroVLsAOauNcFvhaQq4COQRRVQs9rh+StmmizxsxTA7YPxzFrgjaHIUutsdeFAKQ0XWpbsIun8UirIq9sGjE"
    "tAiVLBehW7R118bIm349U9y27FR84+JaNMO6Tjrjr49lbaVKGRgV7oRWXwkfDhLHlWDQp0brkrjhC7ftjvl8IiNv"
    "0KJ9EnL1S+4Up7wdqRsQF9VsgpZlbGG9LMuKtx4ytU+NEdD3VlzmsBubXRxqCNg8nHEN4uqTWFIB3TF6JWUcwgfX"
    "SOq2osrV+TLYWZwjd4u6mp4+txtusSuiGT4oLd0f3f29KKu1rB2yyjASnGx84hupSM8RbuRw2ilCBUtsZTpGn9Ba"
    "EDJqW8FlsfIlOynZ4lNbEWhqYxc0wMq4j0cj2ol8r4mkqoTxyMZbAU7KLIBVvYkP92hxSky7fTdyJ0XYlRZEWaNs"
    "/pYTObdKNGJb1DZ6GAZhnv6LWOKDPhrxWp0WD4pgeRFXkE5RpmYOYeUrK0VcqmrRzX0rq6zrohTioITwmp4fdHhY"
    "0kJ+RQG+8sqEpoXIqBwDibmihgY5bFfFXny4V6LIC1w1y2fY9Zws6IMcDXh/JVNL5OwgMhCJSYqGrkJl637OEgn4"
    "fAxwrh1r8UIxSpWuSdW1Iywkaou4iPwSjTxQGJQ/LZEmmpmUnSnkKJpFNjEpqZc1SOHLIVX95cJDs8QBGLVCEnsH"
    "Dkv86bpaYpVA0VxD3ElwlYrAUhx7BnCeO+DT60gI5Cqq8azVanHc4YCRGimWU8EomHApGObo2VKd3Vq6uhpynrvq"
    "KEawoi2NHaZptiTrZymlt3FbYtRt3hABk8gKPTuE2pEgRS4pksDDxkf0XmBxOU0jVgOqaBdSttDTus4YUEie6yaW"
    "0ymK+qQgrljkvyrfO+Vwkf31jwqtBL5/Ieo4Tpbilsz7mVpSvWDSJg9LqmMGJlGRbMjKZZYy5cnZa7bwrmhh3gj7"
    "HqeBEz9RGtebJdaWC71sDkUCSvp8du1PyVZuZZmp1kWmUUH7rY75Ha5Fcd9BYHZ5cqvPivn4Qy5m0kqHJe47V4b8"
    "PGdzFhnOqr6xa3wWtS0ScUd/sbkAtljaIursnP2TawF8FtJXlanAMjamwNyspgj3/WZNv4SvH5ScGZNxT4r2wKhr"
    "ZGrkkr6NiPObczlNu2yIjyBcukjTPkVyuAVgl0gAYg7C1PRkv+aIOuoayGdFmQvi5bH5N0bRhKgRsE+ZQWDyt4Ob"
    "iLZ7IjASNRUjeb8W9+MIgyy4ma0ZpvfEmn4H3wolpgdmYr0ffIs0TUaunF+nIzJXzIpTZNdi/HgINrAT2Dm1CgNG"
    "R1x06YwBZUfAT0xR+LpyBUEYhYSq9qxqkEt4mmxH1rTz6WmQSXniNC0ymY0FdpF8NHJon7YZSORu7bK0THNeYFY1"
    "XW/95xGadGbKlRPVufvonu7SqOv6QF5+/ugl3ufX7FuzF5gs7AzM0ImRL4HJwg6512zkvHeJI30TfYz8NBdKXti3"
    "ExmfAN+B6w03xJOen6c6BCJV+2S9O7WKOIthiaxFUzmx5ryNmabd5UizEkghP9z5F7eUq4+8ZX0hg5lnk3hDpuZc"
    "ebqOvbrwlYswiEio3TOwNQKr47CrOKsay1oHTOTxfr/fES4ij1aDkEHTIY63cqG2DneT+IY9Td83p6E7iBxT48Og"
    "2NgywPqgGofB+CzhjKzKuqprbOBFZTCAuy4gk43vSO7I1j/Vid2ODZsHDulhinDdIiZ0brtR9bo0kmdOomwZlmV1"
    "YjvikGW/15pfkkSkauvpctw8+000ouX42YFXbTqDl+0CrIf2cVzekboaKmfS0cO1c1XixVH8HuOIml7SLDEuAmPu"
    "xWsTdMNm5mIb13Ln83w+BgZ22RiBnY2JNj0+q9nhfnbgjpyYcbsdHD9UPEds+l5eVSDJjMG4OK48MCrXYmXrwskG"
    "d/58Ju1e6kAYBM8Xv0HNc4NMcfwU6jTREsc9DWSelWt55YBRuVhQNvSacH1uoHbcrWFpbO9FJEwn/M4fzFxdoExI"
    "bZyM7am2nWURvBq1iz0ytoQsuiC3wlJrpjmQtFzSi92jukjk4FtfuFqm02KpMDuJjTGppnX5AgXm9L8QfVH7xsDj"
    "n92hun5ell3xtXQa5LQIiXvt2z9xdpmo5JJMIGOQGDMz9hEOeBpoalhzFfKxbb/78UK3HXLnJxGUj/WljWOHC4Gs"
    "EIwJ44XNv0IbUyUwoKLxolFfU3LFZ7Zk9Oxm9ru5C5qmQcRdumg6zJXg2EkAu/XIi5WDbyC8V9Ma9GumMv6zWMml"
    "5tLaLDD6NJsQl9934jw+h0x5SyVII7eSenJx7Ksfq2VrhmX5fOYXAn9mEZuYgXsH7PSrvIlPW88i17NNH44Eoccx"
    "yU/4dqLtiBq7OIQeUPbhP8+IrPplWbymLfi6gExcnYAh20nYhELGBJrkH19o4unzWti3Yprses8fz1Av1glvhd30"
    "LHCka1f7uEbinciN/cOCEu+8tUE70f0oc4/i425cvj8efX6X5MwB19ddjr7HVgwjZosjsE8VnZ9kYzBh61SlPn2/"
    "b84lk2aO/HoSD+qcNHN0nBwZGfOl/oM+9llb0z8zwKhodyJh92k4Mhdkti/l7Jreh2MvVw5sBSdW2hMGcksz5Sia"
    "duJ0LA0lF9U60x4HApEHYHIvPxLggs8V17vECDy0QAOLPUXEvm3dJPFOruVLW0jlyzsXfYFExqT2EC2zSKrqiXpl"
    "btyWYgcOObm39V5jH+myuCxvPW2azywdAegxra5JYBr/NJVeUC/d85CcENePTgEFTlhLbmdl8hInjo3IzJdb8xac"
    "Wt0pov7EuFgCBVxEuNHouJUquxdypWqaKS5uelU75Jd9jYzN/74E7baYu2l3PWOtZ8zTCOmjp5I00qzh6y5Mpte0"
    "vi/C/NhYYowStB0nlzfMH3zqjCys+y6YF5n0LvU+o1SCap7s8wuJwEVe5q2+5sZED61dMA039s35scWkM1saC1M4"
    "obRWC22nWe0mpe4NFQ1l5ghUoMzs+F6peQ0TehRa0ghvsT/ta+J+leZXCG5qrrO0oE3e1Q1TyYUKmkEkHg1plhCH"
    "4US6GUJ7ITzNVqiA1Vjec2G9W0p21Ai22B3amvZERjO5vRNy3v9gVWtCU3va4rz2al/2UbJQoaVa8amW5vZmaNC0"
    "+NSaK0hrhVl4k3cImza0ofU8lXjwSyGwOR5t483Cjelpb0Qjn6gBA7wtni5OmBJb9MOF5qnltDShHxXdubQ8Tm+3"
    "7eRjQ4fdaLtMgoVAFiWLNyWV3XcdKlZOApi+sZlWDzGHNl2SGtRe2cF5y1583fREJ51mVh/V+dS98naX3oiBOOLP"
    "NImypkZ+8YMJWRsKYLg+RBNsfHnqBnvtYdYNXuhqbkKByG2gfpo8zNrgKu48tcGl8aWTlARwOORHLpYZG8u4mW3+"
    "irZxJ10Gv/NQi6YPBqTOyG/xkPu5cxp0nfe5D+n3u6rRWK2xrwELXIzUQCiOCkPfgUmQaVGypo0dBjqdIi7P5EE6"
    "YLuI83ZaVp6IY7mMTnt/uJrM78UDndboeYeHd6I0TwoW6qgWk80OW52TAY77KCWnz2R0Sxs/s9ErNc4FpfddYv+a"
    "5kDDA5sb/HJLCwgbmnC1VX95WqTAfzx7uZ2ulshLNEQOkY0dMT4UxlLbuHNPMkwzzo+FPDCc3F5R3SdrRQebJMq/"
    "Us9EMST2TEAbTIoXpW6NUpWrFdX5lJkstkOPR4nhZGZq4QZRsdp4y8ltlPf6j3I7TCQ8uv3gh/qSA32J0lLWhvtO"
    "W5E59AL75pfPj38bamGR0bon6Ro49ZW0bx4SmaIDDYsW6uu5UCnPhxPifWA+ZsL7jK2olcvMrxWTsa8tKln19kcI"
    "u8x+ax1lt2vmHMUp9cLV/nF8vIKeha24qis3aFxszT5VS9F1AjPx4k6oKGKbkc4z1F/JoUgIJD27Jg8TaKwniZXq"
    "RtFRJ6wEsINAZNs1ZphsQ2et6IAblinr629G3lySgOyZpkP/WOITJ8PcSdDaGtVaY43Af6UoG8k7y9jF4frKi7py"
    "91zgNrWQv54MpgeTMMtkTeuDGvOAbpU/RScajZ2UG8s0OcvK+ECEdGcE/uG8qfMaYV7TQp03NufDy2iFPkbUjBU3"
    "fYy14OWhvTBFj5bzLUnAPRwuBH9aUJR0MNIYOpMo8DkynJU07owk7/ZB1lkhOQ8Lx82Q8I3N14vovL9qaumznvSS"
    "qXA6lGzfVLev8RFhk40hta386maIpGqlHgnFqNqfHzwft86f9czmY4DiH4LhcKJhQ7uV/3qJ40L5PEz2MCpcLAGS"
    "5fBvb78vXmSCSMpfTPQvF/xysDao+p4JZTg5Xv5JkCegoMfidPhRxgM2yKewEyxZ8Q6/K8M9IlPiFuzU1KbGabI4"
    "BWEmeUF6uBCy9VyutIhqglLkSs9kWHG4FfstFOeiJo4i2P8A51RtivTAwv614n5aMhRw6UbxH+T8AwnL4wk2gLK8"
    "Dvov7lt8/9Ue5bB7dbR5DNfF14ky5P8n4qT/c4UiVaY8efThr7hk+T9ekB+URxwImU4Hyv8z4LUWxNmTC/5rJxeJ"
    "EJEJ5F17v+5HX4PznAMOmyHgo4P+2mc/Zh9VK6X89vdWt6vKHOK+P+FG4bJjVpcZKgzld/E/KFVmqwKx7cfsNpb+"
    "nDvr2ivdF2vgD/5vf0HlDq/CUcYbAOTGWDvj/Be0SrNf6lnyigAAAABJRU5ErkJggg=="
)


def balance_icon_html(size_px):
  """Gibt das eigene Balance-Icon (Originalbild) als img-Tag zurück."""
  return (
      f"<img src='data:image/png;base64,{BALANCE_ICON_B64}' "
      f"style='height:{size_px}px; width:{size_px}px; object-fit:contain; "
      f"vertical-align:middle;' />"
  )


def get_status_color(minutes, goal):
  """Liefert die Statusfarbe passend zur bisherigen Ampel-Logik
  (grau = nichts, rot = wenig, gelb = mittel, grün = Ziel erreicht),
  aber verhältnisbasiert, damit sie zum Ring-Füllstand passt."""
  if minutes <= 0:
    return "#c9c9c9"
  ratio = minutes / goal if goal else 0
  if ratio >= 1:
    return "#2e7d46"
  elif ratio >= 0.66:
    return "#e3a008"
  else:
    return "#d9534f"


def render_progress_ring_svg(minutes, goal, size=40, stroke_width=5):
  """Baut ein Ring-Fortschrittsdiagramm (Donut) als SVG: Füllstand
  proportional zu minutes/goal, Minutenzahl in der Mitte."""
  ratio = 0 if not goal else min(minutes / goal, 1.0)
  color = get_status_color(minutes, goal)
  radius = (size - stroke_width) / 2
  circumference = 2 * math.pi * radius
  offset = circumference * (1 - ratio)
  center = size / 2
  font_size = max(13, round(size * 0.5))
  return (
      f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}'"
      f" style='display:block;'>"
      f"<circle cx='{center}' cy='{center}' r='{radius}' fill='none'"
      f" stroke='#e9e9e9' stroke-width='{stroke_width}' />"
      f"<circle cx='{center}' cy='{center}' r='{radius}' fill='none'"
      f" stroke='{color}' stroke-width='{stroke_width}'"
      f" stroke-linecap='round'"
      f" stroke-dasharray='{circumference:.2f}'"
      f" stroke-dashoffset='{offset:.2f}'"
      f" transform='rotate(-90 {center} {center})' />"
      f"<text x='{center}' y='{center + font_size * 0.36:.1f}'"
      f" text-anchor='middle' font-size='{font_size}' font-weight='700'"
      f" fill='#333'>{int(minutes)}</text>"
      f"</svg>"
  )


def render_icon_box(
    icon_html, minutes, goal, box_height=88, icon_font_size=20, ring_size=42,
    click_key=None, kat_name=None, label_font_size=12, icon_row_height=None,
):
  """Rendert eines der 6 Status-Kästchen (Woche/Heute) mit Icon, der
  Kategorie-Beschriftung (gleiche Optik wie im Übungsarsenal) und einem
  Fortschrittsring (samt Minutenzahl) darunter. Feste Höhe/Breite, damit
  alle 6 Boxen garantiert gleich groß sind. Die Icon-Zeile bekommt eine
  feste Höhe (icon_row_height), damit unterschiedlich große Icons (z.B.
  das größere Beweglichkeit-Bild) Beschriftung und Ring nicht
  verschieben - Text und Ring stehen dadurch bei allen Kategorien auf
  gleicher Höhe. Wenn click_key gesetzt ist, erscheint darunter ein
  kleiner Button, der die Detailliste dieser Kategorie
  (click_key = (scope, kategorie)) öffnet."""
  ring_svg = render_progress_ring_svg(minutes, goal, size=ring_size)
  if icon_row_height is None:
    icon_row_height = icon_font_size + 12
  label_html = (
      f"<span class='icon-box-label' style='font-size: {label_font_size}px;"
      f" font-weight: 800; color: #1f4a34; letter-spacing: 0.2px;"
      f" line-height: 1.15;'>{kat_name}</span>"
      if kat_name
      else ""
  )
  st.markdown(
      f"<div class='icon-box' style='text-align: center; background: white;"
      f" padding: 6px; border-radius: 8px 8px 0 0; border: 1px solid"
      f" #d0edd2; border-bottom: none; width: 100%; height: {box_height}px;"
      f" box-sizing: border-box; display: flex; flex-direction: column;"
      f" align-items: center; justify-content: center; gap: 3px;"
      f" overflow: hidden;'>"
      f"{label_html}"
      f"<span class='icon-box-symbol' style='height: {icon_row_height}px;"
      f" display: flex; align-items: center; justify-content: center;"
      f" font-size: {icon_font_size}px; line-height: 1;'>{icon_html}</span>"
      f"{ring_svg}"
      f"</div>",
      unsafe_allow_html=True,
  )
  if click_key is not None:
    scope, kat_name = click_key
    ist_aktiv = st.session_state.get("detail_ansicht") == click_key
    if st.button(
        "✕" if ist_aktiv else "🔍",
        key=f"detailbtn_{scope}_{kat_name}",
        use_container_width=True,
    ):
      st.session_state["detail_ansicht"] = None if ist_aktiv else click_key
      st.rerun()


def render_arsenal_tile(
    icon_html, kat_name, anzahl, box_height=88,
    state_key="arsenal_detail_kat", button_prefix="arsenaltile",
):
  """Klickbare Kategorie-Kachel - gleiche Optik/Logik wie die Kacheln oben
  im Tagebuch, damit es einheitlich aussieht. Wird sowohl fürs
  Übungsarsenal als auch für die Kategorie-Übersicht bei "Eigene
  Übungen" verwendet; state_key/button_prefix sorgen dabei für
  eindeutige Widget-Keys je Bereich."""
  st.markdown(
      f"<div class='icon-box' style='text-align:center; background:white;"
      f" padding:6px; border-radius:8px 8px 0 0; border:1px solid #d0edd2;"
      f" border-bottom:none; width:100%; height:{box_height}px;"
      f" box-sizing:border-box; display:flex; flex-direction:column;"
      f" align-items:center; justify-content:center; gap:2px;'>"
      f"<span class='icon-box-label' style='font-size:12px; font-weight:800;"
      f" color:#1f4a34; letter-spacing:0.2px;"
      f" line-height:1.15;'>{kat_name}</span>"
      f"<span style='height:38px; display:flex; align-items:center;"
      f" justify-content:center; font-size:26px; line-height:1;'>"
      f"{icon_html}</span>"
      f"<span style='font-size:11px; color:#777;'>({anzahl})</span>"
      f"</div>",
      unsafe_allow_html=True,
  )
  ist_aktiv = st.session_state.get(state_key) == kat_name
  if st.button(
      "✕" if ist_aktiv else "🔍",
      key=f"{button_prefix}_{kat_name}",
      use_container_width=True,
  ):
    st.session_state[state_key] = None if ist_aktiv else kat_name
    st.rerun()



@st.dialog("Sonstiges – bitte kurz beschreiben")
def sonstiges_dialog(state_key):
  """Öffnet ein modales Fenster, in dem man frei Text eintragen kann,
  wenn bei einer Kategorie die Unterkategorie 'Sonstiges' gewählt wurde."""
  text_val = st.text_area(
      "Was genau hast du gemacht?",
      value=st.session_state.get(state_key, ""),
      key=f"{state_key}_input",
  )
  col_d1, col_d2 = st.columns(2)
  with col_d1:
    if st.button(
        "Übernehmen", key=f"{state_key}_ok", type="primary",
        use_container_width=True,
    ):
      st.session_state[state_key] = text_val.strip()
      st.session_state[f"{state_key}_done"] = True
      st.rerun()
  with col_d2:
    if st.button(
        "Abbrechen", key=f"{state_key}_cancel", use_container_width=True
    ):
      st.session_state[f"{state_key}_done"] = True
      st.rerun()


def handle_sonstiges_unterkategorie(selected_unterkat, cat_key):
  """Wenn 'Sonstiges' gewählt ist, öffnet dies (einmalig, bis wieder
  gewechselt wird) das Dialog-Fenster zur Texteingabe und liefert den
  eingegebenen Freitext als tatsächliche Unterkategorie zurück."""
  state_key = f"sonstiges_text_{cat_key}"
  done_key = f"{state_key}_done"

  if selected_unterkat != "Sonstiges":
    st.session_state[done_key] = False
    return selected_unterkat

  if not st.session_state.get(done_key, False):
    sonstiges_dialog(state_key)

  freitext = st.session_state.get(state_key, "").strip()
  if freitext:
    st.caption(f"📝 Sonstiges: {freitext}")
  else:
    st.caption("📝 Sonstiges (noch keine Beschreibung eingetragen)")
  return freitext if freitext else "Sonstiges"


# Initialisierung des Session State für Daten
# Tagebuch-Protokoll: einfache Einträge mit Kategorie/Unterkategorie/
# Minuten (treibt die Woche/Heute-Kacheln oben). Eigene Übungen (weiter
# unten) ist ein zweites, unabhängiges System für Einträge mit Sätzen/
# Wiederholungen/Link/Bild.
if "protokoll" not in st.session_state:
  st.session_state.protokoll = pd.DataFrame(
      columns=[
          "Datum",
          "Kategorie",
          "Unterkategorie",
          "Minuten",
          "Status",
          "Notizen",
          "Verknüpfte Übung",
          "Verknüpfter Link",
          "Verknüpftes Bild",
      ]
  )

if "eigene_uebungen" not in st.session_state:
  st.session_state.eigene_uebungen = pd.DataFrame(
      columns=[
          "Datum",
          "Kategorie",
          "Unterkategorie",
          "Dauer (Min.)",
          "Sätze",
          "Wiederholungen",
          "Notizen",
          "Link",
          "Bild",
      ]
  )
if "eigene_uebung_form_aktiv" not in st.session_state:
  st.session_state.eigene_uebung_form_aktiv = False
if "eigene_uebung_import_aktiv" not in st.session_state:
  st.session_state.eigene_uebung_import_aktiv = False

# Unterkategorien, die nur bei "Balance" zur Auswahl stehen
BALANCE_UNTERKATEGORIEN = [
    "Meditation",
    "Entspannung",
    "Koordination",
    "Gleichgewichtstraining",
    "Jonglieren",
    "Life Kinetik",
    "Beweg dein Hirn",
    "Sonstiges",
]

# Unterkategorien, die nur bei "Ausdauer" zur Auswahl stehen
AUSDAUER_UNTERKATEGORIEN = [
    "Joggen",
    "Nordic Walking",
    "Walking",
    "Wandern",
    "Radfahren",
    "Schwimmen",
    "Treppensteigen",
    "Sonnengruß",
    "Sonstiges",
]

# Unterkategorien, die nur bei "Beweglichkeit" zur Auswahl stehen
BEWEGLICHKEIT_UNTERKATEGORIEN = [
    "Yoga",
    "Ausgleichsübungen",
    "Faszientraining",
    "Rückenfit",
    "Massage",
    "Chi Gong",
    "Sonstiges",
]

# Unterkategorien, die nur bei "Kraft" zur Auswahl stehen
KRAFT_UNTERKATEGORIEN = [
    "Pilates",
    "Rückenfit",
    "Stabilisierungstraining",
    "Therabandtraining",
    "Hanteltraining",
    "Sonstiges",
]

# Unterkategorien, die nur bei "Ernährung" zur Auswahl stehen (für die
# Kategorie-Auswahl bei "Eigene Übungen")
ERNAEHRUNG_UNTERKATEGORIEN = ["Sonstiges"]

# Unterkategorien, die nur bei "Gesamtbefinden" zur Auswahl stehen (für die
# Kategorie-Auswahl bei "Eigene Übungen")
GESAMTBEFINDEN_UNTERKATEGORIEN = ["Sonstiges"]

# Tageszeiten, die nur bei "Ernährung" im Tagebuch-Formular zur Auswahl stehen
ERNAEHRUNG_TAGESZEITEN = ["Morgens", "Mittags", "Abends"]

# Ampel-Status für Ernährung im Tagebuch-Formular: (Anzeige-Label,
# gespeicherter Wert, Farbe)
ERNAEHRUNG_AMPEL = [
    ("🟢 Umgesetzt", "Umgesetzt", "#2e7d46"),
    ("🟡 Teilweise umgesetzt", "Teilweise umgesetzt", "#e3a008"),
    ("🔴 Nicht umgesetzt", "Nicht umgesetzt", "#d9534f"),
]

# Smileys für "Gesamtbefinden" im Tagebuch-Formular
STIMMUNG_SMILEYS = [
    ("😞 Schlecht", "😞 Schlecht"),
    ("😐 Neutral", "😐 Neutral"),
    ("😊 Gut", "😊 Gut"),
]

if "arsenal" not in st.session_state:
  st.session_state.arsenal = pd.DataFrame(
      [
          {
              "Kategorie": "Beweglichkeit",
              "Typ": "Text",
              "Bereich / Übung": "Mobilisation & Dehnen",
              "Link": "https://example.com/mobilitaet",
              "Beschreibung": "Tägliche Routine für den Rücken",
              "Bild": "",
          },
          {
              "Kategorie": "Kraft",
              "Typ": "Text",
              "Bereich / Übung": "Kräftigung Rumpf",
              "Link": "https://example.com/ruecken",
              "Beschreibung": "Aufrechte Haltung, Bauchspannung halten",
              "Bild": "",
          },
          {
              "Kategorie": "Ausdauer",
              "Typ": "Text",
              "Bereich / Übung": "AIMO App",
              "Link": "",
              "Beschreibung": "Empfehlenswerte App zur Unterstützung beim Ausdauertraining",
              "Bild": "",
          },
          {
              "Kategorie": "Kraft",
              "Typ": "Text",
              "Bereich / Übung": "AIMO App",
              "Link": "",
              "Beschreibung": "Empfehlenswerte App zur Unterstützung beim Krafttraining",
              "Bild": "",
          },
      ]
  )

# Kategorien und Typen für das Übungsarsenal (gleiche 6 Kategorien wie im
# Tagebuch, plus Typ: was für eine Art von Eintrag das ist)
ARSENAL_KATEGORIEN = [
    "Ausdauer",
    "Kraft",
    "Beweglichkeit",
    "Balance",
    "Ernährung",
    "Gesamtbefinden",
]
ARSENAL_TYPEN = ["Bild", "Link", "Text"]

if "wochen_ansicht_aktiv" not in st.session_state:
  st.session_state.wochen_ansicht_aktiv = False

# Vitaldaten: Schritte & Gewicht (manuell oder per CSV-Import von
# Garmin/Google Fit erfasst)
if "vitaldaten" not in st.session_state:
  st.session_state.vitaldaten = pd.DataFrame(
      columns=["Datum", "Schritte", "Gewicht", "VO2max"]
  )
if "vital_form_aktiv" not in st.session_state:
  st.session_state.vital_form_aktiv = False
if "vital_import_aktiv" not in st.session_state:
  st.session_state.vital_import_aktiv = False

# ----------------------------------------------------
# 1. STARTSEITE & TAGEBUCH
# ----------------------------------------------------
if True:
  st.title("Tagebuch")
  st.markdown("##### Aktivitätentagebuch Prävention")
  st.write("---")

  # --- Automatische Datums- und Wochenberechnung ---
  heute = datetime.date.today()

  if "wochen_offset" not in st.session_state:
    st.session_state.wochen_offset = 0

  referenz_datum = heute + datetime.timedelta(
      weeks=st.session_state.wochen_offset
  )
  jahr, kalenderwoche, wochentag = referenz_datum.isocalendar()

  start_der_woche = referenz_datum - datetime.timedelta(days=wochentag - 1)
  ende_der_woche = start_der_woche + datetime.timedelta(days=6)

  monate = [
      "Jan",
      "Feb",
      "Mär",
      "Apr",
      "Mai",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Okt",
      "Nov",
      "Dez",
  ]
  start_monat = monate[start_der_woche.month - 1]
  ende_monat = monate[ende_der_woche.month - 1]

  if start_der_woche.month == ende_der_woche.month:
    datum_string = (
        f"{start_der_woche.day}. - {ende_der_woche.day}. {ende_monat}"
        f" {ende_der_woche.year}"
    )
  else:
    datum_string = (
        f"{start_der_woche.day}. {start_monat} - {ende_der_woche.day}."
        f" {ende_monat} {ende_der_woche.year}"
    )

  wochentage_de = [
      "Montag",
      "Dienstag",
      "Mittwoch",
      "Donnerstag",
      "Freitag",
      "Samstag",
      "Sonntag",
  ]
  heute_string = f"{wochentage_de[heute.weekday()]}, {heute.day}. {monate[heute.month - 1]} {heute.year}"

  df = st.session_state.protokoll

  def get_cat_minutes(kat_name):
    if df.empty or kat_name not in df["Kategorie"].values:
      return 0
    woche_df = df[
        (df["Datum"] >= str(start_der_woche))
        & (df["Datum"] <= str(ende_der_woche))
        & (df["Kategorie"] == kat_name)
    ]
    return int(woche_df["Minuten"].sum())

  def get_today_minutes(kat_name):
    if df.empty:
      return 0
    heute_str = str(heute)
    heute_df = df[(df["Datum"] == heute_str) & (df["Kategorie"] == kat_name)]
    if heute_df.empty:
      return 0
    return int(heute_df["Minuten"].sum())

  # --- CSS für den grünen Hauptkasten ---
  # Wichtig: st.container(key="dashcard") erzeugt eine echte Wrapper-Div
  # mit der CSS-Klasse "st-key-dashcard". Damit landet WIRKLICH jedes
  # Element (auch der Button "Eintrag erstellen"), das innerhalb von
  # "with st.container(key='dashcard'):" steht, in diesem Kasten -
  # der alte :has()-Marker-Trick hat das nicht zuverlässig geschafft.
  # Voraussetzung: Streamlit-Version, die den key-Parameter für
  # st.container() unterstützt (ab ca. 1.32).
  st.markdown(
      """
        <style>
        div.st-key-dashcard {
            background-color: #e2efe3;
            border: 1px solid #c8dbc9;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 25px;
        }

        /* Gleiche Kartenoptik wie beim Tagebuch, für das Übungsarsenal */
        div.st-key-arsenalcard {
            background-color: #e2efe3;
            border: 1px solid #c8dbc9;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 25px;
        }

        /* Gleiche Kartenoptik für die Vitalwerte-Karte (Schritte/Gewicht/BMI) */
        div.st-key-vitalcard {
            background-color: #e2efe3;
            border: 1px solid #c8dbc9;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 25px;
        }

        /* Primärer Aktions-Button (z.B. "Eintrag erstellen", "Speichern") -
           gefülltes, gedecktes Waldgrün, harmoniert mit der grünen Karte */
        div.stButton button[kind="primary"] {
            background-color: #3f7a5c !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
        }
        div.stButton button[kind="primary"]:hover {
            background-color: #2f5e45 !important;
        }

        /* Sekundäre Buttons (Navigation ⬅️➡️, Wochen-Titel, Abbrechen) -
           dezent, outline, fügt sich ruhig in die grüne Karte ein */
        div.stButton button[kind="secondary"] {
            background-color: #ffffff !important;
            color: #2f5e45 !important;
            border: 1px solid #a9c9b3 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        div.stButton button[kind="secondary"]:hover {
            background-color: #eef6f0 !important;
            border-color: #3f7a5c !important;
            color: #2f5e45 !important;
        }

        /* Spalten (st.columns) sollen auf dem Handy NICHT untereinander
           stehen, sondern genauso nebeneinander bleiben wie am Desktop.
           Streamlit stapelt Spalten normalerweise unter ~640px Breite -
           das erzwingen wir hier zurück auf eine Reihe. Wichtig: die
           prozentuale Breite (flex-basis) von Streamlit NICHT anfassen,
           sonst richten sich die Boxen nach ihrem Inhalt statt nach der
           Bildschirmbreite und werden zu breit. */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            flex-direction: row !important;
            gap: 4px !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
        }

        /* Auf schmalen Handy-Screens (z.B. Poco F5, ~390-400px breit):
           Kästchen-Innenabstand, Ring-Icon und Schrift verkleinern, damit
           alle 6 Boxen pro Reihe bequem nebeneinander passen. */
        @media (max-width: 480px) {
            div.st-key-dashcard {
                padding: 8px;
            }
            div.st-key-dashcard [data-testid="stHorizontalBlock"] {
                gap: 3px !important;
            }
            .icon-box {
                padding: 3px !important;
            }
            .icon-box svg {
                width: 30px !important;
                height: 30px !important;
            }
            .icon-box .icon-box-symbol {
                font-size: 15px !important;
            }
            .icon-box .icon-box-label {
                font-size: 9px !important;
            }
        }

        /* Plus/Minus-Stepper-Buttons beim Minuten-Eingabefeld ausblenden */
        button[data-testid="stNumberInputStepDown"],
        button[data-testid="stNumberInputStepUp"] {
            display: none !important;
        }

        /* Die 3er-Spalten bei "Weitere Details" und den Filtern
           (Kategorie/Unterkategorie/Zeitraum bzw. Dauer/Sätze/
           Wiederholungen) sollen auf schmalen Handy-Screens untereinander
           stehen dürfen - der nowrap-Zwang oben ist nur für die
           Kategorie-Kacheln gedacht und macht diese Eingabefelder auf dem
           Handy sonst unbenutzbar schmal. */
        @media (max-width: 640px) {
            div.st-key-wd_details_row div[data-testid="stHorizontalBlock"],
            div.st-key-protokoll_filter_row div[data-testid="stHorizontalBlock"],
            div.st-key-uebungen_filter_row div[data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
            }
            div.st-key-wd_details_row div[data-testid="stColumn"],
            div.st-key-protokoll_filter_row div[data-testid="stColumn"],
            div.st-key-uebungen_filter_row div[data-testid="stColumn"] {
                min-width: 100% !important;
            }

            /* Vitalwerte-Kennzahlen: auf schmalen Screens als 2er-Raster
               (3 Reihen) statt 6 in einer viel zu schmalen Reihe */
            div.st-key-vital_metrics_row div[data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
            }
            div.st-key-vital_metrics_row div[data-testid="stColumn"] {
                /* 4px Gap zwischen den Spalten mit einrechnen, sonst
                   passen selbst zwei 50%-Spalten nicht in eine Reihe
                   und jede Kachel landet einzeln in ihrer eigenen Zeile */
                min-width: calc(50% - 4px) !important;
            }
        }

        /* Vitalwerte-Kacheln: einheitlich kleinere, zentrierte Zahlen -
           und das Label darf vollständig umbrechen statt abgeschnitten
           zu werden ("Gewicht heute i..."). Label und Wert werden hier
           beide zwangsweise auf Flex+justify-content:center gesetzt
           (statt uns auf Streamlits eigenes display:grid/block und
           text-align zu verlassen) - sonst können Label und Zahl je
           nach Streamlit-Version unterschiedlich breite Boxen bekommen
           und stehen dann nicht wirklich auf derselben Mittelachse. */
        div.st-key-vitalcard [data-testid="stMetric"] {
            width: 100% !important;
        }
        div.st-key-vitalcard [data-testid="stMetricValue"],
        div.st-key-vitalcard [data-testid="stMetricLabel"] {
            display: flex !important;
            width: 100% !important;
            justify-content: center !important;
            text-align: center !important;
        }
        div.st-key-vitalcard [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
        }
        div.st-key-vitalcard [data-testid="stMetricLabel"] {
            align-items: flex-end;
            /* Feste Mindesthöhe (Platz für 2 Zeilen), damit kurze Labels
               ("BMI") und lange, umgebrochene Labels ("Ø Gewicht (Woche)
               in kg") gleich hoch sind - sonst stehen die Zahlen
               darunter nicht auf einer Höhe. */
            min-height: 2.6rem;
        }
        div.st-key-vitalcard [data-testid="stMetricLabel"] p {
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: unset !important;
            text-align: center;
            width: 100%;
        }
        </style>
        """,
      unsafe_allow_html=True,
  )

  # Echter Container - alles, was hier drin (eingerückt) steht,
  # bekommt den grünen Hintergrund, inklusive des Buttons ganz unten.
  with st.container(key="dashcard"):
    col_w1, col_w2, col_w3 = st.columns([1, 4, 1])
    with col_w1:
      if st.button("⬅️", key="w_back", use_container_width=True):
        st.session_state.wochen_offset -= 1
        st.rerun()
    with col_w2:
      wochen_titel_text = (
          f"Woche {kalenderwoche} (Details ausblenden)"
          if st.session_state.wochen_ansicht_aktiv
          else f"Woche {kalenderwoche} (Details anzeigen)"
      )
      if st.button(wochen_titel_text, key="w_title", use_container_width=True):
        st.session_state.wochen_ansicht_aktiv = (
            not st.session_state.wochen_ansicht_aktiv
        )
        st.rerun()
      st.markdown(
          f"<p style='text-align: center; color: #555; margin: 0;'>{datum_string}</p>",
          unsafe_allow_html=True,
      )
    with col_w3:
      # Vorwärts-Navigation bis Ende des Jahres 2040 begrenzen
      naechste_woche_ende = ende_der_woche + datetime.timedelta(weeks=1)
      if naechste_woche_ende.year > 2040:
        st.button(
            "➡️", key="w_fwd", use_container_width=True, disabled=True
        )
      elif st.button("➡️", key="w_fwd", use_container_width=True):
        st.session_state.wochen_offset += 1
        st.rerun()

    # BEREICH: WOCHE
    st.markdown(
        "<p style='font-weight: bold; margin-top: 15px;'>Woche</p>",
        unsafe_allow_html=True,
    )
    mini_col1, mini_col2, mini_col3, mini_col4, mini_col5, mini_col6 = (
        st.columns(6)
    )
    with mini_col1:
      render_icon_box(
          "🏃‍♂️", get_cat_minutes("Ausdauer"), 90,
          box_height=108, icon_font_size=26, ring_size=34,
          click_key=("woche", "Ausdauer"), kat_name="Ausdauer",
      )
    with mini_col2:
      render_icon_box(
          "🏋️‍♂️", get_cat_minutes("Kraft"), 90,
          box_height=108, icon_font_size=26, ring_size=34,
          click_key=("woche", "Kraft"), kat_name="Kraft",
      )
    with mini_col3:
      render_icon_box(
          beweglichkeit_icon_html(36),
          get_cat_minutes("Beweglichkeit"), 90,
          box_height=108, icon_font_size=26, ring_size=34,
          click_key=("woche", "Beweglichkeit"), kat_name="Beweglichkeit",
      )
    with mini_col4:
      render_icon_box(
          balance_icon_html(36),
          get_cat_minutes("Balance"), 90,
          box_height=108, icon_font_size=26, ring_size=34,
          click_key=("woche", "Balance"), kat_name="Balance",
      )
    with mini_col5:
      render_icon_box(
          "🍽️", get_cat_minutes("Ernährung"), 90,
          box_height=108, icon_font_size=26, ring_size=34,
          click_key=("woche", "Ernährung"), kat_name="Ernährung",
      )
    with mini_col6:
      render_icon_box(
          "😊", get_cat_minutes("Gesamtbefinden"), 90,
          box_height=108, icon_font_size=26, ring_size=34,
          click_key=("woche", "Gesamtbefinden"), kat_name="Gesamtbefinden",
      )

    st.write("")

    # BEREICH: HEUTE
    st.markdown(
        f"<p style='font-weight: bold;'>Heute <span style='font-size: 13px;"
        f" color: #555; float: right;'>{heute_string}</span></p>",
        unsafe_allow_html=True,
    )
    t_col1, t_col2, t_col3, t_col4, t_col5, t_col6 = st.columns(6)
    with t_col1:
      render_icon_box(
          "🏃‍♂️", get_today_minutes("Ausdauer"), 90,
          box_height=98, icon_font_size=22, ring_size=28,
          click_key=("heute", "Ausdauer"), kat_name="Ausdauer",
      )
    with t_col2:
      render_icon_box(
          "🏋️‍♂️", get_today_minutes("Kraft"), 90,
          box_height=98, icon_font_size=22, ring_size=28,
          click_key=("heute", "Kraft"), kat_name="Kraft",
      )
    with t_col3:
      render_icon_box(
          beweglichkeit_icon_html(30),
          get_today_minutes("Beweglichkeit"), 90,
          box_height=98, icon_font_size=22, ring_size=28,
          click_key=("heute", "Beweglichkeit"), kat_name="Beweglichkeit",
      )
    with t_col4:
      render_icon_box(
          balance_icon_html(30),
          get_today_minutes("Balance"), 90,
          box_height=98, icon_font_size=22, ring_size=28,
          click_key=("heute", "Balance"), kat_name="Balance",
      )
    with t_col5:
      render_icon_box(
          "🍽️", get_today_minutes("Ernährung"), 90,
          box_height=98, icon_font_size=22, ring_size=28,
          click_key=("heute", "Ernährung"), kat_name="Ernährung",
      )
    with t_col6:
      render_icon_box(
          "😊", get_today_minutes("Gesamtbefinden"), 90,
          box_height=98, icon_font_size=22, ring_size=28,
          click_key=("heute", "Gesamtbefinden"), kat_name="Gesamtbefinden",
      )

    # Detail-Liste, wenn eine Kachel (Woche oder Heute) angeklickt wurde
    if st.session_state.get("detail_ansicht") is not None:
      detail_scope, detail_kat = st.session_state["detail_ansicht"]
      if detail_scope == "woche":
        detail_df = df[
            (df["Datum"] >= str(start_der_woche))
            & (df["Datum"] <= str(ende_der_woche))
            & (df["Kategorie"] == detail_kat)
        ]
        zeitraum_text = f"Woche {kalenderwoche} ({datum_string})"
      else:
        detail_df = df[
            (df["Datum"] == str(heute)) & (df["Kategorie"] == detail_kat)
        ]
        zeitraum_text = "Heute"

      st.write("---")
      st.markdown(f"#### {detail_kat} – {zeitraum_text}")
      if detail_df.empty:
        st.info(f"Noch keine Einträge für {detail_kat} in diesem Zeitraum.")
      else:
        anzeige_spalten = [
            c
            for c in [
                "Datum", "Unterkategorie", "Minuten", "Status", "Notizen"
            ]
            if c in detail_df.columns
        ]
        st.dataframe(
            detail_df[anzeige_spalten].sort_values("Datum"),
            use_container_width=True,
            hide_index=True,
        )
      if st.button("✕ Schließen", key="detail_schliessen_btn"):
        st.session_state["detail_ansicht"] = None
        st.rerun()

    st.write("")

    # Grüner Button "Eintrag erstellen" - jetzt garantiert INNERHALB
    # des grünen Kastens, da er im selben st.container(key="dashcard") steht.
    # Statt dem bunten ➕-Emoji (auf dunklem Grund schlecht erkennbar) wird
    # ein normales "+"-Zeichen verwendet, das die weiße Button-Schriftfarbe
    # übernimmt und damit gut sichtbar ist.
    if st.button(
        "＋ Eintrag erstellen",
        key="btn_create",
        use_container_width=True,
        type="primary",
    ):
      st.session_state.eintrag_modal_aktiv = True
      st.rerun()

  # Formular für Eintrag (außerhalb des Kastens)
  if st.session_state.get("eintrag_modal_aktiv", False):
    st.write("### 📝 Neuen Eintrag erfassen")
    # Kein st.form() hier: Felder innerhalb eines Formulars lösen erst
    # beim Absenden einen Rerun aus, daher würden die Zusatzfelder nicht
    # sofort erscheinen. Stattdessen normale Widgets + eigene Buttons.
    selected_cat = st.selectbox(
        "Kategorie wählen",
        [
            "Ausdauer",
            "Kraft",
            "Beweglichkeit",
            "Balance",
            "Ernährung",
            "Gesamtbefinden",
        ],
        key="entry_kategorie",
    )

    selected_unterkat = ""
    status_wert = "Aktiv"
    minuten = 0

    if selected_cat == "Ausdauer":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          AUSDAUER_UNTERKATEGORIEN,
          key="entry_unterkategorie_ausdauer",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "ausdauer"
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Balance":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          BALANCE_UNTERKATEGORIEN,
          key="entry_unterkategorie",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "balance"
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Beweglichkeit":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          BEWEGLICHKEIT_UNTERKATEGORIEN,
          key="entry_unterkategorie_beweglichkeit",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "beweglichkeit"
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Kraft":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          KRAFT_UNTERKATEGORIEN,
          key="entry_unterkategorie_kraft",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "kraft"
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Ernährung":
      selected_unterkat = st.radio(
          "Tageszeit",
          ERNAEHRUNG_TAGESZEITEN,
          horizontal=True,
          key="entry_tageszeit",
      )
      ampel_label = st.radio(
          "Status",
          [label for label, _, _ in ERNAEHRUNG_AMPEL],
          horizontal=True,
          key="entry_ampel",
      )
      status_wert = next(
          wert for label, wert, _ in ERNAEHRUNG_AMPEL if label == ampel_label
      )

    elif selected_cat == "Gesamtbefinden":
      smiley_label = st.radio(
          "Stimmung wählen",
          [label for label, _ in STIMMUNG_SMILEYS],
          horizontal=True,
          key="entry_smiley",
      )
      selected_unterkat = next(
          wert for label, wert in STIMMUNG_SMILEYS if label == smiley_label
      )

    else:
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    verknuepfte_uebung = ""
    verknuepfter_link = ""
    verknuepftes_bild = ""
    passende_arsenal_eintraege = st.session_state.arsenal[
        st.session_state.arsenal["Kategorie"] == selected_cat
    ]
    if not passende_arsenal_eintraege.empty:
      arsenal_optionen = ["Keine Auswahl"] + passende_arsenal_eintraege[
          "Bereich / Übung"
      ].tolist()
      gewaehlte_uebung = st.selectbox(
          "🔗 Aus Übungsarsenal wählen (optional)", arsenal_optionen,
          key="entry_arsenal_auswahl",
      )
      if gewaehlte_uebung != "Keine Auswahl":
        arsenal_eintrag = passende_arsenal_eintraege[
            passende_arsenal_eintraege["Bereich / Übung"] == gewaehlte_uebung
        ].iloc[0]
        verknuepfte_uebung = gewaehlte_uebung
        verknuepfter_link = arsenal_eintrag.get("Link", "") or ""
        verknuepftes_bild = arsenal_eintrag.get("Bild", "") or ""
        if arsenal_eintrag.get("Beschreibung"):
          st.caption(arsenal_eintrag["Beschreibung"])
        if verknuepfter_link:
          st.markdown(f"🔗 [{verknuepfter_link}]({verknuepfter_link})")
        if verknuepftes_bild:
          st.image(verknuepftes_bild, use_container_width=True)

    datum = st.date_input("Datum", value=heute, key="entry_datum")
    notizen = st.text_input("Notizen / Details", key="entry_notizen")

    weitere_details_aktiv = st.checkbox(
        "➕ Weitere Details (Sätze, Wiederholungen, Dauer, Link, Bild)",
        key="entry_weitere_details_toggle",
    )
    wd_dauer = wd_saetze = wd_wiederholungen = None
    wd_link = ""
    wd_bild_upload = None
    if weitere_details_aktiv:
      with st.container(key="wd_details_row"):
        wd_col1, wd_col2, wd_col3 = st.columns(3)
        with wd_col1:
          wd_dauer = st.number_input(
              "Dauer (Minuten)", min_value=0, max_value=300, value=None,
              key="entry_wd_dauer",
          )
        with wd_col2:
          wd_saetze = st.number_input(
              "Sätze", min_value=0, max_value=50, value=None,
              key="entry_wd_saetze",
          )
        with wd_col3:
          wd_wiederholungen = st.number_input(
              "Wiederholungen", min_value=0, max_value=1000, value=None,
              key="entry_wd_wiederholungen",
          )
      wd_link = st.text_input("Link – optional", key="entry_wd_link")
      wd_bild_upload = st.file_uploader(
          "Bild – optional", type=["png", "jpg", "jpeg"],
          key="entry_wd_bild",
      )

    col_s1, col_s2 = st.columns(2)
    with col_s1:
      save_btn = st.button(
          "Speichern",
          key="save_entry_btn",
          type="primary",
          use_container_width=True,
      )
    with col_s2:
      cancel_btn = st.button(
          "Abbrechen", key="cancel_entry_btn", use_container_width=True
      )

    if save_btn:
      neuer_eintrag = pd.DataFrame(
          [{
              "Datum": str(datum),
              "Kategorie": selected_cat,
              "Unterkategorie": selected_unterkat,
              "Minuten": minuten if minuten is not None else 0,
              "Status": status_wert,
              "Notizen": notizen,
              "Verknüpfte Übung": verknuepfte_uebung,
              "Verknüpfter Link": verknuepfter_link,
              "Verknüpftes Bild": verknuepftes_bild,
          }]
      )
      st.session_state.protokoll = pd.concat(
          [st.session_state.protokoll, neuer_eintrag], ignore_index=True
      )
      if weitere_details_aktiv:
        wd_bild_data_uri = ""
        if wd_bild_upload is not None:
          wd_bild_b64 = base64.b64encode(wd_bild_upload.getvalue()).decode(
              "utf-8"
          )
          wd_bild_data_uri = f"data:{wd_bild_upload.type};base64,{wd_bild_b64}"
        neue_uebung = pd.DataFrame(
            [{
                "Datum": str(datum),
                "Kategorie": selected_cat,
                "Unterkategorie": selected_unterkat,
                "Dauer (Min.)": wd_dauer,
                "Sätze": wd_saetze,
                "Wiederholungen": wd_wiederholungen,
                "Notizen": notizen,
                "Link": wd_link.strip(),
                "Bild": wd_bild_data_uri,
            }]
        )
        st.session_state.eigene_uebungen = pd.concat(
            [st.session_state.eigene_uebungen, neue_uebung],
            ignore_index=True,
        )
      st.session_state.eintrag_modal_aktiv = False
      st.success("Eintrag erfolgreich gespeichert!")
      st.rerun()
    if cancel_btn:
      st.session_state.eintrag_modal_aktiv = False
      st.rerun()
    st.write("---")

  # WOCHEN-ANSICHT (3x2 Raster wenn aktiviert)
  if st.session_state.wochen_ansicht_aktiv:
    st.write("### 📊 Detail-Auswertung der Kategorien (3x2)")

    def get_cat_stats(kat_name):
      woche_df_all = df[
          (df["Datum"] >= str(start_der_woche))
          & (df["Datum"] <= str(ende_der_woche))
      ]
      if woche_df_all.empty or kat_name not in woche_df_all["Kategorie"].values:
        return 0, "Noch keine Einträge", "⚪"
      kat_df = woche_df_all[woche_df_all["Kategorie"] == kat_name]
      min_sum = kat_df["Minuten"].sum()
      if min_sum >= 90:
        return min_sum, f"{min_sum} min (Ausreichend)", "🟢"
      elif min_sum >= 60:
        return min_sum, f"{min_sum} min (Mittel)", "🟡"
      else:
        return (
            min_sum,
            (
                f"{min_sum} min (Zu wenig)"
                if min_sum > 0
                else "Noch keine Einträge"
            ),
            "🔴" if min_sum > 0 else "⚪",
        )

    kategorien_paare = [
        (("🏃‍♂️ Ausdauer", "Ausdauer"), ("🏋️‍♂️ Kraft", "Kraft")),
        (
            (f"{beweglichkeit_icon_html(20)} Beweglichkeit", "Beweglichkeit"),
            (f"{balance_icon_html(20)} Balance", "Balance"),
        ),
        (("🍽️ Ernährung", "Ernährung"), ("😊 Gesamtbefinden", "Gesamtbefinden")),
    ]

    for kat1, kat2 in kategorien_paare:
      c1, c2 = st.columns(2)
      m1, text1, sym1 = get_cat_stats(kat1[1])
      with c1:
        st.markdown(
            f"""
                    <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9; height: 90px;">
                        <h4 style="margin: 0; color: #333; font-size: 16px;">{kat1[0]}</h4>
                        <p style="margin: 8px 0 0 0; font-size: 14px; color: #555;">{sym1} {text1}</p>
                    </div>
                    """,
            unsafe_allow_html=True,
        )

      m2, text2, sym2 = get_cat_stats(kat2[1])
      with c2:
        st.markdown(
            f"""
                    <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9; height: 90px;">
                        <h4 style="margin: 0; color: #333; font-size: 16px;">{kat2[0]}</h4>
                        <p style="margin: 8px 0 0 0; font-size: 14px; color: #555;">{sym2} {text2}</p>
                    </div>
                    """,
            unsafe_allow_html=True,
        )

    gesamt_minuten = (
        df[
            (df["Datum"] >= str(start_der_woche))
            & (df["Datum"] <= str(ende_der_woche))
        ]["Minuten"].sum()
        if not df.empty
        else 0
    )
    if gesamt_minuten >= 90:
      g_sym, g_text = "🟢", f"{gesamt_minuten} min — Ausreichend (Ziel erreicht)"
    elif gesamt_minuten >= 60:
      g_sym, g_text = "🟡", f"{gesamt_minuten} min — Mittel"
    else:
      g_sym, g_text = (
          ("🔴", f"{gesamt_minuten} min — Zu wenig")
          if gesamt_minuten > 0
          else ("⚪", "Noch keine Einträge")
      )

    st.markdown(
        f"""
        <div style="padding: 18px; border: 2px solid #2F4F4F; border-radius: 10px; margin-top: 10px; margin-bottom: 20px; background-color: #E0EEEE;">
            <h3 style="margin: 0; color: #2F4F4F; font-size: 18px;">📊 Gesamtauswertung dieser Woche</h3>
            <p style="margin: 8px 0 0 0; font-size: 15px; font-weight: bold; color: #333;">{g_sym} {g_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("---")

  # ----------------------------------------------------
  # VITALWERTE: Schritte, Gewicht, BMI
  # ----------------------------------------------------
  vital_df = st.session_state.vitaldaten

  def _vital_heute(spalte):
    if vital_df.empty:
      return None
    treffer = vital_df[vital_df["Datum"] == str(heute)]
    if treffer.empty or treffer[spalte].dropna().empty:
      return None
    return treffer[spalte].dropna().iloc[-1]

  def _vital_zeitraum_df(zeitraum):
    if vital_df.empty:
      return vital_df
    if zeitraum == "Woche":
      zeitraum_df = vital_df[
          (vital_df["Datum"] >= str(start_der_woche))
          & (vital_df["Datum"] <= str(ende_der_woche))
      ]
    else:
      zeitraum_tage = {
          "Monat": 30,
          "3 Monate": 90,
          "6 Monate": 180,
          "Jahr": 365,
      }[zeitraum]
      stichtag = str(heute - datetime.timedelta(days=zeitraum_tage))
      zeitraum_df = vital_df[vital_df["Datum"] >= stichtag]
    return zeitraum_df.sort_values("Datum")

  def _vital_zeitraum_avg(spalte, zeitraum):
    werte = _vital_zeitraum_df(zeitraum)[spalte].dropna()
    if werte.empty:
      return None
    return werte.mean()

  def _vital_letzter_wert(spalte):
    """Letzter bekannter (nicht-leerer) Wert insgesamt - für Werte wie
    VO2max, die sich nicht täglich ändern, sondern nur gelegentlich neu
    gemessen/geschätzt werden."""
    if vital_df.empty or spalte not in vital_df.columns:
      return None
    sortiert = vital_df.sort_values("Datum")
    werte = sortiert[spalte].dropna()
    if werte.empty:
      return None
    return werte.iloc[-1]

  schritte_heute = _vital_heute("Schritte")
  gewicht_heute = _vital_heute("Gewicht")
  vo2max_aktuell = _vital_letzter_wert("VO2max")

  if "koerpergroesse_cm" not in st.session_state:
    st.session_state.koerpergroesse_cm = None

  with st.container(key="vitalcard"):
    st.subheader("📊 Vitalwerte")

    if st.session_state.koerpergroesse_cm is None:
      groesse_input = st.number_input(
          "Körpergröße (cm) – einmalig für BMI-Berechnung",
          min_value=0,
          max_value=250,
          value=None,
          key="groesse_input",
      )
      if groesse_input:
        st.session_state.koerpergroesse_cm = groesse_input
        st.rerun()
    else:
      with st.expander(
          f"Körpergröße: {st.session_state.koerpergroesse_cm:.0f} cm "
          "(ändern)"
      ):
        groesse_input = st.number_input(
            "Körpergröße (cm) – einmalig für BMI-Berechnung",
            min_value=0,
            max_value=250,
            value=st.session_state.koerpergroesse_cm,
            key="groesse_input",
        )
        st.session_state.koerpergroesse_cm = (
            groesse_input if groesse_input else None
        )

    bmi_wert = None
    if gewicht_heute and st.session_state.koerpergroesse_cm:
      groesse_m = st.session_state.koerpergroesse_cm / 100
      bmi_wert = gewicht_heute / (groesse_m**2)

    zeitraum_auswahl = st.selectbox(
        "Zeitraum für die Ø-Werte",
        ["Woche", "Monat", "3 Monate", "6 Monate", "Jahr"],
        key="vital_zeitraum_auswahl",
    )
    schritte_zeitraum_avg = _vital_zeitraum_avg("Schritte", zeitraum_auswahl)
    gewicht_zeitraum_avg = _vital_zeitraum_avg("Gewicht", zeitraum_auswahl)

    with st.container(key="vital_metrics_row"):
      m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
      with m_col1:
        st.metric(
            "Schritte heute",
            f"{int(schritte_heute):,}".replace(",", ".")
            if schritte_heute is not None
            else "–",
        )
      with m_col2:
        st.metric(
            f"Ø Schritte/Tag ({zeitraum_auswahl})",
            f"{int(schritte_zeitraum_avg):,}".replace(",", ".")
            if schritte_zeitraum_avg is not None
            else "–",
        )
      with m_col3:
        st.metric(
            "Gewicht heute in kg",
            f"{gewicht_heute:.1f}" if gewicht_heute is not None else "–",
        )
      with m_col4:
        st.metric(
            f"Ø Gewicht ({zeitraum_auswahl}) in kg",
            f"{gewicht_zeitraum_avg:.1f}"
            if gewicht_zeitraum_avg is not None
            else "–",
        )
      with m_col5:
        st.metric(
            "BMI", f"{bmi_wert:.1f}" if bmi_wert is not None else "–"
        )
      with m_col6:
        st.metric(
            "VO2max (aktuell)",
            f"{vo2max_aktuell:.1f}" if vo2max_aktuell is not None else "–",
        )

    st.write("")
    st.markdown(f"#### 📈 Verlauf ({zeitraum_auswahl})")
    verlauf_df = _vital_zeitraum_df(zeitraum_auswahl)
    if verlauf_df.empty:
      st.info("Noch keine Einträge für diesen Zeitraum.")
    else:
      chart_col1, chart_col2 = st.columns(2)
      with chart_col1:
        st.caption("Schritte")
        schritte_verlauf = verlauf_df.dropna(subset=["Schritte"])
        if schritte_verlauf.empty:
          st.info("Keine Schritte-Einträge in diesem Zeitraum.")
        else:
          st.line_chart(
              schritte_verlauf.set_index("Datum")["Schritte"],
              height=220,
          )
      with chart_col2:
        st.caption("Gewicht (kg)")
        gewicht_verlauf = verlauf_df.dropna(subset=["Gewicht"])
        if gewicht_verlauf.empty:
          st.info("Keine Gewicht-Einträge in diesem Zeitraum.")
        else:
          st.line_chart(
              gewicht_verlauf.set_index("Datum")["Gewicht"],
              height=220,
          )

    st.write("")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
      if st.button(
          "＋ Schritte/Gewicht eintragen",
          key="btn_open_vital_form",
          type="primary",
          use_container_width=True,
      ):
        st.session_state.vital_form_aktiv = True
        st.session_state.vital_import_aktiv = False
        st.rerun()
    with col_v2:
      if st.button(
          "⬆️ CSV importieren",
          key="btn_open_vital_import",
          use_container_width=True,
      ):
        st.session_state.vital_import_aktiv = True
        st.session_state.vital_form_aktiv = False
        st.rerun()

    if st.session_state.vital_form_aktiv:
      st.write("---")
      v_datum = st.date_input("Datum", value=heute, key="vital_datum")
      v_schritte = st.number_input(
          "Schritte", min_value=0, max_value=100000, value=None,
          key="vital_schritte_input",
      )
      v_gewicht = st.number_input(
          "Gewicht (kg)", min_value=0.0, max_value=400.0, value=None,
          step=0.1, key="vital_gewicht_input",
      )
      v_vo2max = st.number_input(
          "VO2max (ml/kg/min) – optional, meist von der Uhr geschätzt",
          min_value=0.0, max_value=100.0, value=None,
          step=0.1, key="vital_vo2max_input",
      )
      col_vs1, col_vs2 = st.columns(2)
      with col_vs1:
        vital_save = st.button(
            "Speichern", key="vital_save_btn", type="primary",
            use_container_width=True,
        )
      with col_vs2:
        vital_cancel = st.button(
            "Abbrechen", key="vital_cancel_btn", use_container_width=True
        )
      if vital_save:
        neuer_vital_eintrag = pd.DataFrame(
            [{
                "Datum": str(v_datum),
                "Schritte": v_schritte,
                "Gewicht": v_gewicht,
                "VO2max": v_vo2max,
            }]
        )
        st.session_state.vitaldaten = pd.concat(
            [st.session_state.vitaldaten, neuer_vital_eintrag],
            ignore_index=True,
        )
        st.session_state.vital_form_aktiv = False
        st.success("Gespeichert!")
        st.rerun()
      if vital_cancel:
        st.session_state.vital_form_aktiv = False
        st.rerun()

    if st.session_state.vital_import_aktiv:
      st.write("---")
      st.caption(
          "Exportiere deine Daten bei Garmin Connect (Einstellungen ›"
          " Daten exportieren) oder bei Google Fit / Health Connect (über"
          " Google Takeout) als CSV und lade die Datei hier hoch."
      )
      csv_upload = st.file_uploader(
          "CSV-Datei auswählen", type=["csv"], key="vital_csv_upload"
      )
      if csv_upload is not None:
        try:
          import_df = pd.read_csv(csv_upload)
          st.write("Vorschau:")
          st.dataframe(import_df.head(), use_container_width=True)

          spalten = import_df.columns.tolist()
          keine_option = "– keine –"
          datum_spalte = st.selectbox(
              "Welche Spalte enthält das Datum?",
              spalten,
              key="csv_datum_spalte",
          )
          schritte_spalte = st.selectbox(
              "Welche Spalte enthält die Schritte? (optional)",
              [keine_option] + spalten,
              key="csv_schritte_spalte",
          )
          gewicht_spalte = st.selectbox(
              "Welche Spalte enthält das Gewicht in kg? (optional)",
              [keine_option] + spalten,
              key="csv_gewicht_spalte",
          )
          vo2max_spalte = st.selectbox(
              "Welche Spalte enthält VO2max? (optional)",
              [keine_option] + spalten,
              key="csv_vo2max_spalte",
          )

          if st.button(
              "Importieren", key="csv_import_btn", type="primary"
          ):
            neue_zeilen = pd.DataFrame()
            neue_zeilen["Datum"] = pd.to_datetime(
                import_df[datum_spalte], errors="coerce"
            ).dt.strftime("%Y-%m-%d")
            neue_zeilen["Schritte"] = (
                pd.to_numeric(
                    import_df[schritte_spalte], errors="coerce"
                )
                if schritte_spalte != keine_option
                else None
            )
            neue_zeilen["Gewicht"] = (
                pd.to_numeric(
                    import_df[gewicht_spalte], errors="coerce"
                )
                if gewicht_spalte != keine_option
                else None
            )
            neue_zeilen["VO2max"] = (
                pd.to_numeric(
                    import_df[vo2max_spalte], errors="coerce"
                )
                if vo2max_spalte != keine_option
                else None
            )
            neue_zeilen = neue_zeilen.dropna(subset=["Datum"])
            st.session_state.vitaldaten = pd.concat(
                [st.session_state.vitaldaten, neue_zeilen],
                ignore_index=True,
            )
            st.session_state.vital_import_aktiv = False
            st.success(f"{len(neue_zeilen)} Zeilen importiert!")
            st.rerun()
        except Exception as e:
          st.error(f"CSV konnte nicht gelesen werden: {e}")

      if st.button("Abbrechen", key="vital_import_cancel_btn"):
        st.session_state.vital_import_aktiv = False
        st.rerun()

  st.write("---")
  st.write("### 📒 Ergänzende Trainingsnotizen")

  UEBUNG_UNTERKATEGORIEN = {
      "Ausdauer": AUSDAUER_UNTERKATEGORIEN,
      "Kraft": KRAFT_UNTERKATEGORIEN,
      "Beweglichkeit": BEWEGLICHKEIT_UNTERKATEGORIEN,
      "Balance": BALANCE_UNTERKATEGORIEN,
      "Ernährung": ERNAEHRUNG_UNTERKATEGORIEN,
      "Gesamtbefinden": GESAMTBEFINDEN_UNTERKATEGORIEN,
  }

  tab_protokoll, tab_uebungen = st.tabs(
      ["Tagebuch-Einträge", "Eigene Übungen (Name, Sätze, Wiederholungen, Dauer)"]
  )

  with tab_protokoll:
    if not df.empty:
      st.markdown("#### 🔍 Tagebuch filtern")
      with st.container(key="protokoll_filter_row"):
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
          p_kategorie = st.selectbox(
              "Kategorie", ["Alle Kategorien"] + ARSENAL_KATEGORIEN,
              key="protokoll_filter_kategorie",
          )
        with p_col2:
          if p_kategorie == "Alle Kategorien":
            p_unterkategorie_optionen = sorted(
                df["Unterkategorie"].dropna().unique().tolist()
            )
          else:
            p_unterkategorie_optionen = UEBUNG_UNTERKATEGORIEN.get(
                p_kategorie, []
            )
          p_unterkategorie = st.selectbox(
              "Unterkategorie",
              ["Alle Unterkategorien"] + list(p_unterkategorie_optionen),
              key="protokoll_filter_unterkategorie",
          )
        with p_col3:
          p_zeitraum = st.selectbox(
              "Zeitraum",
              ["Alle", "Heute", "Letzte Woche", "Letzter Monat",
               "Letzte 3 Monate", "Letztes Jahr"],
              key="protokoll_filter_zeitraum",
          )

      gefilterter_df = df.copy()
      if p_kategorie != "Alle Kategorien":
        gefilterter_df = gefilterter_df[
            gefilterter_df["Kategorie"] == p_kategorie
        ]
      if p_unterkategorie != "Alle Unterkategorien":
        gefilterter_df = gefilterter_df[
            gefilterter_df["Unterkategorie"] == p_unterkategorie
        ]
      if p_zeitraum == "Heute":
        gefilterter_df = gefilterter_df[gefilterter_df["Datum"] == str(heute)]
      elif p_zeitraum != "Alle":
        zeitraum_tage = {
            "Letzte Woche": 7,
            "Letzter Monat": 30,
            "Letzte 3 Monate": 90,
            "Letztes Jahr": 365,
        }[p_zeitraum]
        stichtag = str(heute - datetime.timedelta(days=zeitraum_tage))
        gefilterter_df = gefilterter_df[gefilterter_df["Datum"] >= stichtag]

      st.caption(f"{len(gefilterter_df)} von {len(df)} Einträgen")
      st.dataframe(
          gefilterter_df.sort_values("Datum", ascending=False),
          use_container_width=True,
          column_config={
              "Verknüpftes Bild": st.column_config.ImageColumn(
                  "Verknüpftes Bild"
              ),
              "Verknüpfter Link": st.column_config.LinkColumn(
                  "Verknüpfter Link"
              ),
          },
      )

      @st.cache_data
      def convert_df_to_excel(dataframe):
        from io import BytesIO

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
          dataframe.to_excel(writer, index=False, sheet_name="Protokoll")
        return output.getvalue()

      excel_data = convert_df_to_excel(gefilterter_df)
      st.download_button(
          label="📥 Als Excel-Datei herunterladen",
          data=excel_data,
          file_name="Sport_Tagebuch.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      )
    else:
      st.info("Noch keine Einträge vorhanden.")

  with tab_uebungen:
    st.caption(
        "Alle Übungen an einem Ort: Kategorie, Unterkategorie, Sätze/"
        " Wiederholungen, Dauer, Notizen, Link und Bild."
    )

    col_u1, col_u2 = st.columns(2)
    with col_u1:
      if st.button(
          "＋ Übung erfassen", key="btn_open_uebung_form",
          type="primary", use_container_width=True,
      ):
        st.session_state.eigene_uebung_form_aktiv = True
        st.session_state.eigene_uebung_import_aktiv = False
        st.rerun()
    with col_u2:
      if st.button(
          "⬆️ Excel importieren", key="btn_open_uebung_import",
          use_container_width=True,
      ):
        st.session_state.eigene_uebung_import_aktiv = True
        st.session_state.eigene_uebung_form_aktiv = False
        st.rerun()

    if st.session_state.eigene_uebung_form_aktiv:
      st.write("---")
      u_kategorie = st.selectbox(
          "Kategorie", list(UEBUNG_UNTERKATEGORIEN.keys()),
          key="uebung_kategorie_input",
      )
      u_unterkategorie = st.selectbox(
          "Unterkategorie", UEBUNG_UNTERKATEGORIEN[u_kategorie],
          key=f"uebung_unterkategorie_input_{u_kategorie}",
      )
      u_unterkategorie = handle_sonstiges_unterkategorie(
          u_unterkategorie, f"uebung_{u_kategorie}"
      )
      u_datum = st.date_input("Datum", value=heute, key="uebung_datum_input")
      u_dauer = st.number_input(
          "Dauer (Minuten) – optional", min_value=0, max_value=300,
          value=None, key="uebung_dauer_input",
      )
      u_saetze = st.number_input(
          "Sätze – optional", min_value=0, max_value=50, value=None,
          key="uebung_saetze_input",
      )
      u_wiederholungen = st.number_input(
          "Wiederholungen – optional", min_value=0, max_value=1000,
          value=None, key="uebung_wiederholungen_input",
      )
      u_notizen = st.text_input("Notizen", key="uebung_notizen_input")
      u_link = st.text_input("Link – optional", key="uebung_link_input")
      u_bild_upload = st.file_uploader(
          "Bild – optional", type=["png", "jpg", "jpeg"],
          key="uebung_bild_input",
      )

      col_us1, col_us2 = st.columns(2)
      with col_us1:
        uebung_save = st.button(
            "Speichern", key="uebung_save_btn", type="primary",
            use_container_width=True,
        )
      with col_us2:
        uebung_cancel = st.button(
            "Abbrechen", key="uebung_cancel_btn", use_container_width=True
        )
      if uebung_save:
        u_bild_data_uri = ""
        if u_bild_upload is not None:
          u_bild_b64 = base64.b64encode(u_bild_upload.getvalue()).decode(
              "utf-8"
          )
          u_bild_data_uri = f"data:{u_bild_upload.type};base64,{u_bild_b64}"

        neue_uebung = pd.DataFrame(
            [{
                "Datum": str(u_datum),
                "Kategorie": u_kategorie,
                "Unterkategorie": u_unterkategorie,
                "Dauer (Min.)": u_dauer,
                "Sätze": u_saetze,
                "Wiederholungen": u_wiederholungen,
                "Notizen": u_notizen.strip(),
                "Link": u_link.strip(),
                "Bild": u_bild_data_uri,
            }]
        )
        st.session_state.eigene_uebungen = pd.concat(
            [st.session_state.eigene_uebungen, neue_uebung],
            ignore_index=True,
        )
        st.session_state.eigene_uebung_form_aktiv = False
        st.success("Gespeichert!")
        st.rerun()
      if uebung_cancel:
        st.session_state.eigene_uebung_form_aktiv = False
        st.rerun()

    if st.session_state.eigene_uebung_import_aktiv:
      st.write("---")
      st.caption(
          "Lade eine Excel-Datei mit deinen eigenen Übungen hoch (z.B."
          " Export aus einer Trainings-App oder einer eigenen Tabelle)."
      )
      excel_upload = st.file_uploader(
          "Excel-Datei auswählen", type=["xlsx", "xls"],
          key="uebung_excel_upload",
      )
      if excel_upload is not None:
        try:
          import_df = pd.read_excel(excel_upload)
          st.write("Vorschau:")
          st.dataframe(import_df.head(), use_container_width=True)

          spalten = import_df.columns.tolist()
          keine_option = "– keine –"
          u_datum_spalte = st.selectbox(
              "Welche Spalte enthält das Datum?", spalten,
              key="uebung_import_datum_spalte",
          )
          u_kategorie_spalte = st.selectbox(
              "Welche Spalte enthält die Kategorie?", spalten,
              key="uebung_import_kategorie_spalte",
          )
          u_unterkategorie_spalte = st.selectbox(
              "Welche Spalte enthält die Unterkategorie?",
              [keine_option] + spalten,
              key="uebung_import_unterkategorie_spalte",
          )
          u_dauer_spalte = st.selectbox(
              "Welche Spalte enthält die Dauer in Minuten? (optional)",
              [keine_option] + spalten, key="uebung_import_dauer_spalte",
          )
          u_saetze_spalte = st.selectbox(
              "Welche Spalte enthält die Sätze? (optional)",
              [keine_option] + spalten, key="uebung_import_saetze_spalte",
          )
          u_wdh_spalte = st.selectbox(
              "Welche Spalte enthält die Wiederholungen? (optional)",
              [keine_option] + spalten, key="uebung_import_wdh_spalte",
          )
          u_notizen_spalte = st.selectbox(
              "Welche Spalte enthält Notizen? (optional)",
              [keine_option] + spalten, key="uebung_import_notizen_spalte",
          )
          u_link_spalte = st.selectbox(
              "Welche Spalte enthält den Link? (optional)",
              [keine_option] + spalten, key="uebung_import_link_spalte",
          )

          if st.button(
              "Importieren", key="uebung_import_btn", type="primary"
          ):
            neue_zeilen = pd.DataFrame()
            neue_zeilen["Datum"] = pd.to_datetime(
                import_df[u_datum_spalte], errors="coerce"
            ).dt.strftime("%Y-%m-%d")
            neue_zeilen["Kategorie"] = import_df[u_kategorie_spalte]
            neue_zeilen["Unterkategorie"] = (
                import_df[u_unterkategorie_spalte]
                if u_unterkategorie_spalte != keine_option
                else ""
            )
            neue_zeilen["Dauer (Min.)"] = (
                pd.to_numeric(import_df[u_dauer_spalte], errors="coerce")
                if u_dauer_spalte != keine_option
                else None
            )
            neue_zeilen["Sätze"] = (
                pd.to_numeric(import_df[u_saetze_spalte], errors="coerce")
                if u_saetze_spalte != keine_option
                else None
            )
            neue_zeilen["Wiederholungen"] = (
                pd.to_numeric(import_df[u_wdh_spalte], errors="coerce")
                if u_wdh_spalte != keine_option
                else None
            )
            neue_zeilen["Notizen"] = (
                import_df[u_notizen_spalte]
                if u_notizen_spalte != keine_option
                else ""
            )
            neue_zeilen["Link"] = (
                import_df[u_link_spalte]
                if u_link_spalte != keine_option
                else ""
            )
            neue_zeilen["Bild"] = ""
            neue_zeilen = neue_zeilen.dropna(subset=["Datum", "Kategorie"])
            st.session_state.eigene_uebungen = pd.concat(
                [st.session_state.eigene_uebungen, neue_zeilen],
                ignore_index=True,
            )
            st.session_state.eigene_uebung_import_aktiv = False
            st.success(f"{len(neue_zeilen)} Zeilen importiert!")
            st.rerun()
        except Exception as e:
          st.error(f"Excel-Datei konnte nicht gelesen werden: {e}")

      if st.button("Abbrechen", key="uebung_import_cancel_btn"):
        st.session_state.eigene_uebung_import_aktiv = False
        st.rerun()

    uebungen_df = st.session_state.eigene_uebungen
    if uebungen_df.empty:
      st.info("Noch keine eigenen Übungen erfasst.")
    else:
      uebungen_kategorien = list(UEBUNG_UNTERKATEGORIEN.keys())
      uebungen_icons = {
          "Ausdauer": "🏃‍♂️",
          "Kraft": "🏋️‍♂️",
          "Beweglichkeit": beweglichkeit_icon_html(26),
          "Balance": balance_icon_html(26),
          "Ernährung": "🍽️",
          "Gesamtbefinden": "😊",
      }

      u_kat_col1, u_kat_col2, u_kat_col3, u_kat_col4, u_kat_col5, u_kat_col6 = (
          st.columns(6)
      )
      for spalte, kat in zip(
          [u_kat_col1, u_kat_col2, u_kat_col3, u_kat_col4, u_kat_col5,
           u_kat_col6],
          uebungen_kategorien,
      ):
        with spalte:
          anzahl = len(uebungen_df[uebungen_df["Kategorie"] == kat])
          render_arsenal_tile(
              uebungen_icons.get(kat, "📌"), kat, anzahl,
              state_key="uebungen_detail_kat", button_prefix="uebungtile",
          )

      # Detail-Liste für die angeklickte Kategorie
      aktive_uebungen_kat = st.session_state.get("uebungen_detail_kat")
      if aktive_uebungen_kat is not None:
        kat_eintraege = uebungen_df[
            uebungen_df["Kategorie"] == aktive_uebungen_kat
        ]
        st.write("---")
        st.markdown(f"#### {aktive_uebungen_kat} ({len(kat_eintraege)})")
        if kat_eintraege.empty:
          st.info(f"Noch keine Einträge für {aktive_uebungen_kat}.")
        else:
          anzeige_spalten = [
              c
              for c in [
                  "Datum", "Unterkategorie", "Dauer (Min.)", "Sätze",
                  "Wiederholungen", "Notizen", "Link", "Bild",
              ]
              if c in kat_eintraege.columns
          ]
          st.dataframe(
              kat_eintraege[anzeige_spalten].sort_values("Datum"),
              use_container_width=True,
              hide_index=True,
              column_config={
                  "Bild": st.column_config.ImageColumn("Bild"),
                  "Link": st.column_config.LinkColumn("Link"),
              },
          )
        if st.button("✕ Schließen", key="uebungen_detail_schliessen_btn"):
          st.session_state["uebungen_detail_kat"] = None
          st.rerun()

      # Falls Einträge eine Kategorie außerhalb der Standardliste haben
      sonstige_uebungen = uebungen_df[
          ~uebungen_df["Kategorie"].isin(uebungen_kategorien)
      ]
      if not sonstige_uebungen.empty:
        with st.expander(f"Sonstige Kategorien ({len(sonstige_uebungen)})"):
          st.dataframe(
              sonstige_uebungen,
              use_container_width=True,
              column_config={
                  "Bild": st.column_config.ImageColumn("Bild"),
                  "Link": st.column_config.LinkColumn("Link"),
              },
          )

      st.write("---")
      st.markdown("#### 🔍 Trainingsnotizen filtern")
      with st.container(key="uebungen_filter_row"):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
          f_kategorie = st.selectbox(
              "Kategorie", ["Alle Kategorien"] + uebungen_kategorien,
              key="uebungen_filter_kategorie",
          )
        with f_col2:
          if f_kategorie == "Alle Kategorien":
            f_unterkategorie_optionen = sorted(
                uebungen_df["Unterkategorie"].dropna().unique().tolist()
            )
          else:
            f_unterkategorie_optionen = UEBUNG_UNTERKATEGORIEN.get(
                f_kategorie, []
            )
          f_unterkategorie = st.selectbox(
              "Unterkategorie",
              ["Alle Unterkategorien"] + list(f_unterkategorie_optionen),
              key="uebungen_filter_unterkategorie",
          )
        with f_col3:
          f_zeitraum = st.selectbox(
              "Zeitraum",
              ["Alle", "Letzte Woche", "Letzter Monat", "Letztes Jahr"],
              key="uebungen_filter_zeitraum",
          )

      gefilterte_df = uebungen_df.copy()
      if f_kategorie != "Alle Kategorien":
        gefilterte_df = gefilterte_df[
            gefilterte_df["Kategorie"] == f_kategorie
        ]
      if f_unterkategorie != "Alle Unterkategorien":
        gefilterte_df = gefilterte_df[
            gefilterte_df["Unterkategorie"] == f_unterkategorie
        ]
      if f_zeitraum != "Alle":
        zeitraum_tage = {
            "Letzte Woche": 7,
            "Letzter Monat": 30,
            "Letztes Jahr": 365,
        }[f_zeitraum]
        stichtag = str(heute - datetime.timedelta(days=zeitraum_tage))
        gefilterte_df = gefilterte_df[gefilterte_df["Datum"] >= stichtag]

      st.caption(f"{len(gefilterte_df)} von {len(uebungen_df)} Einträgen")
      if gefilterte_df.empty:
        st.info("Keine Einträge für die gewählten Filter gefunden.")
      else:
        f_anzeige_spalten = [
            c
            for c in [
                "Datum", "Kategorie", "Unterkategorie", "Dauer (Min.)",
                "Sätze", "Wiederholungen", "Notizen", "Link", "Bild",
            ]
            if c in gefilterte_df.columns
        ]
        st.dataframe(
            gefilterte_df[f_anzeige_spalten].sort_values(
                "Datum", ascending=False
            ),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Bild": st.column_config.ImageColumn("Bild"),
                "Link": st.column_config.LinkColumn("Link"),
            },
        )

      st.write("")

      @st.cache_data
      def convert_uebungen_df_to_excel(dataframe):
        from io import BytesIO

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
          dataframe.to_excel(
              writer, index=False, sheet_name="Eigene Übungen"
          )
        return output.getvalue()

      uebungen_excel_data = convert_uebungen_df_to_excel(uebungen_df)
      st.download_button(
          label="📥 Als Excel-Datei herunterladen",
          data=uebungen_excel_data,
          file_name="Eigene_Uebungen.xlsx",
          mime=(
              "application/vnd.openxmlformats-officedocument"
              ".spreadsheetml.sheet"
          ),
          key="uebungen_download_btn",
      )

# ----------------------------------------------------
# 2. ÜBUNGSARSENAL (direkt unter dem Tagebuch, keine eigene Seite mehr)
# ----------------------------------------------------
if True:
  st.write("---")
  st.title("🏋️‍♀️ Übungsarsenal")
  st.write("Deine Sammlung von Links, Bereichen und Übungs-Hinweisen.")

  with st.container(key="arsenalcard"):
    if st.session_state.arsenal.empty:
      st.info("Noch keine Einträge im Übungsarsenal.")
    else:
      arsenal_df = st.session_state.arsenal
      arsenal_icons = {
          "Ausdauer": "🏃‍♂️",
          "Kraft": "🏋️‍♂️",
          "Beweglichkeit": beweglichkeit_icon_html(26),
          "Balance": balance_icon_html(26),
          "Ernährung": "🍽️",
          "Gesamtbefinden": "😊",
      }

      a_col1, a_col2, a_col3, a_col4, a_col5, a_col6 = st.columns(6)
      for spalte, kat in zip(
          [a_col1, a_col2, a_col3, a_col4, a_col5, a_col6],
          ARSENAL_KATEGORIEN,
      ):
        with spalte:
          anzahl = len(arsenal_df[arsenal_df["Kategorie"] == kat])
          render_arsenal_tile(arsenal_icons.get(kat, "📌"), kat, anzahl)

      # Detail-Liste für die angeklickte Kategorie
      aktive_kat = st.session_state.get("arsenal_detail_kat")
      if aktive_kat is not None:
        kat_eintraege = arsenal_df[arsenal_df["Kategorie"] == aktive_kat]
        st.write("---")
        st.markdown(f"#### {aktive_kat} ({len(kat_eintraege)})")
        if kat_eintraege.empty:
          st.info(f"Noch keine Einträge für {aktive_kat}.")
        else:
          for _, eintrag in kat_eintraege.iterrows():
            with st.container(border=True):
              st.markdown(
                  f"<div style='display:flex; justify-content:space-between;"
                  f" align-items:center; flex-wrap:wrap; gap:6px;'>"
                  f"<span style='font-weight:700; font-size:16px;'>"
                  f"{eintrag.get('Bereich / Übung', '')}</span>"
                  f"<span style='background:#e2efe3; color:#2f5e45;"
                  f" padding:2px 10px; border-radius:12px; font-size:12px;"
                  f" font-weight:600; white-space:nowrap;'>"
                  f"{eintrag.get('Typ', '')}</span></div>",
                  unsafe_allow_html=True,
              )
              if eintrag.get("Beschreibung"):
                st.write(eintrag["Beschreibung"])
              if eintrag.get("Link"):
                st.markdown(f"🔗 [{eintrag['Link']}]({eintrag['Link']})")
              if eintrag.get("Bild"):
                st.image(eintrag["Bild"], use_container_width=True)
        if st.button("✕ Schließen", key="arsenal_detail_schliessen_btn"):
          st.session_state["arsenal_detail_kat"] = None
          st.rerun()

      # Falls Einträge eine Kategorie außerhalb der Standardliste haben
      # (z.B. durch ältere Daten), trotzdem anzeigen statt zu verschlucken
      sonstige = arsenal_df[~arsenal_df["Kategorie"].isin(ARSENAL_KATEGORIEN)]
      if not sonstige.empty:
        with st.expander(f"Sonstige ({len(sonstige)})"):
          for _, eintrag in sonstige.iterrows():
            with st.container(border=True):
              st.markdown(f"**{eintrag.get('Bereich / Übung', '')}**")
              if eintrag.get("Beschreibung"):
                st.write(eintrag["Beschreibung"])
              if eintrag.get("Link"):
                st.markdown(f"🔗 [{eintrag['Link']}]({eintrag['Link']})")
              if eintrag.get("Bild"):
                st.image(eintrag["Bild"], use_container_width=True)

    st.write("")
    if "arsenal_form_aktiv" not in st.session_state:
      st.session_state.arsenal_form_aktiv = False

    if not st.session_state.arsenal_form_aktiv:
      if st.button(
          "＋ Neuen Link / Eintrag hinzufügen",
          key="btn_open_arsenal_form",
          type="primary",
          use_container_width=True,
      ):
        st.session_state.arsenal_form_aktiv = True
        st.rerun()
    else:
      st.subheader("Neuen Link / Eintrag hinzufügen")
      kategorie = st.selectbox(
          "Kategorie", ARSENAL_KATEGORIEN, key="arsenal_kategorie"
      )
      titel = st.text_input(
          "Titel (z. B. \"Kräftigung Rumpfmuskulatur\")",
          key="arsenal_titel",
      )
      typ = st.selectbox("Typ", ARSENAL_TYPEN, key="arsenal_typ")
      link = st.text_input("Link / URL", key="arsenal_link")
      beschreibung = st.text_area(
          "Beschreibung / Notiz", key="arsenal_beschreibung"
      )
      bild_upload = st.file_uploader(
          "Screenshot / Bild zur Übung (optional)",
          type=["png", "jpg", "jpeg"],
          key="arsenal_bild",
      )

      col_a1, col_a2 = st.columns(2)
      with col_a1:
        arsenal_submitted = st.button(
            "Hinzufügen",
            key="arsenal_submit_btn",
            type="primary",
            use_container_width=True,
        )
      with col_a2:
        arsenal_cancelled = st.button(
            "Abbrechen",
            key="arsenal_cancel_btn",
            use_container_width=True,
        )

      if arsenal_submitted:
        bild_data_uri = ""
        if bild_upload is not None:
          bild_b64 = base64.b64encode(bild_upload.getvalue()).decode("utf-8")
          bild_data_uri = f"data:{bild_upload.type};base64,{bild_b64}"

        neuer_link = pd.DataFrame(
            [{
                "Kategorie": kategorie,
                "Typ": typ,
                "Bereich / Übung": titel,
                "Link": link,
                "Beschreibung": beschreibung,
                "Bild": bild_data_uri,
            }]
        )
        st.session_state.arsenal = pd.concat(
            [st.session_state.arsenal, neuer_link], ignore_index=True
        )
        st.session_state.arsenal_form_aktiv = False
        st.success("Erfolgreich hinzugefügt!")
        st.rerun()
      if arsenal_cancelled:
        st.session_state.arsenal_form_aktiv = False
        st.rerun()
