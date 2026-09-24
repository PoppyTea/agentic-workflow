"""Weryfikacja liczb z noty `research/workflow/2026-09-21-dox-bench-note.md`.

Każde twierdzenie z noty jest tu wpisane jako oczekiwana wartość i przeliczane od zera
z surowych transkryptów. Skrypt kończy się kodem 1, jeśli cokolwiek się nie zgadza, więc
nadaje się na bramkę.

    python3 verify.py                     # czysta biblioteka standardowa
    uvx --with scipy python3 verify.py    # dodatkowo kontrola krzyżowa przez scipy

Ekstrakcja jest niezależna od `analyze.py`: parsujemy bloki `tool_use` z `message.content`,
a nie tekst JSON regexem. Ta druga droga zawiodła w tym projekcie dwa razy — `429` jako
podciąg transkryptu i `"file_path":"` bez spacji, której `json.dumps` nie produkuje.
"""

from __future__ import annotations

import json
import os
import re
import sys
from itertools import combinations
from math import comb, fsum
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROUND2 = HERE / "results"
BACKUP = Path("/home/lis/projekty/14_moje_workflow/02_aid4u-bench/_results-backup")
VARIANTS = ("with-dox", "no-dox", "pointer-dox", "symlink-dox")
DERAILED = {"with-dox-4", "with-dox-5", "with-dox-10"}

STRATEGY_RE = re.compile(r"/strategy/[\w./-]+\.md|[\w.-]+_strategy\.md")
RULES_RE = re.compile(r"rules_strategy\.md|/strategy/rules/")
TESTFILE_RE = re.compile(r"test_\w+\.py")


# ── ekstrakcja ────────────────────────────────────────────────────────────────

def tool_inputs(path: Path):
    """Wejścia każdego wywołania narzędzia, z parsowania bloków — nie z regexa po JSON."""
    for line in path.open(encoding="utf-8"):
        msg = json.loads(line).get("message")
        if not isinstance(msg, dict):
            continue
        for block in msg.get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name"), (block.get("input") or {})


def result_line(path: Path) -> dict:
    last = None
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        if d.get("type") == "result":
            last = d
    if last is None:
        raise ValueError(f"brak linii result: {path}")
    return last


def load(path: Path) -> dict:
    name = path.name[:-6]
    variant = name.rsplit("-", 1)[0]
    res = result_line(path)
    paths, read_paths = [], []
    for tname, inp in tool_inputs(path):
        vals = [v for k, v in inp.items() if k in ("file_path", "path", "pattern", "command")
                and isinstance(v, str)]
        paths += vals
        if tname == "Read":
            read_paths += vals
    blob, read_blob = " ".join(paths), " ".join(read_paths)
    meta = path.with_suffix(".meta").read_text(encoding="utf-8")
    diff_path = path.with_suffix(".diff")
    diff = diff_path.read_text(encoding="utf-8") if diff_path.exists() else ""
    return dict(
        run=name, variant=variant, derailed=name in DERAILED,
        turns=res["num_turns"], cost=res["total_cost_usd"],
        mins=res["duration_ms"] / 60000, reads=sum(1 for n, _ in tool_inputs(path) if n == "Read"),
        flag="FLAGA: tak" in meta,
        contact_any=bool(STRATEGY_RE.search(blob)),
        contact_read=bool(STRATEGY_RE.search(read_blob)),
        rules=bool(RULES_RE.search(blob)),
        dox_pass="AGENTS.md" in diff,
        own_tests=bool(TESTFILE_RE.search(diff)),
        data_output="data/output" in diff,
    )


def load_all(directory: Path) -> list[dict]:
    if not directory.is_dir():
        return []
    return sorted((load(p) for p in directory.glob("*.jsonl")), key=lambda r: r["run"])


# ── statystyka (dokładna, bez przybliżeń) ─────────────────────────────────────

def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Dokładny test Fishera dla tabeli [[a,b],[c,d]], suma ogonów p <= p_obs."""
    n = a + b + c + d
    row1, col1 = a + b, a + c
    prob = lambda k: comb(row1, k) * comb(n - row1, col1 - k) / comb(n, col1)
    obs = prob(a)
    lo, hi = max(0, col1 - (n - row1)), min(row1, col1)
    return min(1.0, fsum(prob(k) for k in range(lo, hi + 1) if prob(k) <= obs * (1 + 1e-12)))


def permutation_p(xs: list[float], ys: list[float], stat=None) -> float:
    """Dokładny dwustronny test permutacyjny przez pełną enumerację podziałów."""
    stat = stat or (lambda g: fsum(g) / len(g))
    pool = xs + ys
    nx = len(xs)
    obs = abs(stat(xs) - stat(ys))
    idx = range(len(pool))
    hit = total = 0
    for pick in combinations(idx, nx):
        sel = set(pick)
        g1 = [pool[i] for i in idx if i in sel]
        g2 = [pool[i] for i in idx if i not in sel]
        total += 1
        if abs(stat(g1) - stat(g2)) >= obs - 1e-12:
            hit += 1
    return hit / total


def median(a: list[float]) -> float:
    s = sorted(a)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def pearson(xs: list[float], ys: list[float]) -> float:
    mx, my = fsum(xs) / len(xs), fsum(ys) / len(ys)
    cov = fsum((a - mx) * (b - my) for a, b in zip(xs, ys))
    vx = fsum((a - mx) ** 2 for a in xs)
    vy = fsum((b - my) ** 2 for b in ys)
    return cov / (vx * vy) ** 0.5


def holm(pairs: list[tuple[str, float]]) -> list[tuple[str, float, float]]:
    """Holm-Bonferroni: zwraca (nazwa, p, p_skorygowane) w kolejności rosnącego p."""
    ordered = sorted(pairs, key=lambda kv: kv[1])
    m = len(ordered)
    out, running = [], 0.0
    for i, (name, p) in enumerate(ordered):
        running = max(running, min(1.0, (m - i) * p))
        out.append((name, p, running))
    return out


# ── twierdzenia z noty ────────────────────────────────────────────────────────

def claims(r2: list[dict], r1: list[dict]) -> list[tuple[str, object, object]]:
    """(opis, wartość w nocie, wartość przeliczona)."""
    ok = [r for r in r2 if not r["derailed"]]
    by = lambda v, rows=r2: [r for r in rows if r["variant"] == v]
    okby = lambda v: [r for r in ok if r["variant"] == v]
    c = []

    c.append(("liczba przebiegów rundy 2", 40, len(r2)))
    c.append(("ważne przebiegi (bez wykolejonych)", 37, len(ok)))
    c.append(("flagi w rundzie 2", "38/40", f"{sum(r['flag'] for r in r2)}/{len(r2)}"))
    c.append(("wykolejone = te z pracą w tle", sorted(DERAILED),
              sorted(r["run"] for r in r2 if r["derailed"])))

    # mediany i zakresy kosztu liczymy bez wykolejonych, kontakt — ze wszystkimi
    for v, mc, mt in (("with-dox", 2.62, 57), ("no-dox", 1.70, 48.5),
                      ("pointer-dox", 2.03, 53), ("symlink-dox", 2.48, 58)):
        c.append((f"mediana kosztu {v}", mc, round(median([r["cost"] for r in okby(v)]), 2)))
        c.append((f"mediana tur {v}", mt, median([r["turns"] for r in okby(v)])))

    for v, exp in (("with-dox", "0/10"), ("no-dox", "1/10"),
                   ("pointer-dox", "7/10"), ("symlink-dox", "6/10")):
        rows = by(v)
        c.append((f"kontakt ze strategy/ {v} (n=10)", exp,
                  f"{sum(r['contact_any'] for r in rows)}/{len(rows)}"))
    c.append(("kontakt symlink-dox liczony tylko przez Read", "5/10",
              f"{sum(r['contact_read'] for r in by('symlink-dox'))}/10"))
    for v, exp in (("with-dox", "0/10"), ("no-dox", "0/10"),
                   ("pointer-dox", "0/10"), ("symlink-dox", "3/10")):
        c.append((f"kontakt z regułami {v}", exp,
                  f"{sum(r['rules'] for r in by(v))}/{len(by(v))}"))

    p_with = fisher_two_sided(7, 3, 0, 10)
    p_no = fisher_two_sided(7, 3, 1, 9)
    p_der = fisher_two_sided(3, 7, 0, 30)
    c.append(("Fisher kontakt pointer vs with (n=10)", 0.0031, round(p_with, 4)))
    c.append(("Fisher kontakt pointer vs no", 0.0198, round(p_no, 4)))
    c.append(("Fisher wykolejenia with vs pula reszty", 0.0121, round(p_der, 4)))
    c.append(("Fisher wykolejenia parami with vs pojedynczy wariant", 0.21,
              round(fisher_two_sided(3, 7, 0, 10), 2)))

    cost = lambda v: [r["cost"] for r in okby(v)]
    p_ps_mean = permutation_p(cost("pointer-dox"), cost("symlink-dox"))
    p_ns_mean = permutation_p(cost("no-dox"), cost("symlink-dox"))
    p_ps_med = permutation_p(cost("pointer-dox"), cost("symlink-dox"), median)
    p_ns_med = permutation_p(cost("no-dox"), cost("symlink-dox"), median)
    c.append(("permutacja koszt pointer vs symlink (średnie)", 0.0436, round(p_ps_mean, 4)))
    c.append(("permutacja koszt no vs symlink (średnie)", 0.0465, round(p_ns_mean, 4)))
    c.append(("permutacja koszt pointer vs symlink (mediany)", 0.1024, round(p_ps_med, 4)))
    c.append(("permutacja koszt no vs symlink (mediany)", 0.0113, round(p_ns_med, 4)))

    c.append(("korelacja koszt-tury (37 ważnych)", 0.93,
              round(pearson([r["cost"] for r in ok], [float(r["turns"]) for r in ok]), 2)))
    c.append(("korelacja koszt-tury gdyby liczyć wszystkie 40", 0.58,
              round(pearson([r["cost"] for r in r2], [float(r["turns"]) for r in r2]), 2)))

    corrected = dict((n, round(q, 4)) for n, _, q in holm([
        ("kontakt pointer vs with", p_with), ("kontakt pointer vs no", p_no),
        ("wykolejenia", p_der), ("koszt no vs symlink (mediany)", p_ns_med),
        ("koszt pointer vs symlink (mediany)", p_ps_med)]))
    for name, exp in (("kontakt pointer vs with", 0.0155), ("kontakt pointer vs no", 0.0451),
                      ("wykolejenia", 0.0451), ("koszt no vs symlink (mediany)", 0.0451),
                      ("koszt pointer vs symlink (mediany)", 0.1024)):
        c.append((f"Holm: {name}", exp, corrected[name]))

    for v, exp in (("with-dox", "7/7"), ("no-dox", "0/10"),
                   ("pointer-dox", "9/10"), ("symlink-dox", "9/10")):
        rows = okby(v)
        c.append((f"DOX pass {v} (bez wykolejonych)", exp,
                  f"{sum(r['dox_pass'] for r in rows)}/{len(rows)}"))

    if r1:
        c.append(("runda 1: liczba przebiegów (nota: dwanaście)", 12, len(r1)))
        for v, exp in (("with-dox", 2.29), ("no-dox", 2.15)):
            rows = [r for r in r1 if r["variant"] == v]
            if rows:
                c.append((f"runda 1: średnia kosztu {v}", exp,
                          round(fsum(r["cost"] for r in rows) / len(rows), 2)))
    return c


def scipy_crosscheck() -> list[str]:
    try:
        from scipy.stats import fisher_exact  # type: ignore
    except ImportError:
        return ["  scipy niedostępne — kontrola krzyżowa pominięta "
                "(uruchom: uvx --with scipy python3 verify.py)"]
    out = []
    for label, table, mine in (
        ("pointer vs with", [[7, 3], [0, 10]], fisher_two_sided(7, 3, 0, 10)),
        ("pointer vs no", [[7, 3], [1, 9]], fisher_two_sided(7, 3, 1, 9)),
        ("wykolejenia", [[3, 7], [0, 30]], fisher_two_sided(3, 7, 0, 30)),
    ):
        theirs = float(fisher_exact(table)[1])
        agree = abs(theirs - mine) < 1e-9
        out.append(f"  {'OK ' if agree else 'ROZJAZD'} {label}: własne {mine:.9f} | scipy {theirs:.9f}")
    return out


def same(expected, got) -> bool:
    """Zgodność na precyzji, jaką deklaruje nota: 2.03 porównujemy do 2 miejsc, 53 do zera."""
    try:
        e, g = float(expected), float(got)
    except (TypeError, ValueError):
        return str(expected) == str(got)
    txt = str(expected)
    decimals = len(txt.split(".")[1]) if "." in txt else 0
    return round(e, decimals) == round(g, decimals)


def main() -> int:
    r2 = load_all(ROUND2) or load_all(BACKUP / "round-2")
    # Nota opisuje rundę 1 jako przebiegi 1-3 każdego wariantu. Przebiegi nr 1 wariantów
    # with-dox i no-dox leżą w discarded/ (odrzucone przy starcie rundy 2 z powodu
    # widocznej historii gita), ale tabela rundy 1 w nocie je zawiera — więc weryfikacja
    # musi czytać tę samą populację, inaczej sprawdza co innego niż nota twierdzi.
    r1 = sorted(load_all(BACKUP / "round-1") + load_all(BACKUP / "discarded"),
                key=lambda r: r["run"])
    if not r2:
        print("brak transkryptów rundy 2 — sprawdź results/ albo _results-backup/round-2/")
        return 1

    rows = claims(r2, r1)
    bad = [(d, e, g) for d, e, g in rows if not same(e, g)]
    width = max(len(d) for d, _, _ in rows)
    print(f"{'twierdzenie':<{width}}  {'w nocie':>12}  {'przeliczone':>12}")
    print("─" * (width + 30))
    for d, e, g in rows:
        mark = " " if same(e, g) else "  <-- ROZJAZD"
        print(f"{d:<{width}}  {str(e):>12}  {str(g):>12}{mark}")
    print("─" * (width + 30))
    print(f"{len(rows) - len(bad)} zgodnych, {len(bad)} rozjazdów\n")
    print("kontrola krzyżowa:")
    print("\n".join(scipy_crosscheck()))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
