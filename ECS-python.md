# 学習内容  
## 実行手順  
1. PthonでTODOアプリを作成(ローカル環境ver)  
[TODOアプリ](TODOsub.py)  
![空実行](img2/ECS-pthon/picture02.png)  
![追記実行](img2/ECS-pthon/picture01.png)  
  
2. dockerイメージの作成→コンテナ起動  
dockerfileの作成  
[my-flask-app](my-flask-app)  
  
docker build → docker run →　curl https://localhost:5000/  
  
![実行確認](img2/ECS-pthon/picture03.png)  
  
![実行](img2/ECS-pthon/picture04.png)  
  
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

### エラー  
* docker run実行後にcurl: (56) Recv failure: Connection reset by peerのエラー  
エラー内容：Flaskは起動しているがアクセスが切断される  
原因：Flaskのhost設定が127.0.0.1になっているため  
    127.0.0.1はループバックアドレスというコンピュータ自身を指す特別なIPアドレス  
    Docker環境では、Dockerコンテナ内からは接続できるが外部（ホストマシン）からは接続不可  
    詳しくは[Dockerコンテナに127.0.0.1でアクセス不可の場合の解消方法](https://qiita.com/taichikanaya_1989/items/5f60b55e847a33f8db41)を参照  
解決：Pythonアプリ内でhost="0.0.0.0"で指定  
    ```
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    ```  
