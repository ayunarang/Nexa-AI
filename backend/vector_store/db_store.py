from tinydb import TinyDB, Query

db = TinyDB("vector_store/chunk_meta.json")

def save_metadata(id_list, chunk_list, video_id):
    for _id, chunk in zip(id_list, chunk_list):
        db.insert({
            "id": _id,
            "video_id": video_id,
            "start": chunk.start,
            "end": chunk.end,
            "text": chunk.text
        })

def get_chunk_by_id(_id):
    Chunk = Query()
    return db.search(Chunk.id == _id)

def is_video_already_stored(video_id: str) -> bool:
    Chunk = Query()
    return db.contains(Chunk.video_id == video_id)
