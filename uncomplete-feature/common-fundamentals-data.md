Fitur untuk indikator sentimen adalah kombinasi sebagai penentu sentimen tanpa mempertimbangkan sebuah aset tertentu. Fitur ini berisi leading dan lagging indikator.

Leading indikator yang digunakan
1. COT data: 
    - Fokus pada spekulasi positioning as % of open interest. Jika spekulasi mencapai +2 atau -2 standar deviasi dalam rentang 3-5 tahun. 
    - Kelompokan aset berdasarkan korelasi makro.

2. Data yield dan komoditas
    - Real yields (Nominal yield dikurang inflation expectation/TIPS). Jika real yield naik maka liquiditas mengetat meskipun ekonomi sedang kuat
    - Lihat persentase komoditas yang bergerak dalam tren yang sama.

3. News sentimen dan ekonomi kalender
    - Menggunakan Citigroup Economic Surprice Index. Jika data ekonomi terus menerus malampaui estimasi, pasar akan melakukann repricing pada kebijakan bank sentral terpelas apakah datanya bagus secara absolut.
    - Untuk news sentimen fokus pada Central Bank Communication (Fedspeak)/

Variabel lain yang diguankan
1. Global liquidity
    - Komponen yang digunakan gabungan dari federal reserve balance sheet, treasury general account dan overnight reverse repo
    - Mekanisme: Jika TGA naik dan RRP naik maka liquditas net menyusut yang biasanya menjadi berish bagi aset beresiko seperti equities dan crypto.

2. Volatility Index
    - VIX (Equitiy Volatility): standar volatil untuk pasar saham
    - MOVE index (Bond Volatitily): Jika MOVE index melonjak maka pasar obligasi tidak stabil dan akan merusak kebijakan moneter serta menghancurkan sentimen makro secara halus.
    - CVIX (FX Volatility): Mengukur stabiitas arus modal global

3. Credit spread / Option - Adjusted Spread (OAS)
    - Komponen yaitu selisih antara yield High Yield Bonds (Junk Bonds) dengan US treasuries
    - Mekanisme: Jika credit spread melebar menunjukan institusi menuntuk premi resiko yang lebih tinggi karena khawatir akan gagal bayar.

4. Inflation breakevens 
    - Komponen yaitu 10-year breakeven inflation rate
    - Mekanisme: Jika breakeven naik sementara yield nominal tetap maka Real Yield turun. Ini sinyal untuk komoditas dan pertumbuhan ekonomi jangka panjang.

5. Cross asset correlation dan intermarket divergence
    - Variabel DXY vs gold, ini untuk menjadi korelasi negatif jika keduanya naik bersamaan maka terjadi ekstreme global stress


Filtering kolom hasil COT data
1. Market and Exchange Names: Filter instrument yang berguna seperti keyword: gold, forex dollar dan lainnya
2. As of Date in Form YYYY-MM-DD
3. Open Interest (All)
4. Noncommercial Positions-Long (All) & Noncommercial Positions-Short (All):