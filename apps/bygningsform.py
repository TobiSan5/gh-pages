import marimo

__generated_with = "0.12.8"
app = marimo.App(
    width="medium",
    app_title="Bygningsform",
    auto_download=["html"],
)


@app.cell
def _():
    import math as math

    import marimo as mo
    return math, mo


@app.cell
def _(
    bygn_del_tbl,
    etasje_h,
    etasjer_lst,
    etg_ant,
    etg_skiller_h,
    grunnflate,
    opt_bygn_del_tbl,
    opt_etg_ant,
    opt_grunnfl,
):
    sum_overfl = sum([_["areal"] for _ in bygn_del_tbl.data])
    bygn_volum = sum(it["BRA [m2]"] * etasje_h.value for it in etasjer_lst) +\
        (etg_ant - 1) * grunnflate.value * etg_skiller_h.value
    opt_sum_overfl = sum([_["areal"] for _ in opt_bygn_del_tbl.data])
    opt_bygn_volum = opt_grunnfl * etasje_h.value * opt_etg_ant +\
        (opt_etg_ant - 1) * opt_grunnfl * etg_skiller_h.value
    return bygn_volum, opt_bygn_volum, opt_sum_overfl, sum_overfl


@app.cell
def _(
    afl,
    bygn_del_tbl,
    bygn_volum,
    etasje_tabell,
    mo,
    opt_bygn_del_tbl,
    opt_bygn_volum,
    opt_etg_ant,
    opt_grunnfl,
    opt_sum_overfl,
    sum_overfl,
):
    mo.md(
        f"""
        # Beregning av byggets overflateeffektivitet og formfaktor
        ## Definisjoner
        - Overflateeffektivitet: overflate per volum [m2/m3]
        - Formfaktor: overflate per m2 oppvarmet BRA [m2/m2]
        ## Resultater (basert på utfylte inndata under)
        - $A_{{fl}}$: {afl.value} $m^2$
            {"".join([f"""- etg. {_['etg.']}: {_['BRA [m2]']}  
            """ for _ in etasje_tabell.data])}
        - $Sum\\:overflater$: {round(sum_overfl, 2)} $m^2$
            {"".join([f"""- {_['bygn. del']}: {round(_['areal'], 2)}  
            """ for _ in bygn_del_tbl.data])}
        - $Bygningsvolum$: {round(bygn_volum, 2)} $m^3$
        - $Overflateeffektivitet$: {round(sum_overfl / bygn_volum, 2)}
        - $Formfaktor$: {round(sum_overfl / afl.value, 2)}
        ### Optimaler
        - $A_{{fl}}$: {afl.value} $m^2$
            {"".join([f"""- etg. {_}: {round(opt_grunnfl, 2)}  
            """ for _ in range(1, int(opt_etg_ant) + 1)])}
        - $Sum\\:overflater$: {round(opt_sum_overfl, 2)} $m^2$
            {"".join([f"""- {_['bygn. del']}: {round(_['areal'], 2)}  
            """ for _ in opt_bygn_del_tbl.data])}    
        - $Bygningsvolum$: {round(opt_bygn_volum, 2)} $m^3$
        - $Overflateeffektivitet$: {round(opt_sum_overfl / opt_bygn_volum, 2)}
        - $Formfaktor$: {round(opt_sum_overfl / afl.value, 2)}    
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""## Inndata""")
    return


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
    grunnflate = mo.ui.number(start=10.0, stop=500.0, step=0.1, label="$grunnflate [m2]$")
    mo.md(text=f"""
        Boligens grunnflate (uten yttervegger):\n
        {grunnflate}
    """)
    return (grunnflate,)


@app.cell
def _(mo):
    etasje_h = mo.ui.number(start=2.1, stop=5.5, step=0.05, label="$etasjehøyde [m]$")
    mo.md(text=f"""
        Boligens etasjehøyde (eventuelt gjennomsnitt):\n
        {etasje_h}
    """)
    return (etasje_h,)


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
def _(mo):
    himl_h = mo.ui.number(start=0.05, stop=1.0, step=0.05, label="$høyde\\:[m]$")
    mo.md(
        f"""
        Boligens nedforing $himling\\:høyde$:  
        {himl_h}
        """)
    return (himl_h,)


@app.cell
def _(mo):
    mo.md("""## Utregninger""")
    return


@app.cell
def _(afl, grunnflate, math, mo, omkrets):
    # Aktuell etasjefordeling og omkrets

    if not afl.value  >= grunnflate.value:
        raise ValueError("Grunnflate går ikke opp i oppvarmet BRA")

    afl_rest = afl.value % grunnflate.value

    if afl_rest > 1 and afl_rest < 10:
        raise ValueError("Grunnflate gir en rest av oppvarmet BRA mellom 1 m2 og 10 m2")

    etasjer_lst = list()
    grunnflate_ant = int(afl.value // grunnflate.value)

    for _i in range(1, grunnflate_ant +1):
        etasjer_lst.append({"etg.": _i, "BRA [m2]": grunnflate.value, "omkrets": omkrets.value})
    if afl_rest >= 10:
        _skala = pow(afl_rest, 1/2) / math.pow(grunnflate.value, 1/2)
        toppetg_omkr = round(omkrets.value * _skala, 2)
        etasjer_lst.append({"etg.": grunnflate_ant + 1, "BRA [m2]": afl_rest, "omkrets": toppetg_omkr})

    etg_ant = len(etasjer_lst)

    etasje_tabell = mo.ui.table(data=etasjer_lst, label="Etasjefordeling")
    return (
        afl_rest,
        etasje_tabell,
        etasjer_lst,
        etg_ant,
        grunnflate_ant,
        toppetg_omkr,
    )


@app.cell
def _(etasje_tabell):
    etasje_tabell
    return


@app.cell
def _(afl, etasje_h, math, mo):
    # Optimale etasjefordeling og omkrets

    _etg_volum = afl.value * etasje_h.value
    _trerot = math.pow(_etg_volum, 1/3)
    _opt_min_etg_ant = _trerot // etasje_h.value
    _alt_lav = math.fabs(_trerot - _opt_min_etg_ant * etasje_h.value)
    _alt_høy = math.fabs(_trerot - (_opt_min_etg_ant + 1) * etasje_h.value)
    if _alt_lav < _alt_høy:
        opt_etg_ant = _opt_min_etg_ant
    else:
        opt_etg_ant = _opt_min_etg_ant + 1

    opt_etg_ant = int(opt_etg_ant)

    opt_grunnfl = round(afl.value / opt_etg_ant, 2)
    opt_omkrets = round(math.pow(opt_grunnfl, 1/2) * 4, 2)

    opt_etasjer_lst = list()

    for _i in range(1, opt_etg_ant +1):
        opt_etasjer_lst.append({"etg.": _i, "BRA [m2]": opt_grunnfl, "omkrets": opt_omkrets})

    opt_etasje_tabell = mo.ui.table(data=opt_etasjer_lst, label="Optimal etasjefordeling")
    return (
        opt_etasje_tabell,
        opt_etasjer_lst,
        opt_etg_ant,
        opt_grunnfl,
        opt_omkrets,
    )


@app.cell
def _(opt_etasje_tabell):
    opt_etasje_tabell
    return


@app.cell
def _(
    afl,
    awd_prs,
    etasje_h,
    etasje_tabell,
    etasjer_lst,
    etg_skiller_h,
    himl_h,
    mo,
):
    # Aktuell bygningsdelstabell

    # Målvariabler for cellen
    ytterv_ar = 0
    gulv_motgr_ar = 0
    vindu_og_dør_ar = 0
    tak_ar = 0

    _etasje_ar = [_['BRA [m2]'] for _ in etasje_tabell.data]
    _etasje_omkr = [_['omkrets'] for _ in etasje_tabell.data]

    # Loop gjennom etasje-omkretser og bruke omkrets og etasje høyde for å finne areal av yttervegger
    # Bruke omkrets og etasjeskiller mellom to etasjer for å legge til areal av dekkeforkant
    _etg_tell = 0  # variabel for å telle opp til to etasjer med etasjeskiller imellom
    for _omkr in _etasje_omkr:
        _etg_tell += 1
        ytterv_ar += _omkr * (etasje_h.value + himl_h.value)
        if _etg_tell == 2:
            ytterv_ar += _omkr * etg_skiller_h.value
            _etg_tell -= 1
    # Runde av areal av yttervegger
    ytterv_ar = round(ytterv_ar, 2)

    # Dør- og vindusareal regnes ut som prosentandel av A_fl
    vindu_og_dør_ar = round(afl.value * awd_prs.value / 100, 2)

    # Areal av gulv mot grunn er lik BRA mål for 1. etasje
    gulv_motgr_ar = round(etasjer_lst[0]["BRA [m2]"], 2)

    # Areal av tak er lik BRA mål for siste (øverste) etasje
    # Hvis øverste etasje har mindra BRA mål, så legges differansen til tak areal
    tak_ar = etasjer_lst[-1]["BRA [m2]"]
    if tak_ar < gulv_motgr_ar:
        tak_ar += etasjer_lst[-2]["BRA [m2]"] - tak_ar
    # Runde av tak areal
    tak_ar = round(tak_ar, 2)

    # check all variables
    #with mo.redirect_stdout():
    #    _var_dct = vars()
    #    _variables = sorted(
    #        [(k, v) for k, v in _var_dct.items() if k[0] != "_"], 
    #        key=lambda x: x[0]
    #    )
    #    for _var in _variables:
    #        print(f"{_var}")

    # Bygge data for bygningsdels tabell
    bygn_deler = list()
    bygn_deler.append({"bygn. del": "yttervegger", "areal": ytterv_ar})
    bygn_deler.append({"bygn. del": "dør og vindu", "areal": vindu_og_dør_ar})
    bygn_deler.append({"bygn. del": "gulv mot grunn", "areal": gulv_motgr_ar})
    bygn_deler.append({"bygn. del": "tak", "areal": tak_ar})

    bygn_del_tbl = mo.ui.table(data=bygn_deler, label="Bygningsdelstabell")
    return (
        bygn_del_tbl,
        bygn_deler,
        gulv_motgr_ar,
        tak_ar,
        vindu_og_dør_ar,
        ytterv_ar,
    )


@app.cell
def _(bygn_del_tbl):
    bygn_del_tbl
    return


@app.cell
def _(
    afl,
    awd_prs,
    etasje_h,
    etg_skiller_h,
    himl_h,
    mo,
    opt_etasje_tabell,
    opt_etasjer_lst,
):
    # Optimal bygningsdelstabell, basert på :opt_etasje_tabell:

    # Målvariabler for cellen
    opt_ytterv_ar = 0
    opt_gulv_motgr_ar = 0
    opt_vindu_og_dør_ar = 0
    opt_tak_ar = 0

    _etasje_ar = [_['BRA [m2]'] for _ in opt_etasje_tabell.data]
    _etasje_omkr = [_['omkrets'] for _ in opt_etasje_tabell.data]

    # Loop gjennom etasje-omkretser og bruke omkrets og etasje høyde for å finne areal av yttervegger
    # Bruke omkrets og etasjeskiller mellom to etasjer for å legge til areal av dekkeforkant
    _etg_tell = 0  # variabel for å telle opp til to etasjer med etasjeskiller imellom
    for _omkr in _etasje_omkr:
        _etg_tell += 1
        opt_ytterv_ar += _omkr * (etasje_h.value + himl_h.value)
        if _etg_tell == 2:
            opt_ytterv_ar += _omkr * etg_skiller_h.value
            _etg_tell -= 1
    # Runde av areal av yttervegger
    opt_ytterv_ar = round(opt_ytterv_ar, 2)

    # Dør- og vindusareal regnes ut som prosentandel av A_fl
    opt_vindu_og_dør_ar = round(afl.value * awd_prs.value / 100, 2)

    # Areal av gulv mot grunn er lik BRA mål for 1. etasje
    opt_gulv_motgr_ar = round(opt_etasjer_lst[0]["BRA [m2]"], 2)

    # Areal av tak er lik BRA mål for siste (øverste) etasje
    # Hvis øverste etasje har mindra BRA mål, så legges differansen til tak areal
    opt_tak_ar = opt_etasjer_lst[-1]["BRA [m2]"]
    if opt_tak_ar < opt_gulv_motgr_ar:
        opt_tak_ar += opt_etasjer_lst[-2]["BRA [m2]"] - opt_tak_ar
    # Runde av tak areal
    opt_tak_ar = round(opt_tak_ar, 2)

    # Bygge data for bygningsdels tabell
    opt_bygn_deler = list()
    opt_bygn_deler.append({"bygn. del": "yttervegger", "areal": opt_ytterv_ar})
    opt_bygn_deler.append({"bygn. del": "dør og vindu", "areal": opt_vindu_og_dør_ar})
    opt_bygn_deler.append({"bygn. del": "gulv mot grunn", "areal": opt_gulv_motgr_ar})
    opt_bygn_deler.append({"bygn. del": "tak", "areal": opt_tak_ar})

    opt_bygn_del_tbl = mo.ui.table(data=opt_bygn_deler, label="Optimal bygningsdelstabell")
    return (
        opt_bygn_del_tbl,
        opt_bygn_deler,
        opt_gulv_motgr_ar,
        opt_tak_ar,
        opt_vindu_og_dør_ar,
        opt_ytterv_ar,
    )


@app.cell
def _(opt_bygn_del_tbl):
    opt_bygn_del_tbl
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
