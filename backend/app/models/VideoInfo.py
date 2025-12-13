class VideoInfo():
    def __init__(self, video_id: str, titulo: str, miniatura_url: str = "", nombre_canal: str = ""):
        self.video_id = video_id
        self.titulo = titulo
        self.miniatura_url = miniatura_url
        self.nombre_canal = nombre_canal

    def to_dict(self):
        return {
            "video_id": self.video_id,
            "titulo": self.titulo,
            "miniatura_url": self.miniatura_url,
            "nombre_canal": self.nombre_canal
        }