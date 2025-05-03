

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from dataclasses import dataclass
    from langchain_core.documents.base import Document
    import langchain_text_splitters as text_splitters
    import marimo as mo
    import numpy as np
    import openai
    import pandas as pd
    #import pdfplumber
    return Document, mo, np, openai, pd, text_splitters


@app.function
def get_namespace(name: str="Namespace", attributes=None) -> object:
    if not attributes:
        return type(name, (), {})()
    elif isinstance(attributes, dict):
        return type(name, (), attributes)()
    else:
        raise ValueError("param :attributes: is not valid (not of type dict)")


@app.cell
def _(get_lang):
    def get_lang_key() -> str:
        return get_lang().split(" ")[0]
    return (get_lang_key,)


@app.cell
def _():
    lang_opt = ["Norsk \U0001f1f3\U0001f1f4", "English \U0001f1ec\U0001f1e7"]
    return (lang_opt,)


@app.cell
def _(get_lang_key, info_intl):
    lang_ns = get_namespace(
        name="LanguageObject", 
        attributes=info_intl[get_lang_key()],
    )
    return (lang_ns,)


@app.cell
def _():
    info_intl = {
        "English": {
            "evidence_cutoff_slider_label": "Evidence cutoff value",
            "proposition_placeholder": "Proposition to query evidence for",
            "proposition_header": "Proposition formulation",
            "proposition": "In the text input below, write a proposition that you want to look for evidence in the provided feedback.",
            "chat_model_test_header": "Test of selected chat model",
            "chat_model_test_query": "Write a paragraph demonstrating some Markdown formatting.",
            "welcome": r"Welcome to Organisational Consultant!",
            "intro": r"""
            This app is a tailor-made AI designed to assist organizations with internal evaluation of themselves. It can be used at various levels, from project evaluations to workplace environment surveys. The app requires that the user has access to the OpenAI API and can provide an API key string. Please enter your key string below..
                """,
            "file_upload_header": "Upload text file with feedback from the evaluation",
            "file_upload": r"""
            Upload a Markdown file containing the basis for evaluation. This file should be a text file divided into sections with Markdown-formatted headings. Create a section by placing # at the start of a line (denoting a level-1 heading). Begin the document with the section # Background. This section should provide the AI with the context in which the feedback is to be understood. After that, one or more feedback sections may follow. Each feedback section starts with a Markdown heading indicating the area being addressed. Each piece of feedback begins on a new line, preceded by a hyphen, for example:
    `- the collaboration among project participants was good`""",
            "evidence_slider_label": "Evidence cutoff value",
        },
        "Norsk": {
            "evidence_cutoff_slider_label": "Avkuttings verdi for bevis",
            "proposition_placeholder": "Påstand som det søkes dekning for",
            "proposition_header": "Formulering av påstand",
            "proposition": "Skriv inn i tekst-feltet under en formulering av en påstand som du ønsker å se etter bevis for.",
            "chat_model_test_header": "Test av valgt chat modell",
            "chat_model_test_query": "Skriv en paragraf som demonstrere noen av mulighetene med Markdown formatting.",
            "welcome": r"Velkommen til Organisasjons konsulenten!",
            "intro": r"""
                Denne app'en er en skreddersydd KI for å bistå organisasjoner til intern evaluering av egen organisasjon. Den kan benyttes på ulike nivåer, fra prosjektevaluering til arbeidsmiljøundersøkelser. App'en er avhengig av at brukeren har tilgang til OpenAI API og kan angi en nøkkelstreng for API tilgang. Angi nøkkelstreng under.
                """,
            "file_upload_header": "Last opp en tekstfil som inneholder feedback fra evalueringen",
            "file_upload": r"""
            Last opp en Markdown fil med grunnlaget for evaluering. Denne filen skal være en tekstfil som er seksjonert i deler med
            Markdown-formatterte overskrifter. Lag en seksjon i filen ved å bruke `#` i starten av en linje (angir overskriftsnivå 1).
            Innled tekstdokument med avsnittet `# Bakgrunn`. Denne seksjonen skal gi KI-en forståelse for hvilken sammenheng feekback
            skal forstås i. Deretter kan det følge en eller flere seksjoner med feedback. Hver seksjon med feedbak innledes med en
            Markdown-overskrift som fordeller hvilket område det er gitt feedback på.
            Hvert innspill/stykke feedback starter på en ny linje og med en bindestrek foran,
            eksempel: `- samarbeidet mellom deltagerne i prosjektet var bra`.
            """,
            "evidence_slider_value": "Avkuttingsverdi for bevissøk",
        },
    }
    return (info_intl,)


@app.cell
def _(lang_nxt, mo, switch_lang):
    lang_btn = mo.ui.button(on_click=switch_lang, label=lang_nxt)
    lang_btn
    return


@app.cell(hide_code=True)
def _(lang_ns, mo):
    mo.md(
        f"""# {lang_ns.welcome}"""
        f"""{lang_ns.intro}"""
    )
    return


@app.cell
def _(lang_opt, mo):
    get_lang, set_lang = mo.state(lang_opt[0], allow_self_loops=False)
    return get_lang, set_lang


@app.cell
def _(get_lang, lang_opt):
    lang_nxt = lang_opt[lang_opt.index(get_lang()) + 1] if lang_opt.index(get_lang()) < len(lang_opt) -1 else lang_opt[0]
    return (lang_nxt,)


@app.cell
def _(lang_nxt, set_lang):
    def switch_lang(inp):
        set_lang(lang_nxt)
    return (switch_lang,)


@app.cell
def _(mo):
    get_key, set_key = mo.state("", allow_self_loops=False)
    return get_key, set_key


@app.cell
def _(mo):
    field_api_key = mo.ui.text(
        placeholder="OpenAI API key",
        kind="password",
    )
    field_api_key

    return (field_api_key,)


@app.cell
def _(field_api_key, get_key, mo, openai, set_key):
    # 5) Now you can use get_key() safely elsewhere
    _key = field_api_key.value
    _key_len = len(_key) if _key else 0

    if _key:
        set_key(_key)
        openai_client = openai.OpenAI(api_key=get_key())
        openai_client.api_key = get_key()

    mo.md(f"✅ Stored key, length: {_key_len}")

    return (openai_client,)


@app.cell
def _(openai_client):
    def _isvalid_model(mod):
        if any([_exl in mod.id for _exl in ["audio", "realtime", "transcribe"]]):
            return False
        if not mod.id.startswith("gpt"):
            return False
        return True

    models = [mod.id for mod in openai_client.models.list().data if _isvalid_model(mod)]
    return (models,)


@app.cell
def _(mo, models):
    sel_model = mo.ui.dropdown(models)
    return (sel_model,)


@app.cell
def _(sel_model):
    sel_model
    return


@app.cell
def _(lang_ns, mo, openai_client, sel_model):
    _test_response = openai_client.responses.create(
        model=sel_model.value,
        input=lang_ns.chat_model_test_query,
    )
    mo.md(text=f"""
    # {lang_ns.chat_model_test_header}
    {_test_response.output_text}
    """)
    return


@app.cell
def _(lang_ns, mo):
    mo.md(
        f"""
        # {lang_ns.file_upload_header}
        {lang_ns.file_upload}"""
    )
    return


@app.cell
def _(mo):
    file_upload = mo.ui.file()
    file_upload
    return (file_upload,)


@app.cell
def _(file_upload, text_splitters):
    markdown_splitter = text_splitters.MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Seksjonsinndeling"), 
        ],
        return_each_line=True,
        strip_headers=False,
    )
    text_content = str(file_upload.contents(), "utf-8")
    contents = markdown_splitter.split_text(text_content)
    return (contents,)


@app.cell
def _(Document):
    def get_list_from_sections(sections_list: list[Document]) -> list[str]:
        res = list()
        for section in sections_list:
            for line in section.page_content.splitlines():
                if line.startswith("#"): continue
                stripped_line = line.strip("- ")
                formatted_line = f"{stripped_line} {section.metadata=}"
                res.append(formatted_line)
        return res
    return (get_list_from_sections,)


@app.cell
def _(contents, get_list_from_sections):
    text_lines = get_list_from_sections(contents)
    return (text_lines,)


@app.cell
def _(pd, text_lines):
    evaluation_data = pd.DataFrame(data={"textline": text_lines})
    return (evaluation_data,)


@app.cell
def _(openai_client):
    def get_embeddings(texts: list[str], model: str="text-embedding-ada-002") -> list[list[float]]:
        embedding_response = openai_client.embeddings.create(
            model=model,
            input=texts,
        )
        res = [item.embedding for item in embedding_response.data]
        return res
    return (get_embeddings,)


@app.cell
def _(evaluation_data, get_embeddings):
    embedding_vectors = get_embeddings(
        texts=evaluation_data["textline"].tolist()
    )
    return (embedding_vectors,)


@app.cell
def _(embedding_vectors, evaluation_data):
    evaluation_data["embedding"] = embedding_vectors
    return


@app.cell
def _(np):
    def get_cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
        a = np.array(vector_a)
        b = np.array(vector_b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return (get_cosine_similarity,)


@app.cell
def _(lang_ns, mo):
    mo.md(f"""
    # {lang_ns.proposition_header}
    {lang_ns.proposition}""")
    return


@app.cell
def _(lang_ns, mo):
    query_text = mo.ui.text(placeholder=lang_ns.proposition_placeholder, full_width=True)
    query_text
    return (query_text,)


@app.cell
def _(get_embeddings, query_text):
    if query_text.value:
        query_embedding = get_embeddings(texts=[query_text.value, ])[0]
    return (query_embedding,)


@app.cell
def _(evaluation_data, get_cosine_similarity, pd, query_embedding):

    textline_sims: pd.Series = evaluation_data["embedding"].apply(
        lambda emb: get_cosine_similarity(vector_a=emb, vector_b=query_embedding)
    )
    top_5_idxs = textline_sims.sort_values(ascending=False).head().index.values
    return (textline_sims,)


@app.cell
def _(lang_ns, mo):
    evidence_cutoff = mo.ui.slider(
        label=lang_ns.evidence_cutoff_slider_label, 
        start=0.10, 
        stop=0.99, 
        step=0.01,
        value=0.82, 
        full_width=True,
    )
    evidence_cutoff
    return (evidence_cutoff,)


@app.cell
def _(evaluation_data, evidence_cutoff, pd, textline_sims):
    evidence: pd.Series = evaluation_data["textline"].loc[textline_sims > evidence_cutoff.value]
    return (evidence,)


@app.cell
def _(evidence):
    evidence_textbody = "\n\n".join(evidence.to_list())
    return (evidence_textbody,)


@app.cell
def _(evidence_textbody, mo):
    mo.md(f"""
    {evidence_textbody}""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
