# 모피어스 | tti-ri-ring

치매 노인 등 거동과 인지에 불편함을 겪는 약자들과 1인 가구로 살아 도움받지 못하는 사람들에게 또 다른 눈이 되어주는 모피어스 입니다. 모피어스는 웹 카마라와 ETRI의 API 2개 ((1) 사람 상태 이해 API, (2) 얼굴 비식별화 API)를 활용해 모니터링을 하고 있는 사람이 연속적으로 움직임이 없는 지를 검증합니다. 만약 움직임이 지속적으로 없을 시, 주의 상태라고 판단하고, 음성을 활용한 교차 검증을 진행합니다. 최종적으로 위험하다고 확인될 시, 비식별화 된 사람들의 사진과 상태 정보를 구급 기관한테 전달하고, 보호자한테도 내용을 전달합니다. 이같은 모피어스의 기능은 급증하고 있는 독거노인과 같이 보호자가 없이 생활하고 있는 사람들에게 매우 적합합니다.

To run the app, first install the dependencies into your virtualenv
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ensure you have a `.env` file and include the ETRI Open API Key

```
etriAccessKey = "insert key here"
```
