# Reviewer B — human-reference qualification 07

**범위 제한 내부 AI 재검토**이며 새 블라인드 리뷰·외부 동료심사·수집 승인이 아니다. 본인의 기존 문맥을 유지했다. 허용된 packet만 읽었고 부모 저장소·원자료·작성자 대화·다른 리뷰어 보고서는 읽지 않았다. 원자료 집계는 저자 제공이며 독립 확인하지 않았다.

**판정:** 새 audit은 고정 human reference의 해석을 제한하는 데 유용하다. 사람 단위 비중복 remainder와 draw 내 비복원 추출은 코드상 올바르게 구성되어 있다. 그러나 이는 population validation, 새로운 독립 인간 반복표본, 같은 사람/같은 task의 재측정이 아니다. 실제 모델의 가치를 보여주는 결과도 아니다. 작은 수치적 sign-count 결함과 몇 가지 보고/구현 조건을 아래에 남긴다.

## 확인한 코드와 합성 실행

`audit_human_reference_stability.py:53–75`는 중복 source row와 사람 내부 trait 불일치를 검사하고, 네 개의 완전한 profile 및 관측·범위 내 human outcome을 가진 high/low 사람을 남긴다. main/pilot ID의 중복·겹침·불완전 기록을 거부하며 remainder에서 두 집단의 사람을 제외한다. `77–95`는 main의 high/low 인원수를 맞춰 각 draw 안에서 사람을 비복원 추출하고, 그 사람의 모든 행을 함께 분석한다. `summarize`의 high·low·low-minus-high contrast 코딩도 맞다.

독립 합성 자료 248명에 main80·pilot8·remainder160을 구성하여 CLI를 실행했다. **50개 draw**에서 main/pilot 사람과 겹치지 않고, 각 draw의 high40/low40 및 사람당 네 행이 유지되었다. 알려진 high/low recipient contrast **300/450 CAD**, moderation **150 CAD**를 수치 오차 범위에서 모두 복원했다. 동일 seed의 두 실행 결과도 같았다. draw끼리는 실제로 겹쳤다. 이는 코드의 합성 검증이며 저자 source 수치의 재현이 아니다. enclosed script의 hash는 aggregate receipt의 script hash와 일치했다.

## 새 human audit이 허용하는 해석

1. **비중복은 사람에 대한 것이다.** remainder는 main/pilot과 사람을 공유하지 않으나 같은 조사·선택 과정·측정·공개 archive를 공유한다. 이미 결과를 본 source이므로 untouched/external holdout이 아니다. `complete_high_low_pool`은 main/pilot까지 포함하므로 독립적인 세 번째 검증 표본으로 세면 안 된다.
2. **맞춘 composition은 high/low 인원수다.** 다른 respondent facts, recipient profile의 주변/결합 분포, 과제 내용은 맞추지 않는다. 각 draw에서는 사람과 X가 함께 변한다. 따라서 분포는 locked X에서 gamma_H의 측정 오차나 CI가 아니라, 이 archive와 추출 규칙에서의 cohort/task-composition sensitivity다. 이를 J_FN의 sampling CI로 가져오거나 model common-task DID와 빼서 원인별 decomposition으로 해석하면 안 된다.
3. **500회는 500개 새 인간 표본이 아니다.** 저자 제공 stratum 크기를 전제로 두 draw의 예상 공통 사람 수는 `304²/482 + 252²/395 ≈ 352.5명`이다. 반복 분석으로 관측된 인간 수가 늘어나지 않는다. 다만 겹친다는 이유만으로 고정 archive에 조건부인 알고리즘상 Monte Carlo 추출의 독립성까지 부정할 필요는 없다. seed로 반복 생성한 random subset의 빈도는 그 제한된 추출 규칙을 설명할 수 있다. 그것은 human population의 sign probability나 독립 replication 성공률과 다르다.
4. **현재의 양적 한정은 적절하다.** 466/500, 500/500 및 q05/q95를 population 확률·CI로 부르지 않고, locked main target을 바꾸지 않는다는 설명을 유지해야 한다. 500/500 positive도 표본 밖의 모든 cohort 또는 인간에게 positive라는 보장은 아니다. 34개 negative draw 역시 main의 알려진 finite contrast를 불확실한 관측값으로 바꾸지는 않는다.
5. **크기 변화도 숨기지 말아야 한다.** 저자 집계표에서는 main의 high/low recipient contrasts가 약135.6/190.7 CAD이고, remainder draw의 q05가 약151.5/272.1 CAD다. 방향이 모두 positive라는 요약만으로 크기까지 안정적이라고 할 수 없다. 이 숫자는 저자 보고로만 인용하며 p-value나 main cohort의 이상성 판정으로 읽지 않는다. 더 유리한 human subset으로 endpoint를 바꾸는 근거도 아니다.

이 audit은 작은 moderation의 sign reversal 하나에 정치적 결론을 싣지 말라는 경고를 강화한다. 소득이 인간 태도를 인과적으로 바꾸는지, self-interest가 작동하는지, synthetic 응답이 대표성을 갖는지는 새로 식별하지 않는다.

## 검증 가능한 결함과 최소 보완

### B18 — 낮음: 정확히 0인 moderation을 수치적 양·음으로 집계한다

**근거:** `99–106`은 `>0`, `<0`, `==0`을 그대로 사용한다. 합성 remainder의 참 moderation을 정확히 0으로 둔 100개 draw에서 값은 약 −5.3×10⁻¹³부터 8.2×10⁻¹³ CAD였으나 **positive41/negative59/zero0**으로 보고되었다.

**영향:** 일반 입력에서 zero의 sign frequency를 잘못 표현할 수 있다. 실제 저자 466/34가 이 결함 때문에 달라진다고 확인한 것은 아니다.

**최소 수정/검증:** 예를 들어 1e-8 CAD의 명시적인 numerical-zero tolerance로 near-zero를 따로 세고, 이것이 실질적 중요성 margin은 아님을 밝힌다. 모든 draw의 signed CAD 값은 그대로 보존한다. 정확한 additive/no-moderation fixture가 모두 numerical-zero로 분류되는 회귀 테스트를 추가한다.

### Rank-deficient draw는 진단을 남겨야 하며 비식별로 단정하면 안 된다

`summarize:27–29`는 전체 36계수의 full rank를 요구한다. nuisance level을 제거한 독립 fixture는 rank34였지만 primary c는 estimable이었고, 이 함수는 “Full-rank sensitivity design required”로 거절했다. 이는 선언된 구현 제한으로 이해할 수 있으며 c 비식별의 증거가 아니다. high, low, moderation 각각의 estimability는 별도로 확인해야 한다.

현재 코드가 실패 draw를 몰래 버리거나 성공할 때까지 다시 뽑지 않는 점은 좋다. 더 넓게 재사용할 경우 draw ID·rank·conditioning·세 contrast의 row-space residual을 기록하고, 중단/부분 실행 상태를 명시하면 된다. full-rank draw만 재추출해 500개를 채우면 sensitivity law가 바뀐다. 현재 source의 500개가 모두 rank36이었다는 수치는 독립 검증하지 않았다.

### 작은 보고 보완

“composition-matched”는 **income-group-count matched**로 구체화한다. eligibility가 profile completeness뿐 아니라 human allocation의 관측성과 0–4000 범위까지 요구한다는 점과 제외 원인별 수를 기록하면 기존 cohort와의 일관성을 확인하기 쉽다. 공유 `matrix_and_contrast`와 `LEVELS`를 import하므로 script hash 외에 그 coding/dependency version도 함께 고정하는 것이 좋다. draw membership과 결과 hash를 남기는 현재 구현은 유용하다.

## 미구현 disjoint-human comparator

877명으로 학습하여 main의 고정 task를 예측하는 작은 통계 predictor는 유용한 실용 기준이 될 수 있다. 하지만 아직 구현·고정·평가되지 않았으므로 “human-trained baseline과 비교했다”거나 superiority를 주장할 수 없다.

최소한 다음을 먼저 고정해야 한다.

- 입력 feature, 모델 계열, hyperparameter 범위, 출력 범위/rounding 규칙, 학습 목적과 main의 동일 진단·contrast 계산 경로.
- 모든 전처리·변수 선택·튜닝을 포함한 **person-level** 내부 validation. 네 행을 fold 사이에 나누지 않는다. source ID 자체는 predictor feature로 쓰지 않는다.
- main outcomes로 모델·설정·보고 대상을 고르지 않는 절차. 이미 main human 결과를 본 연구라는 사실은 유지하며, disjoint fit만으로 이를 untouched test로 바꾸었다고 하지 않는다.
- 약877명의 네 judgment를 사용하는 labeled access와 label/computation 비용. 비교 목적은 실용 reference이며 zero-shot LLM과 동일 자원 경쟁이 아니다. 공개 source가 LLM 사전학습에 포함되었을 가능성도 배제하지 않는다.

Conditional mean predictor와 single recorded model rollout의 차이도 설명해야 한다. 더 낮은 error가 나오더라도 그것이 인간 개별 trajectory의 재현이나 LLM의 일반적 열등성을 뜻하지는 않는다. main tasks의 support, bounded output과 missing-feature 처리를 사전에 정해야 하며, main label을 보고 사후 보정해서는 안 된다.

## 남는 실증적 기여와 부족한 결과

여전히 가능한 주장은 특정 welfare task에서 **명시적 소득 입력이 어떤 고정 human-reference 판단을 개선·악화시키는지**를 통제된 출력 비교로 밝히는 좁은 실증 결과다. 실제 동일 출력에 coarse 및 stronger conditional diagnostics를 함께 적용하고, repeat/presentation 및 다른 model에서 해석의 안정성을 구분해야 설득력이 생긴다. 방향은 F에 유리할 필요가 없다.

한 번의 rollout에서 gamma가 변하거나 0을 넘는 것, J_FN이 조금 음수인 것, 평균이 맞는 것, human draw의 sign count가 많은 것만으로는 중요한 정치적 왜곡·의미 있는 성공·일반화·새로움을 입증하지 못한다. 단순 income ablation이나 subgroup distortion은 독립적 기여로 충분하지 않다. 실제 main target은 그대로 두고, 새 audit을 post-inspection qualification으로 보존하며, 다음 변경은 audit를 더 늘리기보다 비교 계획과 실행 조건을 고정하는 데 집중하는 것이 낫다.

**보충 노출 기록:** 검토 중 부모 에이전트가 [arXiv:2609.33055](https://arxiv.org/abs/2609.33055)의 v2 날짜(2026-10-18)와 초록에 human income structure, counterfactual income manipulation, explicit-income removal, 다중 model 비교가 포함된다는 요약을 별도로 전달했다. 해당 초록/원문은 직접 읽거나 독립 확인하지 않았다. 이 잠재적 중복 때문에 소득 ablation 자체의 독창성 평가는 더 보수적으로 두며, 정확한 선행연구 주장에는 원문 확인이 필요하다.

native execution·격리·model/settings·비용·repeat/presentation과 실제 model evidence의 미해결 조건은 이번 human audit으로 해소되지 않는다. 검토의 상세함이나 합성 검증 횟수도 실증적 준비도의 대리 지표가 아니다.
