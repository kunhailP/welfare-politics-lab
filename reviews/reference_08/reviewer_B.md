# Reviewer B — reference 08 제한적 재검토

**내부 AI re-review**이며 새 블라인드 리뷰·외부 동료심사·수집 승인이 아니다. 본인의 기존 문맥을 유지했다. 허용된 packet의 질문·사양·코드·테스트·저자 집계만 읽었고 부모 저장소·문서·원자료·다른 리뷰어 보고서·부모 후속 실행은 읽거나 검증하지 않았다.

**판정:** 새 human-trained reference는 이전의 미구현 제안을 실제 비교 코드로 옮겼다. person-level CV, target outcome을 사용하지 않는 feature 경로, 고정 clipping 규칙, component별 선형 bounds와 public replay 연결은 대체로 타당하다. 다만 **training source의 income 일관성 검사가 필터 뒤에 있어 부분적인 사람 기록을 학습에 허용하는 결함**이 있다. component의 joint bounds 설명과 reference 출력의 rollout 표기도 작게 고쳐야 한다. 원자료 집계와 실제 LLM 성능·연구의 독창성은 이번 검증으로 인증되지 않는다.

## 실행·독립 검증

지정 interpreter로 packet에서 `PYTHONPATH=src OPENBLAS_NUM_THREADS=1` 및 bytecode 비활성화를 사용했다. **66개 테스트가 모두 통과했다.** namespace sandbox 제한 때문에 허용된 escalated 실행 경로를 사용했다.

추가 합성 검증은 다음과 같다.

- 200명/800 label 학습, 80명 target, 별도 pilot의 전체 CLI를 실행했다. 학습/target 사람 비중복, 다섯 person fold의 정확한 분할, 알려진 conditional mean 복원을 확인했다. target human labels를 모두 다른 유효값으로 바꾸고 다시 실행해도 세 predictor의 main 예측 배열은 원소별로 같았다.
- 불균형 canonical 설계 50개에서 missing 세 행의 **400개 endpoint completion**을 열거했다. high/low component interval은 각각 실제 선형 최소/최대와 일치했다. high component weight는 low 사람에서, low component weight는 high 사람에서 수치 오차 범위의 0이었다.
- public keyed replay에 canonical X, shuffled attempts, 역순 request/A/B 매핑 및 invalid whole-pair를 넣었다. high 쪽 두 행만 invalid인 경우 high component의 completion width는 약2000 CAD였고 low component는 수치 오차 범위의 point로 남았다. low의 human-reference signed error도 0으로 유지되었다.
- 아래 B19의 비정상 source 입력과 clipping 관련 반례도 독립 실행했다. 모두 합성 자료이며 원자료 실행이 아니다.

## 타당한 부분과 leakage 경계

`statistical_references.py:29–43`은 canonical recipient basis와 선택된 income interaction만 사용한다. ID·task number·target allocation·job risk·parenthood가 feature에 들어가지 않는다. `fit_predict:46–65`는 사람 overlap을 거부하고 training labels만 읽는다. target predictor frame에서 allocation을 제거하는 CLI 경로와 functional whitelist가 함께 작동한다.

`person_folds:68–82`와 CLI `128–146`은 training 사람만 income strata 안에서 분할하고, 같은 사람의 모든 남은 행을 한 fold에 둔다. validation labels는 예측 계산 후 error 평가에만 사용된다. 세 reference를 모두 보고하며 CV winner나 hyperparameter를 고르는 경로가 없다. 모든 사람이 네 행을 가진 정상 입력에서는 pooled row RMSE/MAE도 사람을 동등하게 가중한다.

평균은 **training mean**이고 main mean oracle이 아니다. recipient-only18열, income-interacted36열 OLS 및 no-regularization/full-rank 조건은 사양과 맞는다. [0,4000] clipping은 명시된 statistical prediction rule이므로 invalid LLM reply의 사후 clamping과 구별된다. 연속 conditional mean을 그대로 평가하고 가짜 respondent/provider 기록을 만들지 않는 분리도 적절하다.

이것은 **계산 경로의 target-label 비의존성**이다. 이미 human main 결과를 본 후 reference 사양을 만들었다는 연구 설계상의 적응을 지우지는 않는다. 사양이 fit 전에 작성되었다는 순서는 저자 설명으로 취급하며 독립 인증하지 않았다. 같은 source의 person-disjoint label access는 untouched/external validation과 다르다.

## 결함과 최소 수정

### B19 — 중간: income 필터가 training 사람의 불일치와 부분 행을 숨긴다

**근거/위치:** `statistical_references.py:107–114`. 원래 네 행을 가진 사람을 확인한 뒤 각 행의 income이 high/low인지 필터하고, **그 뒤** `pool.groupby('id').respondent_income.nunique()`를 검사한다. 한 사람의 두 행이 High이고 나머지 두 행이 Medium 또는 missing이면 후자가 사라져 불일치 검사를 통과한다.

독립 합성 CLI에서 정상 source의 한 training 사람의 두 행만 Medium으로 바꾸자, 실행이 성공하고 **training_people=200, training_labels=798**을 보고했다. 원래 규칙의 800 label 대신 두 행만 남은 사람을 학습과 CV에 포함한 것이다. person fold leakage는 없지만 complete four-profile cohort와 equal-person weighting 조건을 위반한다.

**최소 수정/검증:** high/low 필터 **전에 source 사람별 income 일관성을 검사**하고, 필터 후에도 training pool에서 사람당 네 행을 assertion한다. 일관되게 Medium/missing인 사람은 통째로 제외하고, 사람 내부 혼합 category는 거부하는 테스트를 추가한다. 저자 877명/3508 label 집계가 맞다면 이 결함이 실제 보고 결과에 작동했다는 증거는 없다. 그 원자료 조건은 독립 확인하지 않았다.

### B20 — 낮음: canonical component의 joint-feasibility 경고가 현재 설계에는 맞지 않는다

**근거/위치:** `paired_evaluation.py:15–20`은 개별 sharp component interval의 joint set이 직사각형이 아닐 수 있으므로 차감해 sharp gamma를 재구성하지 말라고 한다. 일반적인 여러 contrast에서는 맞는 주의다. 그러나 현재 **완전 상호작용된 canonical 두 그룹 설계와 독립적인 행별 [0,4000] completion box**에서는 특수하게 high/low component가 서로 다른 사람의 outcome에만 의존한다.

OLS를 두 그룹별 regression으로 재매개변수화하면 문제가 분리된다. 따라서 연속 completion에서는 joint component 범위가 직사각형이다. 정수 action만 허용하면 attainable set은 두 그룹의 discrete set의 Cartesian product이며 interval hull이 직사각형이다. 어느 경우에도

`gamma interval = [low_L − high_U, low_U − high_L]`

가 sharp하다. 위 50개 설계에서도 자체 gamma bounds와 일치했다. 공유 budget이나 새로운 cross-row completion 제약이 생기는 경우는 별개다.

**최소 수정/검증:** docstring을 현재 설계의 분리 성질과 일반화 시 주의로 나눠 쓴다. 지금처럼 gamma 자체의 weight로 직접 계산하는 코드는 유지해도 좋다. 계산 오류나 interval 과소포함은 발견하지 않았다. component support 분리와 직접 gamma interval 일치 테스트를 추가하면 된다.

### B21 — 낮음: human-trained reference report 안의 target 표기가 여전히 “one recorded rollout”이다

**근거/위치:** `paired_evaluation.py:50`의 공통 evaluator target 문자열이 statistical reference report에도 그대로 들어간다. 합성 CLI 출력에서도 확인했다. 바깥 status와 limitations는 conditional means이며 trajectories를 만들지 않았다고 정확히 설명한다.

**최소 수정/검증:** generic finite-array target과 outcome provenance를 분리하거나, reference 호출에서 conditional-mean prediction임을 명시한다. LLM replay에만 recorded-rollout 표기를 사용하면 중첩 report의 오해를 없앨 수 있다. 수치 계산에는 영향이 없다.

## 보존해야 할 해석 조건

**Clipping은 recipient-only prediction을 비선형으로 만든다.** clip이 없고 target X가 full rank라면 recipient-only 예측은 base column space 안에 있으므로 moderation projection이 정확히 0이다. 이 성질은 clipping 후에는 보장되지 않는다. bounded training labels로 recipient-only OLS를 학습한 독립 반례에서 target의 778행이 clip되었고, raw prediction의 gamma는 약0, clipped prediction의 gamma는 **약−393.86 CAD**였다. respondent income을 feature로 사용하지 않아도 서로 다른 group task distributions 때문에 가능하다.

따라서 현재 테스트의 zero-interaction 결과를 모든 clipped recipient-only reference에 일반화하면 안 된다. 저자 main fits에서 clipping이 없었다는 보고가 맞다면 현재 0 moderation 설명은 타당하다. raw range와 clipping 수를 CV/main에 계속 남기고, 이 경계 사례를 테스트에 추가하면 충분하다. clipping 규칙 자체를 사후 변경할 이유는 없다.

또한 unclipped interacted predictor의 target projection은 학습한36개 계수를 그대로 복원한다. 그래서 그 component가 training remainder의 group slopes와 같아지는 것은 선형대수적 성질이다. main label과의 discrepancy 및 row prediction errors는 유효한 out-of-person 평가지만, 계수의 재출현 자체가 새로운 validation 증거는 아니다.

component bounds는 고정 X의 **각 선형 contrast에 대해 정확한 completion bounds**다. human reference error는 fully observed human component에서 빼면 된다. missing 행을 삭제하지 않고 signed errors를 보고하는 현재 구현은 맞다. 이것은 sampling/decoding CI나 “각 그룹의 모든 사람이 그 방향으로 응답했다”는 주장이 아니다.

## 남은 실증적 한계와 최소 다음 단계

저자 집계의 human components 약135.59/190.75와 moderation55.16, reference MAE·CV scores·3508 label·source hashes는 **저자 제공 수치**다. 원자료 없이 재현하지 않았다. question에 명시된 aggregate report와 후속 implementation-metadata 변경의 차이도 공개된 한계로 유지한다. 부모의 최종 rerun/hash를 이 검토의 독립 검증으로 취급하지 않는다.

constant predictor가 moderation에서 더 가까우면서 두 recipient slopes를 0으로 만드는 예는 단일 점수의 해석 한계를 보여준다. 그렇다고 primary score를 버리거나 outcome-selected composite를 만들 필요는 없다. 기존 primary/secondary 지위를 유지하고 component·MAE/RMSE·strong conditional diagnostics를 함께 보고하는 것이 적절하다. 더 낮은 reference error는 새로운 인간 조사나 실제 LLM의 열등성 증거가 아니다.

이 reference들은877명의 human labels를 쓰며 job risk/parenthood는 쓰지 않는다. 계획된 N/F/F-I와 정보 접근·feature set·conditional-mean 대 single-rollout 목표가 다르므로 동일 자원 대결이나 깨끗한 prompt-arm ablation comparator가 아니다. public-source 사전학습 노출도 배제할 수 없다. person-level CV는 training-source 내부의 predictive diagnostic이며 population fidelity나 독립 정치적 메커니즘을 식별하지 않는다.

**최소 조치:** B19의 source/person guard를 고치고 B20/B21 표현을 정리한 뒤, 세 reference와 동일 평가를 그대로 고정해 유지한다. 새 oracle나 사후 winner 선택을 더할 필요는 없다. component를 보는 것이 실제 model 결과의 어떤 결론을 바꾸는지는 아직 관측되지 않았다. 반복·presentation·다른 model에서의 안정성, 실제 native isolation/전달/재개, 고정 settings·비용 및 실질적 중요성 조건은 여전히 미검증이다. 소득 ablation·subgroup 관계 자체의 선행연구 중복도 이 구현으로 해소되지 않으며, 새 full-text 확인을 수행한 것은 아니다.
