# Graph memory dla agentów kodujących — szybki przegląd opcji

- Data: 2026-09-21
- Metoda: WebFetch stron GitHub (README + strona główna repo) pobranych 2026-09-21; bez klonowania, bez testów lokalnych
- Punkt odniesienia: GBrain (Garry Tan) — markdown w git + deterministyczna ekstrakcja encji do grafu Postgres/PGLite, hybrydowy BM25 + wektor

## Tabela

| Projekt | Co to jest | Gwiazdki | Ostatni commit/release | Licencja | Zależności runtime | Ontologia/krawędzie | MCP/CLI | Effort setup |
|---|---|---|---|---|---|---|---|---|
| [TrustGraph](https://github.com/trustgraph-ai/trustgraph) | Warstwa orkiestracji kontekstu na hypergrafach (RDF/OWL) dla deterministycznych agentów | 2.7k | brak danych | Apache 2.0 | Docker/K8s, Cassandra, Qdrant, Garage S3, Pulsar/RabbitMQ, LLM lokalny lub API | BYO-ontologia (OWL) lub LLM-extracted | MCP server (`trustgraph-mcp`) + CLI (`npx @trustgraph/config`) | Wysoki (wieloskładnikowy stack) |
| [Semantica](https://github.com/semantica-agi/semantica) | Deterministyczna platforma KG z pełną prowenancją decyzji dla systemów "accountable AI" | 13.3k | v0.6.8 (niedawny) | MIT | Rdzeń: `pip install semantica` (22 zależności); opcjonalnie Neo4j/FalkorDB/AGE/Neptune, Qdrant/Pinecone/inne, LLM API | Nie predefiniowana domyślnie; generowanie OWL + walidacja SHACL, ekstraktory NER/RE deterministyczne lub LLM | MCP server (`semantica.mcp_server`, 16+ narzędzi) + rozbudowany CLI | Niski (rdzeń) / średni (pełny stack) |
| [text2graphs](https://github.com/neostrange/text2graphs) | Framework Python do budowy domenowych KG z tekstu (NLP + Neo4j) | 27 | brak danych | MIT | Neo4j 4.4 + APOC (wymagany), wiele kontenerów Docker (coref, SRL, WSD, temporal), brak wymogu LLM API | Predefiniowana schema (typowanie encji/relacji), bez LLM | Brak MCP; tylko skrypty CLI | Wysoki (5-fazowy pipeline, wiele serwisów) |
| [GBrain](https://github.com/garrytan/gbrain) (referencja) | Markdown w git + deterministyczna ekstrakcja encji do grafu Postgres/PGLite, hybrydowy BM25+wektor, auto-enrichment | 30.2k | brak danych (widoczne 1071 commitów, aktywny) | MIT | Bun ≥1.3.11, Postgres 17 przez WASM (PGLite) lokalnie lub Postgres+pgvector współdzielony | Deterministyczna ekstrakcja encji, auto-linking grafowy (nie czysto LLM) | Wspiera wiele harnessów (Claude Code, Codex i in.); brak jednoznacznej wzmianki o osobnym MCP serwerze w opisie | Niski–średni (jeden runtime Bun + lokalny Postgres) |
| [Graphiti (Zep)](https://github.com/getzep/graphiti) | Framework do budowy temporalnych grafów wiedzy śledzących zmiany faktów w czasie z prowenancją | 31k | brak danych (984 commity) | Apache-2.0 | Python 3.10+, graf: Neo4j 5.26 / FalkorDB / Neptune / Kuzu (deprecated), LLM API wymagany (OpenAI domyślnie) | Oba tryby: "prescribed" (Pydantic, predefiniowane) i "learned" (LLM) | MCP server + REST API (FastAPI) | Średni (osobna baza grafowa + klucz LLM) |
| [Cognee](https://github.com/topoteretes/cognee) | Self-hosted platforma pamięci AI z grafem wiedzy dla trwałej pamięci agentów | 30.9k | v1.6.0, 2026-09-18 | Apache-2.0 | Docker opcjonalnie, Postgres (od v1.0 cały layer na jednej instancji), LLM API opcjonalny (lokalny GLiNER domyślnie) | LLM-extracted (GLiNER lokalnie), wspiera custom ontologie | MCP server + CLI (`cognee-cli`) + REST + SDK | Niski (quickstart pip) / średni (pełny deploy) |
| [mem0](https://github.com/mem0ai/mem0) | Warstwa pamięci "plug-in" dla agentów AI (nie stricte graf — semantic + BM25 + entity linking) | 65.7k | brak danych | Apache 2.0 | Docker (self-host), LLM API wymagany (domyślnie OpenAI), opcjonalnie Qdrant/Spacy | LLM-extracted (entity linking, brak predefiniowanej schemy) | MCP + CLI (`mem0-cli`) | Niski–średni |

## Obserwacje

- Żadna z czterech wskazanych pozycji nie jest idealnym dopasowaniem do "prosty graf z predefiniowanymi krawędziami blisko repo git": TrustGraph i text2graphs są ciężkie infrastrukturalnie (wieloskładnikowy Docker stack, Neo4j+APOC), Semantica jest właściwie najbliżej modelu GBrain (deterministyczna ekstrakcja, niski próg wejścia przy rdzeniu), ale ma szerszy zakres niż potrzeba solo-developerowi.
- GBrain jako referencja wypada dobrze na tle własnej kategorii: jeden runtime (Bun), lokalny Postgres przez PGLite, deterministyczna ekstrakcja zamiast czystego LLM-parsingu — ale nie znaleziono jednoznacznego potwierdzenia MCP servera w pobranej treści strony (może być w dokumentacji, nie w README/stronie głównej).
- Graphiti wyróżnia się jako jedyny projekt oferujący jawnie oba tryby ontologii ("prescribed" z Pydantic = predefiniowane krawędzie, oraz "learned"), co bezpośrednio odpowiada na obawę użytkownika o "prosty graf, który trzeba będzie przebudować" — można zacząć prescribed i nie migrować architektury.
- Cognee ma najniższy próg wejścia z realnej trójki alternatyw (pip install, lokalny GLiNER bez klucza LLM), ale domyślna ekstrakcja jest LLM/model-based, nie predefiniowana — dopasowanie ontologii wymaga świadomej konfiguracji custom ontology.
- mem0, mimo ogromnej popularności (65.7k gwiazdek), nie jest opisany jako graf w sensie jawnych, typowanych krawędzi — bliżej mu do semantic+keyword memory z entity linking niż do modelu GBrain/Graphiti; słabe dopasowanie do wymogu "predefiniowane typy krawędzi".
- Dane części pól (data ostatniego commita) nie były widoczne na pobranych stronach GitHub — WebFetch renderuje statyczną treść i nie zawsze pokazuje sidebar z metadanymi repo; przy realnej decyzji warto zweryfikować `git log -1` lub stronę /commits bezpośrednio.

## Ocena

