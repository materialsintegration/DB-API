=====================================
DB-API 利用手順1
=====================================


概要
==================================================

| 本ドキュメントでは、DB-APIによるデータ検索の手順について説明する。


対象
==================================================

.. csv-table::
    :header: 項目, 内容, 備考
    :widths: 20, 20, 20

    検索対象, 材料データ基盤DB, 文献をベースにした材料DB
    検索内容, クリープ試験情報,



使用方法
==================================================

| 所定のURLにアクセスする。

::

    http://<db-apiサーバ名>/db-api/v1/get/test/NIMS_material/?mimetype=csv&test=creep_rupture_test


* サーバ名(アドレス)は管理者に確認のこと。
* クエリパラメータ(mimetype, test)には以下指定可能。

.. csv-table::
    :header: 項目, 内容, 備考
    :widths: 20, 20, 20

    mimetype, csv/json,
    test, creep_rupture_test, 


| 結果として以下のデータを指定書式(csv/json)にて出力する。

.. csv-table::
    :header: 項目, 内容, 備考
    :widths: 20, 20, 20

    material_id, 材料ごとに付与する一意のID,
    material_code_system, 材料コード体系名,
    material_category, 材料区分名,
    material_category_description, 材料区分の説明,
    material_code, 材料コード,
    material_name, 材料名,
    base_element, 主成分,
    alloying_elements, 合金成分, 主成分が先頭とは限らない
    shape_description, 形状説明,
    Al_min, 組成Alの含有量最小値(%),
    Al_max, 組成Alの含有量最大値(%),
    Al, 組成Alの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Al2O3_min, 組成Al2O3の含有量最小値(%),
    Al2O3_max, 組成Al2O3の含有量最大値(%),
    Al2O3, 組成Al2O3の含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Al_sol._min, 組成Al sol.の含有量最小値(%),
    Al_sol._max, 組成Al sol.の含有量最大値(%),
    Al_sol.,組成Al_sol.の含有量平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Al_total._min, 組成Al total.の含有量最小値(%),
    Al_total._max, 組成Al total.の含有量最大値(%),
    Al_total., 組成Al total.の含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    B_min, 組成Bの含有量最小値(%),
    B_max, 組成Bの含有量最大値(%),
    B, 組成Bの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    C_min, 組成Cの含有量最小値(%),
    C_max, 組成Cの含有量最大値(%),
    C, 組成Cの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    CO_min, 組成COの含有量最小値(%),
    CO_max, 組成COの含有量最大値(%),
    CO, 組成COの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Cr_min, 組成Crの含有量最小値(%),
    Cr_max, 組成Crの含有量最大値(%),
    Cr, 組成Crの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Cu_min, 組成Cuの含有量最小値(%),
    Cu_max, 組成Cuの含有量最大値(%),
    Cu, 組成Cuの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Fe_min, 組成Feの含有量最小値(%),
    Fe_max, 組成Feの含有量最大値(%),
    Fe, 組成Feの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Mn_min, 組成Mnの含有量最小値(%),
    Mn_max, 組成Mnの含有量最大値(%),
    Mn, 組成Mnの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Mo_min, 組成Moの含有量最小値(%),
    Mo_max, 組成Moの含有量最大値(%),
    Mo, 組成Moの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    N_min, 組成Nの含有量最小値(%),
    N_max, 組成Nの含有量最大値(%),
    N, 組成Nの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    N_sol._min, 組成N sol.の含有量最小値(%),
    N_sol._max, 組成N sol.の含有量最大値(%),
    N_sol., 組成N sol.の含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    N_total._min, 組成N total.の含有量最小値(%),
    N_total._max, 組成N total.の含有量最大値(%),
    N_total., 組成N total.の含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Nb_min, 組成Nbの含有量最小値(%),
    Nb_max, 組成Nbの含有量最大値(%),
    Nb, 組成Nbの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Ni_min, 組成Niの含有量最小値(%),
    Ni_max, 組成Niの含有量最大値(%),
    Ni, 組成Niの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    O_min, 組成Oの含有量最小値(%),
    O_max, 組成Oの含有量最大値(%),
    O, 組成Oの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    P_min, 組成Pの含有量最小値(%),
    P_max, 組成Pの含有量最大値(%),
    P, 組成Pの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    S_min, 組成Sの含有量最小値(%),
    S_max, 組成Sの含有量最大値(%),
    S, 組成Sの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Si_min, 組成Siの含有量最小値(%),
    Si_max, 組成Siの含有量最大値(%),
    Si, 組成Siの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Sn_min, 組成Snの含有量最小値(%),
    Sn_max, 組成Snの含有量最大値(%),
    Sn, 組成Snの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Ti_min, 組成Tiの含有量最小値(%),
    Ti_max, 組成Tiの含有量最大値(%),
    Ti, 組成Tiの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    V_min, 組成Vの含有量最小値(%),
    V_max, 組成Vの含有量最大値(%),
    V, 組成Vの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    W_min, 組成Wの含有量最小値(%),
    W_max, 組成Wの含有量最大値(%),
    W, 組成Wの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    Zr_min, 組成Zrの含有量最小値(%),
    Zr_max, 組成Zrの含有量最大値(%),
    Zr, 組成Zrの含有量平均値(%), (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    unit_name, 組成情報の単位,
    test_id, 試験ごとに付与する一意のID,
    creep_test_type_name, クリープ試験の種類,
    test_stress, 試験を実施した応力(MPa),
    test_temperature_min, 試験を実施した温度の下限値。単位はK,
    test_temperature_max, 試験を実施した温度の上限値。単位はK,
    test_temperature, 試験を実施した温度の平均値。単位はK,
    room_temperature, 試験温度が室温の場合はTRUEを設定する,
    test_atmosphere, 試験実施時の雰囲気,
    interruption_count, 試験中断回数,
    fracture_elongation_min, 破断伸びの下限値,
    fracture_elongation_max, 破断伸びの上限値,
    fracture_elongation, 破断伸びの平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    fracture_location_min, 破断位置の下限値,
    fracture_location_max, 破断位置の上限値,
    fracture_location, 破断位置の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    instantaneous_strain_min, 負荷完了時ひずみの下限値,
    instantaneous_strain_max, 負荷完了時ひずみの上限値,
    instantaneous_strain, 負荷完了時ひずみの平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    primary_creep_strain_min, 一次クリープひずみの下限値,
    primary_creep_strain_max, 一次クリープひずみの上限値,
    primary_creep_strain, 一次クリープひずみの平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    reduction_of_area_min, 絞りの下限値,
    reduction_of_area_max, 絞りの上限値,
    reduction_of_area, 絞りの平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    secondary_creep_strain_min, 二次クリープひずみの下限値,
    secondary_creep_strain_max, 二次クリープひずみの上限値,
    secondary_creep_strain, 二次クリープひずみの平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    steady_state_creep_rate_min, 定常クリープ速度の下限値,
    steady_state_creep_rate_max, 定常クリープ速度の上限値,
    steady_state_creep_rate, 定常クリープ速度の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    strain_min, ひずみの下限値,
    strain_max, ひずみの上限値,
    strain, ひずみの平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    strain_rate_min, ひずみ速度の下限値,
    strain_rate_max, ひずみ速度の上限値,
    strain_rate, ひずみ速度の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    tertiary_creep_start_strain_min, 三次クリープ開始ひずみの下限値,
    tertiary_creep_start_strain_max, 三次クリープ開始ひずみの上限値,
    tertiary_creep_start_strain, 三次クリープ開始ひずみの平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_0.5%_total_strain_min, 0.5%ひずみ到達時間の下限値,
    time_to_0.5%_total_strain_max, 0.5%ひずみ到達時間の上限値,
    time_to_0.5%_total_strain, 0.5%ひずみ到達時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_1.0%_total_strain_min, 1.0%ひずみ到達時間の下限値,
    time_to_1.0%_total_strain_max, 1.0%ひずみ到達時間の上限値,
    time_to_1.0%_total_strain, 1.0%ひずみ到達時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_2.0%_total_strain_min, 2.0%ひずみ到達時間の下限値,
    time_to_2.0%_total_strain_max, 2.0%ひずみ到達時間の上限値,
    time_to_2.0%_total_strain, 2.0%ひずみ到達時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_5.0%_total_strain_min, 5.0%ひずみ到達時間の下限値,
    time_to_5.0%_total_strain_max, 5.0%ひずみ到達時間の上限値,
    time_to_5.0%_total_strain, 5.0%ひずみ到達時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_interruption_min, 中断時間の下限値,
    time_to_interruption_max, 中断時間の上限値,
    time_to_interruption, 中断時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_rupture_min, 破断時間の下限値,
    time_to_rupture_max, 破断時間の上限値,
    time_to_rupture, 破断時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_secondary_creep_start_min, 二次クリープ開始時間の下限値,
    time_to_secondary_creep_start_max, 二次クリープ開始時間の上限値,
    time_to_secondary_creep_start, 二次クリープ開始時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット
    time_to_tertiary_creep_start_min, 三次クリープ開始時間の下限値,
    time_to_tertiary_creep_start_max, 三次クリープ開始時間の上限値,
    time_to_tertiary_creep_start, 三次クリープ開始時間の平均値, (最小値+最大値)/2 ただし一方がnullの場合他方をセット




