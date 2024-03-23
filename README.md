<h1>Assembler!</h1>

------------------------------

여러 언어로 16비트 어셈블러를 구현해보는 프로젝트입니다. 

실행 테스트를 위한 16비트 CPU 및 64KB 메모리 에뮬레이터를 포함합니다.

한국교통대학교 컴퓨터공학과 2024년 <컴퓨터 구조> 강의의 2주차 과제에 대한 제출물을 개발하기 위해 시작되었습니다. 

모든 코드는 한국교통대학교 컴퓨터공학전공 22학번 <a  href="https://github.com/Epinephrine00">이두현</a>본인이 강의 내용 외 아무런 외부 도움 없이 독자적으로 작성하였음을 밝힙니다. 

contact : epinephrine00@a.ut.ac.kr / epi00nephrine@gmail.com

혹여나 과제 채점 과정에서 코드 작성자의 개인정보 인증이 필요하다면 위 연락처로 연락 부탁드리겠습니다. 

<br/>

--------------------------------

<h3>어셈블러 소스코드 파일 :</h3>

```
PyAsm/pade.py
CAsm/cas_cade.c
KAsm/app/src/main/kotlin+java/kasm/Kade.kt (프로젝트 생성만 함)
JAsm/app/src/main/java/jasm/Jade.java (프로젝트 생성만 함)
```

--------------------------------

<h3>TODO</h3>

 - _Python으로 16비트 CPU 에뮬레이터 구현_ (완?)
    - 낭만 넘치게 사칙연산 기호에서 손을 떼었습니다. =, |, &, not 연산자만을 이용했습니다!
    - 완성은 하였으나, 예외 처리 및 입출력 명령어 등 귀찮은 부분은 건들이지 않았습니다. 어셈블러가 어떻게든 잘 핸들링해줄거라 믿습니다. 
    - 추후 자잘한 기능 개선이 필요할수도 있습니다. 
 - _Python으로 64KB 메모리 에뮬레이터 구현_ (완)
    - 이건 사칙연산 썼습니다,,,, 리스트로 구현했는데 인덱싱때문에 그냥 반복문 돌리고 인덱스 + - 썼습니다... 
 - Python으로 어셈블러 구현 (진행중)
 - C로 어셈블러 구현 (진행중)
 - Kotlin으로 어셈블러 구현
 - Java로 어셈블러 구현
 - Assembly로 어셈블러 구현

--------------------------------

<h3>Special Thanks</h3>

좋은 강의를 해주시고 즐거운 과제를 내주신 구*근 교수님께 가장 큰 감사를 드립니다. 

 - ...비꼬는게 아닙니다! __진심으로 즐겁게__ 생각하고있습니다.

<br/>

작업 진행중 귀를 심심하지 않게 해준 다나카 케이이치로, 다나카 미나미, 런즈베리 아서 등 여러 음악인 및 성우분들께 감사드립니다. 

----------------------------------

All Wrongs Reserved (ɔ) Epinephrine00 in Embeded System Design Lab., Department of Computer Engineering, School of Computer, Korea National University of Transportation

<br/>

Genesis 1:3  |  _Dixitque Deus: "Fiat Lux", Et Facta Est Lux._  
창세기 1:3  |  _하나님이 이르시되 빛이 있으라 하시니 빛이 있었고._