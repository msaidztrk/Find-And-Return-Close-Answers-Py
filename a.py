from difflib import get_close_matches

import json 
import os

#  note : yapılacaklar ; değişkenler ingilizce , with openlar ise dinamik konumdan oluşacak

def upload_json():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "veritabani.json")
    with open(file_path, "r") as dosya:
        return json.load(dosya)

def write_to_json(veriler):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "veritabani.json")
    with open(file_path, "w") as dosya:
        json.dump(veriler, dosya, indent=2)


def find_closest(soru, sorular):
    eslesen = get_close_matches(soru, sorular, 1, cutoff=0.6)
    return eslesen[0] if eslesen else None


def find_the_answer(soru, veritabani):
    for soru_cevaplar in veritabani["sorular"]:
        if soru_cevaplar["soru"] == soru:
            return soru_cevaplar["cevap"]
    return None


def chat_bot():
    veritabani = upload_json()

    while True:
        soru = input("Siz : ")
        if soru == "cik":
            break

        gelen_sonuc = find_closest(
            soru, [soru_cevaplar["soru"] for soru_cevaplar in veritabani["sorular"]]
        )

        if gelen_sonuc:
            verilecek_cevap = find_the_answer(gelen_sonuc, veritabani)
            print(f"Bot : {verilecek_cevap}")
        else:
            print(f"Bot : Bunu cevaplayamiyorum")
            yeni_cevap = input("Cevabini yazin veya gec diyin")

            if yeni_cevap != "gec":
                veritabani["sorular"].append({"soru": soru, "cevap": yeni_cevap})
                write_to_json(veritabani)

                print('Mesaj kayit edildi')




if __name__ == "__main__":
    chat_bot()
