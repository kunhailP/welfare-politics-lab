# 모델 선택 전까지 준비하는 데이터와 웹 플랫폼 입력

모델·설정·잔액·실제 실행은 사용자가 결정한다. 아래 코드는 원자료를 검증하고
입력과 평가 자료를 분리해 준비하며 모델/API를 호출하지 않는다. 추가 외부 API
지출은 0원이다. 현재 웹 플랫폼의 네이티브 실행·내보내기 연결은 검증하지 않았다.

## 한 명령으로 준비

환경 설치는 [사용자 안내](USER_HANDOFF_KO.md)를 따른다. 이미 전달한
`dataverse.zip`을 지정하고 새 출력 경로와 새 ZIP 경로를 사용한다.

```bash
python scripts/prepare_platform.py \
  --archive /absolute/path/to/dataverse.zip \
  --output runs/platform_ready_01 \
  --zip /absolute/path/to/welfare-generation-inputs.zip
```

원본 ZIP의 SHA256과 7개 파일을 검증하고, 고정 인간 표본·비교모형·민감도 분석과
전체 테스트를 재현한다. 이어 핵심 재현 영수증으로 봉인된 요청만 내보낸다.
실패하면 중단하며 기존 출력이나 원자료를 다른 내용으로 덮어쓰지 않는다.

| 산출물 | 용도 |
| --- | --- |
| `analysis/` | 인간 기준·원자료 분석·평가 파일. 생성 환경에 전달하지 않음 |
| `generation_only/` 및 지정한 ZIP | 아래 다섯 파일만 포함한 입력 전용 묶음 |
| `preparation_receipt.json` | 원자료·코드·핵심 영수증·ZIP 해시, 테스트 수, 실제 호출 0회 기록 |

ZIP 구성은 `primary_requests.jsonl`(3336개), `common_task_requests.jsonl`(96개),
`manifest.json`, `campaign.template.json`, `README.txt`다. 공통 과제는 원래 계획의
모든 셀에 안정적인 `audit_request_id`를 추가한다. 주요 요청은 동결된 파일의
바이트를 그대로 유지한다. 원자료·인간 결과·모형 예측·리뷰는 포함하지 않는다.
개별 과제 입력은 GitHub에 공개하지 않고 소스 자료의 허용된 사용 범위에서 처리한다.

이 묶음은 입력 파일이며, 웹 플랫폼에서 자동으로 실행되는 study ZIP이라고
표시하지 않는다. 플랫폼 개발 도우미는 입력의 가져오기·실제 호출·원문 내보내기를
해당 환경에서 연결해야 한다. 연구 보조 AI가 보는 설계 문서와 응답자 모델의
입력을 구분한다. 응답자 모델에는 각 요청의 `messages`만 새 문맥으로 전송한다.
이전 답변, arm 이름, 평가 결과를 추가하거나 지속 대화 메모리를 켜지 않는다.
파일 선별은 OS 수준 접근 격리의 증거가 아니므로 실행 경로에서 별도로 확인한다.

## 플랫폼에 전달할 개발 지시문

아래 지시문은 연구 개발 도우미에게만 전달한다. 응답자 모델의 프롬프트가 아니다.

> 첨부한 generation-only 묶음의 manifest와 README를 확인하세요. 기존 연구의
> 고정 프롬프트·과제·arm·A/B·실패 규칙을 변경하지 마세요. 먼저 이 웹 환경에서
> messages 배열을 그대로 보내고, 실제 반환 모델 ID·원문·전체 시도·사용 크레딧을
> 기록해 내보낼 수 있는지 코드와 로그 스키마로 점검하세요. 응답자에게는 messages만
> 보냅니다. 원자료·인간 기준·리뷰 파일을 생성 경로에 넣지 마세요. 규칙 대체 응답이나
> 정답을 생성하지 마세요. 사용자 모델·설정·잔액 상한과 반복·제시 방식 계획을 동결하기
> 전에는 실제 응답 수집을 시작하지 마세요. 지원되지 않는 인터페이스는 추정하지 말고
> 미지원으로 기록하세요. 네이티브 study와 내보내기가 실제로 검증된 범위를 보고하세요.

## 실제 로그를 받으면

주요 로그 계약과 CLI는 [응답 기록 형식](RESPONSE_LOG_FORMAT.md)을 따른다.
크레딧이 관측되면 `cost_value`와 `cost_unit`을 사용한다. `SocioVerse_Agent`와
`SocioVerse_Sim`은 서로 합산하거나 달러로 임의 환산하지 않는다. 비용을 모르면
0으로 쓰지 않는다. 플랫폼이 요청별 사용량을 제공하지 않는다면 그 회계 연결을
해결한 뒤 분석한다. 외부 추가 결제가 없다는 사실과 자원 소비가 0이라는 주장은 다르다.

공통 과제는 각 시도에 `audit_request_id`, `audit_base`, `income_label`,
`focal_income`, `focal_position`, `messages_sha256`를 그대로 복사한다.
추가로 `attempt`, `status`, `raw_reply`, `returned_model_id`, 관측된 비용을 기록한다.
전송 실패만 최대 2회 재시도하고, 형식 오류·거절은 쌍 전체를 미관측으로 남긴다.
모든 셀은 응답 또는 명시적으로 소진된 전송 실패 기록을 가져야 한다.

평가에는 보관한 로컬 core의 원래 요청 파일과 **수집 전에 따로 기록한** core
영수증 해시를 사용한다. 내보낸 공통 과제 파일에는 ID가 추가되므로 원본 core
요청 파일의 바이트 해시와 같다고 간주하지 않는다.

```bash
python -m welfare_politics.common_task_responses \
  --requests runs/platform_ready_01/analysis/core/planned_primary_requests/common_task_audit_requests.jsonl \
  --attempts /path/to/actual_common_task_attempts.jsonl \
  --expected-model EXACT_RETURNED_MODEL_ID \
  --frozen-receipt runs/platform_ready_01/analysis/core/receipt.json \
  --expected-receipt-sha256 PRE_GENERATION_RECORDED_CORE_SHA256 \
  --output runs/platform_ready_01/actual_common_task_evaluation.json
```

이 평가기는 순서를 가정하지 않고 ID·셀·프롬프트·A/B·모델·시도 내역을 검증해
기존 공통 과제 요약기에 연결한다. 모델 소득 표지의 효과이며 인간의 반사실적
결과나 실제 계층 정치의 인과효과가 아니다. 반복·제시 변형용 일반 live adapter와
전체 캠페인 동결, 웹 실행 및 실제 모델 결과는 여전히 별도 작업이다.
