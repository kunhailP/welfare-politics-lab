# Reviewer B — round 04 비판적 재검토

**내부 AI 재검토이며 외부 동료심사나 새 블라인드 리뷰가 아니다.** 본인의 기존 문맥을 유지했다. 허용된 `shared/**`와 manifest만 읽었고 부모 저장소·다른 리뷰어 보고서·원자료·Git 메타데이터는 읽지 않았다. 원자료 기반 `author_control_receipt.json`은 저자 제공 집계이며 독립 재현하지 않았다.

**판정:** four-row cycle의 보존·정수 경계·증가/감소 방향은 타당하다. 새 control은 지정된 marginal 점검만으로 interaction fidelity를 식별할 수 없음을 보여주는 평가용 예제로 유용하다. 이는 실제 모델 왜곡이나 새로운 실증적 기여의 증거가 아니다. 아래 세 가지 출력 표현은 더 정확하게 고칠 필요가 있다. 기존 수집 준비도 공백은 해소되지 않았다.

## 검증 결과

지정된 interpreter로 `shared`에서 `PYTHONPATH=src OPENBLAS_NUM_THREADS=1`을 설정하고 bytecode 생성을 막아 실행했다. **45개 테스트가 모두 통과했고 manifest 30개 파일 해시가 모두 일치했다.** 명령은 환경의 namespace sandbox 제한 때문에 허용된 escalated 경로로 실행했다.

독립적으로 불균형 group-by-profile 셀을 갖는 합성표 **200개**, 양방향 control **400개**를 검사했다. 절반은 0·1·2·3998·3999·4000에 집중된 경계값, 나머지는 0–4000의 정수값을 사용했다. 모든 control에서 다음이 성립했다.

- 출력은 정수이며 모든 행이 0–4000 안에 있었다.
- 각 그룹 합계와 전체 그룹을 합친 각 완전 recipient-profile 합계가 정확히 보존되었다. 행 수가 고정되어 각 평균과 전체 평균도 보존된다.
- pooled recipient-factor + group additive 회귀의 계수는 수치 오차 범위에서 같았다.
- `increase`는 원래 contrast보다 작아지지 않았고, `decrease`는 커지지 않았다. 이 표들에서는 모두 실제 변화가 발생했다.

`marginal_control.py:41–55`의 이동을 low(A)에 +t, high(A)에 −t, high(B)에 +t, low(B)에 −t로 쓰면 그룹별 변화와 profile별 변화가 각각 0이다. 같은 group/profile의 행은 X가 같아 contrast weight도 같다. 따라서 contrast 변화는

`Δgamma = t × [(w_low,A − w_high,A) − (w_low,B − w_high,B)]`

이다. `35–43`의 순서와 gap 검사에 의해 증가/감소 방향이 정해지고, `47–55`의 최소 slack만큼 이동하므로 정수성과 행별 경계가 유지된다. 감소 분기에서 부호까지 다시 뒤집지 않는 현재 구현은 맞다.

균형 2×2 fixture의 ±8000 CAD interaction도 오류가 아니다. 각 그룹의 recipient 차이는 ±4000 범위이고, 두 그룹 차이의 차이는 ±8000까지 가능하다. 개별 응답 경계와 회귀 contrast 경계는 다르다.

## 남은 표현·구현 문제

### B14 — 중간: 실제 변화가 없어도 무조건 “counterexamples”라고 반환한다

**위치/근거:** `marginal_control.py:63–75`. 모든 human 응답이 0이거나 모두 4000이면 그룹 합계 보존과 경계 때문에 바꿀 수 없다. 추가 검사에서 두 control 모두 cycles=0, changed_rows=0이었다. 세 이진 recipient factor의 cube를 parity에 따라 두 그룹으로 나눈 **full-rank 8×8 설계**에서도 공유 complete profile이 없어 변화가 0이었다. 그런데 receipt의 interpretation은 모두 “Feasible integer counterexamples”였다.

**영향:** 현재 저자 receipt는 변화가 있다고 보고하므로 이 문제가 그 수치를 반박하지는 않는다. 그러나 재사용 시 실제로 발견하지 못한 interaction 반례를 발견했다고 표현할 수 있다. `increase/decrease`는 비엄격 방향 이름으로는 괜찮지만 항상 엄격한 변화가 보장되지는 않는다.

**수정/검증 기준:** 원래 대비 contrast 변화와 `counterexample_found`를 출력하고, 변화가 허용 오차 이하이면 “unchanged feasible control; no counterexample found by this construction”으로 표시한다. all-zero/all-cap, 공유 profile 없음, 이동 여유 없음 사례를 회귀 테스트로 추가한다. 원래 입력이 그대로 반환되는 것은 올바른 동작이며 실패를 숨길 필요가 없다.

### B15 — 낮음: “all recipient main-effect summaries”의 범위를 좁혀야 한다

**위치/근거:** `marginal_control.py:70–72`와 저자 receipt의 `preserved_exactly`. pooled profile 합계 보존은 marginal recipient 평균 및 recipient-only/additive 회귀를 보존한다. 그러나 그룹 interaction을 포함한 주 분석 회귀의 “main-effect coefficient”는 reference group의 효과이므로 달라질 수 있다. 기존 균형 fixture에서 human의 recipient main coefficient는 약 0, 증가 control에서는 −4000이었다.

**영향:** “all”을 조건부 회귀 계수까지 확장하면 잘못된 보존 주장이다. `critique_questions.md`와 protocol은 conditional group-by-profile outcomes를 보존하지 않는다고 정확히 제한하고 있다.

**수정/검증 기준:** “pooled recipient marginal means and recipient-only/additive projection contrasts”처럼 명시한다. 그룹별 profile 합계, conditional contrasts, 개별 trajectory, 분산·quantile·응답 분포는 보존 대상으로 표시하지 않는다. pooled additive 계수는 같지만 interacted main coefficient는 달라지는 fixture를 추가하면 경계가 명확해진다.

### B16 — 낮음: “비최적해”와 “최적성 미인증”을 구분해야 한다

**위치/근거:** `marginal_control.py:4–5,74`의 `is_sharp_extremum=False`. 기존 2×2 fixture는 실제로 가능한 최종 경계인 ±8000에 도달하므로, “실제로 extremum이 아니다”라는 문자 그대로의 해석은 틀리다.

**영향:** 여기서 정당한 주장은 일반 설계에 대한 sharpness/optimality 증명을 제공하지 않는다는 것이다. 현재의 보수적인 기여 제한은 적절하지만 결과가 반드시 비최적이라고 입증한 것은 아니다.

**수정/검증 기준:** `sharp_extremum_certified=False` 또는 `optimality_certified=False`로 바꾸고 “feasible directional construction; no general optimality certification”이라고 쓴다. 쉬운 toy가 극값을 달성해도 이 미인증 표기와 모순되지 않아야 한다. 이번 검토는 일반 설계의 최적성을 증명하거나 부정하지 않았다.

## 증거와 수집 준비도의 경계

`protocol.md:219–236`과 모듈 상단은 이 작업을 outcome-informed oracle software control로 제한하고, 평가에서만 human outcomes를 읽으며 generation에는 노출하지 말라고 한다. 원자료 receipt도 actual_model_calls=0, empirical_model_results=false를 명시한다. 이 분리는 적절하다. 저자 제공 수치(약 55.16에서 1900.26 또는 −1752.22로 변화, shared profile 323개)는 파일에 보고된 값으로만 취급했다. 원자료 control 배열이 없어 보존 조건이나 그 수치를 독립 재현하지 않았다.

이 control은 **지정된 marginal 진단의 불충분성**을 보인다. conditional group-by-profile 진단, interaction 회귀, 응답 분포나 trajectory를 검사하는 더 강한 기존 방법도 통과한다는 보장은 없다. 기존 문헌 전체가 mean-only라는 주장이나 실제 LLM이 이런 표를 생성한다는 주장은 정당화하지 않는다. `related_work.md`와 검토 질문은 이 제한을 인정한다. 새 기여의 실증적 가치는 실제 세 arm 비교에서 어떤 중요한 오류나 유용성을 추가로 밝혀내는지에 달려 있다.

수정된 recipient-income 문구는 crosswalk와 코드 사이의 정합성만 확인할 수 있다. 이번 허용 범위에 원 논문·supplement 내용이 포함되지 않아 출처 의미 자체를 독립 인증하지 않았다.

**다음 최소 조치:** 위 출력 표현과 퇴화 사례 회귀 테스트를 정리한 뒤 이 control을 평가 도구로 유지하면 된다. live runner의 실제 격리·전달·재개, 고정 model/settings와 비용, 반복 생성 및 presentation 설계는 여전히 별도 조건이다. 소프트웨어 control 추가로 수집 hold, 실질적 해석 기준 또는 실증적 새로움이 해결되었다고 판단하지 않는다.
