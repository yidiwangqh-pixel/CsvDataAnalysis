# CsvDataAnalysis
参考Openai的code-interpreter实现的基于大模型的简易CSV数据分析系统

## 🚀 快速开始

*本项目推荐使用docker运行，如果没有安装docker，则拉取项目后进入项目路径直接运行DataAnalysis.py即可*

### 先决条件

在开始之前，请确保你已安装以下软件：
*   docker
*   Git

### 安装步骤

1.  **克隆仓库**

    拉取仓库并进入项目路径
    ```bash
    git clone https://github.com/yidiwangqh-pixel/CsvDataAnalysis.git
    cd CsvDataAnalysis
    ```

3.  **配置docker国内镜像源**

    *如果可以直接从docker官方源拉取镜像，可以跳过该步骤*  
    首先，打开或创建/etc/docker/daemon.json文件
    ```bash
    sudo vi /etc/docker/daemon.json
    ```
    然后在文件中写入国内镜像源地址
    ```bash
    {
      “registry-mirrors”:[
        "https://docker.m.daocloud.io",
        "https://docker.1ms.run",
        "https://docker.unsee.tech"
      ]
    }
    ```
    保存并重启docker服务，以使配置生效
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```
    验证配置是否生效
    ```bash
    sudo docker info | grep -A 4 "Registry Mirrors"
    ```
    如果输出刚刚配置的镜像源地址，说明配置成功

5.  **创建docker容器**
    基于项目中的dockerfile创建容器csv_data_analysiser
    ```bash
    sudo docker build -t csv_data_analysiser .
    ```

6.  **运行docker容器**
    由于系统需要从命令行获取用户输入，因为一定要以交互方式运行容器，即使用-it参数
    ```bash
    sudo docker run -it csv_data_analysiser
    ```
容器运行后会输出一段简短的反馈，然后依次等待输入要求的三个问题即可，如果代码运行结果有图片，则存储在当前项目路径下，可自行查看
