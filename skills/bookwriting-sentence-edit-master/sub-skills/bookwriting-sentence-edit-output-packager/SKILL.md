---
name: bookwriting-sentence-edit-output-packager
description: 부모 bookwriting-sentence-edit-master의 INTERNAL sub — 다듬은 전문을 본문만 담은 .md 파일로 만들고, 대화창에는 「뺀 것 / 보강한 것 / 출간 전 확인 사항」 세 칸만 짧게 보고한다.
when_to_use: bookwriting-sentence-edit-master Step 7. manuscript-guard 통과 후 마지막으로 자동 호출.
disable-model-invocation: true
---

# bookwriting-sentence-edit-output-packager (Step 7 · 출력)

## 파일
- 원고가 길면 대화창에서 잘리므로 **다듬은 전문은 .md 파일로** 만든다. 파일에는 **본문만** 넣는다(머리말·해설·변경 표시 없음).
- 파일 이름은 원고의 장·절을 알 수 있게 짓는다(예: `03장-2절-다듬음.md`).

## 대화창 보고 — 세 칸, 짧게
1. **뺀 것**: AI식 표현·자기반박을 어떤 유형으로 몇 군데 걷어 냈는지
2. **보강한 것**: 무엇을 채웠고 근거가 무엇인지(원고 / 기존 각주 / 웹 확인)
3. **출간 전 확인 사항**: 「사실 확인」과 「각주 필요」 위치 목록

긴 해설, 고친 문장 전후 대조, 칭찬은 쓰지 않는다.

## 음성 입력 대응
- 저자가 음성으로 지시하므로 오타나 잘못 인식된 단어가 있을 수 있다. 문맥으로 뜻을 읽어 진행한다.
- 정말 모호해서 결과가 달라질 때만 한 번 묻는다.

## 자기검증
- [ ] 파일에 본문 외 내용 0
- [ ] 대화창 보고가 세 칸을 넘지 않는가
- [ ] manuscript-guard 가 넘긴 확인 사항을 빠짐없이 옮겼는가
