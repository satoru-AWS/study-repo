# 学習内容  
# 実行手順  
1. PthonでTODOアプリを作成(ローカル環境ver)  
[TODOアプリ](TODOsub.py)  
![空実行](img2/ECS-pthon/picture02.png)  
![追記実行](img2/ECS-pthon/picture01.png)  
  
2. dockerイメージの作成→コンテナ起動  
dockerfileの作成  
[image(local)](my-flask-app)  
  
docker build → docker run →　curl https://localhost:5000/  
<details>
<summary>docker主要コマンド</summary>
<br>
イメージ作成  
docker build -t イメージ名 .  
- `-t`はタグづけ  
- `.`は現在のディレクトリをビルド対象  
</details>  

![実行確認](img2/ECS-pthon/picture03.png)  
![実行](img2/ECS-pthon/picture04.png)  

