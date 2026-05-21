betise kullanılarak stochastic trendli veri uretilecek ve sonra W1 realdata folderi içinden alıncak.; yeni üretilen verinin size’ı 40-50 falan olsun. eğer sonuç kötü gelirse uzunluğunu artırıp 100 falan yapıp bir daha deneyelim. sorun kısa diye mi acaba



ikisi için de https://github.com/KereMath/tsfresh-ensemble-stationary ve https://github.com/KereMath/ens-final
reposundaki pipelinelar çalıştırılacak sonuçta ne verdiği görülecek
bu iki pipelineda da ara modeller metalearning stationary detector ve multi ve single anomali için ayurı ayrı modeller var ve zaten ikisi de ensemble.   ben her modelin kaç probability ile ne dediğini görmek istiyorum her tekil model için hem ensemble olanda hem ensembleların ensemble si olanda hem stationary detectorde hem de multi single detector için

daha sonra realdatadaki  labeli belili olan her datayı da hem iki repodaki pipeline a da sokup tüm datalarda iki pipeline nası sonuç veriyo ikisini de görmek lazımdır.

: bir de bizim algoritmanın şimdiye kadar ki başarımını kısa seriler özelinde bakabilir miyiz?  her ikisi için de 
