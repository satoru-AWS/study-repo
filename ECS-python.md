# 学習内容  
## 実行手順  
1. PythonでTODOアプリを作成(ローカル環境ver)  
[TODOアプリ](TODOsub.py)  
![空実行](img2/ECS-pthon/picture02.png)  
![追記実行](img2/ECS-pthon/picture01.png)  
  
2. dockerイメージの作成→コンテナ起動  
dockerfileの作成  
[my-flask-app](my-flask-app)  
  
docker build → docker run →　curl https://localhost:5000/  
  
![実行確認](img2/ECS-pthon/picture03.png)  
  
![実行](img2/ECS-pthon/picture04.png)  
  
3. PythonでTODOアプリを作成（AWS環境ver) → ECRへプッシュ  
SQLite → RDS for MySQLに変更しdockerイメージを作成  
[aws-flask-app](aws-flask-app)  

イメージ作成  
```docker build -t aws-flask-app .```  
ECRリポジトリを作成  
```aws ecr create-repository --repository-name aws-flask-app```  
ECRにログイン  
```aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 'repositoryUrl'```  
イメージをタグ付け  
```docker tag aws-flask-app:latest 'repositoryUrl':latest```  
ECRにpush  
```docker push 'repositoryUrl:latest```  

4. ECSの準備  
クラスター：コンテナを配置する実行基盤の集合  
インスタンス：クラスターの中にあるEC2かFargate  
タスク：実行するコンテナアプリ  
サービス：タスクの数や配置ルールを管理するもの  
  
* ECSクラスター作成  
今回は起動タイプをEC2で作成  
>[!NOTE]
>セキュリティグループの設定に注意（詳細は下記エラーで）  
>IAMロールにAmazonEC2ContainerServiceforEC2Roleを含む必要なポリシーを設定  
  
* タスク定義の作成  
今回はflaskを使うため、ポートマッピングに5000を使用  
  
* サービスの作成  

5. EC2のパブリックIPでアクセス  
  
EC2パブリックIP:5000 → Flask is running! Use /todos to manage tasks.  
![Flask is running](img2/ECS-pthon/picture05.png)  
  
EC2パブリックIP:5000/todos → TODOアプリが起動  
![TODOアプリ起動](img2/ECS-pthon/picture06.png)  
  
### docker主要コマンド  
* イメージ作成  
```docker build -t イメージ名 .```  
    - '-t'はタグ付け
    - '.'は現在のディレクトリをビルド対象  
* コンテナの起動  
```docker run -p ホスト側:コンテナ側 イメージ名```
    - '-p'はポートのマッピング  
* すべてのコンテナを表示  
```docker ps -a```  
* ローカルに保存されているdockerイメージの一覧  
```docker images```  
* コンテナの停止  
```docker stop コンテナIDor名前```  
* コンテナの削除  
```docker rm コンテナID```  
* イメージの削除  
```docker rmi イメージIDorイメージ名```  
* イメージの取得  
```docker pull イメージ名```  
* イメージをリポジトリにアップロード  
```docker push イメージ名```  
* イメージにタグ付け  
```docker tag 元:タグ 新:タグ```  

### ❗️エラー  

  
**現象**  
docker run実行後にcurl: (56) Recv failure: Connection reset by peerのエラー    
  
**内容**　　
Flaskは起動しているがアクセスが切断される  
  
**原因**　　
Flaskの`host`設定が`127.0.0.1`になっているため  

- 127.0.0.1はループバックアドレスというコンピュータ自身を指す特別なIPアドレス  
- Docker環境では、Dockerコンテナ内からは接続できるが外部（ホストマシン）からは接続不可  
- 詳しくは[Dockerコンテナに127.0.0.1でアクセス不可の場合の解消方法](https://qiita.com/taichikanaya_1989/items/5f60b55e847a33f8db41)を参照  
  
**解決方法**　　
Pythonアプリ内で`host="0.0.0.0"`を指定  
```
if __name__ == "__main__":
app.run(host="0.0.0.0", port=5000, debug=True)
```  
  
**現象**  
EC2にECS Instanceが作成されたものの、ECSクラスターもインフラストラクチャに該当のEC2が表示されない  
  
**原因**  
EC2のセキュリティグループにHTTPS:443ポートを許可していなかったことが原因
  - ECSエージェントがAWSのECS APIと通信するのに必要なため  
  
なお、事前に下記事項も確認したが問題なかった  

* SSH接続を行い```sudo systemctl status ecs```の結果active
  - EC2内のecs-agentが動いていることが確認  
* /etc/ecs/ecs.configにECS_CLUSTER=<クラスター名>を確認した結果問題なし
  - ECSエージェントが接続するクラスター名が間違っていないことを確認  
* IAMロールに必要なポリシーが設定されているかを確認した結果問題なし
  - AmazonEC2ContainerServiceforEC2Roleポリシーが付与されていることを確認  
  
**解決方法**  
EC2のセキュリティグループにHTTPS（443）を許可に設定  
なお、SSH(22)やFlask(5000)も併せて許可に設定  
  
**現象**  
エラーメッセージ  
```CannotPullContainerError: no matching manifest for linux/amd64 in the manifest list entries```  
  
**内容**  
ECSがイメージをECRからプルしようとしたときに、自身のアーキテクチャと一致するDockerイメージが存在していない  
  
**原因**  
ECRにプッシュしていた'aws-flask-app'のイメージとEC2が扱うアーキテクチャが異なっていた  
AWS EC2のアーキテクチャ:amd64　aws-flask-appのアーキテクチャ:arm64  
---なぜ？---  
使用したPCがMac(M1)であり、特に指定しない限り、arm64のイメージがビルドされるため  
  
**解決方法**  
amd64のアーキテクチャになるように、Dockerイメージをビルドする  
```docker buildx build --platform linux/amd64 -t タグ .```  

**現象**  
ECSでタスクが起動できず、サービスがロールバックされる  
  
**内容**  
エラーメッセージ  
```service was unable to place a task because no container instance met all of its requirements. The closest matching container-instance [...] has insufficient memory available.```  
  
**原因**  
ECSタスクが要求するメモリサイズがEC2インスタンスで確保できなかったため。  
タスクレベルとコンテナレベルのメモリのリソース設定を行う  
  タスクレベル  :ECSがインスタンス上にタスクを配置するために必要な容量  
  コンテナレベル：各コンテナの最小/最大メモリ使用量制限  

---具体的なエラー原因---  
- タスクサイズ(0.5GB)よりも、コンテナ内で設定したmemory(1GB)の方が大きい  
- EC2インスタンスの空きメモリ(t2micro=1.0GB)よりもタスクが要求するメモリが大きい  
  

