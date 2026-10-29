# Reviewer B — round 06 범위 제한 재검토

**내부 AI 재검토**이며 새 블라인드 리뷰·외부 동료심사·수집 허가가 아니다. 본인의 이전 문맥을 유지했다. 허용된 `shared/**`와 manifest만 읽었고 부모 저장소·원자료·상대 리뷰·Git 메타데이터는 읽지 않았다. 저자 제공 source receipt의 실제 원자료 수치는 독립 재현하지 않았다.

**판정:** 새 permutation control, fixed-cell 진단, midpoint-anchor W1 completion bounds 및 public keyed-path 연결에서 중대한 정확성 결함을 발견하지 않았다. 분포·projection/R2 보존은 명시된 additive 설계에 한정하면 타당하다. 더 강한 conditional 검사가 control을 검출한다는 사실도 정직하게 포함되어 있다. 이는 평가 예제의 개선이며 실증적 가치·실제 모델 실패·수집 준비도에 대한 새 증거는 아니다.

## 실행 및 독립 검증

지정된 interpreter로 `shared`에서 `PYTHONPATH=src OPENBLAS_NUM_THREADS=1`과 bytecode 비활성화를 사용했다. **57개 테스트가 모두 통과했고 manifest 34개 해시가 모두 일치했다.** 환경의 namespace 제한 때문에 허용된 escalated 실행 경로를 사용했다.

추가 합성 검증 결과는 다음과 같다.

- 불균형 셀과 반복된 정수 응답을 갖는 **200개 표, 400개 control**을 검사했다. 그중 **312개 control**이 실제로 바뀌었다. 전체·그룹별·pooled complete-profile별 multiset, 개별 응답 경계/정수성, additive cross-products와 sum of squares, OLS 계수와 R2 보존, contrast 이동 방향이 모두 성립했다. `changed_rows = 4 × cycles`도 확인하여 disjoint bookkeeping을 점검했다.
- **3,750개 completion**에서 네 W1 진단과 weighted cell-mean absolute-error 범위가 실제 완성값을 포함했다. 별도로 셀 크기가 **1/3/2/5**인 불균형 설계의 **1,250개 completion**을 수작업 방식의 독립 가중 합과 비교했다. 고정 셀·분모, W1 값, mean-error 값과 completion 범위가 모두 일치했다.
- canonical 설계와 shuffled request/attempt, 역순 A/B 매핑으로 public `evaluate_recorded` 경로를 직접 구성했다. F에 permutation control을 넣었을 때 lower-order W1은 0이고 group-by-profile W1은 **4000 CAD**로 검출되었다. 한 pair를 invalid JSON으로 바꾸면 **8개 행과 4개 joint cell을 유지한 채 2개 행만 unknown**으로 남았고 R2 계산은 중단되었다. 모두 software fixture다.

## 보존 주장: 타당한 범위

`distribution_control.py:27–50`은 서로 다른 profile의 반대 값쌍 `(a,b)`와 `(b,a)`를 선택해 두 profile 안에서 high/low 값을 교환한다. 따라서 각 profile의 multiset이 같고, 각 그룹은 다른 profile에서 a와 b를 서로 맞바꾸므로 그룹 multiset도 같다. 사용한 네 행을 재사용하지 않아 사전 계산한 gain이 후속 교환으로 무효화되지 않는다. `39–46`의 gain과 방향 조건은 실제 contrast 변화와 일치했다. 기존 금액의 permutation이므로 경계와 정수성도 자동으로 유지된다.

보존되는 회귀는 **Z = [recipient basis, group]**인 고정 additive projection이다. profile 합계와 group 합계가 같아 Z'y가 같고, permutation으로 y'y 및 전체 평균도 같으므로 fitted values와 SSE/SST, 따라서 정의되는 경우 R2가 같다. full-rank Z에서는 계수도 같고, rank-deficient Z에서는 고유 fitted projection을 비교해야 한다. `diagnostic_comparison.py:80–96`이 이 구분을 반영한다. 상수 outcome의 R2를 `None`으로 두는 것도 적절하다.

이 보존 주장은 **X = [recipient basis, recipient basis × group]**의 전체 interacted projection, 다른 respondent traits, 개별 trajectory, conditional joint outcome table까지 확장되지 않는다. 현재 receipt의 `not_preserved`와 protocol은 이 제한을 인정한다. `has_changed_contrast_control`과 `sharp_extremum_certified=False`도 변화 없음과 최적성 미인증을 올바르게 구분한다.

변화한 contrast를 만들면서 모든 group-by-profile 분포까지 보존할 수는 없다. 동일 group/profile에서 contrast weight가 같으므로 그 셀 평균들이 모두 보존되면 해당 contrast도 보존된다. 따라서 더 강한 conditional 검사가 검출하는 것은 중요한 비교 결과다. 특정 target contrast만 유일한 검출법이라고 주장할 근거는 없다.

## W1 및 missing-action 처리

`diagnostic_comparison.py:23–61`의 계산은 타당하다. 완성된 actions의 empirical distribution을 Q, unknown을 계산상 2000으로 놓은 anchor를 Q*, human distribution을 P라고 하면, 동일 labelled 행을 연결한 coupling으로

`W1(Q,Q*) ≤ (1/n) Σ_unknown |action_i − 2000| ≤ 2000m/n`

이다. 삼각부등식과 역삼각부등식으로

`max(0, W1(P,Q*) − 2000m/n) ≤ W1(P,Q) ≤ min(4000, W1(P,Q*) + 2000m/n)`

을 얻는다. anchor는 관측값 대체나 point estimate가 아니며, 이 범위는 sharpness 또는 confidence coverage를 주장하지 않는다. integer action에도 유효한 보수적 범위다.

endpoint-only 최악값 가정은 실제로 틀릴 수 있다. human `[0,4000]`, known action `2000` 사례에서 다른 action이 0 또는 4000이면 W1=1000이지만 2000이면 W1=2000이다. 구현은 이 내부값을 포함하는 **[1000,3000]**을 반환한다. 실제 sharp upper 2000보다 넓지만 이는 명시된 보수적 방법과 일치한다.

모든 partition은 outcome 유효 여부와 무관한 X의 원래 group/profile로 정의되며, 가중치는 원래 셀 행 수/n이다. mean bounds도 원래 분모를 유지한다. missing이 있는 셀을 삭제하거나 known subset으로 재정규화하지 않는다. 완전 관측 시 sorted equal-weight W1이 정확하고, missing이 하나라도 있으면 additive projection/R2를 계산하지 않는 현재 분리가 적절하다.

`recorded_responses.evaluate_recorded`는 canonical layout을 확인하고 keyed 조립 후 동일 array evaluator를 호출한다. 따라서 새 진단이 oracle 전용 별도 경로에만 붙은 것은 아니다. 단, 이 오프라인 일관성 검사는 실제 provider 진위·전달·격리·재개를 인증하지 않는다.

## 잔여 제한과 작은 구현 주의

**B17 — 낮음, 일반 재사용 시 scalability:** `distribution_control.py:27–40`은 각 profile의 high×low 쌍과 그 반대 값쌍의 cross-product를 전부 저장한다. 두 profile의 네 group/profile 셀에 각 k개의 반복 응답이 있으면 후보가 k⁴개까지 생길 수 있다. 현재 제한된 예제에서 correctness 문제는 없었지만 큰 중복 셀에서 실행시간/메모리를 일반적으로 보장하지는 않는다. 범용 component로 확장할 때 후보 크기 경고/제한이나 aggregate matching을 검토하면 된다. 이것을 해결하기 위해 현재 연구 범위를 넓힐 필요는 없다.

저자 receipt는 human contrast 약55.16에서 증가 control 약129.71, 감소 control 약−22.03을 보고한다. 원자료와 control 배열 없이 이 수치·실제 후보 수·보존 여부를 독립 검증하지 않았다. 또한 현재 코드의 weighted cell-mean 진단까지 source에서 재실행했다고 인증할 수 없다. 해시 일치는 제공된 파일의 일관성만 뜻한다.

많은 singleton conditional cell의 W1은 사실상 행별 절대 차이를 반영한다. 이를 conditional population distribution 추정이나 개별 심리적 fidelity로 읽으면 안 된다. protocol의 finite same-row 해석과 cell/singleton 수 표시는 그 위험을 적절히 제한한다.

**다음 최소 조치:** 이 기능을 평가용 control과 동일 출력 진단으로 유지하고, 실제 캠페인에도 public keyed 경로를 사용한다. 이번 추가 검증의 불균형 셀 가중치와 public-path 진단 사례를 회귀 테스트로 보존하면 좋다. 실제 세 arm 결과가 어떤 중요한 오류 또는 유용성을 드러내는지는 여전히 열려 있다. native isolation, 고정 model/settings와 비용, repeat/presentation 설계 및 실질적 해석 기준의 미해결 조건은 그대로 남는다. 추가 소프트웨어 복잡성 자체를 연구 기여나 수집 승인으로 평가하지 않는다.
