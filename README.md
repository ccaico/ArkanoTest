# ArkanoTest
# Proyecto ETL con Azure Data Lake Storage, Databricks y SQL Server

## Descripción del Proyecto

Este proyecto está diseñado para realizar un proceso ETL (Extract, Transform, Load) donde se carga un archivo en Azure Data Lake Storage (ADLS), se consume y transforma utilizando Databricks, y finalmente se carga en una base de datos SQL Server. A continuación, se detallan los pasos de configuración necesarios para llevar a cabo este proyecto.

## Requisitos Previos

1. **Cuenta de Azure**: Una suscripción activa de Azure.
2. **Azure Data Lake Storage (ADLS)**: Un contenedor en ADLS para almacenar los archivos de entrada.
3. **Azure Databricks**: Un workspace y un clúster de Databricks.
4. **Azure SQL Server**: Un servidor SQL y una base de datos en Azure.
5. **Azure Key Vault**: Un Key Vault para almacenar las credenciales de acceso de forma segura.

## Pasos de Configuración

### 1. Configuración de Azure Data Lake Storage (ADLS)

1. **Crear una cuenta de almacenamiento**:
   - Ve al portal de Azure y selecciona "Crear un recurso".
   - Busca "Storage account" y sigue las instrucciones para crear una nueva cuenta de almacenamiento.

2. **Crear un contenedor**:
   - Dentro de tu cuenta de almacenamiento, navega a "Containers" y crea un nuevo contenedor para almacenar los archivos de entrada.

3. **Subir archivos**:
   - Sube el archivo que deseas procesar al contenedor creado.

### 2. Configuración de Azure SQL Server

1. **Crear un SQL Server y una base de datos**:
   - En el portal de Azure, selecciona "Crear un recurso" y busca "SQL Server".
   - Sigue las instrucciones para crear un nuevo servidor SQL.
   - Dentro del servidor SQL, crea una nueva base de datos.

### 3. Configuración de Azure Key Vault

1. **Crear un Key Vault**:
   - En el portal de Azure, selecciona "Crear un recurso" y busca "Key Vault".
   - Sigue las instrucciones para crear un nuevo Key Vault.

2. **Agregar secretos al Key Vault**:
   - Navega a tu Key Vault y en la sección de "Secrets", selecciona "Generate/Import".
   - Añade los siguientes secretos:
     - `sql-server-name`: El nombre de tu servidor SQL.
     - `sql-database-name`: El nombre de tu base de datos.
     - `sql-username`: El nombre de usuario de SQL Server.
     - `sql-password`: La contraseña de SQL Server.
     - `adls-storage-account`: El nombre de tu cuenta de almacenamiento ADLS.
     - `adls-container-name`: El nombre de tu contenedor en ADLS.

### 4. Configuración de Azure Databricks

1. **Crear un workspace y un clúster**:
   - Ve a tu instancia de Databricks.
   - Navega a "Clusters" y crea un nuevo clúster.

2. **Configurar Databricks para usar Azure Key Vault**:
   - En el portal de Azure, ve a tu Key Vault y selecciona "Access policies".
   - Agrega una nueva política de acceso para tu clúster de Databricks, dándole acceso a los secretos.

3. **Montar ADLS en Databricks**:
   - En un notebook de Databricks, usa el siguiente código para montar ADLS:

     ```python
     configs = {
         "fs.azure.account.auth.type": "OAuth",
         "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
         "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope="your-scope", key="your-client-id"),
         "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="your-scope", key="your-client-secret"),
         "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/your-tenant-id/oauth2/token"
     }

     dbutils.fs.mount(
         source = f"abfss://{dbutils.secrets.get(scope='your-scope', key='adls-container-name')}@{dbutils.secrets.get(scope='your-scope', key='adls-storage-account')}.dfs.core.windows.net/",
         mount_point = "/mnt/adls",
         extra_configs = configs
     )
     ```

### 5. Conectar Databricks a SQL Server

1. **Configurar la cadena de conexión**:

    ```python
    jdbc_url = f"jdbc:sqlserver://{dbutils.secrets.get(scope='your-scope', key='sql-server-name')}.database.windows.net:1433;database={dbutils.secrets.get(scope='your-scope', key='sql-database-name')};user={dbutils.secrets.get(scope='your-scope', key='sql-username')}@{dbutils.secrets.get(scope='your-scope', key='sql-server-name')};password={dbutils.secrets.get(scope='your-scope', key='sql-password')};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;"
    ```

2. **Leer y escribir datos usando la cadena de conexión**:

    ```python
    # Leer datos del archivo en ADLS
    df = spark.read.format("csv").option("header", "true").load("/mnt/adls/your-file.csv")

    # Transformar datos (ejemplo)
    transformed_df = df.select("column1", "column2").filter(df.column1.isNotNull())

    # Escribir datos a SQL Server
    transformed_df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "your_table_name") \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .mode("append") \
        .save()
    ```

### Conclusión

Siguiendo estos pasos, habrás configurado un entorno completo de ETL en Azure utilizando ADLS, Databricks y SQL Server. Este proceso te permitirá cargar archivos, limpiarlos y transformarlos en Databricks, y finalmente almacenarlos en una base de datos SQL Server.
