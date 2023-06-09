# Earthquake<br>
사용할 자료  <br>
<br>
vs 30  <br>
각 시도별 내진율  → 국토부   <br>
과거 지진 관측 기록  <br>
역사 지진 관측 기록  <br>
지진/지진해일 대피소 현황  <br>
(호오옥시 있으면) 경주/포항 지진 피해 사례(위 경도나 주소 단위로 - 지반데이터랑 연결지어서 경향성 분석하게)  <br>
<br>
<br>
스토리 라인  <br>
<br>
배경  <br>
주제설명  <br>
사용데이터 - 왜 사용했는지(선)  <br>
가공 방법 (나열식)   <br>
—---------------------  <br>
각 자료별로 분석방법 및 결과 (구체적으로)  
5-1 :  VS30 (양화랑)  
격자화<br>
행정단위마다 평균내서 시각화(보류)<br>
5-2 : 과거 지진 관측 기록(조민제) - 히트맵 <br>
시각화<br>
5-3 : 역사 지진 관측 기록(조민제) - 히트맵- 완료<br>
5-4 :  각 시도별 내진율 - (김유일) : 행정구역별로 색칠   <br>  
<br>
5-5 : 지진/지진 해일 대피소 현황 (유지민)<br>
시각화 <br>
// 5-6 : 경주 / 포항 지진 피해 사례<br>
<br>
대비 근거 자료 도출(코로플레스 맵)<br>
지역별 지진위험수치<br>
자료 5-1~5-3로 통합해서 행정구역별 위험수치 지도 시각화<br>
지역별 대비 수치<br>
자료 5-4~5-5 통합<br>
상관관계 분석 → 경주/포항 지진 피해 사례(건축물 손상 정도), 액상화 발생 위치랑 비교하기<br>
격자 위에 피해 입은 곳 표시<br>
해결방안: 대피소(공터) 신설해야 할 곳 선정 + 내진설계 증축 필요지역 선정(6참고)<br>
서울 대지진(규모 6.5) 피해 시뮬레이션?<br>
지진으로 인해 최근 실제로 흔들린 곳(최대진도 II 이상) <br>
<br>
<br>
그냥 순수하게 생각했을 때 일본 내진설계율 vs 우리나라 내진설계율 <br>
<br>
생각했던 내용:<br>
(2023 - 지진 난 년도) + 지진 세기 * k  -> 값 도출해서 지도에 표시	<- 값에 따라 색 바뀌는거<br>
의도 : 한반도 지진 위험하다(경각심)<br>
<br>
<br>
<br>
<br>
행정구역(내진율+지반+시대별 지진빈도) 순위를 매겨서 대피소 수 값을 정해, 부족한 지역이 있다면 짓기기 <br>
<br>
earthquake intensity  * a + ji ban * b + run place * c = ??<br>
map color paint<br>
run place distance check * a + population * b + (able people *c)  = ??<br>
place plus how many?<br>
<br>
지진강도 * a+지반*b+ 대피소*c =??<br>
→ 지도에 색칠<br>
<br>
대피소 개수(대피소갯수 / 시도면적) *a + 인구수 *b + (수용 인구 / living people)*c =??<br>
→ 얼마나 많은 대피소를 추가해야되나 ?<br>
<br>
<br>
2023.06.13<br>
포항과 경주의 대피소 수를 이상적인 값으로 선정하고, 국내 전체와의 비교<br>
고려할 변수 : 지반, 지진 빈도, (인구수)<br>
<br>
<br>
<br>
## 6.16 배분<br>
"시군구 단위"(총 250개)로 데이터 도출해주시면 됩니다.<br>
시군구 단위는 SIGUNGU_2302.json 에서 받아오신 뒤에 DataFrame화 시키시면 됩니다<br>
해당 DataFrame에 열을 하나 새로 만든 뒤에, 시군구 단위로 데이터 값 도출한 거 추가해주시면 됩니다.<br>
<br>
양화랑 - 시군구 별 지반 값(vs30) 평균 값 도출, 규모-> 진도 시뮬레이션<br>
조민제 - 지진 기록을 가지고, 규모를 에너지로 변환해주신 다음, 시군구 별로 "합계"해주시면 됩니다.<br>
변환식 : 10**(11.8+1.5*규모)*(10**-7) <- J(줄)단위로 변환한 겁니다<br>
김유일 - 여진 추이 분석 방법(시계열 or 추세선 or 비 선형분석 등등) 중에 뭐가 적합한 지랑, 구체적으로 파이썬 코드 예시 알아와 주세요.<br>
유지민 - 시군구 별 대피소 수용인원, 시군구별 총 인구수 받아오신 다음, 시군구 별로 "인구 수용 비율" 구해주시면 됩니다.<br>
수용인원 없이 대피소 면적만 나올 경우, 3.3으로 나눠주시면 수용인원 나옵니다.<br>
<br>
## 6.17<br>
지반 값을 사용하는 이유<br>
포항 경주 진도 차이 <br>
<br>
전처리<br>
Vs30 연구 데이터(.dat 파일)를 받아와서 데이터프레임화<br>
numpy 배열로 변환 후 격자단위로 시각화<br>
문제점: 육지 부분 데이터만 추출하기 위해서, 시군구 단위로 분석하기 위해서는<br>
우리나라 시군구 행정 경계 정보 필요<br>
-> 시군구의 행정경계 shp 파일을 각각 받은 뒤,<br>
simplify 및 topology, 좌표계 변환 후, json으로 변환<br>
-> 또 문제점: 시군구가 중복되는 명칭이 많고(중구,서구 등), 어떤 상위도가 있는 지 알 수 없었음<br>
-> 시도 행정경계 shp도 같은 방식으로 json 변환 후<br>
시군구의 대표 점을 잡은 뒤, .contains()를 이용해 포함되는 시도를 찾음<br>
시군구가 어떤 시도가 포함된 지 열을 포함한 하나의 데이터 프레임으로 생성 후, json 파일로 저장, 사용<br>
<br>
이후 격자 점이 담긴 데이터프레임과 시군구 폴리곤이 담긴 데이터프레임을 sjoin해서 각 점에 시군구를 매치시켜서, 시군구별 vs30 평균 값과, 하위 10%값 도출<br> 
<br>
=> 경향성<br>
해안, 강가가 전체적으로 낮다<br>