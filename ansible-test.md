# 学習内容  
Ansibleの使い方  

# Ansibleとは  
構成管理ツールである。ChefやPuppetと違いエージェントが不要なため、モジュールを導入する必要がなく、準備の手間を省ける。  
Ansibleはplaybookという環境設定の定義を記載したYAMLファイルがあれば実行できる。  
Ansibleがインストールされたサーバーと管理対象のサーバーがあればいい。

# テスト実行    
## AWS環境  
## 目的  
今回はAnsibleの利用が初めてなため、「Nginxのインストールと起動」という簡単な内容で試した。  

## 実行手順  
1. 同一VPC内にEC2を２台作成  

Ansibleサーバー→ansible-server(OS:Amazon Linux2)  
管理対象サーバー→ansible-test(OS:Amazon Linux2)  
  
2. Ansibleのインストール  

ansible-serverにAnsibleをインストール  
```
sudo amazon-linux-extras enable ansible2  
sudo yum install -y ansible
```  
インストール確認  
```
ansible --version
```  

3. ansible-serverからansible-testへssh接続を行う  
ローカルからansible-serverに秘密鍵を転送する  
```
scp -i my-key.pem my-key.pem ec2-user@ansible-serverのパブリックIP:/home/ec2-user/  
my-key.pem → 秘密鍵
```  

ansible-serverにSSHでログインし、秘密鍵の権限を設定する  
```
chmod 400 my-key.pem
```  

4. ansible-serverからansible-testにSSH接続を確認  
ansible-serverにSSHでログインし、ansible-testにSSｈ接続を行う  
>[!WARNING]
>セキュリティ上、ansible-testのプライベートIPを使用してSSH接続を行う  
```
ssh -i my-key.pem ec2-user@ansible-testプライベートIP
```  

# 反省点  


