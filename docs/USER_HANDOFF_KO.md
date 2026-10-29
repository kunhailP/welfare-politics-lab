# 여기서 이어서 진행하기

이 저장소는 **복지 수급자 평가의 계층별 패턴을 합성 응답자가 재현하는지**
연구하기 위한 코드와 설계다. 인간 자료 분석, 요청 계획 생성, 저장된 응답의
키 기반 평가가 구현돼 있다. 실제 모델 실험은0회이며, SocioVerse에 올리자마자
본 실험이 실행되는 완성 앱은 아니다. 아래 미구현 항목을 남긴 상태로 인계한다.

## 1. 저장소 받기

공개 GitHub 저장소에서 받는다.

```bash
git clone https://github.com/kunhailP/welfare-politics-lab.git
cd welfare-politics-lab
```

기존 인계 bundle은 게시 전 검토 이력의 별도 백업이다. 필요하면 다른 폴더에 복원한다.

```bash
git clone /path/to/welfare-politics-lab-handoff.bundle welfare-politics-lab
cd welfare-politics-lab
```

소스 ZIP을 받았다면 압축을 풀고 `welfare-politics-lab` 폴더로 이동한다.
ZIP에는 Git 이력이 없으므로 GitHub에 올릴 때 직접 Git 저장소를 초기화하거나
GitHub Desktop에서 로컬 저장소로 추가한다. 이력을 유지하려면 bundle을 권장한다.

## 2. Python 환경 준비

Python3.12 환경에서 검증했다. 패키지 설치에는 인터넷 연결이 필요하다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-tested.txt
python -m pip install -e . --no-deps
```

코드 설치가 끝난 뒤 아래 재현 명령은 모델/API와 인터넷을 사용하지 않는다.

## 3. 원자료를 지정하고 전체 재현

웹 플랫폼에 가져갈 입력까지 준비하려면
[플랫폼 준비 안내](PLATFORM_PREPARATION_KO.md)의 `scripts/prepare_platform.py`를 사용한다.
모델 선택 전에도 로컬 데이터 검증과 정답이 제외된 입력 ZIP을 만들 수 있다.

기존에 보낸 `dataverse.zip`을 별도로 준비한다. 원자료는 저장소에 포함하지 않았다.
[원자료 출처](https://doi.org/10.7910/DVN/LPHMB7)와 파일별 해시는
[자료 안내](../data/README.md)에 있다. 다시 다운로드한 ZIP의 포장 방식 때문에
해시가 달라지면, 검사를 끄지 말고 원본과 출처를 먼저 비교한다.

```bash
python scripts/reproduce_handoff.py \
  --archive /absolute/path/to/dataverse.zip \
  --output runs/my_first_check
```

매번 새 `--output` 경로를 쓴다. 기존 결과를 덮어쓰지 않는다. 이 명령은 원자료
검사, 기존 전체 분석, 인간 기준 민감도, 사람 자료 비교모형, 테스트를 순서대로
수행한다. 실패하면 해당 단계의 로그와 실패 상태를 남기고 중단한다.

완료 후 먼저 볼 파일:

| 파일/폴더 | 용도 |
| --- | --- |
| `handoff_receipt.json` | 전체 재현 상태·테스트 수·산출물 해시 |
| `core/primary_matched_design/` | 인간 기준·설계·고정 행 ID; 생성 환경에 전달하지 않음 |
| `core/planned_primary_requests/requests.jsonl` | 주요 실험3336개 요청의 계획; 실제 응답 아님 |
| `core/planned_primary_requests/common_task_audit_requests.jsonl` | 공통 과제96개 계획; 인간 정답 없음 |
| `source_sensitivity/report.json` | 같은 인간 원자료 안의 코호트 민감도 |
| `statistical_references/report.json` | 겹치지 않는 사람 자료로 학습한3개 비교모형 |

기존 검증 기록은 [최종 인계 검증](FINAL_HANDOFF_VALIDATION.json),
[통계 비교 검증](STATISTICAL_REFERENCE_VALIDATION.json)에 있다. 현재 결과를
검증된 LLM 결과나 논문 게재·우승의 증거로 사용하지 않는다.

## 4. 연구를 이어갈 때 먼저 읽을 것

1. [고정된 질문과 결과표](EMPIRICAL_CLAIM_SPEC_V1.md): 주요 F 대 N은 소득·고용위험·
   자녀의 세 사실 묶음 비교다. 소득만의 추가 효과는 보조 F 대 F-I다.
2. [현재 프로토콜](CURRENT_PROTOCOL.md), [프롬프트와 원 설문의 대조](STIMULUS_CROSSWALK.md).
3. [사람 자료 비교 결과](STATISTICAL_REFERENCE_RESULTS_KO.md), [실제 실행 전 남은 작업](NEXT_STEPS_KO.md).
4. [최종 새 문맥 블라인드 리뷰와 대응](../reviews/final_09/response.md).

주요 인간 표본·대비·점수를 유리한 결과에 맞춰 바꾸지 않는다. 변경이 필요하면
새 버전과 변경 이유를 남기고 기존 결과도 보존한다. 원자료의 선택 편향과
수급자 과제 재구성 한계는 그대로 남는다.

## 5. 실제 응답을 수집한 뒤 평가

현재 포함된 공개 평가기는 주요 실험 로그용이다. 정확한 모델 ID와 시도 기록,
arm·사람·A/B 매핑·프롬프트 해시·rollout을 원래 요청 계획과 일치시켜야 한다.

```bash
python -m welfare_politics.recorded_responses \
  --design runs/my_first_check/core/primary_matched_design/human_reference_design.npz \
  --requests runs/my_first_check/core/planned_primary_requests/requests.jsonl \
  --attempts /path/to/actual_attempts.jsonl \
  --expected-model EXACT_RETURNED_MODEL_ID \
  --frozen-receipt runs/my_first_check/core/receipt.json \
  --expected-receipt-sha256 PRE_GENERATION_RECORDED_RECEIPT_SHA256 \
  --output runs/my_first_check/actual_recorded_evaluation.json
```

로그 계약은 [기록 형식](RESPONSE_LOG_FORMAT.md)을 따른다. 가짜 응답·사람의 정답·
통계모형 예측으로 실제 모델 로그를 채우지 않는다. 생성용 환경에는 요청의
`messages`만 전송하고 인간 기준·평가 파일을 마운트하지 않는다. 저장 폴더를
나누는 것만으로 격리가 구현되지는 않는다.

## 6. 본인 GitHub에서 이어가기

공개 저장소는 [kunhailP/welfare-politics-lab](https://github.com/kunhailP/welfare-politics-lab)이다.
공개 커밋 작성자·커미터는 본인 계정으로 연결했다. AI를 활용한 설계·코드·내부
리뷰 사실과 원자료 저자 표시는 보존했다. 게시 전후 커밋 대응은
[게시 기록](PUBLICATION.md)에 있다.

본인 계정으로 인증한 GitHub Desktop이나 Git을 사용해 변경을 커밋하고 push하면 된다.
공개 저장소를 clone해서 이어가며, 게시 전 bundle 이력으로 원격 main을 덮어쓰지 않는다.
`scripts/publish_github.py`는 별도의 새 비공개 저장소를 만드는 기존 보조 도구이므로
이미 게시된 이 저장소에 다시 실행할 필요가 없다.
원자료·실행 결과·개별 응답·API 키는 Git에 넣지 않는다.
