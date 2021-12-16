#도커 환경 설정 (ubuntu)
##docker 설치

1. 도커 설치
$ curl -fsSL https://get.docker.com/ | sudo sh
만약 curl 툴이 없다면
$ sudo apt-get install curl

2. root 권한 부여하기
$ sudo usermod -aG docker $USER
    