# ml-kubernetes : IMDB Example
ml-kubernetes IMDB is simple project that trains and predicts IMDB dataset in Kubernetes cluster. This projects conducts PoC (Proof of Concept) of distributed machine learning on container environment.

Prerequisite
All steps are done on GKE of Google Cloud Platform. You have to install gcloud comman line to use GKE.

We assume that gcloud is installed and available. If not, please refer the below link, GCP official document.

gcloud install guide : https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu

#Creating Kubernetes Cluster on GKE.
1.Create Kubernetes cluster first using GUI of GKE.
![image](https://user-images.githubusercontent.com/77087144/146132088-7fb116e0-4164-4ebd-afaf-084d5d64aed5.png)


You can adjust specified options, such as --zone, --disk-size, --num-nodes, etc.

You can set specified options, such as 'zone','disk-size','num_nodes', etc.

If you want to build Kubernetes Cluster with AutoScaling, then you have to set autoscaling option in default-pool menu.
And set the default of num_nodes to 2 for nfs-server. Also you have to set surge upgrade option to 3 for trainer jobs.

![image](https://user-images.githubusercontent.com/77087144/146133192-fb690b4d-7c8f-4c31-baf7-e33493e2aeca.png)


2.Get access credential for Kubernetes.

$ gcloud container clusters get-credentials my-kube-cluster --zone us-central1-a
Test the kubectl command.

$ kubectl get nodes
NAME                                             STATUS   ROLES    AGE   VERSION
gke-my-kube-cluster-default-pool-d0ed872d-33mt   Ready    <none>   49s   v1.21.5-gke.1302
gke-my-kube-cluster-default-pool-d0ed872d-gd42   Ready    <none>   49s   v1.21.5-gke.1302
gke-my-kube-cluster-default-pool-d0ed872d-wpv4   Ready    <none>   49s   v1.21.5-gke.1302
Create a external disk to provide dataset to each Kubernetes node.

Also, you can adjust the options such as --size, --zone, etc.

$ gcloud compute disks create --type=pd-standard \
--size=10GB --zone=asia-northeast3-a ml-disk
Congraturation! You has just created a Kubernetes cluster with 3 worker nodes.

Architecture Diagram


Copier copy IMDB dataset into multiple dataset.

Trainer conducts distributed learning process in Kubernetes container.

Aggregator aggregates output models extracted from step 2.

Server container provides web page to demonstrate IMDB prediction.

Quickstart of Distributed IMDB
First, define environment values used in distributed IMDB learning.

$ export WORKER_NUMBER=5
$ export EPOCH=3
$ export BATCH=100
$WORKER_NUMBER : The number of workers in distributed learning. If it is set to 5, copier will copy IMDB dataset into 5 files, and the 5 trainers will be spawn in each Kubernetes node as a container.
$EPOCH : // TODO
$BATCH : // TODO
Create NFS container to store datasets and models. It will be used as a PV, PVC in Kubernetes. 1-nfs-deployment.yaml creates NFS server container to be mounted to other components, such as splitter, trainer.

$ kubectl apply -f 1-nfs-deployment.yaml
$ kubectl apply -f 2-nfs-service.yaml
Create PV and PVC using NFS container.

$ export NFS_CLUSTER_IP=$(kubectl get svc/nfs-server -o jsonpath='{.spec.clusterIP}')
$ cat 3-nfs-pv-pvc.yaml | sed "s/{{NFS_CLUSTER_IP}}/$NFS_CLUSTER_IP/g" | kubectl apply -f -
[Optional (but recommended) ]

If you want to view directory of NFS server, create busybox deployment and enter into container. By default, index.html and lost+found files exist.

$ kubectl apply -f 9999-busybox.yaml
$ kubectl exec -it $(kubectl get pods | grep busybox | awk '{print $1}') sh

/ # ls /imdb
index.html  lost+found
/ # exit
Copier IMDB dataset using copier. Copier will create datasets, the number of $(WORKER_NUMBER)

$ cat 4-splitter.yaml | sed "s/{{WORKER_NUMBER}}/$WORKER_NUMBER/g" | kubectl apply -f -
To check datasets are created, check in busybox deployment. Copied datasets exist as *.npz

$ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /mnt/data
0.npz
1.npz
2.npz
3.npz
4.npz
Train each dataset in Kubernetes workers. Below bash commands create trainers as deployment to train and extract neural network model.

$ for (( c=0; c<=($WORKER_NUMBER)-1; c++ ))
do
  echo $(date) [INFO] "$c"th Creating th trainer in kubernetes..
  cat 5-trainer.yaml | sed "s/{{EPOCH}}/$EPOCH/g; s/{{BATCH}}/$BATCH/g; s/{{INCREMENTAL_NUMBER}}/$c/g;" | kubectl apply -f - &
done
After about a few minitues, you can view the status of trainer job. Status should be completed.

$ kubectl get po
NAME                          READY   STATUS      RESTARTS   AGE
mnist-splitter-qgkxf          0/1     Completed   0          14m
mnist-trainer-0-g896k         0/1     Completed   0          3m
mnist-trainer-1-6xfkg         0/1     Completed   0          3m
mnist-trainer-2-ppnsc         0/1     Completed   0          3m
Also you can check generated models using busybox deployment.

$ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /imdb/model
0-model.h5
1-model.h5
2-model.h5
3-model.h5
4-model.h5
Aggregate generated models into one model. Below command creates aggregator, which aggregate models into single model.

$ kubectl apply -f 6-aggregator.yaml
Check a aggregated model.

$ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /imdb
aggregated-model.h5
...
If you want to test accuracy of aggregated model, use 9999-accuracy-test deployment.

$ kubectl apply -f 9999-accuracy-test.yaml
$ kubectl logs --tail 1 $(kubectl get pods | grep accuracy-test | awk '{print $1}')
10000/10000 [==============================] - 10s 997us/sample - loss: 1.2667 - acc: 0.8728
Create server deployment for demo. You can test MNIST prediction.

$ kubectl apply -f 7-server.yaml
After a few seconds, you can see the external IP to access the demo web page. Below example shows external IP is a.b.c.d, so you can access a.b.c.d:80 in web browser

$ kubectl get svc
NAME               TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
...
imdb-server-svc   LoadBalancer   10.19.253.70   a.b.c.d   80:30284/TCP                 12m
...
Write a sample IMDB data in IMDB test dataset.

After writing IMDB sample, web page shows prediction result.


Detailed Arguments of Each Component
Copier : copier copies IMDB data equally by the number of contents. so total number of IMDB train dataset is 25000, each number of data.npz is 25000.

--n_container : number of training container.

--savedir : saved directory path of splitted data. each data files saved .npz file format will be saved as number of --n_container.
 
Trainer : trainer will independently learn the data into each container and create a model for each container as *.h5 file format.

--data : Data you want to learn from the container.

--epoch : number of epoch.

--batch : size of batch.

--savemodel : saved model in each container. model format should be h5 file format.

Usage Example

$python train.py --data 0.npz --epoch 3 --batch 100 --savemodel model.h5
                                    
Aggregater : aggregater averages the stored models in each container. aggregater will find *.h5 file format in --dir directory and average it.

--dir : In trainer.py, *.h5 files saved in specific directory. This --dir parameter refers to its saved folder.

--savefile : savefile is final averaged model. model format should be h5 file format.

Usage Example

$python aggregater.py --dir ./models --savefile final_model.h5
Server : server serves as the final average model and serves through flasks.

Usage Example

model = tf.keras.models.load_model('your_model.h5', compile=False)
