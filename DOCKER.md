# 도커 환경 설정 (ubuntu) 및 도커 이미지
## docker 설치

도커 설치

    $ curl -fsSL https://get.docker.com/ | sudo sh    

만약 curl 툴이 없다면

    $ sudo apt-get install curl

root 권한 부여하기

    $ sudo usermod -aG docker $USER

## docker login / logout

도커 허브 가입 후
로그인

    $ docker login
    명령 후, Username / Password 를 넣으면 login 성공
  
로그아웃

    $ docker logout

## docker image

Dockerfile 작성 후, 이미지 빌드

    $ docker build --tag {USERNAME}}/{NAME} .

Docker hub 에 push

    $ docker push {USERNAME}}/{NAME}
