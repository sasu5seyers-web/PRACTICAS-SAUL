def vf(valor):
    return 'V' if valor else 'F'


def genera_tabla():
    print("P | Q | ~P | P ^ Q | P v Q |  P -> Q | P <-> Q")


    for p, q in [[1, 1], [1, 0], [0, 1], [0, 0]]:

        neg = not p
        conj = p and q
        disy = p or q
        cond = (not p) or q
        bicond = p == q

        print(
            f"{vf(p)} | {vf(q)} | "
            f" {vf(neg)} |"
            f"   {vf(conj)}   |"
            f"   {vf(disy)}   |"
            f"   {vf(cond)}   |"
            f"    {vf(bicond)}"
        )


genera_tabla()