# Project: MoonBeats-ClassicVer
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FYjisuY%2FMoonBeats-ClassicVer.git&count_bg=%23FFE2E2&title_bg=%238785A2&icon=&icon_color=%23FFC7C7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)


## 1.	프로젝트 배경 및 목표
### 프로젝트의 추진 배경
최근 학과 ‘데이터마이닝’ 수업에서 Clustering(군집화)에 대해 배우는 과정 중 12개의 클래식 곡을 학생들에게 들려주고 선호도를 조사한 자료를 통해 군집분석을 실습해보았던 경험이 있다. 학과 특성상 파이썬을 통계 분석이나 데이터 마이닝의 용도로 대부분 사용했었지만, 이번 프로젝트에 대해 고민해보며 ‘군집화의 결과를 프로그램 개발에 직접 이용해보자’라는 아이디어가 떠올랐다. 그래서 파이썬을 이용한 간단한 게임제작이라는 주제로부터 출발하여 ‘군집분석’의 결과를 추가한, 전공 분야를 결합한 게임을 제작하는 프로젝트를 추진하게 되었다.

### 달성하고자 하는 목표
옛날부터 클래식 음악에 많은 관심이 있었던 점을 고려하여 프로젝트의 초기에는 게임에서 사용될 음악을 ‘클래식’으로 한정하여 군집분석을 시행하고, 게임을 관심있게 플레이할 주요 타겟층도 ‘클래식 음악에 관심이 있는 사람’으로 생각한다. 그 후, 게임 시스템이 많은 데이터베이스를 기반으로 성공적인 개발이 되었다면, 음악 샘플의 주제를 클래식 외에도 ‘가요’를 추가하여 위와 동일한 방식으로 새로운 데이터들을 수집하고, 군집을 구성하여 주요 타켓층을 좀 더 넓혀간다. 이러한 과정을 통해 특정 음악에 관심이 있는 사람들만 재미있게 플레이 할 수 있는 것이 아닌, 더 많은 사람들이 재미있게 게임을 플레이할 수 있도록 하는 것이 큰 목표이다. 하지만 이 부분에 있어서는 음원에 관한 저작권 문제도 있고, 군집화에 필요한 데이터를 수집하는 것에 많은 시간이 소요되므로, 이번 프로젝트의 실질적인 목표는 ‘클래식’으로 한정하여 군집분석을 시행하고, 게임 개발을 성공적으로 마무리하는 것으로 정해 놓는다. 또한, 어떤 프로그램을 개발하는 것은 처음 해보는 과제이기때문에 비교적 쉬운 프로그램일지라도 처음부터 실현 불가능한 목표를 잡는 것은 지양하여 ‘클래식’이라는 한 개의 주제를 이용한 게임개발을 성공적으로 마치는 것을 이번 프로젝트의 목표과제로 설정한다.

### 공개 시의 기대 효과
먼저 ‘클래식’을 주요 음악 샘플로 한 첫 프로그램을 공개하게 되면 클래식에 관심이 있거나 리듬게임을 즐겨 하는 사용자들이 게임을 플레이할 것이다. 이렇게 사용자가 증가하게 되면 클래식 음악 선호도에 관련된 군집을 더 세분화하여 구성할 수 있게 되고, 사람들의 선호도 데이터를 갖게 되므로, 해당 게임 프로그램에만 활용하는 것이 아니라, 데이터마이닝 분야에서도 데이터를 활용할 수 있게 된다. 또한 이를 이용하여 구글 플레이스토어, 앱스토어, 스팀 등의 스토어들에 정식으로 출시를 고려해볼 수 있고, 정식 출시가 승인되면 이 프로그램을 통하여 수익을 창출할 수도 있다. 이렇게 클래식 음악을 주제로 한 프로그램이 성공적으로 개발되었다면 한국가요, 팝 등 더 많은 주제를 노래의 샘플로 추가하며 게임의 버전을 여러 개로 출시할 수 있게 된다. 이 과정에서 기존의 클래식 버전을 이용하던 사용자들에 합하여 새로 유입되는 사용자들의 선호도에 대한 데이터도 얻을 수 있다. 따라서 단순한 게임 프로그램의 개발에서 나아가, 음악의 각 분야에 대한 사용자들의 선호도 데이터를 얻어, 다른 분야에도 활용할 수 있는 기회를 제공할 것으로 기대할 수 있다.
#
#

## 2. 프로젝트에서 제공하고자 하는 기능
- 게임의 메인 화면에서 사용자는 4가지(한국어, 영어, 일본어, 중국어(간체)) 언어 중 하나를 선택하여 플레이할 수 있다.
-	사용자는 12개의 곡에 대한 선호도를 1점~10점까지 입력하여 군집분석을 통해 자신과 비슷한 경향을 가진 사람의 군집이 있다면 그 군집에 대한 추천 곡을 플레이 가능한 곡으로 받을 수 있다.
- 만약 사용자의 성향과 비슷한 군집이 없을 경우, 여러 분위기의 곡을 골고루 섞어 놓은 곡들을 플레이 가능한 곡으로 받게 된다.
- 위와 같은 과정을 거쳐 받은 플레이 가능한 곡들(3개) 중 사용자는 하나를 선택하여 게임을 플레이할 수 있다.
- 게임이 시작되면 사용자는 가운데의 원 모양을 회전해가며 동서남북에서 날아오는 부채꼴들의 색을 원의 색과 형태에 일치시키면 점수를 획득할 수 있다.
- 게임이 끝나면 사용자는 자신이 획득한 점수와 해당 곡을 플레이 함으로서 얻을 수 있는 최고점수(퍼펙트 점수)를 화면에서 볼 수 있다.
- 만약 사용자가 퍼펙트 점수를 얻게 되면 곡의 선택창에서 해당 곡에 ‘퍼펙트 클리어!’라는 글자가 생긴다.
- 위와 같은 과정으로 사용자는 3개의 클래식 곡들을 들으며 재미있는 리듬게임을 플레이할 수 있게 된다.

### UI 스케치, 개략적인 화면 및 메뉴 구성, 사용자 시나리오, 스토리 보드 등 활용 가능
-	게임의 첫 시작화면(추후 코딩과 함께 언어, 게임방법, 플레이 버튼을 추가)
<img src="https://user-images.githubusercontent.com/130039117/234804134-d9a2b7bf-48d1-4aa4-bb72-e80ea7909e4b.png" width="30%" height="30%">

-	게임의 곡 선택화면

<img src="https://user-images.githubusercontent.com/130039117/234804206-81a7a32d-eb12-4684-94da-661a1529401c.png" width="30%" height="30%">

-	게임의 진행 화면

<img src="https://user-images.githubusercontent.com/130039117/234804265-4f21177e-764f-4754-9599-c9de71cde637.png" width="30%" height="30%">

-	게임이 끝난 후 결과 화면 

<img src="https://user-images.githubusercontent.com/130039117/234804311-c62d596e-930b-4e9a-a5dd-e744ed8f2c16.png" width="30%" height="30%">



## 3. 목표 달성 여부 판단 기준
-	목표 달성 여부는 아래와 같은 10가지의 기준으로 목표 달성 여부를 판단한다.

<img src="https://user-images.githubusercontent.com/130039117/234806343-dcd930c5-0ec3-4b41-a1b0-8a87a6d42107.png" width="30%" height="30%">


## 4. 추진계획
### 작업일정
- 1주차: 클래식 음원 파일 수집(직접 곡을 연주하여 녹음), 기존 데이터로 군집분석 실행
- 2주차: 사용자에게 선호도를 직접 입력 받아 군집분석을 실행하고 이를 바탕으로 사용자 맞춤 노래 샘플을 구성하는 코드작성
- 3주차: 사용자가 선택한 음악을 재생하여 게임이 실행되고 리듬에 맞추어 사용자가 게임을 진행할 수 있는 게임의 주요 코드작성
- 4주차: 2~3주차에 코딩했던 내용을 바탕으로 게임 시작부터 종료까지 전반적인 과정의 코드를 작성하고 수정
-5주차: 최종 게임 구성 및 검토 후 주변 지인들을 통해 게임 테스트 후 피드백 진행


### 소요 장비 또는 자원 조달 계획
이번 프로젝트는 오로지 클래식 버전이고, 클래식 음악도 저작권이 존재함을 인지하여, 많은 클래식 곡을 직접 연주할 수 있는 개발자 본인의 능력으로 저작권에서 발생하는 비용을 없앴다.
이 프로그램 자체는 슈퍼컴퓨터가 필요할 정도로 빅데이터를 다루지 않기 때문에 개발자 본인의 노트북으로도 충분히 구현할 수 있는 수준이다. 따라서 소요 장비는 노트북정도가 필요할 것이고 자원 조달 같은 경우에도 외부의 영향을 최소화하는 방법으로 본인이 직접 곡을 녹음하여 음원을 제작하므로 저작권은 개발자 본인에게 존재하게 된다.
만약 클래식 버전의 게임 출시가 성공적으로 이루어져서 가요 버전까지 제작을 계획하게 된다면 아래의 사진과 같은 법률에 따라 곡의 개수에 따른 저작권 비용을 지불해야 할 것이다. 

<img src="https://user-images.githubusercontent.com/130039117/234809401-ac5ee8f4-cb4d-4c4d-a195-4b0f80ccbc1d.png" width="30%" height="30%">


### 사용하고자 하는 오픈소스SW
- python


## 5. 위험 평가 및 대책
### 예상되는 위험 요인 및 대책
-	클래식 음악을 사용할 경우 저작권 문제: 이 문제는 클래식 음악에는 작곡가가 사망한지 오랜 시간이 지났기 때문에 저작권이 없을 것이라는 본인의 생각과 다름을 인지하여, 개발자 본인의 능력으로 직접 클래식 음악을 연주, 녹음하여 사용하면 해결가능하다.

-	가요음악을 사용할 경우 저작권 문제: 이 경우 참고문헌의 법률 내용처럼 타당한 저작권 비용을 지불하여 사용가능하다.

-	프로그램 구현의 초기에는 샘플이 부족하여 군집화가 적절히 이루어지지 않을 가능성이 있다. 이 문제는 향후 교내 설문조사 또는 온라인 설문조사를 통하여 많은 데이터베이스를 구축함으로써 어느정도 해결 가능한 문제이다.


## 6. 주요 용어 설명
-	Clustering(군집화): 주어진 데이터 집합을 유사한 데이터들의 그룹으로 나누는 것을 군집화(clustering)라 하고 이렇게 나누어진 유사한 데이터의 그룹을 군집(cluster)이라 한다. 군집화는 예측 문제와 달리 특정한 독립변수와 종속변수의 구분도 없고 학습을 위한 목표값도 필요로 하지 않는 비지도학습의 일종이다.

- 게임 과정의 용어들은 앞서 설명한 게임 진행 과정에서 잘 나타나있다.


## 7. 참고 문헌
• https://treeof.tistory.com/174 (클래식의 저작권에 관해)

•	https://www.mangoboard.net (사용자 UI – 망고보드를 이용하여 직접 디자인)

•	http://www.koscap.or.kr/community/dataroom_view/?f_seq=393 (가요 음악 저작권 사용료에 관한 법률)

•	https://datascienceschool.net/03%20machine%20learning/16.01%20%EA%B5%B0%EC%A7%91%ED%99%94.html (군집화 설명)
