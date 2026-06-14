# Data Dictionary

Ce document liste les colonnes des tables Silver, gold et marts du projet. Les définitions sont basées sur les modèles DBT et les transformations visibles dans `dbt/models/`.

---

## Silver

### `stg_flights`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `FL_DATE` | Date d’exploitation du vol | Raw CSV 2009-2018 / parquet nettoyé | Date / texte | YYYY-MM-DD | Silver |
| `YEAR` | Année d’exploitation dérivée de `FL_DATE` | Calcul DBT | Int | 2009–2018 | Silver |
| `MONTH` | Mois dérivé de `FL_DATE` | Calcul DBT | Int | 1–12 | Silver |
| `QUARTER` | Trimestre dérivé de `FL_DATE` | Calcul DBT | Int | 1–4 | Silver |
| `DAY_OF_WEEK` | Jour de la semaine dérivé de `FL_DATE` | Calcul DBT | Int | 1–7 | Silver |
| `OP_CARRIER` | Code IATA du transporteur opérationnel | Raw CSV / parquet nettoyé | Texte | Codes IATA (ex. AA, DL, UA) | Silver |
| `OP_CARRIER_FL_NUM` | Numéro de vol du transporteur | Raw CSV / parquet nettoyé | Texte | Nombre ou chaîne de vol | Silver |
| `ORIGIN` | Aéroport de départ | Raw CSV / parquet nettoyé | Texte | Code OACI / IATA (ex. JFK, LAX) | Silver |
| `DEST` | Aéroport d’arrivée | Raw CSV / parquet nettoyé | Texte | Code OACI / IATA | Silver |
| `DEP_DELAY` | Retard au départ en minutes | Raw CSV / parquet nettoyé | Numérique | Minutes, peut être négatif | Silver |
| `ARR_DELAY` | Retard à l’arrivée en minutes | Raw CSV / parquet nettoyé | Numérique | Minutes, peut être négatif | Silver |
| `CANCELLED` | Indicateur de vol annulé | Raw CSV / parquet nettoyé | Int / Bool | 0 ou 1 | Silver |
| `CANCELLATION_CODE` | Code de motif d’annulation | Raw CSV / parquet nettoyé | Texte | A, B, C, D | Silver |
| `DIVERTED` | Indicateur de déroutement | Raw CSV / parquet nettoyé | Int / Bool | 0 ou 1 | Silver |
| `CARRIER_DELAY` | Minutes de retard imputées au transporteur | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `WEATHER_DELAY` | Minutes de retard imputées à la météo | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `NAS_DELAY` | Minutes de retard imputées au réseau aérien national | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `SECURITY_DELAY` | Minutes de retard imputées à la sécurité | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `LATE_AIRCRAFT_DELAY` | Minutes de retard imputées à un avion en retard | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `DISTANCE` | Distance de vol | Raw CSV / parquet nettoyé | Numérique | Miles | Silver |
| `CRS_ELAPSED_TIME` | Durée planifiée du vol | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `ACTUAL_ELAPSED_TIME` | Durée réelle du vol | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `AIR_TIME` | Temps de vol effectif | Raw CSV / parquet nettoyé | Numérique | Minutes | Silver |
| `IS_DELAYED_ARR` | Indicateur de retard à l’arrivée | Calcul DBT (`ARR_DELAY > 0`) | Bool | TRUE / FALSE | Silver |

---

## Dimensional tables

### `dim_carrier`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `carrier_key` | Identifiant interne du transporteur | Calcul DBT depuis `OP_CARRIER` | Int | Clé séquence | `dim_carrier` |
| `iata_code` | Code IATA du transporteur | `OP_CARRIER` du Silver | Texte | AA, DL, UA, WN, B6, AS, NK, F9, US, CO, FL, Autre | `dim_carrier` |
| `carrier_name` | Nom commercial du transporteur | Mapping DBT | Texte | American Airlines, Delta Air Lines, ... | `dim_carrier` |
| `carrier_type` | Catégorie de transporteur | Segmentation DBT | Texte | Legacy, Low Cost, Ultra Low Cost, Other | `dim_carrier` |
| `merged_into` | Code du transporteur absorbant | Mapping DBT des anciens codes | Texte | UA, AA, WN, NULL | `dim_carrier` |

### `dim_date`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `date_key` | Identifiant interne de la date | Calcul DBT depuis `FL_DATE` | Int | Clé séquence | `dim_date` |
| `full_date` | Date complète du vol | Calcul DBT | Date | YYYY-MM-DD | `dim_date` |
| `year` | Année civile | Calcul DBT | Int | 2009–2018 | `dim_date` |
| `month` | Mois civil | Calcul DBT | Int | 1–12 | `dim_date` |
| `quarter` | Trimestre civil | Calcul DBT | Int | 1–4 | `dim_date` |
| `day_of_week` | Jour de la semaine | Calcul DBT | Int | 1–7 | `dim_date` |
| `is_weekend` | Indique un week-end | Calcul DBT | Bool | TRUE / FALSE | `dim_date` |

---

## `fact_flights`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `flight_key` | Identifiant de vol dans le fait | Calcul DBT | Int | Clé séquence | `fact_flights` |
| `carrier_key` | Référence vers transporteur | FK vers `dim_carrier.carrier_key` | Int | Clé étrangère | `fact_flights` |
| `date_key` | Référence vers date | FK vers `dim_date.date_key` | Int | Clé étrangère | `fact_flights` |
| `OP_CARRIER_FL_NUM` | Numéro de vol opérant | Silver | Texte | Numéro de vol | `fact_flights` |
| `ORIGIN` | Aéroport de départ | Silver | Texte | Code aéroport | `fact_flights` |
| `DEST` | Aéroport d’arrivée | Silver | Texte | Code aéroport | `fact_flights` |
| `DEP_DELAY` | Retard au départ en minutes | Silver | Numérique | Minutes | `fact_flights` |
| `ARR_DELAY` | Retard à l’arrivée en minutes | Silver | Numérique | Minutes | `fact_flights` |
| `CANCELLED` | Indicateur de vol annulé | Silver | Int / Bool | 0, 1 | `fact_flights` |
| `CANCELLATION_CODE` | Motif d’annulation | Silver | Texte | A, B, C, D | `fact_flights` |
| `DIVERTED` | Indicateur de déroutement | Silver | Int / Bool | 0, 1 | `fact_flights` |
| `CARRIER_DELAY` | Retard dû au transporteur | Silver | Numérique | Minutes | `fact_flights` |
| `WEATHER_DELAY` | Retard dû à la météo | Silver | Numérique | Minutes | `fact_flights` |
| `NAS_DELAY` | Retard dû au réseau aérien national | Silver | Numérique | Minutes | `fact_flights` |
| `SECURITY_DELAY` | Retard dû à la sécurité | Silver | Numérique | Minutes | `fact_flights` |
| `LATE_AIRCRAFT_DELAY` | Retard dû à un avion en retard | Silver | Numérique | Minutes | `fact_flights` |
| `DISTANCE` | Distance du vol | Silver | Numérique | Miles | `fact_flights` |
| `CRS_ELAPSED_TIME` | Temps prévu du vol | Silver | Numérique | Minutes | `fact_flights` |
| `ACTUAL_ELAPSED_TIME` | Temps réel du vol | Silver | Numérique | Minutes | `fact_flights` |
| `AIR_TIME` | Temps de vol effectif | Silver | Numérique | Minutes | `fact_flights` |
| `IS_DELAYED_ARR` | Indicateur de retard à l’arrivée | Silver | Bool | TRUE / FALSE | `fact_flights` |

---

## Marts

### `mart_benchmarking`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `carrier_key` | Référence transporteur | FK depuis `fact_flights` | Int | Clé étrangère | `mart_benchmarking` |
| `carrier_name` | Nom du transporteur | `dim_carrier` | Texte | Nom de transporteur | `mart_benchmarking` |
| `year` | Année analytique | `dim_date` | Int | 2009–2018 | `mart_benchmarking` |
| `total_flights` | Volume total de vols | Agrégation de `fact_flights` | Int | Nombre de vols | `mart_benchmarking` |
| `avg_arr_delay` | Retard moyen à l’arrivée | Agrégation | Numérique | Minutes | `mart_benchmarking` |
| `cancellation_rate` | Taux d’annulation | Agrégation | Pourcentage | 0–100 (%) | `mart_benchmarking` |
| `otp_pct` | Taux OTP (on-time performance) | Agrégation | Pourcentage | 0–100 (%) | `mart_benchmarking` |
| `rank_otp` | Classement OTP par année | Calcul window | Int | Rang | `mart_benchmarking` |
| `rank_cancellation` | Classement annulation par année | Calcul window | Int | Rang | `mart_benchmarking` |
| `rank_delay` | Classement retard moyen par année | Calcul window | Int | Rang | `mart_benchmarking` |
| `score_composite` | Score composite de benchmark | Calcul pondéré des rangs | Float | Score pondéré | `mart_benchmarking` |
| `peer_group` | Groupe de transporteurs | `carrier_type` depuis `dim_carrier` | Texte | Legacy, Low Cost, Ultra Low Cost, Other | `mart_benchmarking` |

### `mart_otp_monthly`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `carrier_key` | Référence transporteur | FK depuis `fact_flights` | Int | Clé étrangère | `mart_otp_monthly` |
| `carrier_name` | Nom du transporteur | `dim_carrier` | Texte | Nom de transporteur | `mart_otp_monthly` |
| `year` | Année analytique | `dim_date` | Int | 2009–2018 | `mart_otp_monthly` |
| `month` | Mois analytique | `dim_date` | Int | 1–12 | `mart_otp_monthly` |
| `total_flights` | Volume total de vols | Agrégation de `fact_flights` | Int | Nombre de vols | `mart_otp_monthly` |
| `avg_arr_delay` | Retard moyen à l’arrivée | Agrégation | Numérique | Minutes | `mart_otp_monthly` |
| `cancellation_rate` | Taux d’annulation | Agrégation | Pourcentage | 0–100 (%) | `mart_otp_monthly` |
| `otp_pct` | Taux OTP par mois | Agrégation | Pourcentage | 0–100 (%) | `mart_otp_monthly` |

### `mart_otp_annual`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `carrier_name` | Nom du transporteur | `dim_carrier` | Texte | Nom de transporteur | `mart_otp_annual` |
| `year` | Année analytique | `dim_date` | Int | 2009–2018 | `mart_otp_annual` |
| `total_flights` | Volume total de vols | Agrégation de `fact_flights` | Int | Nombre de vols | `mart_otp_annual` |
| `avg_arr_delay` | Retard moyen à l’arrivée | Agrégation | Numérique | Minutes | `mart_otp_annual` |
| `cancellation_rate` | Taux d’annulation | Agrégation | Pourcentage | 0–100 (%) | `mart_otp_annual` |
| `otp_percentage` | Taux OTP annuel | Agrégation | Pourcentage | 0–100 (%) | `mart_otp_annual` |
| `otp_rank` | Classement OTP annuel | Calcul window | Int | Rang | `mart_otp_annual` |

### `mart_cancellations`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `carrier_key` | Référence transporteur | FK depuis `fact_flights` | Int | Clé étrangère | `mart_cancellations` |
| `carrier_name` | Nom du transporteur | `dim_carrier` | Texte | Nom de transporteur | `mart_cancellations` |
| `year` | Année analytique | `dim_date` | Int | 2009–2018 | `mart_cancellations` |
| `CANCELLATION_CODE` | Motif d’annulation | Silver | Texte | A, B, C, D | `mart_cancellations` |
| `cancellation_count` | Nombre de vols annulés | Agrégation | Int | Nombre de vols | `mart_cancellations` |
| `pct` | Part des annulations par code | Calcul | Pourcentage | 0–100 (%) | `mart_cancellations` |

### `mart_delay_causes`

| Colonne | Description métier | Source BTS | Type | Valeurs possibles / Unité | Table d'appartenance |
|---|---|---|---|---|---|
| `carrier_key` | Référence transporteur | FK depuis `fact_flights` | Int | Clé étrangère | `mart_delay_causes` |
| `carrier_name` | Nom du transporteur | `dim_carrier` | Texte | Nom de transporteur | `mart_delay_causes` |
| `year` | Année analytique | `dim_date` | Int | 2009–2018 | `mart_delay_causes` |
| `total_delay_minutes` | Somme des retards à l’arrivée | Agrégation | Minutes | `mart_delay_causes` |
| `pct_carrier` | Part du retard dû au transporteur | Calcul | Pourcentage | 0–100 (%) | `mart_delay_causes` |
| `pct_weather` | Part du retard dû à la météo | Calcul | Pourcentage | 0–100 (%) | `mart_delay_causes` |
| `pct_nas` | Part du retard dû au réseau aérien | Calcul | Pourcentage | 0–100 (%) | `mart_delay_causes` |
| `pct_security` | Part du retard dû à la sécurité | Calcul | Pourcentage | 0–100 (%) | `mart_delay_causes` |
| `pct_late_aircraft` | Part du retard dû à avion en retard | Calcul | Pourcentage | 0–100 (%) | `mart_delay_causes` |
