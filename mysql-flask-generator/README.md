sqlalchemy + MySQL 5.5.62 

```dockerfile
version: '3.4'

volumes:
  mysql_volume:
    name: my-sql-volume
    external: false

services:

  mysql:
    container_name: mysql_db
    image: "mysql:5.5"    
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=my_db
      - MYSQL_USER=user
      - MYSQL_PASSWORD=user
      - MYSQL_PORT=3306
    ports:
    - 3310:3306
    volumes:
    - mysql_volume:/var/lib/mysql
    - ./scripts:/scripts

  mysql_admin:
    container_name: mysql_admin
    image: adminer
    restart: always
    ports:
      - 8080:8080
```

virtual env
```bash
python2 -m virtualenv venv 
source venv/bin/activate
```

download and install pip
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python2 get-pip.py

```


install via python shell 
```python
# python2
import pip
pip.__version__
pip.main(["install", "sqlacodegen"])
pip.main(["install", "mysqlclient"])
pip.main(["install", "oursql"])
```


install via pip 
```
pip2 install sqlacodegen==2.2.0
pip2 install pymysql==0.9.3
pip2 install flask-sqlacodegen==1.1.7

pip2 show sqlacodegen
pip2 show pymysql
pip2 show flask-sqlacodegen
```

```sh
sqlacodegen "mysql+pymysql://admin:admin@localhost:3310/masterdb?charset=utf8" > generated-code.txt
flask-sqlacodegen --flask  "mysql+pymysql://admin:admin@localhost:3310/masterdb?charset=utf8"
```





flask-sqlacodegen "mysql+pymysql://hlm_admin:hlm_admin@localhost:3310/hlm_masterdb" > generated-code.txt
