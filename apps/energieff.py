import marimo

__generated_with = "0.12.8"
app = marimo.App(
    width="medium",
    app_title="Bygningsform",
    auto_download=["html"],
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(
    bygn_del_tbl,
    etasje_h,
    etasjer_lst,
    etg_ant,
    etg_skiller_h,
    grunnflate,
    opt_etg_ant,
    opt_grunnfl,
):
    sum_overfl = sum([_["areal"] for _ in bygn_del_tbl.data])
    bygn_volum = sum(it["BRA [m2]"] * etasje_h.value for it in etasjer_lst) +\
        (etg_ant - 1) * grunnflate.value * etg_skiller_h.value
    opt_sum_overfl = sum([_["opt. areal"] for _ in bygn_del_tbl.data])
    opt_bygn_volum = opt_grunnfl * etasje_h.value * opt_etg_ant +\
        (opt_etg_ant - 1) * opt_grunnfl * etg_skiller_h.value
    return bygn_volum, opt_bygn_volum, opt_sum_overfl, sum_overfl


@app.cell
def _(afl, bygn_volum, mo, opt_bygn_volum, opt_sum_overfl, sum_overfl):
    mo.md(
        f"""
        # Beregning av byggets overflateeffektivitet og formfaktor
        ## Definisjoner
        - Overflateeffektivitet: overflate per volum [m2/m3]
        - Formfaktor: overflate per m2 oppvarmet BRA [m2/m2]
        ## Resultater (basert på 'Norgeshus Demobolig', rediger inndata lengre ned for andre resultater)
        - $A_{{fl}}$: {afl.value} $m^2$
        - $Sum\\:overflater$: {round(sum_overfl, 2)} $m^2$
        - $Bygningsvolum$: {bygn_volum} $m^3$
        - $Overflateeffektivitet$: {round(sum_overfl / bygn_volum, 2)}
        - $Formfaktor$: {round(sum_overfl / afl.value, 2)}
        ### Optimaler
        - $Sum\\:overflater$: {round(opt_sum_overfl, 2)} $m^2$
        - $Bygningsvolum$: {opt_bygn_volum} $m^3$
        - $Overflateeffektivitet$: {round(opt_sum_overfl / opt_bygn_volum, 2)}
        - $Formfaktor$: {round(opt_sum_overfl / afl.value, 2)}    
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        f"""
        ## Utviklingsressurser
        Marimo API: https://docs.marimo.io/api/
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        f"""
        ## Inndata og beregninger
        """
    )
    return


@app.cell
def _(mo):
    grunnflate = mo.ui.number(start=10.0, stop=500.0, step=0.1, label="$grunnflate [m2]$")
    mo.md(text=f"""
        Boligens grunnflate:\n
        {grunnflate}
    """)
    return (grunnflate,)


@app.cell
def _(mo):
    etasje_h = mo.ui.number(start=2.1, stop=5.5, step=0.05, label="$etasjehøyde [m]$")
    mo.md(text=f"""
        Boligens etasjehøyde:\n
        {etasje_h}
    """)
    return (etasje_h,)


@app.cell
def _(mo):
    afl = mo.ui.number(start=10.0, stop=750.0, step=0.1, label="$A_{fl} [m2]$")
    mo.md(text=f"""
        Boligens oppvarmet BRA:\n
        {afl}
    """)
    return (afl,)


@app.cell
def _(mo):
    omkrets = mo.ui.number(start=12.0, stop=120.0, step=0.1, label="$omkrets [m]$")
    mo.md(text=f"""
        Boligens eksponerte omkrets:\n
        {omkrets}
    """)
    return (omkrets,)


@app.cell
def _(mo):
    etg_skiller_h = mo.ui.number(start=0.15, stop=0.5, step=0.05, label="$høyde etasjeskiller [m]$")
    mo.md(text=f"""
        Boligens etasjeskiller høyde:\n
        {etg_skiller_h}
    """)
    return (etg_skiller_h,)


@app.cell
def _(mo):
    awd_prs = mo.ui.number(start=10.0, stop=60.0, step=0.1, label="$vindu-og-dør-andel [prosent]$")
    mo.md(text=f"""
        Boligens andelsprosent vindu og dører av $A_{{fl}}$:\n
        {awd_prs}
    """)
    return (awd_prs,)


@app.cell
def _(afl, grunnflate, mo):
    if not afl.value  >= grunnflate.value:
        raise ValueError("Grunnflate går ikke opp i oppvarmet BRA")

    afl_rest = afl.value % grunnflate.value

    if afl_rest > 1 and afl_rest < 10:
        raise ValueError("Grunnflate gir en rest av oppvarmet BRA mellom 1 m2 og 10 m2")

    etasjer_lst = list()
    grunnflate_ant = int(afl.value // grunnflate.value)

    for _i in range(1, grunnflate_ant +1):
        etasjer_lst.append({"etg.": _i, "BRA [m2]": grunnflate.value})
    if afl_rest >= 10:
        etasjer_lst.append({"etg.": grunnflate_ant + 1, "BRA [m2]": afl_rest})

    etasje_tabell = mo.ui.table(data=etasjer_lst)
    etg_ant = len(etasjer_lst)
    return afl_rest, etasje_tabell, etasjer_lst, etg_ant, grunnflate_ant


@app.cell
def _(etasje_tabell):
    etasje_tabell
    return


@app.cell
def _(
    afl,
    awd_prs,
    etasje_h,
    etasjer_lst,
    etg_ant,
    etg_skiller_h,
    grunnflate,
    mo,
    omkrets,
):
    import math
    areal_dekkeforkant = omkrets.value * etg_skiller_h.value
    areal_ytterv_grunnfl = grunnflate.value * etg_ant * etasje_h.value
    if etg_ant > 1:
        _areal_rest = etasjer_lst[-1]["BRA [m2]"]
        _areal_grf = etasjer_lst[-2]["BRA [m2]"]
        if _areal_rest < _areal_grf:
            _skala = math.sqrt(_areal_rest) / math.sqrt(_areal_grf)
        else:
            _skala = 0
        omkrets_toppetg = omkrets.value * _skala
    else:
        omkrets_toppetg = 0
    areal_ytterv_toppetg = omkrets_toppetg * etasje_h.value
    areal_vindudør = afl.value * awd_prs.value / 100
    areal_ytterv = areal_dekkeforkant + areal_ytterv_grunnfl + areal_ytterv_toppetg - areal_vindudør

    # Optimaler
    _etg_volum = afl.value * etasje_h.value
    _trerot = math.pow(_etg_volum, 1/3)
    opt_etg_ant = _trerot // etasje_h.value
    opt_grunnfl = afl.value / opt_etg_ant
    opt_omkrets = pow(opt_grunnfl, 1/2) * 4
    opt_yttervegg = opt_omkrets * opt_etg_ant * etasje_h.value +\
        opt_omkrets * (opt_etg_ant - 1) * etg_skiller_h.value -\
        areal_vindudør

    bygn_deler = list()
    bygn_deler.append({"bygn. del": "yttervegger", "areal": areal_ytterv, "opt. areal": opt_yttervegg})
    bygn_deler.append({"bygn. del": "dør og vindu", "areal": areal_vindudør, "opt. areal": areal_vindudør})
    bygn_deler.append({"bygn. del": "gulv mot grunn", "areal": grunnflate.value, "opt. areal": opt_grunnfl})
    bygn_deler.append({"bygn. del": "tak", "areal": etasjer_lst[-1]["BRA [m2]"], "opt. areal": opt_grunnfl})

    bygn_del_tbl = mo.ui.table(data=bygn_deler)

    return (
        areal_dekkeforkant,
        areal_vindudør,
        areal_ytterv,
        areal_ytterv_grunnfl,
        areal_ytterv_toppetg,
        bygn_del_tbl,
        bygn_deler,
        math,
        omkrets_toppetg,
        opt_etg_ant,
        opt_grunnfl,
        opt_omkrets,
        opt_yttervegg,
    )


@app.cell
def _(bygn_del_tbl):
    bygn_del_tbl
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
