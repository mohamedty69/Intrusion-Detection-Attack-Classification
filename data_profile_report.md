# Data Profile Report

## Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
- Rows: 225745
- Missing values (total cells): 4
- Infinity values (+/-inf, numeric-coerced columns): 64
- Duplicate rows: 2633
- Label distribution:
  - DDoS: 128027 (56.71%)
  - BENIGN: 97718 (43.29%)

## Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
- Rows: 286467
- Missing values (total cells): 15
- Infinity values (+/-inf, numeric-coerced columns): 727
- Duplicate rows: 72353
- Label distribution:
  - PortScan: 158930 (55.48%)
  - BENIGN: 127537 (44.52%)

## Friday-WorkingHours-Morning.pcap_ISCX.csv
- Rows: 191033
- Missing values (total cells): 28
- Infinity values (+/-inf, numeric-coerced columns): 216
- Duplicate rows: 6888
- Label distribution:
  - BENIGN: 189067 (98.97%)
  - Bot: 1966 (1.03%)

## Monday-WorkingHours.pcap_ISCX.csv
- Rows: 529918
- Missing values (total cells): 64
- Infinity values (+/-inf, numeric-coerced columns): 810
- Duplicate rows: 26935
- Label distribution:
  - BENIGN: 529918 (100.00%)

## Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
- Rows: 288602
- Missing values (total cells): 18
- Infinity values (+/-inf, numeric-coerced columns): 396
- Duplicate rows: 35630
- Label distribution:
  - BENIGN: 288566 (99.99%)
  - Infiltration: 36 (0.01%)

## Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
- Rows: 170366
- Missing values (total cells): 20
- Infinity values (+/-inf, numeric-coerced columns): 250
- Duplicate rows: 6066
- Label distribution:
  - BENIGN: 168186 (98.72%)
  - Web Attack � Brute Force: 1507 (0.88%)
  - Web Attack � XSS: 652 (0.38%)
  - Web Attack � Sql Injection: 21 (0.01%)

## Tuesday-WorkingHours.pcap_ISCX.csv
- Rows: 445909
- Missing values (total cells): 201
- Infinity values (+/-inf, numeric-coerced columns): 327
- Duplicate rows: 24065
- Label distribution:
  - BENIGN: 432074 (96.90%)
  - FTP-Patator: 7938 (1.78%)
  - SSH-Patator: 5897 (1.32%)

## Wednesday-workingHours.pcap_ISCX.csv
- Rows: 692703
- Missing values (total cells): 1008
- Infinity values (+/-inf, numeric-coerced columns): 1586
- Duplicate rows: 81909
- Label distribution:
  - BENIGN: 440031 (63.52%)
  - DoS Hulk: 231073 (33.36%)
  - DoS GoldenEye: 10293 (1.49%)
  - DoS slowloris: 5796 (0.84%)
  - DoS Slowhttptest: 5499 (0.79%)
  - Heartbleed: 11 (0.00%)

## Overall Summary
- Total rows across files: 2830743
- Total missing values: 1358
- Total infinity values: 4376
- Total duplicate rows: 256479
- Overall label distribution:
  - BENIGN: 2273097 (80.30%)
  - DoS Hulk: 231073 (8.16%)
  - PortScan: 158930 (5.61%)
  - DDoS: 128027 (4.52%)
  - DoS GoldenEye: 10293 (0.36%)
  - FTP-Patator: 7938 (0.28%)
  - SSH-Patator: 5897 (0.21%)
  - DoS slowloris: 5796 (0.20%)
  - DoS Slowhttptest: 5499 (0.19%)
  - Bot: 1966 (0.07%)
  - Web Attack � Brute Force: 1507 (0.05%)
  - Web Attack � XSS: 652 (0.02%)
  - Infiltration: 36 (0.00%)
  - Web Attack � Sql Injection: 21 (0.00%)
  - Heartbleed: 11 (0.00%)

## Split Decision
Use a stratified split by label and keep file/time awareness to reduce leakage:
- Train: Monday, Tuesday, Wednesday
- Validation: Thursday
- Test: Friday
Reason: CICIDS2017 traffic is time-ordered and attack scenarios cluster by day. Random row split can leak near-duplicate flows and inflate metrics.

If you prefer row-level split instead of day-level holdout, use stratified 70/15/15 by Label after deduplication.