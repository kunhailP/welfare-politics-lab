# Reviewer B — 제한 검증 05

본인의 기존 문맥을 유지한 **내부 AI targeted verification**이다. 새 블라인드 리뷰·기여 재평가·수집 준비도 심사가 아니다. 허용된 `shared/**`와 manifest만 읽었고, 다른 리뷰어 보고서·부모 저장소·원자료·Git 메타데이터는 읽지 않았다.

**결과:** 지정된 interpreter와 `PYTHONPATH=src OPENBLAS_NUM_THREADS=1`로 **49개 테스트가 모두 통과**했다. manifest **28개 해시가 모두 일치**했다. bytecode 생성을 막았으며, 환경의 namespace 제한 때문에 허용된 escalated 실행 경로를 사용했다.

| 검증 대상 | 판정과 근거 |
| --- | --- |
| **B14 — 무변화 control 표기** | **수정 확인.** `marginal_control.py:75–77`이 실제 contrast 변화 여부를 출력하며 unchanged control은 반례 증거가 아니라고 명시한다. all-zero/all-cap 및 full-rank 무중첩 profile 테스트가 이를 확인한다. |
| **B15 — 보존 범위** | **주요 수정 확인.** `70–74`가 pooled recipient means와 additive 회귀 범위로 한정하고 분포·분산을 비보존 대상으로 추가했다. 테스트는 pooled additive 계수 보존과 interacted fit의 recipient main coefficient 변화(−4000)를 구분한다. 더 엄밀하게는 “additive-regression sufficient statistics”를 “fixed additive design의 X' y와 그에 따른 OLS 계수”로 쓰면 좋다. 잔차제곱합/분산 추론까지 보존하는 것은 아니다. |
| **B16 — 최적성 표기** | **메타데이터 수정 확인; 작은 문구 잔여.** `sharp_extremum_certified=False`는 실제로 극값에 도달할 수 있는 toy와 모순되지 않는다. 다만 모듈 docstring `4–5`에는 여전히 “not sharp extrema”가 남아 있다. “no general sharpness/optimality certification”으로 통일해야 실제 비최적성의 입증처럼 읽히지 않는다. |
| **공유 canonical coding** | **확인.** `primary_design.py:15–29`의 `matrix_and_contrast`를 `construct`가 호출한다(`65–68`). 독립 fixture에서 두 경로의 X와 c가 원소별로 정확히 일치했다. 보조함수는 이미 high/low로 제한한 행을 받는다는 사용 조건을 지켜야 한다. `construct`는 이 필터를 명시적으로 적용한다. |
| **estimability 진단** | **핵심 논리 확인.** `32–44`는 SVD row-space에 c를 투영한 잔차를 검사하며 전체 계수 식별과 특정 contrast의 estimability를 분리한다. 이는 현재 full-rank 평가기의 적용 가능성과도 별개다. |

독립적으로 nuisance factor level 하나를 제거한 **320행×36열 합성 fixture**를 만들었다. rank는 **34**, c의 row-space residual은 **2.73×10⁻¹⁵**였고 진단은 `contrast_estimable_in_design=True`를 반환했다. null-space 방향으로 회귀계수를 바꾸어도 적합값과 c'β가 같음을 확인했다. 해당 contrast 값은 약 **150 CAD**로 유지되었다. 반대로 제거된 nuisance 계수 자체의 contrast는 nonestimable로 판정했다.

동일한 rank-deficient X를 현 `contrast_bounds`에 넣으면 full-column-rank guard가 거절한다. 이것은 **현재 구현이 그 설계를 지원하지 않는다는 뜻이며, c가 비식별이라는 뜻이 아니다.** 수학적으로는 c가 X의 row space에 있을 때 c'β가 해 선택에 불변이다. 향후 rank-deficient 평가를 지원하려면 그 조건과 수치 안정성을 검사하는 별도 구현/검증이 필요하다. 이번 진단 추가가 evaluator 지원 범위를 확장한 것은 아니다.

저자가 전달한 실제 pilot의 rank34/36 및 residual 약9.5×10⁻¹⁶은 원자료 없이 재현하지 않았다. “full-rank evaluator 거절 ⇒ c 비식별” 해석을 바로잡아야 한다는 논리만 위 fixture로 독립 확인했다. 진단의 estimability 판정은 출력에 명시된 수치 허용오차 기준이다.

이 검증은 원자료 수치, 독창성, 실제 모델 응답, provider 진위, 실시간 runner·전달·재개 또는 수집 준비도에 새 근거를 제공하지 않는다. B16 docstring의 작은 잔여 표현을 제외하면 요청된 오프라인 수정과 estimability 구분에서 새로운 중대한 결함은 발견하지 않았다.
