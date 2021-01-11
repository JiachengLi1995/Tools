from tqdm import tqdm
from wikipedia2vec.dump_db import DumpDB
import json
from wikipedia2vec.utils.wiki_dump_reader import WikiDumpReader
from sentence_tokenizer import SentenceTokenizer
import multiprocessing
from contextlib import closing
from multiprocessing.pool import Pool

def build_dump_db():
    dump_file = 'enwiki-latest-pages-articles-multistream.xml.bz2'
    out_file = 'dumpdb_file'
    dump_reader = WikiDumpReader(dump_file)
    DumpDB.build(dump_reader, out_file, pool_size=multiprocessing.cpu_count(), chunk_size=100)


def _initialize_worker(
        dump_db: DumpDB
    ):
        global _dump_db

        _dump_db = dump_db

def _process_page(page_title: str):

    page_data = []

    for paragraph in _dump_db.get_paragraphs(page_title):

        data_line = {'page_title':page_title}
        paragraph_text = paragraph.text

        # First, get paragraph links.
        # Parapraph links are represented its form (link_title) and the start/end positions of strings
        # (link_start, link_end).
        paragraph_links = []
        for link in paragraph.wiki_links:
            link_title = _dump_db.resolve_redirect(link.title)
            # remove category links
            if link_title.startswith("Category:") and link.text.lower().startswith("category:"):
                paragraph_text = (
                    paragraph_text[: link.start] + " " * (link.end - link.start) + paragraph_text[link.end :]
                )
            else:

                paragraph_links.append((link_title, link.start, link.end))
        
        if len(paragraph_links)==0:
            continue
        data_line['paragraph']=paragraph_text.rstrip()
        data_line['entities'] = paragraph_links

        page_data.append(data_line)

    return page_data

def build_wikipedia_pretraining_dataset(output_file: str):

    dump_db_file = 'dumpdb_file'
    dump_db = DumpDB(dump_db_file)
    #sentence_tokenizer = SentenceTokenizer.from_name(sentence_tokenizer)

    _build(dump_db, output_file)

def _build(dump_db, output_file):

    target_titles = [
                title
                for title in dump_db.titles()
                if not (":" in title and title.lower().split(":")[0] in ("image", "file", "category"))
            ]
    out_f = open(output_file, 'w', encoding='utf8')
    pool_size=multiprocessing.cpu_count()
    chunk_size=100
    with tqdm(total=len(target_titles)) as pbar:
        initargs = (
            dump_db,
        )
        with closing(
            Pool(pool_size, initializer=_initialize_worker, initargs=initargs)
        ) as pool:
            for ret in pool.imap(
                _process_page, target_titles, chunksize=chunk_size
            ):
                for data in ret:
                    out_f.write(json.dumps(data))
                pbar.update()
    out_f.close()


build_wikipedia_pretraining_dataset('./wiki_paragraph_entity.json')