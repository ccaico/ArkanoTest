# Databricks notebook source
# MAGIC %md
# MAGIC Conexion con ADLS

# COMMAND ----------

service_credential = dbutils.secrets.get(scope="kv-secret-adls",key="secret-adls-1")

spark.conf.set("fs.azure.account.auth.type", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id", "019e6452-8d07-428b-83d0-4b89a98743c5")
spark.conf.set("fs.azure.account.oauth2.client.secret", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint", "https://login.microsoftonline.com/1eba443f-23e5-4534-90d1-0976aabe86ac/oauth2/token")

# COMMAND ----------

complaints_df = spark.read.format("csv").option("header","true").option("separator","|").load("abfss://desa@adlstestarkano.dfs.core.windows.net/bronze/complaints.csv")


# COMMAND ----------

complaints_df.display()

# COMMAND ----------

from pyspark.sql.functions import col, to_date, when, isnull, lit, cast

# COMMAND ----------

##Se filtran solo las fechas válidas y ID no nulos 
complaints_df0 = complaints_df.filter((~isnull(to_date(col("Date received"),"yyyy-mm-dd"))) & (~isnull(col("Complaint ID"))))
complaints_df0.display()

# COMMAND ----------

##Se filtran solo los ID válidos
complaints_df1 = complaints_df0.filter(~isnull(col("Complaint ID").cast("int")))
complaints_df1.display()

# COMMAND ----------

##Quitar ID duplicados
complaints_df2 = complaints_df1.dropDuplicates()
complaints_df2.display()

# COMMAND ----------

complaints_df3 = complaints_df2.select(
    col('Date Received').alias('DATERECEIVED'),
    col('Product').alias('PRODUCT'),
    col('Sub-product').alias('SUBPRODUCT'),
    col('Issue').alias('ISSUE'),
    col('Sub-issue').alias('SUBISSUE'),
    col('Consumer complaint narrative').alias('COMPLAINTNARRATIVE'),
    col('Company public response').alias('COMPANYRESPONSE'),
    col('Company').alias('COMPANY'),
    col('State').alias('STATE'),
    col('ZIP code').alias('ZIPCODE'),
    col('Tags').alias('TAGS'),
    col('Consumer consent provided?').alias('FLAGCONSENT'),
    col('Submitted via').alias('SUBMITTEDVIA'),
    col('Date sent to company').alias('DATESENTCOMPANY'),
    col('Company response to consumer').alias('COMPANYRESPONSE'),
    col('Timely response?').alias('FLAGTIMELYRESPONSE'),
    col('Consumer disputed?').alias('FLAGDISPUTED'),
    col('Complaint ID').alias('COMPLAINTID')
)
