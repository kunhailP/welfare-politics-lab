# Review B — 통계·원자료 재구성·재현성

검토일: 2026-10-29. **새 문맥에서 수행한 procedural blind internal AI review**이다. 외부 인간 동료심사나 학회 판정이 아니며 수상·채택 확률을 부여하지 않는다. 작성자 신원, 이전 대화·평가, 다른 검토자의 보고서를 제공받거나 읽지 않았다. 허용된 packet, packet_manifest.json, private/study1.tab 및 private/cohort_linkage.tsv만 연구 증거로 사용했다. 부모 저장소 README/AGENTS/Git 및 interpreter 주변 프로젝트는 열지 않았다. 절차적 블라인드는 OS에 의해 강제된 것이 아니다. 외부 논문·원 배포 archive·원 R 코드의 직접 검증은 이 검토 범위 밖이다. 응답자 모델/API 호출과 네트워크 접근은 모두 0회이다.

**판단:** 원자료에서 주요 인원수·인간 대비값·세 참고모형의 CV/평가 결과를 독립 재구성했고, 확인한 범위에서 수치 불일치나 주 분석 수식 오류를 발견하지 않았다. 고정 코호트의 기술적 평가 부품으로는 상당히 검증되었다. 실제 LLM 결과가 없고 실행 격리·실행 manifest·반복/표현 변경 실행 경로가 완성되지 않아, LLM 충실도나 사실 묶음의 효과를 입증한 연구로 해석할 수는 없다. 아래 실행 전 수정사항과 선택·표현의 제약을 유지해야 한다.

## 1. 검증 방법과 구별

1. **저자 코드 재실행:** packet에서 지정 interpreter와 `PYTHONPATH=src OPENBLAS_NUM_THREADS=1`로 unittest 67개를 실행하여 전부 통과했다. `welfare_politics.statistical_references` CLI를 두 private 파일로 실행했다. 재실행 report와 `author_reference_results.json`은 재귀 비교에서 숫자 허용오차 1e-7 이상 또는 문자열·구조 차이가 없었다. 이는 같은 구현의 재현성 확인이다.
2. **독립 원자료 계산:** 저자 모듈을 import하지 않은 별도 스크립트에 범주 기준을 직접 전사하고, 인간 대비값은 소득집단별 18열 OLS 정상방정식으로 각각 계산했다. 참고모형은 평균/18열 OLS/서로 겹치지 않는 집단별 18+18열 모수화를 사용했다. 별도 person-stratified 5-fold 구현으로 CV를 재계산했다. 이 결과를 저자 SVD·상호작용 모수화와 비교했다. 본 설계의 조건수가 약 52이므로 정상방정식은 이 독립 교차검산에 사용했으며 일반적인 고조건수 구현 권고는 아니다.
3. **별도 스트레스 검사:** 실제 평가 설계에서 결측 6행의 64가지 0/4000 끝점 완성을 열거하고, 원자료 타깃의 label·ID를 교란하고, 합성 로그의 A/B·도착순서·누락·모델·재시도 및 비정상 JSON을 검사했다. 검사 편의를 위해 저자 평가/파서 함수를 호출한 부분은 독립 추정치와 구분했다.
4. manifest에 기재된 packet 47개와 private 2개, 합계 **49개 파일의 SHA256가 모두 일치**했다. 검토 종료 시에도 동일했다.

절차 편차: 처음 지정 unittest 실행에서 `PYTHONDONTWRITEBYTECODE=1`을 빠뜨렸다. 이후 packet 내 `__pycache__`를 발견했으므로 bytecode cache가 생성·갱신되었을 가능성을 배제할 수 없다. manifest의 동결 소스와 private 원자료 내용은 모두 동일하며 수정하지 않았다. 이후 모든 Python 실행은 bytecode 생성을 껐고 산출물은 본인 scratch에만 저장했다. cache를 임의 삭제하여 패킷을 추가 변경하지 않았다. 이는 동결 경로 무변경 지침에 대한 잠재적 절차 편차이며 과학적 수치 일치와 별개로 명시한다.

## 2. 독립적으로 확인한 원자료와 인간 기준

| 구분 | 사람 | 행 | 추가 확인 |
|---|---:|---:|---|
| 공개 Study1 원자료 | 2,295 | 9,180 | id/vignette 중복 0, 번호 1–4 |
| 네 프로필 완전 사례 | 2,003 | 8,012 | 원자료 allocation 결측/범위 밖 모두 0 |
| 완전 사례 고·저소득 pool | 1,458 | 5,832 | 고소득 799, 저소득 659 |
| main 후보 전체 | 768 | 3,072 | seed 20261029의 추첨을 독립 재현 |
| pilot 후보 전체 | 32 | 128 | main과 중복 0; 고·저소득 25명 |
| main 고·저소득 평가 | 556 | 2,224 | 고소득 304, 저소득 252 |
| 모든 main/pilot 후보 제외 학습 | 877 | 3,508 | 고소득 482, 저소득 395; 평가 중복 0 |

수식상 대비는 각 집단 내 수령인 30k-minus-120k의 다른 7요인을 조정한 가산 OLS 기울기, gamma는 저소득-minus-고소득 기울기이다. 두 집단을 독립 적합한 결과는 완전 상호작용 36열 구현과 일치한다.

| 인간 코호트 | 고소득 집단 대비 CAD | 저소득 집단 대비 CAD | gamma CAD |
|---|---:|---:|---:|
| 고정 main 556명 | 135.588237 | 190.746065 | 55.157828 |
| 분리된 remainder/학습 877명 | 248.883342 | 369.503353 | 120.620011 |
| 완전 고·저소득 pool 1,458명 | 200.551325 | 291.476589 | 90.925264 |
| 고·저소득의 행별 완전 사례 6,357행 / 1,666명 | 192.203269 | 304.406795 | 112.203526 |

마지막 행은 일부 불완전 사람의 관측 행도 포함한 별도 기술적 민감도이며 main의 대체 기준값이 아니다. 사람·과제 구성이 바뀌므로 차이를 순수한 사람 선택 효과로 분해할 수 없다.

소득별 네 프로필 완전 사례 비율은 고소득 799/854 = **93.56%**, 저소득 659/813 = **81.06%**, 중간소득 384/438 = 87.67%, 소득 미보고 161/190 = 84.74%이다. 따라서 완전 사례를 일반 캐나다 시민의 대표 표본처럼 해석하면 안 된다. raw와 seed로 기존 main/pilot linkage를 정확히 재구성했으므로 관측된 배정 자체가 allocation 값에 따라 선택된 흔적은 찾지 못했다. 다만 결과를 본 뒤의 연구 설계·명세 개발 이력까지 제거되는 것은 아니다.

소스 배정 마진도 독립 확인했다. 시민권은 born citizen 7,344/9,180 = 80%, noncitizen 1,218, naturalized/foreign-born citizen 618로 균등하지 않다. employment는 pandemic unemployed 2,746, other unemployed 2,274, employed full-time 1,897, reduced income 1,825, 결측 438이다. 제공된 표만으로 원래 배정 확률·원인·recruitment-to-release 제외를 복원할 수 없으며 causal AMCE 주장을 지지하지 않는다.

소스 민감도 500회도 저자 함수를 사용하지 않고 동일 seed 및 집단 수를 유지해 재구성했다. gamma의 min/q05/median/q95/max는 **-104.104193 / -7.967731 / 122.965420 / 265.769592 / 406.331937 CAD**, 양 466회·음 34회였다. 두 집단 기울기는 모두 500회 양수였다. 이는 중첩되는 remainder 추첨의 기술적 분포이며 93.2%의 모집단 양의 확률, 독립 반복성, CI로 바꾸어 말할 수 없다.

## 3. 통계 참고모형 — 독립 재현 결과

학습 행은 3,508개이고 모든 CV에서 사람의 네 행을 함께 배치했다. fold 인원은 176/176/175/175/175명이다. 고정 모형의 rank는 1/18/36이고 본 평가에서 clipping은 모두 0행이었다. 독립 예측과 저자 예측의 최대 절대 차이는 모형별 4.55e-13, 1.82e-12, 1.36e-11 CAD였다.

| 고정 참고모형 | CV RMSE | CV MAE | main RMSE | main MAE | 고/저소득 대비 | gamma |
|---|---:|---:|---:|---:|---|---:|
| B_mean | 1085.003733 | 906.482203 | 1089.024712 | 891.691344 | 0 / 0 | 0 |
| B_recipient_OLS | 1052.918677 | 854.926589 | 1050.182156 | 844.216126 | 303.522734 / 303.522734 | 0 |
| B_income_interacted_OLS | 1054.405566 | 858.269021 | 1053.445108 | 848.652822 | 248.883342 / 369.503353 | 120.620011 |

단위는 모두 CAD이며 1e-11 수준의 수치 오차는 0으로 표시했다. B_mean의 학습 평균은 1655.152794 CAD이다. recipient OLS 예측 범위는 867.102877–2277.003509, income-interacted OLS는 680.608450–2475.561689 CAD였다.

참고모형의 gamma 절대오차는 평균/recipient OLS가 55.157828, income-interacted OLS가 65.462183 CAD이다. 그 한 값만으로 승자를 정하면 안 된다. 마지막 모형의 두 성분 signed error는 +113.295105/+178.757288 CAD이며 recipient OLS는 +167.934497/+112.776669 CAD이다. 모형·지표에 따라 다른 결과가 나온다.

`statistical_references.py:46`은 target allocation을 읽지 않고 whitelist predictor만 사용한다. 실제 main label을 -1e12로 바꾸고 ID를 +1e8 이동시킨 세 모형의 예측 차이가 정확히 0이었다. 학습·평가 중복 거부와 person CV도 시험했다. **계산상 target-label 누출 증거는 발견하지 못했다.** 다만 연구자들이 main 인간 결과를 이미 본 이력, 미래 모델의 공개자료 사전학습 노출, 향후 filesystem-enabled runner의 접근권한은 이 시험으로 검증되지 않는다.

B_recipient_OLS가 여기서 gamma 0인 이유는 clipping 없이 예측값 자체가 평가 recipient basis의 선형 결합이기 때문이다. 이것을 모든 group-blind N 응답이 gamma 0이라는 명제로 확대할 수 없다. 비선형 응답과 서로 다른 집단 과제는 N에서도 moderation을 만들 수 있다. B_income_interacted_OLS의 평가 대비가 학습 대비와 같은 것도 동일 basis의 선형 예측을 다시 투영한 구조적 결과이며 새로운 인간 궤적의 복제 증거가 아니다. 877명의 인간 label을 쓴 참고모형과 zero-shot LLM은 label 접근과 feature가 다르며, 참고모형은 job risk/parenthood를 사용하지 않는다. 현재 명세의 이러한 구별은 유지해야 한다.

## 4. 결측 경계·진단·로그 검증

**선형 완성 경계:** `contrast_validity.py:10`의 SVD weight는 `w = X(X'X)^(-1)c`의 안정적 표현이다. 알려진 행의 기여를 고정하고 결측 weight 부호에 따라 0/4000을 넣는 구간은 고정 full-rank X에서 선형 gamma에 대해 sharp하다. 정수 허용에서도 끝점은 정수라 동일 극값이다. 실제 main X에서 결측 6행의 64가지 끝점을 별도 OLS로 계산한 범위는 **[38.095961, 81.151805] CAD**이며 구현과 최대 차이 4.55e-13이었다. 집단 성분 구간으로 얻은 gamma 경계와 직접 gamma 경계 차이는 2.16e-12였다. 전부 결측인 4행 평균의 경계 [0,4000]도 유지된다. invalid pair를 양쪽 결측으로 남기는 정책과 고정 분모는 적절하다.

완전 상호작용에서 두 성분은 서로 다른 집단의 결과에만 의존하므로 연속 completion joint set의 직사각형 설명은 타당하다. 이를 제약/부분 상호작용에 일반화하면 안 된다. absolute-error/J는 interval hull에 대한 보수적 범위이며 정수 lattice에서 항상 sharp하다는 주장을 하지 않는 것이 옳다. W1 midpoint-anchor triangle bounds 역시 미관측값을 실제 2000으로 관측 처리하지 않는 보수적 경계로 읽어야 한다. CI나 실패가 무작위라는 가정은 아니다.

**조건부 진단의 실효성:** 실제 2,224행의 group-by-profile cell은 **1,788개**, singleton 1,418개(전체 행의 **63.76%**)이며 size 2/3/4 cell은 311/52/7개이다. pooled profile cell은 1,465개다. 따라서 더 강한 진단의 상당 부분은 한 사람·한 과제의 절대오차가 되고, 안정된 population conditional distribution을 추정한 것처럼 설명할 수 없다. 고정 행의 기술적 거리와 공개된 cell size로 제시하는 현재 제한은 필요하다. outcome-informed permutation/mean controls도 소프트웨어 반례이지 실제 모델 오류율이나 외부 benchmark 전체의 실패를 보여주지 않는다.

**Keyed replay:** 도착 순서와 A/B 역매핑을 독립된 서로 다른 amount 합성값으로 검사하여 정렬이 맞음을 확인했다. missing log, 응답 뒤 추가 retry, 잘못된 returned_model_id는 거부되었다. 기존 67개 시험에서는 중복 요청/시도, prompt·arm·person·mapping·rollout 불일치, transport 3회 소진, invalid whole pair도 확인한다. provider 진위 인증이 아니라는 표시는 정확하다.

## 5. 필요한 수정사항

### 중요: 실제 생성 전 실행·설계 결합을 완성할 것

`recorded_responses.py:22,99`는 전달된 request plan 내부의 hash 일관성을 검증하지만, 그것이 사전에 동결한 **올바른 의미의 과제/프롬프트/설계**인지 독립적으로 확정하지 않는다. 합성 검사에서 prompt 내용을 바꾸고 messages hash와 request ID 및 해당 attempt identity를 함께 다시 계산하면 동일 row ID로 통과했다. 이는 선언된 provider 진위 비보장과 양립하는 내부 일관성 검증의 한계이지, hash가 깨졌다는 주장은 아니다. 현 report의 사후 `request_plan_sha256` 기록만으로 사전 동결을 증명할 수 없다.

필수 수정은 실제 실행 전에 신뢰할 수 있는 campaign manifest를 별도로 고정하고, replay가 expected plan/design/row/cohort/contrast hash와 정확한 모델·설정·rollout 및 실행 버전을 대조하도록 하는 것이다. 같은 ID의 profile/income/arm 의미가 renderer와 분석 X에 맞는지도 검증해야 한다. 맹목적으로 외부 공격을 막자는 요구가 아니라 실수로 다른 prompt/design을 평가하는 것을 막기 위한 측정 연결이다. label을 읽을 수 없는 실행 격리, messages-only 전송, 모델/temperature 등 decoding 설정, 총 비용 상한, 반복·pair/name/presentation 변경 계획의 동결과 실행은 아직 검증되지 않았다. 이 준비가 끝나기 전 실제 모델 결과나 robustness를 주장하면 안 된다.

### 중요: 선택된 고정 벤치마크와 사후 개발 범위를 결과에서도 유지할 것

main gamma 55.16은 remainder 120.62, 전체 완전 pool 90.93과 같지 않으며, 완전 사례 비율도 소득에 따라 12.50 percentage points 차이가 난다. 원래 pairing·이름·언어·UI와 recruitment-to-release 제외는 복원되지 않는다. **동일 행·동일 X에서의 기술적 인간 기준 비교**로 표기하고 국가 수준 welfare politics, 인간 자기이익의 인과효과, 안정된 계층 갈등/연대 메커니즘으로 확장하지 말아야 한다. 기존 명세가 이미 이를 인정하므로 새로운 대조군을 더 만드는 것보다 실제 결과표·논의·제목에서도 이 약속을 지키는 것이 필요하다. 별도 소스의 계수를 main coefficient의 오류 기준으로 대입하지 말 것.

### 코드 수정: 깊은 중첩 JSON이 전체 replay를 중단시킬 수 있음

`render.py:75–90`은 ValueError/TypeError만 잡는다. 지정 interpreter에서 `parse_pair('['*20000+'0'+']'*20000)`는 invalid 반환 대신 **uncaught RecursionError**를 일으켰다. 일반적인 bool/float/duplicate key/NaN/code fence는 올바르게 invalid가 되었다. 이 예외는 주 통계 수치를 바꾸는 오류는 아니지만, 임의 응답은 whole-pair invalid로 회계 처리한다는 계약에 어긋난다. decoder recursion 실패를 invalid로 변환하고, 사전에 정한 응답 길이/중첩 제한과 해당 회귀 시험을 추가할 것. semantic retry나 값 clamping으로 바꾸지 말 것. 본 패킷은 검토용이므로 직접 수정하지 않았다.

### 경미: 재현 명령의 쓰기 부작용과 산출물 동결 절차 명시

검토·read-only 실행 안내에도 `PYTHONDONTWRITEBYTECODE=1`을 포함하거나 scratch bytecode 경로를 지정할 것. frozen manifest 대조와 별도로 허용되지 않은 추가 파일 생성을 관리해야 한다. 위에서 본 검토 자체의 잠재적 cache 쓰기 편차를 공개했다.

## 6. 남은 경험적 한계와 검토의 결론

실제 N/F/F-I 응답과 무효율, J_FN/J_FI, signed explicit-income change, 반복 변동, presentation/model 민감도는 **아직 알 수 없다**. 원자료의 고정 인간 대비와 인간 label 학습 참고모형만 확인했다. native SocioVerse 실행·독립 컨텍스트·outcome 파일 접근 불가를 실제로 시험하지 않았고, 원 source instrument/배정 확률/원 R 구현과의 정확한 동등성도 이번 파일 범위에서 인증하지 않았다. 새로운 과제 96요청의 common-task DID는 모델 입력 민감도이며 인간 반사실이나 archive gamma의 차감 분해가 아니다.

현재 수학·원자료 재현성에서 연구를 중단시킬 불일치는 발견하지 못했다. 중요한 남은 작업은 위의 실행 연결과 parser 보강, 동결한 평가를 실제로 수행한 뒤 성분 오류·선택 한계와 함께 결과를 제한적으로 보고하는 것이다. 새로운 baseline/oracle 계열을 원하는 순서가 나올 때까지 늘릴 이유는 확인되지 않았다.

검증 산출물: `/tmp/welfare_final_blind_09/reviewer_B_scratch/independent.py`, `independent_results.json`, `adversarial.py`, `adversarial_results.json`, `author_reference/report.json` 및 예측 NPZ. 원 응답자 행을 공개 문서로 복사하지 않았다. 깊은 중첩 parser 추가 시험은 별도 terminal 실행으로 확인했으며 초기 adversarial JSON의 depth 1100 결과와 구별했다.
