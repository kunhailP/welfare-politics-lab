# Reviewer B — 제한된 구현 검증 03

이 문서는 **내부 AI 구현 검증**이며, 새 블라인드 리뷰·외부 동료심사·새 수집 준비도 심사가 아니다. 본인의 이전 리뷰 문맥을 유지했다. 허용된 `shared/**`와 manifest만 읽었으며, 다른 리뷰어 보고서·부모 저장소·원자료는 읽지 않았다.

**판정: B10·B11의 요청된 오프라인 수정과 B13의 표시/기대폭 계산을 확인했다. 해당 범위에서 새로운 중대한 결함은 발견하지 않았다.** 이는 live runner 또는 실제 모델 결과에 대한 검증이 아니다.

검증은 지정된 interpreter로 `shared`에서 `PYTHONPATH=src OPENBLAS_NUM_THREADS=1`을 설정하여 실행했다. bytecode 생성을 비활성화했다. **42개 테스트가 모두 통과했고, manifest의 25개 파일 해시가 모두 일치했다.** 네임스페이스 sandbox 제한으로 명령 실행에는 허용된 escalated 경로를 사용했다.

| 항목 | 검증 결과 | 근거 |
| --- | --- | --- |
| **B10 — arm 파일의 ablation 불변식** | **오프라인 수정 확인** | `render.py:97–121`의 `validated_agents`가 중복 agent, 모순된 arm 표기, 서로 다른 대상 집합, 알 수 없는 사실/값, 비어 있지 않은 N, F에서 income만 제거한 결과와 다른 F-I를 거부한다. `plan`과 common-task 계획에서 이를 호출한다. 실제 파일 변조를 사용하는 테스트가 income 누출·고용/자녀 정보 변경·누락·중복을 거부한다. |
| **B11 — 요청 식별 및 keyed response 정렬** | **오프라인 수정 확인** | `render.py:124–131,156–163`이 respondent·arm·A/B profile 순서·rollout·prompt hash를 request ID에 결합한다. `recorded_responses.py:21–95`가 계획의 전체 행 회계, prompt/identity digest, attempt별 identity·model ID·비용, 중복/누락/추가 기록, 연속된 재시도 이력을 검사한다. 도착 순서 대신 명시된 A/B 매핑으로 고정 행에 재정렬한다. invalid pair는 두 행 모두 unknown으로 유지하며, reply 뒤 재시도를 허용하지 않는다. 전송 실패 소진에는 세 attempt 기록을 요구한다. |
| **B11 — 분석 진입점/영수증** | **오프라인 수정 확인** | `evaluate_recorded`가 keyed 조립 후 계산하며, `evaluate_arrays`는 연결을 입증하지 못하는 하위 software-control API로 명시되었다. human outcome·contrast·design·row hash가 기록되고, CLI는 attempt log hash를 기록하며 기존 출력 파일 덮어쓰기를 거부한다. |
| **B13 — 무작위 실패 표시와 기대폭** | **수정 및 독립 수치 확인** | `failure_budget.py:28–32`가 한 seeded scenario와 uniform-subset 기대폭을 구분한다. 기대폭 `4000 × m/K × sum(pair absolute weight)`는 정확하다. 비균등 가중치의 4-pair 설계에서 2-pair 실패의 모든 6개 부분집합을 열거하여 평균 **761.9047619 CAD**, 최대 **1142.8571429 CAD**가 구현과 일치함을 확인했다. |

추가로, 기존 replay fixture는 pair 내부의 A/B 금액이 같아 slot 교환 오류를 단독으로 드러내기 어렵다. 모든 행에 서로 다른 금액을 부여하고, 역순 A/B profile 매핑과 request/attempt 셔플을 함께 적용한 독립 검사에서 **세 arm 모두 원래 행별 금액을 정확히 복원했다**. 따라서 현재 매핑 구현은 그 더 강한 검사도 통과한다. 이 사례를 정식 회귀 테스트에 추가하면 유용하다.

남은 조건은 검증 범위의 경계다. 입력 request plan을 신뢰할 수 있는 고정 계획으로 보관하고, 향후 live runner가 그 계획의 메시지만 실제 전송하며 반환 metadata·설정·비용을 정확히 기록하는지는 이번 검증으로 입증되지 않는다. hash는 입력 기록 간 일관성을 확인하며 provider 진위나 독립적인 생성 전 고정 시점을 인증하지 않는다. 실제 전송, 중단 후 재개, 중복 과금/호출 방지, 생성 격리도 검증하지 않았다. 코드의 `provider_authenticity_verified=False`와 문서의 미구현 표시는 이 범위를 정직하게 반영한다.

B12의 실증적 안정성·실질적 해석 조건이나 이전 수집 준비도 판정은 이번 제한 검증으로 변경하지 않는다. 원자료 정합성·실제 모델 실패율·모델 성능·새로움에 관한 증거도 추가되지 않았다.
