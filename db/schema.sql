CREATE TABLE kategori_putusan (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link TEXT NOT NULL,
    count BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS putusan_ma (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    pengadilan TEXT,
    tanggal_register TEXT,
    tanggal_putus TEXT,
    tanggal_upload TEXT,
    views TEXT,
    downloads TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table informasi_putusan (
  id serial not null,
  link_detail text not null,
  tingkat_proses text null,
  klasifikasi text null,
  kata_kunci text null,
  lembaga_peradilan text null,
  jenis_lembaga_peradilan text null,
  hakim_ketua text null,
  hakim_anggota text null,
  panitera text null,
  amar text null,
  amar_lainnya text null,
  catatan_amar text null,
  kaidah text null,
  abstrak text null,
  tahun_putusan integer null,
  tanggal_register text null,
  tanggal_musyawarah text null,
  tanggal_dibacakan text null,
  jumlah_view integer null default 0,
  jumlah_download integer null default 0,
  link_zip text null,
  link_pdf text null,
  timestamp timestamp without time zone null default CURRENT_TIMESTAMP,
  constraint informasi_putusan_pkey primary key (id)
) TABLESPACE pg_default;