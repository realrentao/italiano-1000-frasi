#!/usr/bin/env python3
"""补全缺失的77句音频"""
import hashlib, re, json, os, base64, subprocess

CACHE = r'D:/意大利语材料/常用意大利语1000句/.audio_cache/cache.json'
OUT = r'D:/意大利语材料/常用意大利语1000句'
AUDIO_CACHE = r'D:/意大利语材料/常用意大利语1000句/.audio_cache'
VOICE = "it-IT-ElsaNeural"

with open(CACHE, 'r', encoding='utf-8') as f:
    cache = json.load(f)

# 缺失句子
missing_texts = [
    (917, "Mi attrai tantissimo"), (918, "Sei il tipo che mi piace"),
    (919, "Trovo che tu sia bellissimo"), (920, "Non riesco a smettere di pensarti"),
    (921, "Mi fai girare la testa"), (922, "Hai un bel sorriso"),
    (923, "Mi piace il tuo modo di essere"), (924, "Sei diverso dagli altri"),
    (925, "Non ho mai incontrato nessuno come te"), (926, "Mi fai sentire speciale"),
    (927, "Sei la persona più bella che conosca"), (928, "Mi perdo nei tuoi occhi"),
    (929, "Hai un fascino incredibile"), (930, "Mi emozioni ogni volta"),
    (931, "Vuoi essere la mia ragazza?"), (932, "Vuoi essere il mio ragazzo?"),
    (933, "Usciamo insieme da un mese"), (934, "Stiamo insieme da due anni"),
    (935, "Siamo fidanzati"), (936, "Ci sposiamo a giugno"),
    (937, "Ti amo con tutto il cuore"), (938, "Sei l'amore della mia vita"),
    (939, "Non potrei vivere senza di te"), (940, "Voglio passare la mia vita con te"),
    (942, "La mia anima gemella"), (944, "Non ti lascerò mai"),
    (946, "Ti penso sempre"), (949, "Sono pazzo di te"),
    (951, "Ti voglio tanto bene"), (952, "Sei nei miei pensieri"),
    (953, "Vorrei essere con te adesso"), (954, "Sei la cosa più bella della mia vita"),
    (955, "Baciami"), (956, "Vieni più vicino"), (957, "Abbracciami"),
    (958, "Tienimi la mano"), (959, "Sei romantico"), (960, "Che serata romantica"),
    (961, "Non funziona più tra noi"), (962, "Ho bisogno di tempo per pensare"),
    (963, "Non sono pronto per una relazione"), (964, "Sei troppo gentile con me"),
    (965, "Non sei il tipo che fa per me"), (966, "Non ti vedo in questo modo"),
    (967, "Ho bisogno di spazio"), (968, "Forse è meglio così"),
    (969, "Non prendertela"), (970, "Possiamo essere amici?"),
    (971, "Mi hai spezzato il cuore"), (972, "Non ti ama più"),
    (973, "È finita tra noi"), (974, "Non chiamarmi più"),
    (975, "Ho chiuso con te"), (976, "Ti auguro il meglio"),
    (977, "Troverai qualcuno di meglio"), (978, "Non ti dimenticherò mai"),
    (979, "È stato bellissimo"), (981, "Vuoi sposarmi?"),
    (982, "Sarai per sempre mia"), (983, "Ti amo più di ogni cosa"),
    (984, "Prometto di amarti per sempre"), (985, "Sei la mia anima gemella"),
    (986, "Non vedo l'ora di invecchiare con te"), (987, "Hai la mia parola"),
    (988, "Farò qualsiasi cosa per te"), (989, "Sei il mio tutto"),
    (990, "Con te per sempre"), (991, "Mi affido a te"),
    (992, "Ti starò sempre accanto"), (993, "Insieme nella buona e nella cattiva sorte"),
    (994, "Ti amo più di ieri"), (995, "Sei il mio universo"),
    (996, "Ogni giorno con te è un dono"), (997, "Ti scelgo ogni giorno"),
    (998, "Mio e tuo per sempre"), (999, "Il nostro amore è eterno"),
    (1000, "Grazie a tutti!"),
]

ok = 0
for num, text in missing_texts:
    text_clean = text.strip()
    key = hashlib.md5(text_clean.lower().strip('.,!?;:').encode()).hexdigest()
    mp3 = os.path.join(AUDIO_CACHE, f"{key}.mp3")
    
    if key in cache:
        print(f"  #{num:03d} 已有缓存，跳过")
        b64 = cache[key]
    else:
        safe = text_clean[:120].replace('"', "'")
        cmd = f'edge-tts --voice "{VOICE}" --text "{safe}" --write-media "{mp3}"'
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or not os.path.exists(mp3) or os.path.getsize(mp3) < 100:
            print(f"  ✗ #{num:03d} 失败: {text[:50]}")
            continue
        with open(mp3, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        cache[key] = b64
        print(f"  ✓ #{num:03d} {text[:40]}")
    
    # 生成JS
    n3 = f"{num:03d}"
    js = f"var AUDIO_{n3} = " + json.dumps(b64, ensure_ascii=False) + ";\n"
    with open(os.path.join(OUT, f"audio_{n3}.js"), "w", encoding="utf-8") as fp:
        fp.write(js)
    ok += 1

# 保存缓存
with open(CACHE, "w", encoding="utf-8") as f:
    json.dump(cache, f)

print(f"\n完成: {ok}个")
