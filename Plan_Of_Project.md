# Intrusion Detection & Attack Classification - Plan_Of_Project

## 1) What This Project Is About

### Project idea in one line
You are building a system that reads network flow records and predicts whether each flow is normal (BENIGN) or an attack, and if attack, which attack type.

### What problem this solves
In real systems, attacks happen inside huge amounts of normal traffic. Security teams cannot inspect everything manually. This project helps by:

- Detecting suspicious traffic automatically.
- Classifying the attack category (DDoS, PortScan, Web Attack, etc.).
- Reducing alert fatigue and response time.
- Creating a reusable ML pipeline that can later be integrated into backend services.

### What the data represents
Your CSV files are network flow-level statistics (not raw packet payload). Each row is one flow/session summary with numerical features.

- A flow is like: source-to-destination communication over time.
- Features describe packet counts, byte sizes, timing, flags, rates, active/idle periods.
- The target label is in column `Label` (in these files it appears as ` Label` with a leading space).

### What your model will do with this data
You can solve this in 2 layers:

1. Binary detection:
- BENIGN vs ATTACK.

2. Multi-class classification:
- Which attack family (DDoS, DoS Hulk, PortScan, Bot, FTP-Patator, etc.).

### Main benefits of this project

- Practical cybersecurity value: faster detection and triage.
- Strong portfolio project: combines data engineering, ML, and backend serving.
- Real-world constraints: class imbalance, noisy labels, concept drift, attack diversity.
- Architecture value: you can expose a model endpoint and add monitoring/logging like a production backend system.

### End goal (clear output)
By project end, you should have:

- A reproducible training pipeline.
- A validated model with measurable metrics.
- A backend API endpoint for prediction.
- A short report/dashboard explaining performance and limitations.

---

## 2) Your Dataset Files and What Each One Means

You currently have 8 raw files in `data/raw`. They match CICIDS-style splits by weekday/time and scenario.

### Shared schema facts

- Each file has 79 columns.
- 78 are features + 1 target label column (` Label`).
- Feature schema is consistent across files.

### File-by-file breakdown (using actual counts from your files)

1. **Monday-WorkingHours.pcap_ISCX.csv**
- Rows: 529,918
- Labels: only BENIGN (529,918)
- Meaning: clean baseline traffic day.
- Usefulness: learn normal behavior; useful for anomaly baselining.

2. **Tuesday-WorkingHours.pcap_ISCX.csv**
- Rows: 445,909
- Labels:
  - BENIGN: 432,074
  - FTP-Patator: 7,938
  - SSH-Patator: 5,897
- Meaning: brute-force style attacks against auth services.
- Usefulness: credential attack detection.

3. **Wednesday-workingHours.pcap_ISCX.csv**
- Rows: 692,703
- Labels:
  - BENIGN: 440,031
  - DoS Hulk: 231,073
  - DoS GoldenEye: 10,293
  - DoS slowloris: 5,796
  - DoS Slowhttptest: 5,499
  - Heartbleed: 11
- Meaning: mostly DoS families + tiny rare class (Heartbleed).
- Usefulness: stress-test class imbalance handling.

4. **Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv**
- Rows: 170,366
- Labels:
  - BENIGN: 168,186
  - Web Attack - Brute Force: 1,507
  - Web Attack - XSS: 652
  - Web Attack - Sql Injection: 21
- Meaning: web application attacks.
- Usefulness: rare event classification in application-layer behavior.

5. **Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv**
- Rows: 288,602
- Labels:
  - BENIGN: 288,566
  - Infiltration: 36
- Meaning: lateral/inside compromise-like behavior with extreme rarity.
- Usefulness: demonstrates difficulty of very rare class detection.

6. **Friday-WorkingHours-Morning.pcap_ISCX.csv**
- Rows: 191,033
- Labels:
  - BENIGN: 189,067
  - Bot: 1,966
- Meaning: botnet-like activity.
- Usefulness: low prevalence bot detection.

7. **Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv**
- Rows: 286,467
- Labels:
  - PortScan: 158,930
  - BENIGN: 127,537
- Meaning: scanning-heavy period.
- Usefulness: high-signal scanning behavior; usually easier to classify.

8. **Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv**
- Rows: 225,745
- Labels:
  - DDoS: 128,027
  - BENIGN: 97,718
- Meaning: volumetric attack period.
- Usefulness: strong attack signature for detection/classification.

### Important observation
Your data is **highly imbalanced** for some classes (for example Heartbleed, Infiltration, SQL Injection). This will strongly affect model design and metric selection.

---

## 2.1) What the Features Mean (Practical Explanation)

Below is the practical meaning of all feature groups so you can reason about behavior, even if you are new to ML.

### A) Flow identity and size context
- Destination Port
- Flow Duration
- Total Fwd Packets
- Total Backward Packets
- Total Length of Fwd Packets
- Total Length of Bwd Packets

Why it matters:
- Attack traffic often has unusual port patterns, short repetitive flows, or abnormal packet/byte volume ratios.

### B) Packet length statistics
- Fwd Packet Length Max/Min/Mean/Std
- Bwd Packet Length Max/Min/Mean/Std
- Min Packet Length
- Max Packet Length
- Packet Length Mean
- Packet Length Std
- Packet Length Variance
- Average Packet Size
- Avg Fwd Segment Size
- Avg Bwd Segment Size

Why it matters:
- Different attack tools generate characteristic packet-size fingerprints.

### C) Rate and throughput features
- Flow Bytes/s
- Flow Packets/s
- Fwd Packets/s
- Bwd Packets/s

Why it matters:
- DDoS and DoS can show extreme rates.
- Slow attacks can show suspiciously low but persistent patterns.

### D) Timing/inter-arrival features (IAT)
- Flow IAT Mean/Std/Max/Min
- Fwd IAT Total/Mean/Std/Max/Min
- Bwd IAT Total/Mean/Std/Max/Min

Why it matters:
- Timing regularity/irregularity is often a stronger signal than packet count alone.

### E) TCP flags and header-level behavior
- Fwd PSH Flags, Bwd PSH Flags
- Fwd URG Flags, Bwd URG Flags
- FIN Flag Count, SYN Flag Count, RST Flag Count, PSH Flag Count, ACK Flag Count, URG Flag Count, CWE Flag Count, ECE Flag Count
- Fwd Header Length, Bwd Header Length, Fwd Header Length.1

Why it matters:
- Scans and connection abuse create unusual SYN/ACK/RST patterns.

### F) Directional balance and subflow
- Down/Up Ratio
- Subflow Fwd Packets, Subflow Fwd Bytes
- Subflow Bwd Packets, Subflow Bwd Bytes

Why it matters:
- Normal client-server sessions and attack sessions often have different directionality.

### G) Bulk transfer behavior
- Fwd Avg Bytes/Bulk
- Fwd Avg Packets/Bulk
- Fwd Avg Bulk Rate
- Bwd Avg Bytes/Bulk
- Bwd Avg Packets/Bulk
- Bwd Avg Bulk Rate

Why it matters:
- Useful to detect burst-transfer patterns and tool-driven traffic.

### H) Window/segment and payload activity
- Init_Win_bytes_forward
- Init_Win_bytes_backward
- act_data_pkt_fwd
- min_seg_size_forward

Why it matters:
- Captures transport-level mechanics that can separate normal stacks from malicious automation.

### I) Active/idle period behavior
- Active Mean/Std/Max/Min
- Idle Mean/Std/Max/Min

Why it matters:
- Bots, scanners, and low-and-slow attacks often alternate active and idle phases differently than human usage traffic.

### J) Target label
- Label

This is what you predict.

---

## 3) Execution Plan for You (Backend Developer Friendly)

You are a backend developer, so this plan uses backend-style thinking:

- Clear modules
- Reproducible pipelines
- API-first deployment
- Logging/monitoring mindset

## Timeline overview (8 weeks, simple and realistic)

1. Week 1: Data understanding and quality checks
2. Week 2: Baseline preprocessing + baseline models
3. Week 3: Metrics, imbalance handling, and model improvements
4. Week 4: Multi-class strategy and error analysis
5. Week 5: Training pipeline packaging (scripts + configs)
6. Week 6: Inference service (FastAPI) + validation
7. Week 7: Monitoring hooks + model card/report
8. Week 8: Final polish, documentation, and demo

---

## Phase-by-phase detailed plan

### Phase 1 (Week 1): Data Inventory and Sanity
Goal:
- Trust the data before modeling.

Tasks:
1. Build a profiling notebook/script that prints:
- row count per file
- label distribution per file
- missing values per feature
- infinity/NaN checks
- duplicate row checks

2. Standardize column names:
- remove leading spaces from headers (for consistency)
- unify label naming artifacts (for example weird character in Web Attack labels)

3. Decide train/validation/test split strategy:
- Prefer split by file/day or time-aware split to reduce leakage.

Deliverables:
- data_profile_report.md
- cleaned dataset metadata summary

### Phase 2 (Week 2): Baseline Pipeline
Goal:
- Build first end-to-end working model quickly.

Tasks:
1. Create preprocessing pipeline:
- numeric cleaning
- handling inf values
- optional robust scaling (tree models may not need scaling)

2. Start with easy baseline models:
- RandomForest
- LightGBM/XGBoost (if you install one)
- Logistic Regression (for reference baseline)

3. Do binary task first:
- BENIGN vs ATTACK

Deliverables:
- reproducible training script
- baseline metrics table

### Phase 3 (Week 3): Metric Design + Imbalance Handling
Goal:
- Avoid misleading high accuracy.

Tasks:
1. Use better metrics:
- Precision, Recall, F1 (macro and weighted)
- PR-AUC for rare attack classes
- Confusion matrix

2. Handle imbalance:
- class weights
- oversampling (SMOTE or simple resampling, carefully)
- threshold tuning for binary detector

3. Create a risk-oriented metric view:
- false negatives are usually more costly in security.

Deliverables:
- imbalance_experiments.md
- best binary detector checkpoint

### Phase 4 (Week 4): Multi-class Attack Classification
Goal:
- Identify specific attack family.

Tasks:
1. Train multiclass model with tuned preprocessing.
2. Analyze per-class confusion:
- which attacks get confused with benign
- which attacks get confused with each other
3. Decide policy for ultra-rare classes:
- keep as-is
- merge to OTHER_ATTACK
- hierarchical approach (binary then multiclass)

Deliverables:
- multiclass model + evaluation report

### Phase 5 (Week 5): Production-style Training Package
Goal:
- Move from notebook-only to maintainable project structure.

Tasks:
1. Add scripts/modules in `src/`:
- data_loading.py
- preprocessing.py
- train.py
- evaluate.py
- predict.py

2. Add configuration file:
- model params
- split config
- feature list

3. Save artifacts:
- model.pkl
- scaler/encoder if used
- metrics.json

Deliverables:
- repeatable CLI training pipeline

### Phase 6 (Week 6): Backend Inference API
Goal:
- Expose model as a backend service.

Tasks:
1. Build FastAPI endpoint:
- POST /predict
- input validation with Pydantic
- response: predicted class + confidence + optional risk level

2. Add health/version endpoints:
- GET /health
- GET /model-info

3. Add request/response logging (without sensitive data leakage).

Deliverables:
- running API service
- curl/Postman examples

### Phase 7 (Week 7): Monitoring and Security-Aware Ops
Goal:
- Prepare for real usage patterns.

Tasks:
1. Add inference logs for drift monitoring:
- feature summary stats over time
- predicted class frequency shifts

2. Add simple alerts:
- sudden increase in ATTACK probability

3. Create model card:
- training data scope
- known weak points (rare classes)
- intended usage and non-usage

Deliverables:
- monitoring checklist
- model card document

### Phase 8 (Week 8): Final Delivery
Goal:
- Present complete project professionally.

Tasks:
1. Final README with architecture and run steps.
2. Add diagrams:
- training flow
- inference flow
3. Demo script:
- run training
- run API
- send sample prediction request

Deliverables:
- final repo ready for portfolio/interview/demo

---

## Practical Working Style (for your background)

As a backend dev, focus on this loop:

1. Build small reliable scripts.
2. Add logging and config early.
3. Validate with tests on data contracts and API schema.
4. Keep notebooks for exploration only, not as final pipeline source.

Recommended principle:
- "Notebook for discovery, src/ for production."

---

## Suggested Milestone Checklist (simple tracking)

- [ ] Data profile completed
- [ ] Label cleanup rules finalized
- [ ] Binary baseline model trained
- [ ] Imbalance strategy selected
- [ ] Multi-class model evaluated
- [ ] Training pipeline scripted in `src/`
- [ ] FastAPI inference endpoint working
- [ ] Monitoring + report completed

---

## Risks You Should Expect (and how to handle)

1. Class imbalance hides failure on rare attacks.
- Mitigation: macro metrics + class weights + targeted evaluation.

2. Data leakage from random split across correlated flows.
- Mitigation: split by file/time scenario when possible.

3. Overfitting to known CICIDS distributions.
- Mitigation: validate by day/scenario holdout, not only random CV.

4. Encoding/label naming inconsistencies.
- Mitigation: normalize labels in one preprocessing function and version-control it.

---

## Final note
This is a strong project choice. It gives you cybersecurity domain value and lets you showcase backend strengths by shipping a real prediction service, not only a notebook model.