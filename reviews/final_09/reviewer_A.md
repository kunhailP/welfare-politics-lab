# Reviewer A — 블라인드 과학 검토

검토일: 2026-10-29. 판정: **과학적 질문은 제한된 검증 연구로서 타당하지만, 현재 산출물은 실증 연구의 완성본이 아니다. 주요 수정이 필요하다.** 좋은 평가 소프트웨어를 만들었다는 근거와 새로운 정치학적·경험적 발견을 했다는 근거를 분리해야 한다.

## 검토 범위와 독립성

새 문맥에서 제공된 packet, packet_manifest.json, 허용된 private/study1.tab 및 cohort_linkage.tsv만 로컬 자료로 읽었다. 부모 저장소의 README/AGENTS/Git, 저자 대화, 기존 평가 및 다른 리뷰어 보고서는 읽지 않았다. packet에 기재된 primary-paper URL만 열람했다. 이것은 **문맥을 분리한 블라인드 internal AI review**이며, 외부 동료심사나 OS 수준의 완벽한 접근통제가 아니다. 별도의 저자 식별정보는 받지 않았고 우발적 저자정보·기존평가 노출은 없었다. 실제 응답모델/API 호출과 응답 생성은 하지 않았다.

기본 shell 실행은 bwrap namespace 생성 오류로 실패했다. 이후 허용된 경로만 지정한 명령을 require_escalated로 실행했다. 계산과 파일 출력은 scratch_science에서 수행했다. packet/private는 수정하지 않았다. 제공된 인터프리터는 실행에만 사용했고 이웃 프로젝트 파일은 읽지 않았다.

직접 확인한 것:

- private 두 파일 SHA256이 manifest와 일치한다.
- 저자의 회귀 함수를 호출하지 않고, 원자료에서 소득집단별로 별도 treatment-coded 가산 OLS를 구성해 아래 대비를 재계산했다. 각 집단 설계의 rank는 18이었다.
- 2,295명/9,180행, 완전한 네 프로필 2,003명, complete high/low 1,458명, main high/low 556명/2,224행, main high 304명·low 252명, remainder 877명/3,508행을 확인했다.
- 제공된 67개 unit test가 통과했다. scratch에서 처음 실행할 때 packet의 `scripts` import 경로가 없어 1개 import error가 났고, PYTHONPATH에 packet root를 추가하자 전부 통과했다. 이는 지시된 packet 작업 디렉터리의 import 경로를 scratch에서 재현한 것이다.

| 직접 재계산한 고정 코호트 | High의 recipient 30k−120k | Low의 recipient 30k−120k | Low−High gamma |
| --- | ---: | ---: | ---: |
| Main | 135.588 CAD | 190.746 CAD | 55.158 CAD |
| Disjoint remainder | 248.883 CAD | 369.503 CAD | 120.620 CAD |
| Complete high/low pool | 200.551 CAD | 291.477 CAD | 90.925 CAD |

이 수치는 저자 수치와 수치오차 범위에서 일치한다. 재계산 코드는 scratch_science/independent_check.py, 결과는 independent_summary.json에 있다. 통계 참조모형의 CV/RMSE/MAE, 세부 W1, 500회 source sensitivity draw와 sign counts는 이 검토에서 다시 계산하지 않았다. 이하 해당 값은 **author aggregate**다. unit test 통과는 그 수치의 독립 재현이나 과학적 타당성 인증과 다르다.

## 주요 발견과 필요한 수정

### 1. 선행연구 대비 기여가 아직 조건문이며, 평가장치의 정교함이 이를 대신하지 못한다

[Taday Morocho et al.](https://arxiv.org/html/2602.18462v1)의 본문을 열람했다. 이미 persona/no-persona의 matched comparison과 subgroup error를 다룬다. 따라서 F−N, subgroup 평가, 평균만 맞아도 충분하지 않다는 주장 자체는 새로운 기여로 내세울 수 없다. 이 프로젝트에서 가치가 생길 수 있는 부분은 **동일 welfare allocation 출력에서 어떤 수혜자 소득 비교를 보존하고, 어떤 응답자 소득집단 비교를 잘못 재현하는지 구체적으로 진단하는 것**이다. 이것은 아직 실제 모델 출력이 없어서 입증되지 않았다.

packet의 [SSDataBench](https://doi.org/10.1073/pnas.2538145123), [FairFund-Bench](https://aclanthology.org/2026.findings-emnlp.1340/), [Powdthavee v2](https://arxiv.org/abs/2609.33055v2) 링크는 이 세션의 web 도구에서 각각 403/접근불가/cache miss로 본문을 검증하지 못했다. 해당 연구의 범위에 대한 packet 설명은 저자 제공 요약이며, 독립 확인된 문헌사실로 취급하지 않는다. 특히 current v2 전문이 확인되지 않았다는 packet의 유보는 유지해야 한다. 이 상태에서 포괄적 최초성이나 누락 없는 관련연구 검토를 보증할 수 없다.

**필요한 수정:** 질문·초록·결론의 기여 문장을 하나의 실제 추론 대상으로 좁혀라. 예를 들어 “두 집단 모두 저소득 수혜자에게 더 많이 배정하는 비교와, 그 차이가 저소득 응답자에서 더 큰지라는 비교가 각각 얼마나 재현되는가”를 중심에 두면 된다. 주효과를 이미 다루는 문헌과의 차이는 실제 결과의 오류 구조로 보여야 한다. 모델 결과가 작은 기존 persona effect에 그친다면 제한된 도메인 복제 연구라고 쓰는 것이 적절하다. 새로운 지표나 oracle 가족을 더 붙여 이 문제를 해결하려 해서는 안 된다.

### 2. 정치학적 해석은 계층 갈등보다 훨씬 좁으며, `supported`의 의미를 더 명확히 해야 한다

Main의 human reference는 두 집단에서 모두 30k−120k 대비가 양수다. 55.158 CAD의 gamma는 두 집단이 반대 진영이라는 증거가 아니라, 같은 방향의 비교에서 크기가 다르다는 고정 설계 기술량이다. 응답자 소득은 자산·직업적 지위·계층 정체성을 포괄하는 “class”와 동일하지 않다. 코로나 시기의 한 배정 문항은 실제 예산 제약하의 정책 선택·투표·연합을 측정하지 않는다.

원 [Bridgman et al. 논문](https://doi.org/10.1017/XPS.2021.10)은 Study1의 소득집단별 AMCE 차이가 통계적으로 유의하지 않다고 보고한다. 이 검토의 고정 코호트 gamma는 다른 선택·분석 대상을 가지므로 그 정치학적 발견을 뒤집는 증거로 읽으면 안 된다. 새 연구의 유용성은 알려진 유한 자료의 패턴을 생성 출력이 얼마나 보존하는지에 있다.

`claim_specification.md`는 이미 자기이익·연대·인과 해석을 금지하고, 두 component와 signed error를 gamma 옆에 보이도록 요구한다. 이는 적절한 강점이다. 다만 “어떤 비교가 supported되는가”는 fidelity의 허용오차나 중요성 기준이 없는 현재 설계에서 이분법적 결론을 연상시킬 수 있다. 수치적 0을 completion bounds가 배제하는 것은 그 run의 부호가 결정된다는 뜻이지 정치적으로 중요한 차이라는 뜻이 아니다.

**필요한 수정:** 결과 서술에서는 “이 run의 관측/완성가능 범위에서 대비의 부호와 CAD 오차가 이렇다”라고 써라. 연구를 income-group-conditioned comparison으로 명시하고, `class`를 쓴다면 관측된 household-income band라는 조작적 의미를 바로 설명하라. 무근거 pass threshold를 새로 만들 필요는 없다. 양 component와 gamma의 방향·크기·오차를 같은 표에서 실제로 보여주는 기존 규칙을 실행하면 된다.

### 3. 주 비교와 보조 비교는 논리적으로 타당하지만 서로 다른 질문에 답한다

F−N의 J_FN은 income/job-risk/parenthood **묶음**이 이 fixed-score의 절대오차를 바꾸는지 묻는다. income을 추가한 기여라고 부르면 안 된다. F−F-I는 다른 두 사실이 주어진 상태에서 explicit-income 문장을 지운 효과다. F-I에서도 간접 소득정보를 추론할 수 있으며, job-risk/parenthood의 실제 분포는 소득집단 간 다를 수 있다. 따라서 F−F-I는 소득정보 전체의 제거 실험이나 인간 소득의 효과가 아니다. packet은 이 구분을 이미 잘 적었다.

J_FN이 음수라는 사실만으로 비교 전체가 나아졌다는 결론도 안 된다. gamma의 오차는 component 오차의 차이여서 두 component가 함께 이동하면 상쇄된다. frozen reporting table이 이 함정을 다루고 있으므로 별도 종합점수 추가는 필요하지 않다.

N은 같은 사람의 동일 task에서 F와 matched되어 있지만 집단 간 task는 동일하지 않다. 비선형 group-blind N에서 gamma가 생기는 것을 소득 stereotype의 증거로 읽을 수 없다. 16-base common-task audit은 이 해석을 검사하는 유용한 작은 보조 진단이지만, 인간 대응 관측이 없고 특정 base 집합에 조건부인 model-input sensitivity다. archive gamma에서 그 값을 빼서 “순수 demographic effect”를 얻을 수 없다.

**필요한 수정:** 현행 J_FN primary/J_FI secondary 위계는 유지하라. 음수/양수 결과와 무관하게 F·N·F-I의 두 component, signed error, gamma, J, invalidity 및 completion bounds를 함께 완성하라. frozen common-task manifest와 그 focal-position mapping도 실제 실행 전 고정해야 한다. 결과에서 bundle improvement, explicit-sentence effect, common-task responsiveness를 별도의 문장으로 해석하라. 지금 더 많은 ablation arm을 늘릴 이유는 없다.

### 4. 인간 기준의 선택성과 자극 복원은 실질적인 외적 타당성 한계다

직접 확인한 완전응답률은 high 799/854=93.56%, low 659/813=81.06%다. 이는 observed-income 집단별 비율이며 missing-income 사람을 포함한 전체 모집단 비율이 아니다. Main과 remainder의 gamma는 각각 55.158과 120.620 CAD이며, complete pool도 90.925 CAD다. 다른 사람과 task를 포함하므로 이를 sampling CI나 순수 사람 구성효과로 바꿔 해석해서는 안 된다. 다만 main의 구체적인 small moderation이 전체 자료를 대표한다는 주장을 경계할 충분한 근거다. 선택 seed가 outcome을 직접 사용하지 않는 점과 연구자가 결과를 본 뒤 target을 개발한 역사는 동시에 성립한다.

원자료 citizenship margin은 born citizen 7,344행, noncitizen 1,218행, naturalized citizen 618행이었다. 고르지 않은 공개 데이터가 왜 생겼는지는 이 자료만으로 확인할 수 없다. 실제 assignment probabilities나 원본 coding을 복원하지 못한 채 OLS를 causal AMCE로 복권해서는 안 된다. 현재 descriptive fixed-design 명칭은 옳다.

pair ID·원래 이름·언어·UI는 복원되지 않았다. JSON 정수, 독립 금액의 명시, canonical names, 재구성된 pair는 인간 실험과 다른 elicitation이다. source-crosswalk의 현재 유보는 적절하지만, 그 유보를 적었다는 것만으로 format robustness가 성립하지 않는다. 특히 source pairing을 모르면 인간이 본 상대 profile 문맥과 모델 문맥이 달라질 수 있다.

**필요한 수정:** source flow와 위 income별 완전응답률, main/pool/remainder 대비를 본문 또는 핵심 부록의 한 표에 보여라. source completeness sensitivity는 main 점수와 섞지 말고 현재 locked cohort를 유지하라. assignment의 불일치는 원자료 제공자 확인 등으로 해소될 때까지 미확인 provenance로 표시하라. presentation robustness를 주장하려면 이미 제안한 pair/name/presentation 비교의 정확한 manifest를 고정해 실행해야 한다. 실행하지 못하면 reconstructed-task validation으로 연구 범위를 제한하라. 원래 설계의 정확한 replication이라고 쓰지 않는 수정만으로도 큰 과장은 막을 수 있다.

### 5. 현재 prompt의 respondent 사실 귀속을 명시할 필요가 있다

`render.messages`는 `Household income: ...`, `Employment category: ...`, `Children: ...`를 user message 앞에 붙이고 system에서는 일반적으로 survey participant로 응답하라고 한다. 그러나 이 사실이 **응답할 가상 참여자 자신의 사실**이라는 연결 문장이 없다. recipient 설명은 이후 A/B로 분리되어 있어 의도는 추정할 수 있지만, 핵심 조작을 독자의 추정에 맡길 이유가 없다. 또한 `classified as ...`는 공개자료의 이진 코딩 범주라는 사실을 전달하는 문구로서, 풍부한 실제 biography를 제공하는 것과 다르다.

**필요한 수정:** generation 전에 F/F-I의 facts block을 “다음은 당신이 응답할 참여자의 알려진 사실이다”와 같은 명시적 귀속으로 고정하고, N의 일반 survey instruction과 나머지 task wording을 matched 상태로 유지하라. 이를 새 증거가 아닌 elicitation specification 변경으로 버전·해시 기록하라. 동일한 사실을 richer persona로 확장하거나 missing facts를 만들어낼 필요는 없다.

### 6. 인간학습 참조모형은 유용하지만 새로운 실증 발견이나 공정한 경쟁 결과가 아니다

877명의 분리된 사람으로 학습하고 person-fold CV를 쓰며 main label을 prediction 함수에서 제거한 구조는 좋은 engineering이다. 사전 결과 열람의 영향을 없애지는 않는다. 단순 조건부 평균 예측과 단회 respondent 출력을 RMSE·분포로 비교하면 목적함수가 다르다. 공개 원자료를 미래 LLM이 학습 중 접했는지도 배제할 수 없다. job-risk/parenthood 사용 여부 역시 다르므로 참조모형은 F−N의 대체 실험이 아니다.

author aggregate에서 B_mean/B_recipient_OLS의 gamma는 사실상 0, B_income_interacted_OLS는 120.620 CAD다. 후자는 동일한 가산 집단별 계수로 예측했기 때문에 remainder gamma를 target에서 재투영하는 성질을 갖는다(일반적으로 clipping이 계수를 바꿀 수 있으므로 해당 raw-range 확인이 전제). 이는 이미 확인한 remainder와 main 간 차이를 보여주는 실용적 기준이지, synthetic citizen의 개인적 일관성이나 외부 타당성을 입증하는 독립 실험이 아니다. author aggregate상 main gamma 오차는 0-reference 약55.16 CAD, interacted reference 약65.46 CAD로, 복잡한 reference가 이 한 점수에서 더 좋다는 결과도 아니다. 그 숫자만으로 constant model이 allocation을 잘 재현한다고 결론내릴 수도 없다.

**필요한 수정:** 기존의 세 참조모형을 모두 남기되 human-trained conditional-mean reference라는 표제를 매 표에 유지하라. 어느 것이 global winner라는 서술을 하지 말고 component·prediction·distribution 결과의 충돌을 보여라. 더 많은 model family를 추가할 필요는 없다. 지금 있는 비교만 정확히 해석하는 것이 우선이다.

## 작은 수정과 실행 전 요구사항

- `confirmatory`라는 내부 phase 이름은 source 결과를 본 후 개발했다는 설명과 나란히 두어라. 모델 출력에 대해서는 prospective일 수 있지만 untouched human confirmation은 아니다.
- 3336은 main의 최초 요청 수다. pilot, common-task 96, transport retry, repeat 및 presentation/model check를 포함한 전체 cap과 정확한 model ID/settings가 아직 고정되지 않았다. 이것은 사소한 재현 메타데이터가 아니라 어떤 경험적 대상을 측정할지 정하는 부분이다. 실행 전 한 manifest로 고정하라. 이 검토는 실행 허가가 아니다.
- provider consistency와 provider authenticity의 차이를 유지하라. 로그·hash가 실제 격리나 제공자 신원을 증명한다는 서술은 안 된다.
- conservative nonlinear completion ranges와 exact linear completion bounds의 성격을 구분해 표기하라. null/invalid를 삭제해 좋아진 점수나 유효응답 분모를 만들지 않는 현재 원칙은 유지해야 한다.
- group-by-profile W1은 author aggregate상 singleton row 비중이 약63.76%다. 이를 풍부한 집단별 응답분포를 검증한 결과로 설명하지 말고, 해당 셀 크기를 같은 표에 보여라. 더 세밀한 셀을 만드는 것이 해결책은 아니다.

## 남는 한계와 평가

검토한 수치에서 main human contrast의 재구성 오류는 찾지 못했다. 고정 행 유지, whole-pair invalidation, outcome-free 생성 입력, component 보고, 고정 reference와 사후개발 이력 공개는 이 프로젝트의 강점이다. 67개 테스트의 통과는 이 장치의 일부가 구현되어 있다는 근거다.

그러나 실제 응답모델 관측은 아직 0이고, 모델·실행계획·presentation/repeat adapter는 미완성이다. 따라서 현재 입증된 것은 재현 가능한 평가 구성요소와 선택된 인간 reference의 기술적 특성이다. 향후 생성 출력이 제공되어도 결론은 한 역사적 survey의 선택 코호트와 복원된 elicitation에 조건부일 것이다. 정치적 메커니즘, 국민여론, 인간 개인의 복제, 새로운 일반적 fidelity 법칙으로 나아갈 근거는 없다.

다음 단계의 과학적 우선순위는 지표·가상대조자료 확장이 아니다. **응답자 사실 귀속을 명확히 한 고정 elicitation, 실행 가능한 사전 manifest, 실제 모델 출력에 대한 기존 component 표의 완성, 그리고 근접 문헌을 넘어 어떤 welfare inference가 달라지는지의 구체적 설명**이다. 그 증거가 없으면 연구 기여는 잘 설계된 제한적 검증 프로토콜로 남는다.
