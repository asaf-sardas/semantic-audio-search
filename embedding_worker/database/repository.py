import psycopg2
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
import os




class VectorDBRepository:
    def __init__(self, collection_name: str, dimension: int):

        self.table_name = f"content_embeddings_{collection_name}"

        try:
            self.connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
            self._ensure_table_exists(dimension)
            register_vector(self.connection)
            print(f"[*] Vector DB Ready. Using table: {self.table_name}")
        except Exception as e:
            print(f"[X] CRITICAL: Failed to connect to database: {e}")
            raise

    def _ensure_table_exists(self, dimension: int):
        query = f"""
            CREATE EXTENSION IF NOT EXISTS vector;

            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                video_id TEXT NOT NULL,
                start_time FLOAT NOT NULL,
                end_time FLOAT NOT NULL,
                content TEXT NOT NULL,
                embedding VECTOR({dimension}) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
            );

            CREATE INDEX IF NOT EXISTS idx_{self.table_name}_video_id 
            ON {self.table_name}(video_id);
        """
        with self.connection.cursor() as cur:
            cur.execute(query)
        self.connection.commit()

    def save_embedded_chunks(self, video_id: str, chunks: list) -> bool:
        if not chunks:
            return True

        data_to_insert = [
            (video_id, chunk["start"], chunk["end"], chunk["text"], chunk["embedding"])
            for chunk in chunks
        ]

        query = f"""
            INSERT INTO {self.table_name} (video_id, start_time, end_time, content, embedding)
            VALUES %s
        """

        try:
            with self.connection.cursor() as cur:
                execute_values(cur, query, data_to_insert)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"[!] Database error while saving chunks for video {video_id}: {e}")
            raise