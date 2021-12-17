# 분산 학습 on GKE - IMDB Example -
이 프로젝트는 `Kubernetes 클러스터에서` `IMDB 데이터셋`을 학습하고 예측하는 간단한 프로젝트이다. 이 프로젝트는 컨테이너 환경에서 분산 머신러닝을 수행한다.

* Prerequisite
    - 모든 단계는 Google Cloud Platform의 GKE에서 수행됩니다. GKE를 사용하려면 gcloud command line을 설치해야 한다.
    - gcloud install guide : https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu

# GKE에서 Kubernetes Cluster 생성하기
1. 먼저 'GKE의 GUI'를 사용하여 Kubernetes 클러스터를 만든다.
![image](https://user-images.githubusercontent.com/77087144/146132088-7fb116e0-4164-4ebd-afaf-084d5d64aed5.png)


If you want to build Kubernetes Cluster with `AutoScaling`, then you have to set `autoscaling option` in `default-pool menu`.
And set the default of num_nodes to 2 for `nfs-server`. Also you have to set surge upgrade option to 3 for trainer jobs.
Then you can use `node AutoScaling`.

![image](https://user-images.githubusercontent.com/77087144/146133192-fb690b4d-7c8f-4c31-baf7-e33493e2aeca.png)


2.Kubernetes에 대한 accress credential를 가져온다.

    $ gcloud container clusters get-credentials imdb-cluster --zone asia-northeast3-a
  

    $ kubectl get nodes
    NAME                                             STATUS   ROLES    AGE   VERSION
    gke-my-kube-cluster-default-pool-d0ed872d-33mt   Ready    <none>   49s   v1.21.5-gke.1302
    gke-my-kube-cluster-default-pool-d0ed872d-gd42   Ready    <none>   49s   v1.21.5-gke.1302
    gke-my-kube-cluster-default-pool-d0ed872d-wpv4   Ready    <none>   49s   v1.21.5-gke.1302
  
각 Kubernetes 노드에 데이터 세트를 제공하기 위해 외부 디스크를 생성한다.

`--size`, `--zone` 등과 같은 옵션을 조정할 수 있다.

    $ gcloud compute disks create --type=pd-standard \
    --size=10GB --zone=asia-northeast3-a ml-disk
  
3개의 worker 노드가 있는 Kubernetes 클러스터 생성이 완료 되었다.



1.`copier` copy IMDB dataset into multiple dataset.

2.`Trainer` conducts distributed learning process in Kubernetes container.

3.`Aggregator` aggregates output models extracted from step 2.

4.`Server` container provides web page to demonstrate IMDB prediction.

# Quickstart 1번째 방법
먼저, 분산 IMDB 학습에 사용되는 환경 값을 정의한다.

    $ export WORKER_NUMBER=5
    $ export EPOCH=3
    $ export BATCH=100
    
* $WORKER_NUMBER 
    - 분산 학습의 worker 수 이다. 5로 설정하면 복사기가 IMDB 데이터 세트를 5개로 복사하고 5개의 trainer가 각 Kubernetes 노드에서 컨테이너로 생성된다.

* $EPOCH 
* $BATCH

데이터 세트 및 모델을 저장할 NFS 컨테이너를 생성한다. Kubernetes에서 PV, PVC로 사용된다. nfs-deployment.yaml은 splitter, trainer와 같은 다른 구성 요소에 mounted할 NFS 서버 컨테이너를 생성한다.

    $ kubectl apply -f nfs-deployment.yaml
    $ kubectl apply -f nfs-service.yaml
    
NFS 컨테이너를 사용하여 PV 및 PVC를 생성한다.

    $ export NFS_CLUSTER_IP=$(kubectl get svc/nfs-server -o jsonpath='{.spec.clusterIP}')
    $ cat nfs-pv-pvc.yaml | sed "s/{{NFS_CLUSTER_IP}}/$NFS_CLUSTER_IP/g" | kubectl apply -f -
    
[ 옵션 ]

NFS 서버의 디렉토리를 보고 싶다면 busybox 배포를 생성하고 컨테이너에 들어간다. 기본적으로 index.html 및 lost+found 파일이 존재한다.

    $ kubectl apply -f busybox.yaml
    $ kubectl exec -it $(kubectl get pods | grep busybox | awk '{print $1}') sh

    / # ls /imdb
    index.html  lost+found
    / # exit
    
copier가 $(WORKER_NUMBER)개의 데이터 세트를 생성한다.

    $ cat copier.yaml | sed "s/{{WORKER_NUMBER}}/$WORKER_NUMBER/g" | kubectl apply -f -
    
데이터 세트가 생성되었는지 확인하려면 busybox 배포를 확인한다. 복사된 데이터세트는 *.npz로 존재한다.

    $ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /mnt/data
    0.npz
    1.npz
    2.npz
    3.npz
    4.npz
    
Kubernetes worker에서 각 데이터 세트를 학습시킨다. 아래 bash 명령은 neural network model을 학습하고 추출하기 위한 trainer를 만든다.

    $ for (( c=0; c<=($WORKER_NUMBER)-1; c++ ))
    do
        echo $(date) [INFO] "$c"th Creating th trainer in kubernetes..
        cat trainer.yaml | sed "s/{{EPOCH}}/$EPOCH/g; s/{{BATCH}}/$BATCH/g; s/{{INCREMENTAL_NUMBER}}/$c/g;" | kubectl apply -f - &
    done
    
몇 분 후에 trainer job의 상태를 볼 수 있다. (상태가 완료되어야 한다.)

    $ kubectl get po
    NAME                          READY   STATUS      RESTARTS   AGE
    mnist-copier-qgkxf            0/1     Completed   0          14m
    mnist-trainer-0-g896k         0/1     Completed   0          3m
    mnist-trainer-1-6xfkg         0/1     Completed   0          3m
    mnist-trainer-2-ppnsc         0/1     Completed   0          3m
    
이것 또한 busybox 배포를 사용하여 생성된 모델을 확인할 수 있다.

    $ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /imdb/model
    0-model.h5
    1-model.h5
    2-model.h5
    3-model.h5
    4-model.h5
    
데모용 서버 배포를 만들어서 IMDB 예측을 test할 수 있다.
    $ kubectl apply -f server_ver2.yaml

Aggregate generated models into one model. Below command creates aggregator, which aggregate models into single model.

    $ kubectl apply -f aggregator.yaml

몇 초 후 외부 IP가 표시되어 데모 웹 페이지에 액세스할 수 있다. 아래 예는 외부 IP가 a.b.c.d이므로 웹 브라우저에서 a.b.c.d:80에 액세스할 수 있음을 보여준다.

    $ kubectl get svc
    NAME               TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
    ...
    imdb-server-svc   LoadBalancer   10.19.253.70   a.b.c.d   80:30284/TCP                 12m
    ...
    

# 2번째 방법
Check a aggregated model.

    $ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /imdb
    aggregated-model.h5
    ...
    
Create server deployment for demo. You can test MNIST prediction.
    $ kubectl apply -f server.yaml
    
After a few seconds, you can see the external IP to access the demo web page. Below example shows external IP is a.b.c.d, so you can access a.b.c.d:80 in web browser

    $ kubectl get svc
    NAME               TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
    ...
    imdb-server-svc   LoadBalancer   10.19.253.70   a.b.c.d   80:30284/TCP                 12m
    ...
    
Write a sample IMDB data in IMDB test dataset.

After writing IMDB sample, web page shows prediction result.


# Detailed Arguments of Each Component
`Copier` : copier copies IMDB data equally by the number of contents. so total number of IMDB train dataset is 25000, each number of data.npz is 25000.

--n_container : number of training container.

--savedir : saved directory path of splitted data. each data files saved .npz file format will be saved as number of --n_container.
 
`Trainer` : trainer will independently learn the data into each container and create a model for each container as *.h5 file format.

--data : Data you want to learn from the container.

--epoch : number of epoch.

--batch : size of batch.

--savemodel : saved model in each container. model format should be h5 file format.

Usage Example

    $python train.py --data 0.npz --epoch 3 --batch 100 --savemodel model.h5
                                    
`Aggregater` : aggregater averages the stored models in each container. aggregater will find *.h5 file format in --dir directory and average it.

--dir : In trainer.py, *.h5 files saved in specific directory. This --dir parameter refers to its saved folder.

--savefile : savefile is final averaged model. model format should be h5 file format.

Usage Example

    $python aggregater.py --dir ./models --savefile final_model.h5
    
`Server` : server serves as the final average model and serves through flasks.

Usage Example

    model = tf.keras.models.load_model('your_model.h5', compile=False)
